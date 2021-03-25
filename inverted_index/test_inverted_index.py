import json
import pytest
import inverted_index


def test_can_import_inverted_index_module_1():
    import inverted_index


def test_can_load_load_documents_2():
    assert inverted_index.load_documents


def test_len_document_3():
    """Unit Testing"""
    # Проверка длины документы
    test_link = inverted_index.work_links['dataset']
    with open(file=test_link, mode='r', encoding='utf-8') as file:
        data = file.readlines()
        assert len(data) == 4100


def test_work_function_load_documents_with_one_doc_4(tmpdir):
    test_doc = tmpdir.join('datatest.txt')  # создаю временный тестовый документ
    # временные тестовые данные
    test_doc.write('0\tTest text testing, my work now! Train testing this, working, bool?')
    test_index, test_words = inverted_index.load_documents(test_doc)
    etalon_index = [0]
    etalon_words = [{'test', 'text', 'testing', 'my', 'work', 'now', 'train', 'this', 'working', 'bool'}]
    assert etalon_index == test_index
    assert etalon_words == test_words


def test_work_function_load_documents_with_lot_doc_5(tmpdir):
    test_doc = tmpdir.join('datatest.txt')  # создаю временный тестовый документ
    test_doc.write('0\tTest text! test number one...\n1\tTest text... number two!')
    test_index, test_words = inverted_index.load_documents(test_doc)
    etalon_index = {0, 1}
    etalon_words = {0: {'test', 'text', 'number', 'one'},
                    1: {'test', 'number', 'two', 'text'}}
    assert etalon_index == set(test_index)
    for text, index in zip(test_words, test_index):
        assert text == etalon_words[index]


def test_work_function_load_documents_with_an_extra_newline_character_6(tmpdir):
    test_doc = tmpdir.join('datatest.txt')  # создаю временный тестовый документ
    test_doc.write('0\tTest text! test number one...\n1\tTest text... number two!\n')
    test_index, test_words = inverted_index.load_documents(test_doc)
    etalon_index = {0, 1}
    etalon_words = {0: {'test', 'text', 'number', 'one'},
                    1: {'test', 'number', 'two', 'text'}}
    assert etalon_index == set(test_index)
    for text, index in zip(test_words, test_index):
        assert text == etalon_words[index]


def test_work_function_load_documents_with_lot_doc_7(tmpdir):
    test_doc = tmpdir.join('datatest.txt')  # создаю временный тестовый документ
    test_doc.write('0\tTest text! test number one...\n1\tTest text... number two!\n'
                   '2\tKent!!!! red gay\n3\tBoys len lan\n12\tTrest!!! best wreit!')
    test_index, test_words = inverted_index.load_documents(test_doc)
    etalon_index = {0, 1, 2, 3, 12}
    etalon_words = {0: {'test', 'text', 'number', 'one'},
                    1: {'test', 'number', 'two', 'text'},
                    2: {'kent', 'red', 'gay'},
                    3: {'boys', 'len', 'lan'},
                    12: {'trest', 'best', 'wreit'}}
    assert etalon_index == set(test_index)
    for text, index in zip(test_words, test_index):
        assert text == etalon_words[index]


def test_load_stop_words_8(tmpdir):
    test_doc = tmpdir.join('datatest.txt')
    test_doc.write('Test\ntext\ntest\nnumber\none\nTe\ntext\nnumber2\ntwo')
    test_words = inverted_index.load_stop_words(test_doc)
    etalon_words = {'test', 'text', 'number', 'one', 'te', 'number2', 'two'}
    assert etalon_words == test_words


def test_load_stop_words_with_an_extra_newline_character_9(tmpdir):
    test_doc = tmpdir.join('datatest.txt')  # создаю временный тестовый документ
    test_doc.write('Test\ntext\ntest\nnumber\none\nTe\ntext\nnumber2\ntwo\n')
    test_words = inverted_index.load_stop_words(test_doc)
    etalon_words = {'test', 'text', 'number', 'one', 'te', 'number2', 'two'}
    assert etalon_words == test_words


