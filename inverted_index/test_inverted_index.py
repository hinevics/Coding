import json
import pytest
import inverted_index

"""Unit Testing"""


def test_can_import_inverted_index_module_1():
    """
        Ипорт модуля inverted_index
    """
    assert inverted_index


def test_can_load_load_documents_2():
    """
        существует ли функция load_documents
    """
    assert inverted_index.load_documents


def test_len_document_3():
    """
        Проверка файла с документами
    """
    test_link = inverted_index.work_links['dataset']
    with open(file=test_link, mode='r', encoding='utf-8') as file:
        data = file.readlines()
        assert len(data) == 4100


def test_work_function_load_documents_with_one_doc_4(tmpdir):
    """
        Как отрабатывает функция при работе с одним нормальным документом в файле,  для записи тестируемого документа
        :param tmpdir: создаю файл во временной директории
    """
    test_doc = tmpdir.join('datatest.txt')  # создаю файл во временной директории
    # временные тестовые данные
    test_doc.write('0\tTest text testing, my work now! Train testing this, working, bool?')
    test_index, test_words = inverted_index.load_documents(test_doc)
    etalon_index = [0]  # Ожидается что будет один индекс документа
    etalon_words = [{'test', 'text', 'testing', 'my', 'work', 'now', 'train', 'this', 'working', 'bool'}]
    assert etalon_index == test_index
    assert etalon_words == test_words


def test_work_function_load_documents_with_lot_doc_5(tmpdir):
    """
        Как отрабатывает функция при работе с двумя нормальным документом в файле,  для записи тестируемого документа
        :param tmpdir: создаю файл во временной директории, для записи тестируемого документа
    """
    test_doc = tmpdir.join('datatest.txt')
    test_doc.write('0\tTest text! test number one...\n1\tTest text... number two!')
    test_index, test_words = inverted_index.load_documents(test_doc)
    etalon_index = [0, 1]
    etalon_words = [{'test', 'text', 'number', 'one'}, {'test', 'number', 'two', 'text'}]
    assert test_words == etalon_words
    assert test_index == etalon_index


def test_work_function_load_documents_with_an_extra_newline_character_6(tmpdir):
    """
        Как отработает функция если в файле будет один документ, который содержит в конце символ "\n"
        :param tmpdir: создаю файл во временной директории, для записи тестируемого документа
    """
    test_doc = tmpdir.join('datatest.txt')  # создаю временный тестовый документ
    test_doc.write('0\tTest text! test number one...\n1\tTest text... number two!\n')
    test_index, test_words = inverted_index.load_documents(test_doc)
    etalon_index = [0, 1]
    etalon_words = [{'test', 'text', 'number', 'one'}, {'test', 'number', 'two', 'text'}]
    assert test_index == etalon_index
    assert test_words == etalon_words


def test_work_function_load_documents_with_lot_doc_7(tmpdir):
    """
        Проверка работы функции load_documents при большом числе документов записанных в файл
        :param tmpdir: создаю файл во временной директории, для записи тестируемого документа
    """
    test_doc = tmpdir.join('datatest.txt')  # создаю временный тестовый документ
    test_doc.write('0\tTest text! test number one...\n1\tTest text... number two!\n'
                   '2\tKent!!!! red gay\n3\tBoys len lan\n12\tTrest!!! best wreit!')
    test_index, test_words = inverted_index.load_documents(test_doc)
    etalon_index = [0, 1, 2, 3, 12]
    etalon_words = [{'test', 'text', 'number', 'one'}, {'test', 'number', 'two', 'text'},
                    {'kent', 'red', 'gay'}, {'boys', 'len', 'lan'}, {'trest', 'best', 'wreit'}]
    assert test_index == etalon_index
    assert test_words == etalon_words


def test_load_stop_words_8(tmpdir):
    """
        Проврека работы load_stop_words
        :param tmpdir: создаю файл во временной директории, для записи тестируемого документа
    """
    test_doc = tmpdir.join('datatest.txt')
    test_doc.write('Test\ntext\ntest\nnumber\none\nTe\ntext\nnumber2\ntwo')
    test_words = inverted_index.load_stop_words(test_doc)
    etalon_words = {'test', 'text', 'number', 'one', 'te', 'number2', 'two'}
    assert etalon_words == test_words


