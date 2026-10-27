"""Unicode code-point character error; not word error or intent correctness."""
import unicodedata


def normalize(text):
    text=unicodedata.normalize('NFKC',text).casefold()
    return ''.join(c for c in text if not c.isspace() and not unicodedata.category(c).startswith('P'))


def edit_distance(reference,hypothesis):
    previous=list(range(len(hypothesis)+1))
    for i,left in enumerate(reference,1):
        current=[i]
        for j,right in enumerate(hypothesis,1):
            current.append(min(current[-1]+1,previous[j]+1,previous[j-1]+int(left!=right)))
        previous=current
    return previous[-1]


def score(reference,hypothesis):
    ref,hyp=normalize(reference),normalize(hypothesis)
    if not ref:raise ValueError('Empty normalized reference')
    errors=edit_distance(ref,hyp)
    return {'normalized_reference_characters':len(ref),'character_edits':errors,'cer':errors/len(ref),
            'normalized_exact':ref==hyp}
