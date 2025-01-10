from os import getenv
import re
import numpy as np
import pandas as pd
import joblib
from scipy.stats import entropy
from urllib.parse import urlparse, parse_qs
import nltk

nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('averaged_perceptron_tagger_eng')
nltk.download('stopwords')

TOP_10M_DOMAINS_PATH = getenv('TOP_10M_DOMAINS_PATH')
TLD_ENCODER_PATH = getenv('TLD_ENCODER_PATH')
KNOWN_PHISHING_DOMAINS_PATH = getenv('KNOWN_PHISHING_DOMAINS_PATH')

def _nltk_pos_tagger(nltk_tag):
    if nltk_tag.startswith('J'):
        return nltk.corpus.wordnet.ADJ
    elif nltk_tag.startswith('V'):
        return nltk.corpus.wordnet.VERB
    elif nltk_tag.startswith('N'):
        return nltk.corpus.wordnet.NOUN
    elif nltk_tag.startswith('R'):
        return nltk.corpus.wordnet.ADV
    else:          
        return None


def _nltk_pos_lemmatizer(lemmatizer, token, tag):
    if tag is None:
        return lemmatizer.lemmatize(token)
    else:        
        return lemmatizer.lemmatize(token, tag)


def text_pre_processing(txt, m=2):
    if txt is not None:
        lemmatizer = nltk.WordNetLemmatizer()
        stop_words = set(nltk.corpus.stopwords.words('english'))

        tokens = nltk.word_tokenize(txt)
        tokens = [w for w in tokens if w.isalpha()]
        tokens = [w for w in tokens if w not in stop_words]
        tokens = nltk.pos_tag(tokens)
        tokens = [(t[0], _nltk_pos_tagger(t[1])) for t in tokens]
        tokens = [_nltk_pos_lemmatizer(lemmatizer, w, t).lower() for w,t in tokens]
        tokens = [w for w in tokens if len(w) > m]
    else:
        tokens = []
    return tokens

def extract_features(url):
    top_10m_domains = pd.read_csv(TOP_10M_DOMAINS_PATH, usecols=['Domain'])
    top_10m_domains = set(top_10m_domains['Domain'])

    known_phishing_domains = pd.read_csv(KNOWN_PHISHING_DOMAINS_PATH, header=None, names=['domain'])
    known_phishing_domains = set(known_phishing_domains['domain'])

    parsed_url = urlparse(url)
    domain = parsed_url.netloc.replace('www.', '') # ignore www
    url = url.replace('www.', '', 1)
    url = url.replace('http://', '')
    url = url.replace('https://', '')
    features = {}
    
    # Check if the domain is in the Open Page Rank dataset
    # top_10m_domains is a dictionary with the top 10 million domains
    features['in_top_10m'] = 1 if domain in top_10m_domains else 0

    # Check if the domain is in the known phishing domains list
    features['in_phishing_domains'] = 1 if domain in known_phishing_domains else 0

    # URL Features
    features['url_length'] = len(url)
    features['digits_count'] = len(re.findall(r'\d', url))
    features['letters_count'] = len(re.findall(r'[a-zA-Z]', url))
    features['digits_to_letters_ratio'] = features['digits_count'] / (features['letters_count'] + 1)
    features['special_chars_count'] = len(re.findall(r'[^a-zA-Z0-9]', url))

    # Domain Features
    features['domain_length'] = len(domain)
    features['has_ip'] = 1 if re.search(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', domain) else 0
    features['subdomain_count'] = len(domain.split('.')) - 2  # Subtract domain + TLD

    tld_encoder = joblib.load(TLD_ENCODER_PATH)
    tld = domain.split('.')[-1]
    features['tld'] = tld_encoder.transform([tld])[0] if tld in tld_encoder.classes_ else -1

    # Shannon entropy of the URL and domain
    features['shannon_entropy_url'] = shannon_entropy(url)
    features['shannon_entropy_domain'] = shannon_entropy(domain)

    # Query Features
    features['query_length'] = len(parsed_url.query)
    features['params_count'] = len(parse_qs(parsed_url.query))
    features['longest_query_key_length'] = max([len(key) for key in parse_qs(parsed_url.query)] + [0])
    features['longest_query_value_length'] = max([len(value[0]) for value in parse_qs(parsed_url.query).values()] + [0])

    # Path Features
    features['path_length'] = len(parsed_url.path)
    features['url_path_depth'] = len(parsed_url.path.strip('/').split('/'))
    features['longest_path_segment'] = max([len(p) for p in parsed_url.path.split('/')], default=0)
    features['last_path_segment_length'] = len(parsed_url.path.split('/')[-1])

    return pd.DataFrame([features])

def shannon_entropy(s):
    # Calculate the probability distribution of characters in the string
    char_counts = {char: s.count(char) for char in set(s)}
    total_chars = len(s)
    
    # Probability distribution
    probs = np.array([count / total_chars for count in char_counts.values()])
    
    # Use scipy's entropy function to calculate the Shannon entropy
    return entropy(probs, base=2)
