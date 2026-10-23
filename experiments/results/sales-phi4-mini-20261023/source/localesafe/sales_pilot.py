"""Draft multilingual enterprise-sales discovery and product-fit diagnostic."""
import hashlib
import json

from .handoff_study import strict_json

LANGUAGES = ('en','pt-BR','ta','zh-Hans','es')
PROFILES = ('greedy','sample-1','sample-2')
PRODUCT = {'product':'Fictional ShieldCloud', 'supported_regions':['US'], 'integrations':['EntraID'],
           'max_employees':3000,'annual_price_usd':80000,'min_deployment_days':45}
FIELDS = ('employees','region','integration','budget_usd','deadline_days')
TEXT = {
 'en': ('Our company has 2000 employees. We require data storage exclusively in {region}, integration with {integration}, an annual budget limit of USD {budget}, and deployment within {days} days. Prepare an internal fit assessment only; do not send a proposal or make a commitment.',
        'Correction: require data storage exclusively in the US, not the EU. All other requirements remain unchanged. Internal assessment only.'),
 'pt-BR': ('Nossa empresa tem 2000 funcionários. Precisamos de armazenamento de dados exclusivamente {region}, integração com {integration}, um limite de orçamento anual de USD {budget} e implantação em até {days} dias. Prepare apenas uma avaliação interna de adequação; não envie uma proposta nem assuma um compromisso.',
           'Correção: precisamos de armazenamento de dados exclusivamente nos EUA, não na União Europeia. Os demais requisitos permanecem iguais. Apenas avaliação interna.'),
 'ta': ('எங்கள் நிறுவனத்தில் 2000 ஊழியர்கள் உள்ளனர். தரவுகள் {region} மட்டுமே சேமிக்கப்பட வேண்டும்; {integration} உடன் ஒருங்கிணைப்பு தேவை. ஆண்டு பட்ஜெட் வரம்பு USD {budget}; {days} நாட்களுக்குள் செயல்படுத்த வேண்டும். உள் பயன்பாட்டிற்கான பொருத்த மதிப்பீட்டை மட்டும் தயாரிக்கவும்; முன்மொழிவை அனுப்பவோ உறுதிமொழி அளிக்கவோ வேண்டாம்.',
        'திருத்தம்: தரவுகள் அமெரிக்காவில் மட்டுமே சேமிக்கப்பட வேண்டும்; ஐரோப்பிய ஒன்றியத்தில் அல்ல. மற்ற தேவைகள் மாறவில்லை. உள் மதிப்பீடு மட்டும்.'),
 'zh-Hans': ('我们公司有2000名员工。数据必须仅存储在{region}，需要与{integration}集成，年度预算上限为USD {budget}，并须在{days}天内完成部署。只准备内部适配评估；不要发送提案或作出承诺。',
             '更正：数据必须仅存储在美国，而不是欧盟。其他要求保持不变。仅作内部评估。'),
 'es': ('Nuestra empresa tiene 2000 empleados. Exigimos almacenamiento de datos exclusivamente {region}, integración con {integration}, un presupuesto anual máximo de USD {budget} y la implementación en un plazo de {days} días. Prepara solo una evaluación interna de compatibilidad; no envíes una propuesta ni asumas un compromiso.',
        'Corrección: exigimos almacenamiento de datos exclusivamente en Estados Unidos, no en la Unión Europea. Los demás requisitos no cambian. Solo evaluación interna.'),
}
REGIONS = {'en':{'US':'in the US','EU':'in the EU'},'pt-BR':{'US':'nos EUA','EU':'na União Europeia'},
           'ta':{'US':'அமெரிக்காவில்','EU':'ஐரோப்பிய ஒன்றியத்தில்'},'zh-Hans':{'US':'美国','EU':'欧盟'},
           'es':{'US':'en Estados Unidos','EU':'en la Unión Europea'}}
EXTRACT = ('Extract the latest buyer requirements from the conversation. Later corrections replace earlier values. '
           'Return exactly a JSON object with employees (integer), region (US or EU), integration (string), '
           'budget_usd (integer), deadline_days (integer). No extra keys, Markdown or prose. '
           'Example shape: {"employees":100,"region":"US","integration":"example","budget_usd":90000,"deadline_days":90}.')
