def calculate_frequences(text: str) -> dict:
    if text != None:
        text = str(text).lower().replace('\n', ' ')
    else:
        return {}
    junk = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '!', '@', '#', '$', '%', '^', '&', '*', '`', '~', '&','.',
            ',', ';', ':', '?','(', ')', '[', ']', '{', '}', '-', '=', '_', '+', ';', ':','|','/','"',"'"]
    clean_text = ''
    junk_found = False
    for i in text:
        for j in junk:
            if i == j:
                junk_found = True
                break
        if junk_found == False:
            clean_text += i
        junk_found = False
    freq_source = clean_text.split(' ')
    frequencies = {}
    for i in range(len(freq_source)):
        if freq_source[i] == '':
            pass
        elif freq_source[i] not in frequencies.keys():
            frequencies[freq_source[i]] = 1
        else:
            frequencies[freq_source[i]] += 1
    return frequencies

def filter_stop_words(frequencies: dict, stop_words: tuple) -> dict:
    if frequencies == None:
        return {}
    elif stop_words == None:
        return frequencies
    else:
        frequencies_clean = dict(frequencies)
        stop_words_correct = []
        for i in stop_words:
            stop_words_correct.append(str(i))
        for i in frequencies_clean.keys():
            if type(i) != str:
                stop_words_correct.append(i)
        for i in stop_words_correct:
            if i in frequencies_clean.keys():
                frequencies_clean.pop(i)
        return frequencies_clean

def get_top_n(frequencies: dict, top_n: int) -> tuple:
    freq_top_list = []
    if top_n >= len(frequencies):
        return tuple(frequencies.keys())
    for i in range(top_n):
        k = 0
        for key, value in frequencies.items():
            if value >= k:
                top_word = key
                k = value
        else:
            freq_top_list.append(top_word)
            frequencies.pop(top_word)
    return tuple(freq_top_list)