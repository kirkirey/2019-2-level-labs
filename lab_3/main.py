"""
Labour work #3
 Building an own N-gram model
"""

import math

REFERENCE_TEXT = ''


if __name__ == '__main__':
    with open('not_so_big_reference_text.txt', 'r') as f:
        REFERENCE_TEXT = f.read()


class WordStorage:
    def __init__(self):
        self.storage = {}

    def put(self, word: str) -> int:
        if word in self.storage or not isinstance(word, str):
            return -1
        word_id = len(self.storage)
        self.storage[word] = word_id
        return word_id

    def get_id_of(self, word: str) -> int:
        if word not in self.storage or not isinstance(word, str):
            return -1
        return self.storage[word]

    def get_original_by(self, id: int) -> str:
        if id not in self.storage.values() or not isinstance(id, int):
            return 'UNK'
        for key, value in self.storage.items():
            if id == value:
                return key

    def from_corpus(self, corpus: tuple):
        if not isinstance(corpus, tuple):
            return -1
        for word in corpus:
            self.put(word)
        return corpus


class NGramTrie:
    def __init__(self, n=2):
        self.size = n
        self.gram_frequencies = {}
        self.gram_log_probabilities = {}

    def fill_from_sentence(self, sentence: tuple) -> str:
        if not isinstance(sentence, str) or self.size > len(sentence):
            return "ERROR"
        grams = []
        for i in range(len(sentence)):
            if len(sentence) - i > self.size:
                grams.append(sentence[i:i + self.size])
            elif len(sentence) - i == self.size:
                grams.append(sentence[i:len(sentence)])
            else:
                pass
        for gram in grams:
            try:
                self.gram_frequencies[gram] += 1
            except ValueError:
                self.gram_frequencies[gram] = 1
        return 'OK'

    def calculate_log_probabilities(self):
        for gram in self.gram_frequencies:
            k = 0
            for gram_source in self.gram_frequencies.keys():
                if gram_source[:-1] == gram[:-1]:
                    k += list(self.gram_frequencies.values())[gram_source]
            log_source = self.gram_frequencies[gram] / k
            self.gram_log_probabilities[gram] = math.log(log_source)

    def predict_next_sentence(self, sentence: tuple) -> list:
        if not isinstance(sentence, tuple) or len(sentence) is not self.size - 1:
            return []
        #for k in range(round(len(self.gram_log_probabilities) / 2)):
        for k in range(len(self.gram_log_probabilities) // 2):
            grams = list(sentence)
            for i, j in self.gram_log_probabilities.items():
                if grams[k:] == list(i)[:self.size - 1]:
                    try:
                        max_value = j
                    except ValueError:
                        max_value = j
            for i, j in self.gram_log_probabilities.items():
                if j == max_value:
                    grams.append(i[-1])
        return grams


def encode(storage_instance, corpus) -> list:
    corpus_final = []
    sentence_list = []
    for sentence in corpus:
        for word in sentence:
            word_source = storage_instance.get_id_of(word)
            sentence_list += [word_source]
        corpus_final += [sentence_list]
        sentence_list = []
    return corpus_final


def split_by_sentence(text: str) -> list:
    if not isinstance(text, str):
        return []
    text = str(text).lower().replace('\n', ' ')
    sentence = []
    sentence_text = ''
    corpus = []
    for letter in text:
        if letter not in '.!?':
            if letter.isalpha() or letter is ' ':
                sentence_text += letter
        else:
            sentence_text = '<s> ' + sentence_text + ' </s>'
            sentence.extend(sentence_text.split(' '))
            while '' in sentence:
                sentence.remove('')
            corpus.append(sentence)
            sentence = []
            sentence_text = ''
    return corpus


string = 'Mar#y wa$nted, to swim! However, she was afraid of sharks.'
