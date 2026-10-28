"""Audit public-audio smoke results; optionally verify the downloaded audio bytes."""
import argparse
import json
from pathlib import Path

from localesafe.asr_metrics import score
from localesafe.collect_audio_smoke import MODEL,SOURCES,jobs_for
from localesafe.evaluate import sha256,read_jsonl


def audit(directory,packet=None):
    hashes=json.loads((directory/'archive-sha256.json').read_text(encoding='utf-8'))
    inventory={p.relative_to(directory).as_posix() for p in directory.rglob('*') if p.is_file() and p.name!='archive-sha256.json'}
    if set(hashes)!=inventory:raise ValueError('Archive inventory mismatch')
    for name,digest in hashes.items():
        path=(directory/name).resolve()
        if not path.is_relative_to(directory.resolve()) or sha256(path)!=digest:raise ValueError('Archive path/hash mismatch')
    manifest=json.loads((directory/'manifest.json').read_text(encoding='utf-8'));s=manifest['settings']
    if manifest['status']!='completed' or manifest['attempts']!=40 or manifest['scheduled_requests']!=40:
        raise ValueError('Incomplete ASR run')
    if (s['model']!=MODEL or s['device']!='cpu' or s['dtype']!='float32' or s['threads']!=4
        or s['interop_threads']!=1 or s['deterministic_algorithms'] is not True
        or s['decoding']!='greedy' or s['beams']!=1 or s['task']!='transcribe' or s['timestamps'] is not False
        or s['max_new_tokens']!=128 or s['schedule_seed']!=20261027 or s['transformers']!='4.57.6'
        or set(s['sources'])!=set(SOURCES)):
        raise ValueError('Frozen ASR settings mismatch')
    for name,digest in s['sources'].items():
        if sha256(directory/'source'/name)!=digest:raise ValueError('Source hash mismatch')
    if sha256(directory/'samples.json')!=s['samples_sha256']:raise ValueError('Input manifest mismatch')
    if s['samples_sha256']!='4b35dfcaefc569cb1285500d8c9a60a0548b74e140d6d0d44438d6acf3b458c5':
        raise ValueError('Frozen public packet mismatch')
    packet_data=json.loads((directory/'samples.json').read_text(encoding='utf-8'));samples=packet_data['samples']
    if len(samples)!=20 or len({r['id'] for r in samples})!=20:raise ValueError('Invalid clip grid')
    if packet is not None:
        if sha256(packet/'samples.json')!=s['samples_sha256']:raise ValueError('External packet manifest mismatch')
        for row in samples:
            path=(packet/row['audio_file']).resolve()
            if not path.is_relative_to(packet.resolve()) or sha256(path)!=row['audio_sha256']:raise ValueError('External audio hash mismatch')
    indexed={r['id']:r for r in samples};jobs=jobs_for(samples);rows=read_jsonl(directory/'attempts.jsonl')
    if len(rows)!=40 or sha256(directory/'attempts.jsonl')!=manifest['attempts_sha256']:raise ValueError('Attempt hash/count mismatch')
    matched={}
    defaults=json.loads((directory/'generation-defaults.json').read_text(encoding='utf-8'))
    eos=defaults['eos_token_id'];eos={eos} if isinstance(eos,int) else set(eos or [])
    for job,row in zip(jobs,rows):
        if row['job']!=job or row['scores']!=score(indexed[job['sample_id']]['reference'],row['raw_output']):raise ValueError('Job/score mismatch')
        if not isinstance(row['token_ids'],list) or not row['token_ids'] or any(type(x) is not int for x in row['token_ids']):raise ValueError('Invalid token IDs')
        capped=not any(t in eos for t in row['token_ids']) and len(row['token_ids'])>=128
        if row['no_eos_at_budget']!=capped:raise ValueError('Decode-budget flag mismatch')
        for key in ('waveform_sha256','input_features_sha256'):
            value=row[key]
            if not isinstance(value,str) or len(value)!=64 or any(c not in '0123456789abcdef' for c in value):raise ValueError('Invalid feature hash')
        fingerprint=(row['waveform_sha256'],row['input_features_sha256'])
        if job['sample_id'] in matched and matched[job['sample_id']]!=fingerprint:raise ValueError('Paired arms used different waveform/features')
        matched[job['sample_id']]=fingerprint
    return manifest,samples,rows


