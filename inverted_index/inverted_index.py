import json
from re import sub
import os
import argparse
import typing

# Global Variables
# Default link will use in add_arguments
DEFAULT_LINK_WIKI_SAMPLE = r'..\Data\wikipedia_sample'
DEFAULT_LINK_STOP_WORDS = r'..\Data\stop_words_en.txt'
DEFAULT_LINK_INVERTED_INDEX = r'D:\Development\Coding\result-inverted-index'
DEFAULT_LINK_REQUESTED_DOCUMENTS = r'D:\Development\Coding\result-inverted-index'
DEFAULT_NAME_FILE_INVERTED_INDEX = r'inverted.index'
DEFAULT_NAME_FILE_DOCUMENTS = r'documents.txt'


class StoragePolicy:
    def dump(self, word_to_docs_mapping, index_fio, ):
        raise IndentationError

    def load(self, index_dio):
        raise IndentationError


class JsonIndexPolicy(StoragePolicy):
    def dump(self, word_to_docs_mapping, index_fio):
        words_doc_ids = {
            word: list(ids) for word, ids in word_to_docs_mapping.items()}
        dump = json.dumps(word_to_docs_mapping)
        index_fio.write(dump)


class InvertedIndex:
    def __init__(self, word_to_docs_mapping: dict):

        self.word_to_docs_mapping = {
            word: doc_ids for word, doc_ids in word_to_docs_mapping.items()}

    def query(self, words):
        result_query = set(
            self.word_to_docs_mapping.setdefault(words[0], [])
        )
        for word in words[1:]:
            result_query.intersection(set(
                self.word_to_docs_mapping.setdefault(word, [])
            ))
        return result_query

    def dump(self, filepath: str, storage_policy=None):
        storage_policy = storage_policy or JsonIndexPolicy()

        words_doc_ids = {
            word: list(ids) for word, ids in self.word_to_docs_mapping.items()}

        # dumping in file
        with open(file=filepath, mode='w') as file:
            storage_policy.dump(words_doc_ids, file)

    def rewriting(self, filepath: str):
        """
        overwrite existing inverted index
        :param filepath: path to file
        """

        words_doc_ids = {
            word: list(ids) for word, ids in self.word_to_docs_mapping.items()}

        # Checking for the existence of a file
        check_file = os.path.isfile(filepath)

        # This is interface work with  file
        if check_file:
            # If the file is
            with open(file=filepath, mode='r') as file:
                words_with_file = json.load(fp=file)
        else:
            # an empty dictionary for a file that does not exist
            words_with_file = dict()

        # update dict
        if set(words_doc_ids.keys()).isdisjoint(set(words_with_file.keys())):
            words_with_file.update(words_doc_ids)
        else:
            # update words
            keys_intersection = set(words_doc_ids.keys()) & set(words_with_file.keys())
            keys_difference = set()
            for key in keys_intersection:
                words_with_file[key] += words_doc_ids[key]
            for key in keys_difference:
                words_with_file[key] = words_doc_ids[key]

        # rewriting file
        with open(file=filepath, mode='w') as file:
            json.dump(words_with_file, file)

    @classmethod
    def load(cls, filepath: str, storage_policy=None):
        storage_policy = storage_policy or JsonIndexPolicy()
        # read from disk
        with open(file=filepath, mode='r', encoding='utf-8') as file:
            return InvertedIndex({index: set(words) for index, words in json.load(fp=file).items()})

    @classmethod
    def search_documents(cls, filpath: str):
        raise IndentationError


def word_frequency():
    # Функция поиска частоты слов
    raise IndentationError


def open_documents(filepath: str):
    # Выделяет индекс и сами документа
    raise IndentationError


def load_documents(filepath: str):
    """
    Функци для получения пар индес-слова
    :param filepath: path to document
    :return:
    """
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


def function_create_index_document_pair(path_dataset):
    with open(file=path_dataset, mode='r', encoding='utf-8') as file:
        reading_file = {int(index): docs for index, docs in map(lambda x: x.split('\t', 1), file.readlines())}
        return reading_file


def squeak_of_documents_by_index(path_datasets, path_stopwords, path_documents, query_words, name_documents):
    full_name_path_save_doc = '{path}/{name}'.format(path=path_documents,
                                                     name=name_documents)
    if query_words:
        print('.........LODING.........')
        print('Documents path: {path}'.format(path=repr(path_datasets)))
        print('loading documents ...')
        indexs, words = load_documents(path_datasets)
        print('loading documents is complete')
        print('Stop words path: {path}'.format(path=repr(path_stopwords)))
        print('loading stop words ...')
        stop_words = load_stop_words(path_stopwords)
        print('loading stop words is complete')
        print('start build inverted index ... ')
        inverted_index1 = build_inverted_index(indexs=indexs, words=words, stop_words=stop_words)
        print('build inverted index is complete')
        print('.........SEARCH_INDEXS.........')
        search_index = inverted_index1.query(query_words)
        print('.........SAVE_DOCUMENTS.........')
        print('Save documents path: {fullpath}'.format(fullpath=full_name_path_save_doc))
        with open(file=full_name_path_save_doc,
                  mode='w', encoding='utf-8') as file_write:
            create_index_document_pair = function_create_index_document_pair(path_datasets)
            for ind in search_index:
                file_write.write('{ind}\t'.format(ind=ind) + create_index_document_pair[ind])
                print('save documents number {f1} ...'.format(f1=ind))
    else:
        print('Enter the words you want to find as arguments!',
              f'Positional Argument requested_word={query_words}.\n'
              f'Pass an argument "-q"')


