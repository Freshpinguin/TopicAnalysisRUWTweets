import html
import textacy.preprocessing as tprep
import regex as re
import spacy
from tqdm.auto import tqdm
tqdm.pandas()
from spacy.language import Doc
import pandas as pd
import math
import warnings
from spacy import Language



def normalize(text: str) -> str:
    """
    Normalizes text.
    """
    text = tprep.normalize.hyphenated_words(text)
    text = tprep.normalize.quotation_marks(text)
    text = tprep.normalize.unicode(text)
   #text = tprep.remove.accents(text)
    text = text.lower()
    return text


def clean(text:str) -> str:
    """
    Cleans and normalizes text.
    """
    # convert html escapes like &amp; to characters.
    text = html.unescape(text) 
    # tags like <tab>
    text = re.sub(r'<[^<>]*>', ' ', text)
    # markdown URLs like [Some text](https://....)
    text = re.sub(r'\[([^\[\]]*)\]\([^\(\)]*\)', r'\1', text)
    # text or code in brackets like [0]
    text = re.sub(r'\[[^\[\]]*\]', ' ', text)
    # standalone sequences of specials, matches &# but not #cool
    text = re.sub(r'(?:^|\s)[&#<>{}\[\]+|\\:-]{1,}(?:\s|$)', ' ', text)
    # standalone sequences of hyphens like --- or ==
    text = re.sub(r'(?:^|\s)[\-=\+]{2,}(?:\s|$)', ' ', text)
    # sequences of white spaces
    text = re.sub(r'\s+', ' ', text)
    # hashtags
    text = re.sub(r'#', ' ', text)

    
    text = re.sub(r'@[^ ]+', '', text)



    # using default substitution _URL_
    text = tprep.replace.urls(text, ' ')
    text = normalize(text)
    return text.strip()

def extract_entities(doc: Doc,unused_param=None, sep='_') -> list[str]:

    ents = [e for e in doc.ents if len(e) <= 2 ]

    # append label and entity text like Angela_Merkel/PER
    ents = [sep.join([t.text for t in e]).strip('.\n')+'/'+e.label_ for e in ents]
    
    return ents

def extract_nlp(doc: Doc) -> dict[str,list[str]]:

    # same definition as above - just in case
    def extract_lemmas(doc, include_pos = None): # None extracts all lemmas
        return [t.lemma_ for t in doc 
            if include_pos is None or t.pos_ in include_pos and not t._.is_emoji or 'EMOJI' in include_pos and t._.is_emoji ]

    return {
    'lemmas'          : extract_lemmas(doc, 
                          include_pos = ['ADJ', 'ADP', 'ADV', 'VERB', 'INTJ', 
                                         'NOUN', 'PROPN', 'PRON', 'VERB']),
    'adjs_verbs'      : extract_lemmas(doc, include_pos = ['ADJ', 'VERB']),
    'nouns'           : extract_lemmas(doc, include_pos = ['NOUN', 'PROPN']),
    'entities'        : extract_entities(doc, ['PER', 'ORG', 'GPE', 'LOC']),
    'emojis'          : extract_lemmas(doc, include_pos=['EMOJI'])
    }

def display_nlp(doc: Doc, include_punct=False):
    """Generate data frame for visualization of spaCy tokens."""
    rows = []
    for i, t in enumerate(doc):
        if not t.is_punct or include_punct:
            row = {'token': i,  'text': t.text, 'lemma_': t.lemma_, 
                   'is_stop': t.is_stop, 'is_alpha': t.is_alpha,
                   'pos_': t.pos_, 'dep_': t.dep_, 
                   'ent_type_': t.ent_type_, 'ent_iob_': t.ent_iob_}
            rows.append(row)
    
    df = pd.DataFrame(rows).set_index('token')
    df.index.name = None
    return df

def add_lemmas_to_df(df: pd.DataFrame, nlp:Language ) -> pd.DataFrame:
    batch_size = 100
    num_batches = math.ceil(len(df) / batch_size)


    nlp_columns = list(extract_nlp(nlp.make_doc('')).keys())


    for col in nlp_columns:
        df[col] = None

    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=pd.errors.SettingWithCopyWarning)
        for i in tqdm(range(0, len(df), batch_size), total=num_batches):
            
            # spaCy Batch-Verarbeitung mit nlp.pipe, liefert eine Liste von Ergebnis-Docs
            docs = nlp.pipe(df['cleaned_text'][i:i+batch_size])

            try:
                # Extraktion der Lemmas und Eintragen im DataFrame für einen Batch
                for j, doc in enumerate(docs):
                    for col, values in extract_nlp(doc).items():
                        df[col].iloc[i+j] = values
            except:
                print('ERROR', i)
                raise

    return df