def summarize(manifest,samples,rows):
    indexed={s['id']:s for s in samples};groups=[]
    for dataset,config in sorted({(s['dataset'],s['config']) for s in samples}):
        for arm in ('auto_language','provided_language'):
            group=[r for r in rows if indexed[r['job']['sample_id']]['dataset']==dataset
                   and indexed[r['job']['sample_id']]['config']==config and r['job']['arm']==arm]
            edits=sum(r['scores']['character_edits'] for r in group);chars=sum(r['scores']['normalized_reference_characters'] for r in group)
            groups.append({'dataset':dataset,'config':config,'arm':arm,'clips':len(group),'edits':edits,
                           'posthoc_reference_basis':'released_asr_hypothesis' if dataset=='PolyAI/minds14' else 'released_read_speech_reference',
                           'reference_characters':chars,'cer':edits/chars,'normalized_exact':sum(r['scores']['normalized_exact'] for r in group),
                           'no_eos_at_budget':sum(r['no_eos_at_budget'] for r in group)})
    by_id={(r['job']['sample_id'],r['job']['arm']):r for r in rows}
    pairs=[]
    for sample in samples:
        auto=by_id[sample['id'],'auto_language'];provided=by_id[sample['id'],'provided_language']
        delta=provided['scores']['character_edits']-auto['scores']['character_edits']
        pairs.append({'sample_id':sample['id'],'provided_minus_auto_edits':delta,
                      'lower_with_provided':delta<0,'higher_with_provided':delta>0,'equal_edits':delta==0,
                      'identical_decoded_output':auto['raw_output']==provided['raw_output'],
                      'identical_token_ids':auto['token_ids']==provided['token_ids']})
    return {'calls':len(rows),'clips':len(samples),'model':manifest['settings']['model'],'groups':groups,'paired_language_hint':pairs,
            'notice':'Tiny public-corpus transcription smoke test. CER is not intent, word accuracy, cultural understanding or agent task success. Contents differ across configurations.'}


def render(result):
    lines=['# Free public-audio transcription smoke test','',
           '20 public clips, 40 local CPU Whisper-small transcriptions. Two clips per dataset configuration; no confidence intervals, ranking, cultural or deployed-product conclusions.','',
           'Ratios are character-edit distance to released references. **MINDS references are ASR hypotheses, not verified human gold; its ratios measure transcript disagreement.**','',
           '| Dataset | Configuration | Automatic-language edit ratio | Supplied-language edit ratio |','|---|---|---:|---:|']
    for dataset,config in sorted({(g['dataset'],g['config']) for g in result['groups']}):
        cells=[]
        for arm in ('auto_language','provided_language'):
            g=next(g for g in result['groups'] if g['dataset']==dataset and g['config']==config and g['arm']==arm)
            cells.append(f"{g['edits']}/{g['reference_characters']} ({100*g['cer']:.1f}%)")
        lines.append('| '+dataset+' | '+config+' | '+' | '.join(cells)+' |')
    pairs=result['paired_language_hint']
    lines+=['',f"Supplying language lowered edit count on {sum(p['lower_with_provided'] for p in pairs)}/20 clips, increased it on {sum(p['higher_with_provided'] for p in pairs)}/20 and tied on {sum(p['equal_edits'] for p in pairs)}/20.",'',
            f"Decoded outputs matched exactly across arms on {sum(p['identical_decoded_output'] for p in pairs)}/20 clips; token sequences matched on {sum(p['identical_token_ids'] for p in pairs)}/20.",'',
            'CER uses Levenshtein Unicode-code-point edits after NFKC/casefold and removal of punctuation/whitespace. It is not word error rate or semantic correctness. Scripts, content, speakers and recording conditions differ; cross-language percentages are not a controlled language comparison.','',
            'FLEURS uses released read speech. MINDS-14 uses released banking-intent speech; its [source paper](https://arxiv.org/html/2104.08524) describes Google ASR-generated transcriptions. Reference errors or omissions can affect the ratios, so larger disagreements are not automatically hallucinations. pt-PT is European Portuguese, while FLEURS pt_br is Brazilian Portuguese. Published references and consent records have not been independently reverified by LocaleSafe. No ElevenLabs, Wispr Flow or downstream agent was evaluated. Source audio stays in ignored local artifacts; pinned retrieval and per-clip hashes support reproduction.','',
            '[Recording sources and licenses](../experiments/audio-pilot/DATA_SOURCES.md) · [Frozen protocol](../experiments/audio-pilot/PROTOCOL.md).']
    return '\n'.join(lines)+'\n'


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('directory',type=Path);p.add_argument('--packet',type=Path);p.add_argument('--output-dir',type=Path,required=True)
    a=p.parse_args();m,s,r=audit(a.directory,a.packet);result=summarize(m,s,r)
    a.output_dir.mkdir(parents=True,exist_ok=False)
    (a.output_dir/'summary.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    (a.output_dir/'RESULTS.md').write_text(render(result),encoding='utf-8')
    print(json.dumps({'calls':len(r),'clips':len(s)}))


if __name__=='__main__':main()
