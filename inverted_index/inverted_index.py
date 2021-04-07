import json
from re import sub
import os.path
import argparse
import typing

default_links = {
    'link_wiki_sample': r'..\Data\wikipedia_sample',
    'link_stop_words': r'..\Data\stop_words_en.txt',
    'link_inverted_index': r'D:\Development\Coding\result-inverted-index\inverted.index'}

parser = argparse.ArgumentParser(description='This program creates an Inverted Index from a set of documents')
parser.add_argument("--link_wiki_sample", default=default_links['link_wiki_sample'],
                    help='This is a link to a file with documents from which will be converted to an inverted index',
                    type=str)
parser.add_argument("--link_stop_words", default=default_links['link_stop_words'],
                    help='This is a link to a file stop words',
                    type=str)
parser.add_argument("--link_inverted_index", default=default_links['link_inverted_index'],
                    help='This is a link where the inverted index will be saved',
                    type=str)

parser.add_argument('--rword', help='Words that will determine the indices of the files where it occurs',
                    required=True, type=str)
args = parser.parse_args()

requested_word = args.rword.split('-')
work_links = {
    'link_wiki_sample': args.link_wiki_sample,
    'link_stop_words': args.link_stop_words,
    'link_inverted_index': args.link_inverted_index
}


class InvertedIndex:
    def __init__(self, word_to_docs_mapping: dict):

        self.word_to_docs_mapping = {
            word: doc_ids for word, doc_ids in word_to_docs_mapping.items()}

    def query(self, words):
        return {word: self.word_to_docs_mapping[word] if word in self.word_to_docs_mapping else {}
                for word in words}

    def dump(self, filepath: str):
        # преобразую set в list для записи в json
        words_doc_ids = {
            word: list(ids) for word, ids in self.word_to_docs_mapping.items()}
        # проверка файла
        check_file = os.path.isfile(filepath)
        if check_file:
            with open(file=filepath, mode='r') as file:
                words_with_file = json.load(fp=file)
        else:
            words_with_file = dict()  # пустой словарь для файла которого нет

        # update dict
        if set(words_doc_ids.keys()).isdisjoint(set(words_with_file.keys())):
            words_with_file.update(words_doc_ids)
        else:
            keys_intersection = set(words_doc_ids.keys()) & set(words_with_file.keys())
            keys_difference = set()
            for key in keys_intersection:
                words_with_file[key] += words_doc_ids[key]
            for key in keys_difference:
                words_with_file[key] = words_doc_ids[key]
        # запись в файл
        with open(file=filepath, mode='w') as file:
            json.dump(words_with_file, file)

    @classmethod
    def load(cls, filepath: str):
        # считывем с диска
        with open(file=filepath, mode='r', encoding='utf-8') as file:
            return InvertedIndex({index: set(words) for index, words in json.load(fp=file).items()})


def load_documents(filepath: str):
    # выхов pdb
    # from pdb import set_trace
    # set_trace()

    # вызов ipython
    # from IPython import embed
    # embed()
    with open(file=filepath, encoding='utf-8') as file:
        documents = [i for i in sub(r'[\.\,\!\?]', '', file.read()).split('\n') if i != '']
    index, words = [], []
    for document in map(lambda x: x.split('\t'), documents):
        # через map разбиваю документ (ввиде целой стороки разеделнной пробелами) на список символов
        # 0 это индекс назавания статьи и index'a документа
        index.append(int(document[0]) if document[0] != '' else None)
        words.append(set([i.lower() for i in document[1].split(' ') if i.isalpha()]) if document[1] != '' else None)
    return index, words


def load_stop_words(filepath: str):
    with open(file=filepath, encoding='utf-8') as file:
        result = set(map(lambda x: x.lower().strip('\n'), file.readlines()))
    return result


def build_inverted_index(indexs: list, words: list, stop_words: set) -> InvertedIndex:
    inverted_index = dict()
    for word, index in zip(words, indexs):
        if not ((word is None) or (word == {})):
            word.difference_update(stop_words)
            for w in word:
                if not (w in inverted_index.keys()):
                    inverted_index[w] = {index}
                else:
                    inverted_index[w].update({index})
    return InvertedIndex(inverted_index)


def main():
    indexs, words = load_documents(work_links['link_wiki_sample'])
    stop_words = load_stop_words(work_links['link_stop_words'])
    inverted_index1 = build_inverted_index(indexs=indexs, words=words, stop_words=stop_words)
    inverted_index1.dump(work_links['link_inverted_index'])  # json записывается на диск
    inverted_index2 = InvertedIndex.load(work_links['link_inverted_index'])
    document_ids = inverted_index2.query(requested_word)
    print(f'Your query {document_ids}')


if __name__ == "__main__":
    main()
