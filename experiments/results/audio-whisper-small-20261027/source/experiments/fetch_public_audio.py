"""Retrieve a deterministic, attributed public-audio smoke-test packet."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import re

SOURCES=(
 {'key':'fleurs','repo':'google/fleurs','revision':'168de341b3db6859a9bac1c50a2ef5e3b47647e0','split':'test',
  'configs':{'en_us':'en','es_419':'es','hi_in':'hi','pt_br':'pt','cmn_hans_cn':'zh','ta_in':'ta'}},
 {'key':'minds14','repo':'PolyAI/minds14','revision':'0c617db2d3e8c3576abdd7548af4a9f5ff41d2cb','split':'train',
  'configs':{'en-US':'en','es-ES':'es','pt-PT':'pt','zh-CN':'zh'}},
)


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output-dir',type=Path,required=True);a=p.parse_args()
    import pyarrow.parquet as pq
    import soundfile as sf
    from huggingface_hub import hf_hub_download
    root=a.output_dir;root.mkdir(parents=True,exist_ok=False);(root/'audio').mkdir()
    samples=[];files=[];skipped=[]
    for source in SOURCES:
        for config,language in source['configs'].items():
            name=f"{config}/{source['split']}/0000.parquet"
            path=Path(hf_hub_download(source['repo'],name,repo_type='dataset',revision=source['revision'],token=False,
                      local_dir=Path('reports/public-audio-cache')/source['key']))
            files.append({'dataset':source['repo'],'revision':source['revision'],'file':name,
                          'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
            parquet=pq.ParquetFile(path)
            columns=['audio','transcription']+(['id','raw_transcription'] if source['key']=='fleurs' else ['intent_class','path'])
            selected=0;seen_intents=set();row_index=-1
            for batch in parquet.iter_batches(batch_size=8,columns=columns):
                for row in batch.to_pylist():
                    row_index+=1;text=row['transcription']
                    reason=None
                    if not isinstance(text,str) or not text.strip():reason='empty_reference'
                    elif re.search(r'\d{7,}|[\w.+-]+@[\w.-]+',text):reason='long_digit_sequence_or_email'
                    raw=row['audio']['bytes']
                    if raw is None:raise ValueError('Expected embedded licensed audio bytes')
                    info=sf.info(io.BytesIO(raw))
                    if not 1<=info.duration<=20:reason='duration_outside_1_to_20_seconds'
                    if source['key']=='minds14' and row['intent_class'] in seen_intents:reason='intent_already_selected'
                    if reason:
                        skipped.append({'dataset':source['key'],'config':config,'row':row_index,'reason':reason});continue
                    sample_id=f"{source['key']}-{config}-{row_index:04d}"
                    extension='.wav' if info.format=='WAV' else '.flac' if info.format=='FLAC' else None
                    if extension is None:raise ValueError('Unexpected source audio container')
                    audio_name='audio/'+sample_id+extension;(root/audio_name).write_bytes(raw)
                    samples.append({'id':sample_id,'dataset':source['repo'],'dataset_revision':source['revision'],
                                    'dataset_file':name,'row_index':row_index,'source_item_id':row.get('id',row.get('path')),
                                    'config':config,'language':language,'split':source['split'],'license':'CC-BY-4.0',
                                    'source_url':'https://huggingface.co/datasets/'+source['repo'],
                                    'audio_file':audio_name,'audio_sha256':hashlib.sha256(raw).hexdigest(),
                                    'duration_seconds':info.duration,'sample_rate':info.samplerate,'channels':info.channels,
                                    'reference':text,'raw_reference':row.get('raw_transcription',text),
                                    'intent_class_id':row.get('intent_class'),'review_status':'dataset-reference-not-independently-reviewed',
                                    'consent_basis':'public_dataset_release_not_individually_reverified'})
                    if source['key']=='minds14':seen_intents.add(row['intent_class'])
                    selected+=1
                    if selected==2:break
                if selected==2:break
            if selected!=2:raise ValueError('Frozen selection could not retrieve two eligible clips')
    manifest={'status':'public-audio-smoke-packet','samples':samples,'source_files':files,'skipped_before_selection':skipped,
              'notice':'Public upstream datasets under CC-BY-4.0; retain attribution. Not original LocaleSafe recordings, domain-agent tasks, consent certification or independently reviewed cultural evidence.'}
    (root/'samples.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'clips':len(samples),'configs':len(files),'manifest_sha256':hashlib.sha256((root/'samples.json').read_bytes()).hexdigest()}))


if __name__=='__main__':main()
