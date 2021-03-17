import json
# from collections import defaultdict

work_links = {
    'dataset': r'D:\Development\Coding\Coding\Data\wikipedia_sample',
    'stop_words': r'D:\Development\Coding\Coding\Data\stop_words_en.txt',
    'invert_index': ...}


class InvertedIndex:
    def __init__(self, word_to_docs_mapping):
        self.word_to_docs_mapping = {
            word: doc_ids for word, doc_ids in word_to_docs_mapping.items()}

    def query(self, words):
        raise NotImplementedError

    def dump(self, filepath):
        # загрузка на диск
        with open(file=filepath, mode='w') as file:
            words_doc_ids = {
                word: list(ids) for word, ids in self.word_to_docs_mapping.items()}
            json.dump(words_doc_ids, file)

    @classmethod
    def load(cls, filepath):
        # считывем с диска
        with open(file=filepath, mode='r') as file:
            return {index: set(words) for index, words in json.load(fp=file).items()}


def load_documents(filepath):
    with open(file=filepath, encoding='utf-8') as file:
        documents = file.readlines()
    index, words = [], []
    for document in map(lambda x: x.split(' '), documents):
        # через map разбиваю документ (ввиде целой стороки разеделнной пробелами) на список символов
        index_doc = int(document.pop(0).split('\t')[0])  # 0 это индекс назавания статьи и index'a документа
        index.append(index_doc)
        words.append(set([i.lower() for i in document if i.isalpha()]))
    return index, words


def load_stop_words(filepath):
    with open(file=filepath, encoding='utf-8') as file:
        result = set(map(lambda x: x.strip('\n'), file.readlines()))
    return result


def build_inverted_index(indexs, words, stop_words):
    inverted_index = dict()
    for word, index in zip(words, indexs):
        word.difference_update(stop_words)
        for w in word:
            if not (w in inverted_index.keys()):
                inverted_index[w] = {index}
            else:
                inverted_index[w].update({index})
    return InvertedIndex(inverted_index)


def main():
    indexs, words = load_documents(work_links['dataset'])
    stop_words = load_stop_words(work_links['stop_words'])
    inverted_index = build_inverted_index(indexs=indexs, words=words, stop_words=stop_words)
    inverted_index.dump("inverted.index")  # json записывается на диск
    inverted_index = InvertedIndex.load("inverted.index")
    print(inverted_index['diggers'])

    # document_ids = inverted_index.query(["two", "words"])


if __name__ == "__main__":
    main()