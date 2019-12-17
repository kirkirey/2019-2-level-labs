import math

REFERENCE_TEXTS = []


def clean_tokenize_corpus(texts: list) -> list:
    corpus = []
    for text in texts:
        text_source = ''
        corpus_source = []
        if not isinstance(text, str):
            corpus.append([])
        else:
            text = text.lower().replace('\n', ' ')
        for letter in text:
            if letter.isalpha() or letter is ' ':
                text_source += letter
        else:
            corpus_source = text_source.split(' ')
            while '' in corpus_source:
                corpus_source.remove('')
        corpus.append(corpus_source)
    return corpus


class TfIdfCalculator:
    def __init__(self, corpus):
        self.corpus = corpus
        self.tf_values = []
        self.idf_values = {}
        self.tf_idf_values = []

    def calculate_tf(self):
        if self.corpus:
            for text in self.corpus:
                if not isinstance(text, list):
                    continue  # скип
                tf_value = {}
                for word in text:
                    if not isinstance(word, str):
                        continue  # скип
                    if word not in tf_value:
                        tf_value[word] = text.count(word) / len(text)
                self.tf_values.append(tf_value)
        return self.tf_values

    def calculate_idf(self):
        if self.corpus:
            for text in self.corpus:
                if not isinstance(text, list):
                    continue  # скип
                for word in text:
                    if not isinstance(word, str):
                        continue  # скип
                    word_freq_in_corpus = 0
                    for text_2 in self.corpus:
                        if not isinstance(text_2, list):
                            continue  # скип
                        if word in text_2:
                            word_freq_in_corpus += 1
                    self.idf_values[word] = math.log(len(self.corpus) / word_freq_in_corpus)
        return self.idf_values

    def calculate(self):
        if self.tf_values and self.idf_values:
            for tf_values in self.tf_values:
                tf_idf_value = {}
                for word, tf_value in tf_values.items():
                    tf_idf_value[word] = tf_value * self.idf_values[word]
                self.tf_idf_values.append(tf_idf_value)
        return self.tf_idf_values

    def report_on(self, word, document_index):
        if not self.tf_idf_values or document_index >= len(self.corpus):
            return ()
        try:
            tf_idf_value = self.tf_idf_values[document_index][word]
        except TypeError:
            return ()
        whew = sorted(self.tf_idf_values[document_index], key=lambda a: int(self.tf_idf_values[document_index][a]),
                      reverse=True)
        return tf_idf_value, whew.index(word)


if __name__ == '__main__':
    texts = ['5_7.txt', '15_2.txt', '10547_3.txt', '12230_7.txt']
    for text in texts:
        with open(text, 'r') as f:
            REFERENCE_TEXTS.append(f.read())
    # scenario to check your work
    test_texts = clean_tokenize_corpus(REFERENCE_TEXTS)
    tf_idf = TfIdfCalculator(test_texts)
    print('tf_tf.calculate_idf() ', tf_idf.calculate_tf())
    print('tf_idf.calculate_idf() ', tf_idf.calculate_idf())
    print('tf_idf.calculate() ', tf_idf.calculate())
    print(tf_idf.report_on('good', 0))
    print(tf_idf.report_on('and', 1))
