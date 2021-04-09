import json
from re import sub
import os.path
import argparse
import typing

# Global Variables
# Default link will use in add_arguments
DEFAULT_LINK_WIKI_SAMPLE = r'..\Data\wikipedia_sample'
DEFAULT_LINK_STOP_WORDS = r'..\Data\stop_words_en.txt'
DEFAULT_LINK_INVERTED_INDEX = r'D:\Development\Coding\result-inverted-index\inverted.index'

# work_links = {
#     'link_wiki_sample': r'..\Data\wikipedia_sample',
#     'link_stop_words': r'..\Data\stop_words_en.txt',
#     'link_inverted_index': r'D:\Development\Coding\result-inverted-index\inverted.index'}


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


def set_parser(parser):
    # argument to set path dataset file
    parser.add_argument('-d', "--dataset", default=DEFAULT_LINK_WIKI_SAMPLE,
                        help='This is a link to a file with documents'
                             'from which will be converted to an inverted index.',
                        type=str)
    # required=True -- делает обязательным аргументом

    # argument to set path stop words file
    parser.add_argument('-sw', "--stopwords", default=DEFAULT_LINK_STOP_WORDS,
                        help='This is a link to a file stop words.',
                        type=str)
    # argument to set the path for save inverted index file
    parser.add_argument('-pathii', "--path_invertedindex", default=DEFAULT_LINK_INVERTED_INDEX,
                        help='This is a link where the inverted index will be saved',
                        type=str)

    # argument to query for words
    parser.add_argument('-q', '--query', help='Words that will determine the indices of the files where it occurs',
                        type=str, nargs='*', default=None)

    # flag for creat inverted index
    parser.add_argument(
        '-c', '--creat',
        action='store_true',
        default=False,
        help='Create an inverted index file')

    # flag for search words in inverted index
    parser.add_argument(
        '-s', '--search',
        action='store_true',
        default=False,
        help='Search for words in inverted index. This flag requires a positional argument',
    )

def main():
    # Argument processing
    parser = argparse.ArgumentParser(
        description='This program (%(prog)s) creates an Inverted Index from a set of documents',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    set_parser(parser)
    args = parser.parse_args()
    # search words
    requested_word = args.query
    # flags
    flag_c = args.creat
    flag_s = args.search
    # links derived from arguments
    work_links = {
        'link_wiki_sample': args.dataset,
        'link_stop_words': args.stopwords,
        'link_inverted_index': args.path_invertedindex
    }

    # creation script inverted index
    if flag_c:
        # Creat inverted index and save her in filt by path
        print('loading documents ...')
        indexs, words = load_documents(work_links['link_wiki_sample'])
        print('loading documents is complete')
        print('loading stop words ...')
        stop_words = load_stop_words(work_links['link_stop_words'])
        print('loading stop words is complete')
        print('start build inverted index ... ')
        inverted_index1 = build_inverted_index(indexs=indexs, words=words, stop_words=stop_words)
        print('dump inverted index ... ')
        inverted_index1.dump(work_links['link_inverted_index'])
        print(f'The inverted index is built.\nThe path to the file\n\t{work_links["link_inverted_index"]}')
    elif flag_s:
        # Search words in inverted index
        if requested_word:
            print("loading inverted index ...")
            f_inverted_index = InvertedIndex.load(filepath=work_links['link_inverted_index'])
            print('loading inverted index is complete')
            print("search words ...")
            return_id_docs_with_requested_words = f_inverted_index.query(requested_word)
            print('Your query: {f1}'.format(f1=return_id_docs_with_requested_words))
        else:
            print('Enter the words you want to find as arguments!',
                  f'Positional Argument requested_word={requested_word}')
    # indexs, words = load_documents(work_links['link_wiki_sample'])
    # stop_words = load_stop_words(work_links['link_stop_words'])
    # inverted_index1 = build_inverted_index(indexs=indexs, words=words, stop_words=stop_words)
    # inverted_index1.dump(work_links['link_inverted_index'])  # json записывается на диск
    # inverted_index2 = InvertedIndex.load(work_links['link_inverted_index'])
    # document_ids = inverted_index2.query(requested_word)
    # print(f'Your query {document_ids}')


if __name__ == "__main__":
    main()