def search_index_of_documents_by_words(query_words, path_invertedindex):
    # Search words in inverted index
    print('\n.......Search inverted index.......')
    if query_words:
        print("loading inverted index ...")
        print('Inverted index path: {fullname}'.format(fullname=path_invertedindex))
        f_inverted_index = InvertedIndex.load(filepath=path_invertedindex)
        print('loading inverted index is complete')
        print("search words ...")
        return_id_docs_with_requested_words = f_inverted_index.query(query_words)
        print('Your query: {f1}'.format(f1=return_id_docs_with_requested_words))
        return return_id_docs_with_requested_words
    else:
        print('Enter the words you want to find as arguments!',
              f'Positional Argument requested_word={query_words}'
              f'Pass an argument "-q"')


def creating_inverted_index(path_datasets, path_stopwords, path_invertedindex, name_inverted_index):
    # function to create an inverted index

    full_name_inverted_index = '{path}/{name}'.format(path=path_invertedindex,
                                                      name=name_inverted_index)
    print('loading documents ...')
    indexs, words = load_documents(path_datasets)
    print('loading documents is complete')
    print('loading stop words ...')
    stop_words = load_stop_words(path_stopwords)
    print('loading stop words is complete')
    print('start build inverted index ... ')
    inverted_index1 = build_inverted_index(indexs=indexs, words=words, stop_words=stop_words)
    print('dump inverted index ... ')
    inverted_index1.dump(filepath=full_name_inverted_index)
    print(f'The inverted index is built.\n'
          f'The path to the file\n{full_name_inverted_index}')
    print('.......Completion of work.......')


def processing_query(query_argumen):
    search_index_of_documents_by_words(
        query_words=query_argumen.query,
        path_invertedindex=query_argumen.path_invertedindex
    )


def processing_build_inverted_index(build_arguments):
    creating_inverted_index(
        path_datasets=build_arguments.path_dataset,
        path_stopwords=build_arguments.path_stopwords,
        path_invertedindex=build_arguments.path_invertedindex,
        name_inverted_index=build_arguments.name_inverted_index
    )


def processing_search(search_arguments):
    squeak_of_documents_by_index(
        path_datasets=search_arguments.path_dataset,
        path_stopwords=search_arguments.path_stopwords,
        path_documents=search_arguments.path_documents,
        name_documents=search_arguments.name_documents,
        query_words=search_arguments.query
    )


def set_parser(parser):
    # creat subparser
    subparsers = parser.add_subparsers(help='choose command to run')

    # arguments parser for creat inverted index
    creat_parser = subparsers.add_parser('build', help='Build an inverted index file',
                                         formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    creat_parser.set_defaults(callback=processing_build_inverted_index)

    # Creat Inverted Index

    # argument to set path dataset file
    creat_parser.add_argument('-pds', "--path_dataset", default=DEFAULT_LINK_WIKI_SAMPLE,
                              help='This is a link to a file with documents'
                                   'from which will be converted to an inverted index.',
                              type=str)
    # required=True -- делает обязательным аргументом

    # argument to set path stop words file
    creat_parser.add_argument('-psw', "--path_stopwords", default=DEFAULT_LINK_STOP_WORDS,
                              help='This is a link to a file stop words.',
                              type=str)

    # argument to set the path for save inverted index file
    creat_parser.add_argument('-pii', "--path_invertedindex", default=DEFAULT_LINK_INVERTED_INDEX,
                              help='This is a link where the inverted index will be saved',
                              type=str)
    # arguments with the name of the inverted index file
    creat_parser.add_argument(
        '-nii', '--name_inverted_index', default=DEFAULT_NAME_FILE_INVERTED_INDEX,
        help='The name of the resulting file in which the inverted index will be saved', type=str
    )

    # Query words

    query_parser = subparsers.add_parser('query', help='Two test subparses',
                                         formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    query_parser.add_argument('-pii', "--path_invertedindex",
                              default='{path}/{name}'.format(
                                  path=DEFAULT_LINK_INVERTED_INDEX,
                                  name=DEFAULT_NAME_FILE_INVERTED_INDEX),
                              help='This is a link where the inverted index will be saved',
                              type=str)
    query_parser.add_argument('-q', '--query',
                              help='Words that will determine the indices of the files where it occurs',
                              type=str, nargs='*', default=None)
    query_parser.set_defaults(callback=processing_query)

    # Search documents

    search_parser = subparsers.add_parser('search', help='Search documents by words')

    # path datasets
    search_parser.add_argument('-pds', "--path_dataset", default=DEFAULT_LINK_WIKI_SAMPLE,
                               help='This is a link to a file with documents'
                                    'from which will be converted to an inverted index.',
                               type=str)

    # path stop words
    search_parser.add_argument('-psw', "--path_stopwords", default=DEFAULT_LINK_STOP_WORDS,
                               help='This is a link to a file stop words.',
                               type=str)

    # path documents save
    search_parser.add_argument('-psd', '--path_documents',
                               help='path where documents will be saved',
                               default=DEFAULT_LINK_REQUESTED_DOCUMENTS,
                               type=str)
    # name save documents
    search_parser.add_argument('-nd', '--name_documents',
                               help='this arguments with name of file with search documents',
                               type=str, default=DEFAULT_NAME_FILE_DOCUMENTS)
    # query
    search_parser.add_argument('-q', '--query',
                               help='Words that will determine the indices of the files where it occurs',
                               type=str, nargs='*', default=None)
    search_parser.set_defaults(callback=processing_search)


def main():
    # Argument processing
    parser = argparse.ArgumentParser(
        description='This program (%(prog)s) creates an Inverted Index from a set of documents',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    set_parser(parser)
    args = parser.parse_args()
    args.callback(args)  # callback for branches


if __name__ == "__main__":
    main()
