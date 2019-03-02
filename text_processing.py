import string
import numpy as np

punc_list = list(string.punctuation)
whitespace_list = list(string.whitespace)
delete_list = punc_list + whitespace_list

def parse_text(file_name):
    lines = []
    words = []

    with open(file_name) as text:
        for line in text:
            processed_line = line.strip()
            lines.append(processed_line)

    for i in range(len(lines)):
        words.extend(lines[i].split())

    for i in range(len(words)):
        words[i] = words[i].strip("".join(delete_list))
        words[i] = words[i].lower()
    return words[1000:len(words)-1000] # chop off the beginning and end of the
    # text file because a lot of these parts are not the actual model

def build_dataset(file_name):
    """
    This dataset will be used to train a model to predict what word follows the
    preceding four words.
    """
    words = parse_text(file_name)
    len_words = len(words)
    index_lim = len_words - 5
    data = np.ndarray((index_lim,2),dtype='a100')
    for i in range(index_lim):
        try:
            data[i][0] = "{} {} {} {}".format(words[i], words[i+1], words[i+2], words[i+3])
            data[i][1] = words[i+4]
        except:
            continue
    return data

if __name__ == "__main__":
    file_name = "Adventures of Huckleberry Finn___Mark Twain.txt"
    data = build_dataset(file_name)
    print(data[0][0])