def test_build_inverted_index_10():
    assert inverted_index.build_inverted_index


def test_build_inverted_index11():
    test_index = [0, 1, 3]
    test_words = [{'test', 'null', 'hi'}, {'test', 'one', 'lol'}, {'test', 'two', 'cant'}]
    test_stop_words = {'hi', 'cant', 'lol'}
    test_result = inverted_index.build_inverted_index(indexs=test_index, stop_words=test_stop_words,
                                                      words=test_words)
    assert test_result.word_to_docs_mapping == {'test': {0, 1, 3},
                                                'null': {0},
                                                'one': {1},
                                                'two': {3}}


def test_build_inverted_index_12():
    test_index = [0, 1, 3]
    test_words = [{'test', 'null', 'hi'}, {'test', 'one', 'lol'}, {'test', 'two', 'cant'}]
    test_stop_words = {'hi', 'cant', 'lol'}

    test_index2 = [15, 25]
    test_words2 = [{'one'}, {'two'}]
    test_result = inverted_index.build_inverted_index(indexs=test_index, stop_words=test_stop_words,
                                                      words=test_words)
    inverted_index.build_inverted_index(indexs=test_index2,
                                        stop_words=test_stop_words,
                                        words=test_words2)

    assert test_result.word_to_docs_mapping == {'test': {0, 1, 3},
                                                'null': {0},
                                                'one': {1},
                                                'two': {3}}


def test_class_invertedindex_and_build_inverted_index_13(tmp_path):
    f1 = tmp_path / 'temp'
    test_index = [0, 1, 3]
    test_words = [{'test', 'null', 'hi'}, {'test', 'one', 'lol'}, {'test', 'two', 'cant'}]
    test_stop_words = {'hi', 'cant', 'lol'}
    test_result = inverted_index.build_inverted_index(indexs=test_index, stop_words=test_stop_words,
                                                      words=test_words)
    test_result.dump(filepath=f1)
    test_inverted_index_load = inverted_index.InvertedIndex.load(filepath=f1)
    result = test_inverted_index_load.word_to_docs_mapping
    assert result == {
        'test': {0, 1, 3},
        'null': {0},
        'one': {1},
        'two': {3}
    }


def test_class_invertedindex_load_14(tmp_path):
    """
    Test for checking the work of the class load method in class InvertedIndex
    :param tmp_path: path to temporary file
    """
    f1 = tmp_path / 'temp'
    test_index = [0, 1, 2]
    test_words = [{'test', 'null', 'hi'}, {'test', 'one', 'lol'}, {'test', 'two', 'cant'}]
    test_stop_words = {'hi', 'cant', 'lol'}
    test_result = inverted_index.build_inverted_index(indexs=test_index, stop_words=test_stop_words,
                                                      words=test_words)
    test_result.dump(filepath=f1)

    test_inverted_index_load = inverted_index.InvertedIndex.load(filepath=f1)  # loading an object from a file
    test_inverted_index_word_to_mapping = test_inverted_index_load.word_to_docs_mapping
    etalon_inverted_index = {
        'test': {0, 1, 2},
        'null': {0},
        'one': {1},
        'two': {2}
    }
    assert test_inverted_index_word_to_mapping == etalon_inverted_index


def test_class_invertedindex_build_inverted_index_and_dump_load_15(tmp_path):
    f1 = tmp_path / 'temp'
    test_index = [0, 1, 3]
    test_words = [{'test', 'null', 'hi'}, {'test', 'one', 'lol'}, {'test', 'two', 'cant'}]
    test_stop_words = {'hi', 'cant', 'lol'}
    test_result = inverted_index.build_inverted_index(indexs=test_index, stop_words=test_stop_words,
                                                      words=test_words)
    test_result.dump(filepath=f1)

    test_index2 = [15, 25]
    test_words2 = [{'one'}, {'two'}]
    test_result2 = inverted_index.build_inverted_index(indexs=test_index2, stop_words=test_stop_words,
                                                       words=test_words2)

    test_result2.dump(filepath=f1)

    test_inverted_index_load = inverted_index.InvertedIndex.load(filepath=f1)

    assert test_inverted_index_load.word_to_docs_mapping == {
        'test': {0, 1, 3},
        'null': {0},
        'one': {1, 15},
        'two': {3, 25}
    }


