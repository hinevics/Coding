import json
import pytest
import inverted_index

"""Unit Testing"""


def test_can_import_inverted_index_module_1():
    """
        Ипорт модуля inverted_index
    """
    import inverted_index


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


def test_class_invertedindex_and_build_inverted_index_12(tmp_path):
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


def test_class_invertedindex_build_inverted_index_and_dump_load_15(tmp_path):
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


def test_class_invertedindex_load_out_indices_16(tmp_path):
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


def test_class_invertedindex_query_17():
    """
        Как производится посик слова InvertedIndex.query и вывод результата
    """
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


def test_class_invertedindex_query_with_two_words_18():
    """
        Поиск двух одинаовых слов в методе InvertedIndex.query
    """
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


# @pytest.mark.skip(reason='not implemented test 19')
def test_class_inverted_index_query_if_not_word_19(tmp_path):
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
    test_query = test_load_inverted_index.query(['begin'])
    etalon = {'begin': {}}
    assert test_query == etalon


def test_class_invertedindex_query_work_with_loaded_index_20(tmp_path):
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
    test_query = test_load_inverted_index.query(['two'])
    etalon = {
        'two': {3, 25}
    }
    assert test_query == etalon


def test_all_21(tmp_path, tmpdir):
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
    document_ids = test_inverted_index_load.query(["two"])
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


def test_class_invertedindex_query_17_with_fixture_22(fixture_inverted_index):
    test_query = fixture_inverted_index.query(['two', 'test'])
    etalon = {
        'two': {3},
        'test': {0, 1, 3}}
    assert test_query == etalon


def test_class_invertedindex_query_with_two_words_18_with_fixture_23(fixture_inverted_index):
    test_query = fixture_inverted_index.query(['two', 'two'])
    etalon = {
            'two': {3}
        }
    assert test_query == etalon


# Что делать с документом у которого нет индекса ?
def test_doc_do_not_contaon_index(tmpdir):
    """
        Тест для отработки ситуации если документ не содержит индеса
        :param tmpdir: временная директория для тестового файла
    """
    test_doc = tmpdir.join('test_wiki_doc.txt')
    test_doc.write('\tName Doc this test doc. I will use this text for the test.')
    test_indexs, test_words = inverted_index.load_documents(test_doc)
    etalon_index = [[]]  # вместо индеса должна прийти пустая список
    # создается множество слов
    etalon_words = [{'name', 'doc', 'this', 'test', 'i', 'will', 'use', 'text', 'for', 'the'}]
    assert test_indexs == etalon_index
    assert etalon_words == test_words


# Добавить тесты, которые обрабатываеют результаты некоректных данных, которые передаюется далее по программе:
# что будет делать build_inverted_index, если не будет номера документа и тд...