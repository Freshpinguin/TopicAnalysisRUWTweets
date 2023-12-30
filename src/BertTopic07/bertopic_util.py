from spacy.lang.de import stop_words as de_stop_words
from spacy.lang.ru import stop_words as ru_stop_words
from spacy.lang.en import stop_words as en_stop_words
from spacy.lang.uk import stop_words as uk_stop_words
from spacy.lang.es import stop_words as es_stop_words
from spacy.lang.fr import stop_words as fr_stop_words
from spacy.lang.it import stop_words as it_stop_words

stop_words_list = [de_stop_words, ru_stop_words, es_stop_words, fr_stop_words, it_stop_words, en_stop_words, uk_stop_words]


all_stop_words = [words for stop_words in stop_words_list for words in stop_words.STOP_WORDS ]