def test_load_stop_words_with_an_extra_newline_character_9(tmpdir):
    """
        Проврека работы load_stop_words при наличии "\n" в конце файла со stop_words
        :param tmpdir: создаю файл во временной директории, для записи тестируемого документа
    """
    test_doc = tmpdir.join('datatest.txt')  # создаю временный тестовый документ
    test_doc.write('Test\ntext\ntest\nnumber\none\nTe\ntext\nnumber2\ntwo\n')
    test_words = inverted_index.load_stop_words(test_doc)
    etalon_words = {'test', 'text', 'number', 'one', 'te', 'number2', 'two'}
    assert etalon_words == test_words


def test_build_inverted_index_10():
    """
        Проверка сущестования build_inverted_index
    """
    assert inverted_index.build_inverted_index


def test_build_inverted_index11():
    """
        Проферка работы функции build_inverted_index на коректных данных
    """
    test_index = [0, 1, 3]
    test_words = [{'test', 'null', 'hi'}, {'test', 'one', 'lol'}, {'test', 'two', 'cant'}]
    test_stop_words = {'hi', 'cant', 'lol'}
    test_result = inverted_index.build_inverted_index(indexs=test_index, stop_words=test_stop_words,
                                                      words=test_words)
    assert test_result.word_to_docs_mapping == {'test': {0, 1, 3},
                                                'null': {0},
                                                'one': {1},
                                                'two': {3}}


"""
    Добавть вариант теста, где отрабатывается некоректный случай работы!!!!
"""


def test_build_inverted_index_not_core_data_12():
    """
        Как отработает build_inverted_index на данные с отстуствием индекса
    :return:
    """
    test_indexs = [None]
    test_words = [{'name', 'begin', 'where', 'test', 'work', 'he', 'i'}]
    test_stop_words = {'he', 'i'}

    test_inverted_index = inverted_index.build_inverted_index(indexs=test_indexs,
                                                              words=test_words,
                                                              stop_words=test_stop_words)

    etalon = {
        'name': {None},
        'begin': {None},
        'where': {None},
        'test': {None},
        'work': {None}
    }
    assert test_inverted_index.word_to_docs_mapping == etalon


@pytest.fixture
def build_inverted_index_for_creat_data_not_corect(tmpdir):
    test_doc = tmpdir.join('wiki_doc')
    test_doc.write('\tName Shasha train this program and work with data like!\n'
                   '4\tTest name number two and test, i like programming!')

    test_doc_stop_words = tmpdir.join('stop_words.txt')
    test_doc_stop_words.write('and\ni\n')

    result_load_doc = inverted_index.load_documents(filepath=test_doc)
    result_load_stop_words = inverted_index.load_stop_words(filepath=test_doc_stop_words)

    result_inverted_index_build_inverted_index = inverted_index.build_inverted_index(stop_words=result_load_stop_words,
                                                                                     words=result_load_doc[1],
                                                                                     indexs=result_load_doc[0])
    return result_inverted_index_build_inverted_index


def test_build_inverted_index_not_core_data_13(build_inverted_index_for_creat_data_not_corect):
    etalon = {
        'name': {None, 4},
        'shasha': {None},
        'train': {None},
        'this': {None},
        'program': {None},
        'work': {None},
        'with': {None},
        'data': {None},
        'test': {4},
        'number': {4},
        'two': {4},
        'like': {None, 4},
        'programming': {4}
    }
    assert etalon == build_inverted_index_for_creat_data_not_corect.word_to_docs_mapping


def test_dump_load_inverted_index_not_corect_data_14(build_inverted_index_for_creat_data_not_corect, tmp_path):
    temp_path = tmp_path / 'tmp'
    build_inverted_index_for_creat_data_not_corect.dump(filepath=temp_path)
    test_load_inverted_index = inverted_index.InvertedIndex.load(filepath=temp_path)
    etalon = {
        'name': {None, 4},
        'shasha': {None},
        'train': {None},
        'this': {None},
        'program': {None},
        'work': {None},
        'with': {None},
        'data': {None},
        'test': {4},
        'number': {4},
        'two': {4},
        'like': {None, 4},
        'programming': {4}
    }
    assert etalon == test_load_inverted_index.word_to_docs_mapping