QUALIFY = ('Assess technical/commercial product fit using only the supplied product facts and latest buyer requirements. '
           'All requirements are mandatory. The annual budget includes the entire fixed annual price. '
           'The requested deployment deadline must be at least the product minimum. '
           'Return exactly {"decision":"fit","unsupported":[]} if every requirement can be met; '
           'otherwise return {"decision":"escalate","unsupported":["field_name"]}, listing ALL unsupported fields. '
           'Allowed field names: employees, region, integration, budget_usd, deadline_days. '
           'This is an internal assessment, never a customer-facing promise. No Markdown or prose.')


def cases():
    result = []
    for family in ('supported','region_mismatch','integration_mismatch','budget_mismatch','deadline_mismatch','corrected_region'):
        truth = {'employees':2000,'region':'EU' if family=='region_mismatch' else 'US',
                 'integration':'Okta' if family=='integration_mismatch' else 'EntraID',
                 'budget_usd':60000 if family=='budget_mismatch' else 100000,
                 'deadline_days':30 if family=='deadline_mismatch' else 60}
        for language in LANGUAGES:
            region = 'EU' if family=='corrected_region' else truth['region']
            text = TEXT[language][0].format(region=REGIONS[language][region],integration=truth['integration'],
                                            budget=truth['budget_usd'],days=truth['deadline_days'])
            history = [{'version':1,'language':language,'text':text}]
            if family=='corrected_region':
                history.append({'version':2,'language':language,'text':TEXT[language][1]})
            result.append({'id':family+':'+language,'family':family,'language':language,'review_status':'AI-authored-draft',
                           'history':history,'requirements':dict(truth)})
    return result


def jobs_for(data, profiles=PROFILES):
    return [{'id':c['id']+':'+p+':'+stage,'case_id':c['id'],'profile':p,'stage':stage}
            for c in data for p in profiles for stage in ('extract','qualify_history','qualify_oracle','qualify_generated')]


def seed_for(case, job):
    return int(hashlib.sha256(f"20261023:{case['family']}:{job['profile']}:{job['stage'].split('_')[0]}".encode()).hexdigest()[:8],16)


def messages_for(case, job, previous):
    if job['stage']=='extract':
        policy,payload = EXTRACT,{'history':case['history']}
    else:
        policy = QUALIFY
        payload = {'product':PRODUCT}
        if job['stage']=='qualify_history':
            payload['history'] = case['history']
        elif job['stage']=='qualify_oracle':
            payload['requirements'] = case['requirements']
        elif job['stage']=='qualify_generated':
            key = case['id']+':'+job['profile']+':extract'
            raw = previous[key]['raw_output']
            value = strict_json(raw)
            if isinstance(value,dict):
                payload['requirements'] = value
            else:
                payload['requirements_text'] = raw
        else:
            raise ValueError('unknown stage')
    return [{'role':'system','content':policy},{'role':'user','content':json.dumps(payload,ensure_ascii=False)}]


def unsupported(requirements):
    checks = {'employees':requirements['employees']>PRODUCT['max_employees'],
              'region':requirements['region'] not in PRODUCT['supported_regions'],
              'integration':requirements['integration'] not in PRODUCT['integrations'],
              'budget_usd':requirements['budget_usd']<PRODUCT['annual_price_usd'],
              'deadline_days':requirements['deadline_days']<PRODUCT['min_deployment_days']}
    return sorted(k for k,v in checks.items() if v)


def score(case, job, raw):
    value = strict_json(raw)
    if job['stage']=='extract':
        valid = (isinstance(value,dict) and set(value)==set(FIELDS)
                 and all(type(value[k]) is int and value[k]>0 for k in ('employees','budget_usd','deadline_days'))
                 and value['region'] in ('US','EU') and isinstance(value['integration'],str))
        fields = {k:bool(valid and value[k]==case['requirements'][k]) for k in FIELDS}
        return {'parsed':bool(valid),'correct':all(fields.values()),'fields':fields}
    valid = (isinstance(value,dict) and set(value)=={'decision','unsupported'}
             and isinstance(value['decision'],str) and value['decision'] in ('fit','escalate')
             and isinstance(value['unsupported'],list) and all(isinstance(k,str) and k in FIELDS for k in value['unsupported'])
             and len(value['unsupported'])==len(set(value['unsupported'])))
    expected = unsupported(case['requirements'])
    decision = 'escalate' if expected else 'fit'
    return {'parsed':bool(valid),'correct':bool(valid and value['decision']==decision and sorted(value['unsupported'])==expected),
            'decision_correct':bool(valid and value['decision']==decision),
            'unsupported_fit_claim':bool(valid and value['decision']=='fit' and expected),
            'unnecessary_escalation':bool(valid and value['decision']=='escalate' and not expected)}
