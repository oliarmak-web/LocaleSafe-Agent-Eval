"""Validate local speech/transcript evidence without uploading audio or calling providers."""
import argparse
import hashlib
import json
from pathlib import Path
import wave
from .domain_study import cases

KINDS=('human_reference','asr_output','dictation_output','injected_text_control')


def validate(manifest,audio_root):
    if set(manifest)!={'format_version','records'} or manifest['format_version']!=1 or not isinstance(manifest['records'],list):
        raise ValueError('Invalid speech evidence envelope')
    indexed={c['id']:c for c in cases()};seen=set();counts={k:0 for k in KINDS};reviewed=0
    for row in manifest['records']:
        if set(row)!={'id','case_id','source_kind','provider','provider_version','settings','review_status','reviewer_id','events'}:
            raise ValueError('Invalid evidence fields')
        if not isinstance(row['id'],str) or not row['id'] or row['id'] in seen:raise ValueError('Missing/duplicate evidence ID')
        seen.add(row['id'])
        if row['case_id'] not in indexed or row['source_kind'] not in KINDS:raise ValueError('Unknown case/source kind')
        if not isinstance(row['settings'],dict):raise ValueError('Provider settings must be explicit')
        if row['review_status'] not in ('unreviewed','independently-reviewed'):raise ValueError('Unknown review status')
        if row['review_status']=='independently-reviewed':
            if not isinstance(row['reviewer_id'],str) or not row['reviewer_id']:raise ValueError('Review attribution required')
            reviewed+=1
        elif row['reviewer_id'] is not None:raise ValueError('Unreviewed evidence cannot name a reviewer')
        if row['source_kind'] in ('asr_output','dictation_output'):
            if not all(isinstance(row[k],str) and row[k] for k in ('provider','provider_version')):
                raise ValueError('Provider and version required')
        reference=indexed[row['case_id']]['history']
        if not isinstance(row['events'],list) or len(row['events'])!=len(reference):raise ValueError('Incomplete event alignment')
        for event,ref in zip(row['events'],reference):
            if set(event)!={'event_seq','transcript','audio_file','audio_sha256','audio_origin','license','consent'}:
                raise ValueError('Invalid event evidence')
            if type(event['event_seq']) is not int or event['event_seq']!=ref['event_seq']:
                raise ValueError('Event alignment mismatch')
            if not isinstance(event['transcript'],str) or not event['transcript'].strip():raise ValueError('Missing transcript')
            if row['source_kind']=='injected_text_control':
                if any(event[k] is not None for k in ('audio_file','audio_sha256','audio_origin','license','consent')):
                    raise ValueError('Injected text is not audio evidence')
                continue
            if event['audio_origin'] not in ('human_recorded','synthetic') or not isinstance(event['license'],str) or not event['license']:
                raise ValueError('Audio origin/license declaration required')
            if event['consent'] not in ('documented','synthetic_no_person'):raise ValueError('Consent declaration required')
            if event['audio_origin']=='human_recorded' and event['consent']!='documented':raise ValueError('Human recording needs documented consent')
            if not isinstance(event['audio_file'],str) or not event['audio_file']:raise ValueError('Audio path required')
            relative=Path(event['audio_file'])
            path=(audio_root/relative).resolve()
            if relative.is_absolute() or not path.is_relative_to(audio_root.resolve()) or not path.is_file():
                raise ValueError('Unsafe/missing audio path')
            if not 0<path.stat().st_size<=50_000_000:raise ValueError('Audio size outside local intake limit')
            if hashlib.sha256(path.read_bytes()).hexdigest()!=event['audio_sha256']:raise ValueError('Audio hash mismatch')
            if path.suffix.lower()=='.wav':
                with wave.open(str(path),'rb') as audio:
                    if audio.getframerate()<=0 or not 0<audio.getnframes()/audio.getframerate()<=120:
                        raise ValueError('Invalid/oversized audio duration')
        counts[row['source_kind']]+=1
    return {'records':len(seen),'source_kinds':counts,'declared_independent_reviews':reviewed,
            'notice':'Technical/provenance validation only; declarations do not independently verify licensing, consent, translation or intent. No provider was called.'}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('manifest',type=Path);p.add_argument('--audio-root',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();result=validate(json.loads(a.manifest.read_text(encoding='utf-8')),a.audio_root)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    with a.output.open('x',encoding='utf-8') as stream:json.dump(result,stream,indent=2);stream.write('\n')
    print(json.dumps(result))


if __name__=='__main__':main()