def test_class_invertedindex_and_build_inverted_index_15(tmp_path):
    """
        Как работает build_inverted_index, запись в файл InvertedIndex.dump и считывание InvertedIndex.load
        :param tmp_path: создаю файл во временной директории, для записи тестируемого документа
    """
    f1 = tmp_path / 'temp'  # временная директория
    test_index = [0, 1, 3]  # полученые номера документов
    test_words = [{'test', 'null', 'hi'}, {'test', 'one', 'lol'}, {'test', 'two', 'cant'}]  # слова документов
    test_stop_words = {'hi', 'cant', 'lol'}
    # строю инвертированный индекс
    test_result = inverted_index.build_inverted_index(indexs=test_index, stop_words=test_stop_words,
                                                      words=test_words)
    test_result.dump(filepath=f1)  # записываю инвертированный индекс в временную директорию
    test_inverted_index_load = inverted_index.InvertedIndex.load(filepath=f1)  # считываю инверт индекс
    result = test_inverted_index_load.word_to_docs_mapping
    assert result == {
        'test': {0, 1, 3},
        'null': {0},
        'one': {1},
        'two': {3}
    }


def test_class_invertedindex_build_inverted_index_and_dump_load_16(tmp_path):
    """
        Проверка работы записи и перезаписи файла с инвертированным индексом
        :param tmp_path: создаю файл во временной директории, для записи тестируемого документа
    """
    f1 = tmp_path / 'temp'

    test_index = [0, 1, 3]
    test_words = [{'test', 'null', 'hi'}, {'test', 'one', 'lol'}, {'test', 'two', 'cant'}]
    test_stop_words = {'hi', 'cant', 'lol'}
    test_result = inverted_index.build_inverted_index(indexs=test_index, stop_words=test_stop_words,
                                                      words=test_words)
    test_result.dump(filepath=f1)  # запись первого набора данных

    test_index2 = [15, 25]
    test_words2 = [{'one'}, {'two'}]
    test_result2 = inverted_index.build_inverted_index(indexs=test_index2, stop_words=test_stop_words,
                                                       words=test_words2)

    test_result2.dump(filepath=f1)  # запись второго набора данных

    test_inverted_index_load = inverted_index.InvertedIndex.load(filepath=f1)

    assert test_inverted_index_load.word_to_docs_mapping == {
        'test': {0, 1, 3},
        'null': {0},
        'one': {1, 15},
        'two': {3, 25}
    }


def test_class_invertedindex_load_out_indices_17(tmp_path):
    """
        Считывание инверт индекса из файла
        :param tmp_path: феременная директория для файла test_index_inverted.index
    """
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

    inverted_index_load = inverted_index.InvertedIndex.load(test_path)

    etalon = {
        'test': {0, 1, 3},
        'null': {0},
        'one': {1, 15},
        'two': {3, 25}
    }
    assert etalon == inverted_index_load.word_to_docs_mapping


def test_class_invertedindex_query_18():
    """
        Как производится посик слова InvertedIndex.query и вывод результата
    """
    test_index = [0, 1, 3]
    test_words = [{'test', 'null', 'hi'}, {'test', 'one', 'lol'}, {'test', 'two', 'cant'}]
    test_stop_words = {'hi', 'cant', 'lol'}
    test_result = inverted_index.build_inverted_index(indexs=test_index, stop_words=test_stop_words,
                                                      words=test_words)
    test_query = test_result.query('two', 'test')
    etalon = {
        'two': {3},
        'test': {0, 1, 3}
    }
    assert test_query == etalon


def test_class_invertedindex_query_with_two_words_19():
    """
        Поиск двух одинаовых слов в методе InvertedIndex.query
    """
    test_index = [0, 1, 3]
    test_words = [{'test', 'null', 'hi'}, {'test', 'one', 'lol'}, {'test', 'two', 'cant'}]
    test_stop_words = {'hi', 'cant', 'lol'}
    test_result = inverted_index.build_inverted_index(indexs=test_index, stop_words=test_stop_words,
                                                      words=test_words)
    test_query = test_result.query('two', 'two')
    etalon = {
        'two': {3}
    }
    assert test_query == etalon