def test_class_invertedindex_load_out_indices_16(tmp_path):
    test_inverted_index = {
        'test': [0, 1, 3],
        'null': [0],
        'one': [1, 15],
        'two': [3, 25]
    }
    test_path = tmp_path / 'test_index_inverted.index'
    ftest = test_path.open(mode='w', encoding='utf-8')
    json.dump(test_inverted_index, ftest)
    ftest.close()

    inverted_index_load= inverted_index.InvertedIndex.load(test_path)

    etalon = {
        'test': {0, 1, 3},
        'null': {0},
        'one': {1, 15},
        'two': {3, 25}
    }
    assert etalon == inverted_index_load.word_to_docs_mapping


def test_class_invertedindex_query_17(tmp_path):
    test_index = [0, 1, 3]
    test_words = [{'test', 'null', 'hi'}, {'test', 'one', 'lol'}, {'test', 'two', 'cant'}]
    test_stop_words = {'hi', 'cant', 'lol'}
    test_result = inverted_index.build_inverted_index(indexs=test_index, stop_words=test_stop_words,
                                                      words=test_words)
    test_query = test_result.query(['two', 'test'])
    etalon = {
        'two': {3},
        'test': {0, 1, 3}
    }
    assert test_query == etalon


def test_class_invertedindex_query_with_two_words_18(tmp_path):
    test_index = [0, 1, 3]
    test_words = [{'test', 'null', 'hi'}, {'test', 'one', 'lol'}, {'test', 'two', 'cant'}]
    test_stop_words = {'hi', 'cant', 'lol'}
    test_result = inverted_index.build_inverted_index(indexs=test_index, stop_words=test_stop_words,
                                                      words=test_words)
    test_query = test_result.query(['two', 'two'])
    etalon = {
        'two': {3}
    }
    assert test_query == etalon


@pytest.mark.skip(reason='not implemented test 19')
def test_class_inverted_index_query_if_not_word_19(tmp_path):
    """
    Тест направлен на проверку отработки случая отсутствия слова в наборе всех слов
    :param tmp_path:
    :return:
    """
    ...


def test_class_invertedindex_query_work_with_loaded_index_20(tmp_path):
    test_inverted_index = {
        'test': [0, 1, 3],
        'null': [0],
        'one': [1, 15],
        'two': [3, 25]
    }
    test_path = tmp_path / 'test_index_inverted.index'
    ftest = test_path.open(mode='w', encoding='utf-8')
    json.dump(test_inverted_index, ftest)
    ftest.close()

    test_load_inverted_index = inverted_index.InvertedIndex.load(test_path)
    test_query = test_load_inverted_index.query(['two'])
    etalon = {
        'two': {3, 25}
    }
    assert test_query == etalon


def test_all_21(tmp_path, tmpdir):
    test_doc = tmpdir.join('datatest.txt')  # создаю временный тестовый документ
    test_doc.write('0\tTest text! test number one...\n1\tTest text... number two!\n'
                   '2\tKent!!!! red gay\n3\tBoys len lan, two\n12\tTrest!!! best wreit!')
    test_doc2 = tmpdir.join('stop_words.txt')
    test_doc2.write('Test\ntest\nnumber\nTe\ntext\nnumber2')

    test_doc3 = tmpdir.join('inverted.index')

    indexs, words = inverted_index.load_documents(test_doc)
    stop_words = inverted_index.load_stop_words(test_doc2)

    test_inverted_index2 = inverted_index.build_inverted_index(indexs=indexs, words=words, stop_words=stop_words)
    test_inverted_index2.dump(test_doc3)  # json записывается на диск

    test_inverted_index_load = inverted_index.InvertedIndex.load(test_doc3)
    document_ids = test_inverted_index_load.query(["two"])
    etalon = {
        'two': {1, 3}
    }
    assert etalon == document_ids
