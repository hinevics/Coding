import pandas as pd
import json

work_links = {
    'dataset': r'.\wikipedia_sample',
    'stop_words': r'.\stop_words_en.txt',
    'invert_index': ...}


class InvertedIndex(object):
    def query(self, words):
        pass

    def dump(self, filepath):
        pass

    @classmethod
    def load(cls, filepath):
        pass


def load_documents(filepath):
    with open(file=filepath, encoding='utf-8') as file:
        result = file.readlines()
    return result


def load_stop_words(filepath):
    with open(file=filepath, encoding='utf-8') as file:
        result = set(map(lambda x: x.strip('\n'), file.readlines()))
    return result


def build_inverted_index(documents, stop_words):
    # id_words words id_doc
    # id_doc
    # allwords_alldocs_list -- unique --  sorted -- del stop_words -- index
    for document in map(lambda x: x.split(' '), documents):
        # через map разбиваю документ (ввиде целой стороки разеделнной пробелами) на список символов
        index = document.pop(0).split('\t')  # 0 это индекс назавания статьи и index'a документа
        print(index)
        break


def main():
    documents = load_documents(work_links['dataset'])
    stop_words = load_stop_words(work_links['stop_words'])
    # inverted_index = build_inverted_index(documents, stop_words)
    # inverted_index.dump("inverted.index")  # json
    # inverted_index = InvertedIndex.load("inverted.index")
    # document_ids = inverted_index.query(["two", "words"])


if __name__ == "__main__":
    main()