# @pytest.mark.skip(reason='not implemented test 20')
def test_class_inverted_index_query_if_not_word_20(tmp_path):
    """
        Тест направлен на проверку отработки случая отсутствия слова в наборе всех слов
        :param tmp_path: временная директория
    """
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
    test_query = test_load_inverted_index.query('begin')
    etalon = {'begin': {}}
    assert test_query == etalon


def test_class_invertedindex_query_work_with_loaded_index_21(tmp_path):
    """
        Поиск слова и индексов этого слова из загруженого инверт индекса
        :param tmp_path: временная директория
        :return:
    """
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
    test_query = test_load_inverted_index.query('two')
    etalon = {
        'two': {3, 25}
    }
    assert test_query == etalon


def test_all_22(tmp_path, tmpdir):
    """
        Общий тест функционала: обратока документов, создание инверт индеса, запись его и считывание. Поиск слова
        :param tmp_path: временная диретория
        :param tmpdir: добавление временого файла
    """
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
    document_ids = test_inverted_index_load.query("two")
    etalon = {
        'two': {1, 3}
    }
    assert etalon == document_ids


# приминение pytest.fixture
@pytest.fixture
def fixture_inverted_index(tmp_path):
    test_index = [0, 1, 3]
    test_words = [{'test', 'null', 'hi'}, {'test', 'one', 'lol'}, {'test', 'two', 'cant'}]
    test_stop_words = {'hi', 'cant', 'lol'}
    test_result = inverted_index.build_inverted_index(indexs=test_index, stop_words=test_stop_words, words=test_words)
    return test_result


def test_class_invertedindex_query_with_fixture_23(fixture_inverted_index):
    test_query = fixture_inverted_index.query('two', 'test')
    etalon = {
        'two': {3},
        'test': {0, 1, 3}}
    assert test_query == etalon


def test_class_invertedindex_query_with_two_words_with_fixture_24(fixture_inverted_index):
    test_query = fixture_inverted_index.query('two', 'two')
    etalon = {
        'two': {3}
    }
    assert test_query == etalon


# Что делать с документом у которого нет индекса ?
def test_doc_do_not_contaon_index_25(tmpdir):
    """
        Тест для отработки ситуации если документ не содержит индеса
        :param tmpdir: временная директория для тестового файла
    """
    test_doc = tmpdir.join('test_wiki_doc.txt')
    test_doc.write('\tName Doc this test doc. I will use this text for the test.')
    test_indexs, test_words = inverted_index.load_documents(test_doc)
    etalon_index = [None]  # вместо индеса должна прийти пустая список
    # создается множество слов
    etalon_words = [{'name', 'doc', 'this', 'test', 'i', 'will', 'use', 'text', 'for', 'the'}]
    assert test_indexs == etalon_index
    assert etalon_words == test_words


# Добавить тесты, которые обрабатываеют результаты некоректных данных, которые передаюется далее по программе:
# что будет делать build_inverted_index, если не будет номера документа и тд...


@pytest.fixture
def creat_not_corect_data(tmpdir):
    not_corect_data = '4\tI sit by the window and make a program test\n' \
                      '\tSasha ate porridge, a little, but it was delicious test\n' \
                      '5\tThe third test is about something\n' \
                      '\tI am watching south park now, test'
    test_doc = tmpdir.join('wiki_file')
    test_doc.write(not_corect_data)
    stop_words = 'the\ni\na\nate\nby\nand\nbut\nit\nis\nam\n'

    test_stop_words = tmpdir.join('stop_words')
    test_stop_words.write(stop_words)

    result_stop_words = inverted_index.load_stop_words(test_stop_words)
    result_index, result_words = inverted_index.load_documents(test_doc)
    return result_index, result_words, result_stop_words


def test_not_number_doc_where_lot_documents_26(creat_not_corect_data):
    indexs, words, stop_words = creat_not_corect_data

    test_inverted_index = inverted_index.build_inverted_index(indexs=indexs,
                                                              words=words,
                                                              stop_words=stop_words).word_to_docs_mapping

    etelon = {
        'sit': {4},
        'window': {4},
        'make': {4},
        'program': {4},
        'sasha': {None},
        'porridge': {None},
        'little': {None},
        'was': {None},
        'delicious': {None},
        'third': {5},
        'test': {None, 5, 4},
        'about': {5},
        'something': {5},
        'watching': {None},
        'south': {None},
        'park': {None},
        'now': {None}
    }
    assert etelon == test_inverted_index


def test_not_number_doc_where_lot_documents_with_two_doc_have_not_number_27(creat_not_corect_data, tmp_path):
    tile_path = tmp_path / 'tmp'

    indexs, words, stop_words = creat_not_corect_data

    test_inverted_index = inverted_index.build_inverted_index(indexs=indexs,
                                                              words=words,
                                                              stop_words=stop_words)

    test_inverted_index.dump(filepath=tile_path)
    load_test_inverted_index = inverted_index.InvertedIndex.load(tile_path)
    etelon = {
        'sit': {4},
        'window': {4},
        'make': {4},
        'program': {4},
        'sasha': {None},
        'porridge': {None},
        'little': {None},
        'was': {None},
        'delicious': {None},
        'third': {5},
        'test': {None, 5, 4},
        'about': {5},
        'something': {5},
        'watching': {None},
        'south': {None},
        'park': {None},
        'now': {None}
    }
    assert etelon == load_test_inverted_index.word_to_docs_mapping


def test_query_not_number_doc_where_lot_documents_with_two_doc_have_not_number_28(creat_not_corect_data, tmp_path):
    tile_path = tmp_path / 'tmp'

    indexs, words, stop_words = creat_not_corect_data

    test_inverted_index = inverted_index.build_inverted_index(indexs=indexs,
                                                              words=words,
                                                              stop_words=stop_words)

    test_inverted_index.dump(filepath=tile_path)
    load_test_inverted_index = inverted_index.InvertedIndex.load(tile_path)
    result_query = load_test_inverted_index.query('south')
    assert result_query == {'south': {None}}


@pytest.fixture
def creat_doc_have_not_words(tmpdir):
    not_corect_data = '4\tI sit by the window and make a program test\n' \
                      '8\t\n' \
                      '5\tThe third test is about something\n' \
                      '6\tI am watching south park now, test'

    test_file = tmpdir.join('wiki_file')
    test_file.write(not_corect_data)

    return inverted_index.load_documents(test_file)


# @pytest.mark.skip(reason='not implemented test 20')
def test_number_and_no_words_in_document_27(creat_doc_have_not_words):
    indexs, words = creat_doc_have_not_words
    etalon_indexs = [4, 8, 5, 6]
    etalon_words = [{'i', 'sit', 'by', 'the', 'window', 'and', 'make', 'a', 'program', 'test'},
                    None,
                    {'the', 'third', 'test', 'is', 'about', 'something'},
                    {'i', 'am', 'watching', 'south', 'park', 'now', 'test'}]
    assert etalon_words == words
    assert etalon_indexs == indexs


# @pytest.mark.skip(reason='not implemented test 28')
def test_number_and_no_words_in_document_28(creat_doc_have_not_words):
    indexs, words = creat_doc_have_not_words
    stop_words = {'i', 'a', 'am', 'is', 'by', 'and', 'the'}
    test_inverted_index = inverted_index.build_inverted_index(indexs=indexs, words=words, stop_words=stop_words)
    etalon = {
        'sit': {4},
        'window': {4},
        'make': {4},
        'program': {4},
        'test': {4, 5, 6},
        'third': {5},
        'about': {5},
        'something': {5},
        'watching': {6},
        'south': {6},
        'park': {6},
        'now': {6}
    }
    assert etalon == test_inverted_index.word_to_docs_mapping


@pytest.fixture
def create_not_corect_data_with_two_doc_have_one_ndex(tmpdir):
    not_corect_data = '4\tI sit by the window and make a program test\n' \
                      '8\t\n' \
                      '5\tThe third test is about something\n' \
                      '6\tI am watching south park now, test\n' \
                      '8\tTest number tree'

    test_file = tmpdir.join('wiki_file')
    test_file.write(not_corect_data)
    return test_file


def test_number_and_no_words_in_document_29(create_not_corect_data_with_two_doc_have_one_ndex):
    test_file = create_not_corect_data_with_two_doc_have_one_ndex
    indexs, words = inverted_index.load_documents(test_file)
    etalon_indexs = [4, 8, 5, 6, 8]
    etalon_words = [{'i', 'sit', 'by', 'the', 'window', 'and', 'make', 'a', 'program', 'test'},
                    None,
                    {'the', 'third', 'test', 'is', 'about', 'something'},
                    {'i', 'am', 'watching', 'south', 'park', 'now', 'test'},
                    {'test', 'number', 'tree'}]
    assert etalon_words == words
    assert etalon_indexs == indexs


def test_build_inverted_one_doc_have_doc_with_dont_new_index_30(create_not_corect_data_with_two_doc_have_one_ndex):
    test_file = create_not_corect_data_with_two_doc_have_one_ndex
    indexs, words = inverted_index.load_documents(test_file)
    stop_words = {'i', 'a', 'am', 'is', 'by', 'and', 'the'}

    test_inverted_idex = inverted_index.build_inverted_index(stop_words=stop_words, indexs=indexs, words=words)
    etalan = {
        'test': {4, 5, 8, 6},
        'sit': {4},
        'window': {4},
        'make': {4},
        'program': {4},
        'third': {5},
        'about': {5},
        'something': {5},
        'number': {8},
        'tree': {8},
        'now': {6},
        'south': {6},
        'watching': {6},
        'park': {6}
    }
    assert etalan == test_inverted_idex.word_to_docs_mapping


"""
Testing with parametrize
"""


@pytest.mark.parametrize('task,result',
                         [(([0, 1],
                            [{'words', 'name'}, {'words', 'name', 'testing'}]),
                           {
                               'words': {0, 1},
                               'name': {0, 1},
                               'testing': {1}
                           }),
                          (([0, 1],
                            [{'words', 'test'}, {}]),
                           {
                               'words': {0},
                               'test': {0}
                           })])
def test_inverted_index_build_inverted_index_31(task, result):
    assert inverted_index.build_inverted_index(indexs=task[0],
                                               words=task[1],
                                               stop_words={}).word_to_docs_mapping == result


def creat_test_file_for_load_with_him():
    index = [0, 1]
    words = [{'words', 'name', 'test'}, {'words', 'green', 'man'}]
    test_inverted_index = inverted_index.build_inverted_index(indexs=index,
                                                              words=words,
                                                              stop_words={})
    return test_inverted_index


@pytest.mark.parametrize('task2', [creat_test_file_for_load_with_him])
def test_InverteIndex_load_32(task2):
    assert task2().query('two') == {'two': {}}


"""
Using Test Class
"""


@pytest.fixture
def creat_data_file_wiki_sample(tmpdir):
    """
        Create a text file for running tests
    :param tmpdir: Temporary file
    :return: Temporary file with test wiki sample
    """
    test_wiki_text = "0\tDon't believe in tears\n" \
                     "1\tThe wind is making noise in my head\n" \
                     "2\tWalking with spring"
    tmpfile = tmpdir.join('wiki_test_smple')
    tmpfile.write(test_wiki_text)
    return tmpfile


@pytest.fixture
def creat_index_and_words_with_temp_file(creat_data_file_wiki_sample):
    return inverted_index.load_documents(creat_data_file_wiki_sample)


@pytest.fixture
def creat_temp_file_with_stop_words(tmpdir):
    test_stop_words_text = 'it\ni\nis\nmy\nin\nthe'

    tmpfile = tmpdir.join('stop_words')
    tmpfile.write(test_stop_words_text)
    return tmpfile


@pytest.fixture
def creat_stop_words_wher_load_stop_words_with_fiel(creat_temp_file_with_stop_words):
    return inverted_index.load_stop_words(filepath=creat_temp_file_with_stop_words)


@pytest.fixture
def creat_inverted_index(creat_index_and_words_with_temp_file,
                         creat_stop_words_wher_load_stop_words_with_fiel):
    indexs, words = creat_index_and_words_with_temp_file
    stop_words = creat_stop_words_wher_load_stop_words_with_fiel
    return inverted_index.build_inverted_index(indexs=indexs,
                                               words=words,
                                               stop_words=stop_words)
@pytest.fixture
def creat_file_inverted_index(creat_inverted_index, tmp_path):
    tpath = tmp_path / 'tmp'
    tinverted_index = creat_inverted_index
    tinverted_index.dump(filepath=tpath)
    return tpath

class TestLoadDocuments:
    """
    function testing load_documents
    """

    def test_can_use_fuction_load_documents(self):
        assert inverted_index.load_documents

    def test_can_open_file_in_load_documents(self, creat_data_file_wiki_sample):
        index, words = inverted_index.load_documents(filepath=creat_data_file_wiki_sample)
        assert index == [0, 1, 2]
        assert words == [{'believe', 'in', 'tears'}, {'the', 'wind', 'is', 'making',
                                                      'noise', 'in', 'my', 'head'},
                         {'walking', 'with', 'spring'}]


class TestLoadStopWords:
    """
    function testing load_stop_words
    """

    def test_can_use_fuction_load_stop_words(self):
        assert inverted_index.load_stop_words

    def test_load_stop_words_with_temp_file(self, creat_temp_file_with_stop_words):
        stop_words = inverted_index.load_stop_words(filepath=creat_temp_file_with_stop_words)
        assert stop_words == {'it', 'i', 'is', 'my', 'in', 'the'}


class TestBuildInvertedIndex:
    """
    function testing build_inverted_index
    """

    def test_can_use_fuction_build_inverted_index(self):
        assert inverted_index.build_inverted_index

    def test_can_build_inverted_index(self, creat_index_and_words_with_temp_file,
                                      creat_stop_words_wher_load_stop_words_with_fiel):
        index, words = creat_index_and_words_with_temp_file
        tinverted_index = inverted_index.build_inverted_index(
            indexs=index,
            words=words,
            stop_words=creat_stop_words_wher_load_stop_words_with_fiel)
        assert tinverted_index.word_to_docs_mapping == {
            'believe': {0}, 'tears': {0}, 'wind': {1},
            'making': {1}, 'noise': {1}, 'head': {1}, 'walking': {2}, 'with': {2}, 'spring': {2}
        }


class TestClassInverteIndex:
    """
    Test class inverted index
    """

    def test_can_use_class_inverted_index(self):
        assert inverted_index.InvertedIndex

    def test_get_word_to_docs_mapping(self, creat_inverted_index):
        assert creat_inverted_index.word_to_docs_mapping == {
            'believe': {0}, 'tears': {0}, 'wind': {1},
            'making': {1}, 'noise': {1}, 'head': {1},
            'walking': {2}, 'with': {2}, 'spring': {2}
        }

    def test_can_use_dump_inverted_index(self, creat_inverted_index, tmp_path):
        tpath = tmp_path / 'tmp'
        tinverted_index = creat_inverted_index
        tinverted_index.dump(filepath=tpath)
        assert tpath.open(mode='r')

    def test_can_load_file_inverted_index(self, creat_inverted_index, creat_file_inverted_index):
        assert inverted_index.InvertedIndex.load(creat_file_inverted_index).word_to_docs_mapping == \
               creat_inverted_index.word_to_docs_mapping

    def test_can_use_query_inverted_index(self, creat_file_inverted_index):
        tinverted_index = inverted_index.InvertedIndex.load(creat_file_inverted_index)
        assert tinverted_index.query('wind') == {
            'wind': {1}
        }

    def test_can_use_query_with_two_words(self, creat_file_inverted_index):
        tinverted_index = inverted_index.InvertedIndex.load(creat_file_inverted_index)
        assert tinverted_index.query('two', 'wind') == {
            'two': {},
            'wind': {1}
        }