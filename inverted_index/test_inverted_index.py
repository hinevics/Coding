import pytest
import inverted_index


def test_can_import_inverted_index_module():
    import inverted_index


def test_can_load_stop_words():
    assert inverted_index.load_documents


def test_can_read_documents():
    test_link = inverted_index.work_links['dataset']
    assert inverted_index.load_documents(filepath=test_link)


def test_len_document():
    """Unit Testing"""
    # Проверка длины документы
    test_link = inverted_index.work_links['dataset']
    with open(file=test_link, mode='r', encoding='utf-8') as file:
        data = file.readlines()
        assert len(data) == 4100


def test_import_fuction_load_documents():
    test_link = inverted_index.work_links['dataset']
    assert inverted_index.load_documents(filepath=test_link)


def test_work_function_load_documents_with_one_doc(tmpdir):
    test_doc = tmpdir.join('datatest.txt')  # создаю временный тестовый документ
    test_doc.write('0\tTest text testing my work now!') # временные тестовые данные
    test_index, test_words = inverted_index.load_documents(test_doc)
    etalon_index = [0]
    etalon_words = [{'test', 'text', 'testing', 'my', 'work'}]
    assert etalon_index == test_index
    assert etalon_words[0] == etalon_words[0]


def test_work_function_load_documents_with_lot_doc(tmpdir):
    test_doc = tmpdir.join('datatest.txt')  # создаю временный тестовый документ
    test_doc.write('0\tTest text test number one\n'
                   '1\tTest text number two') # временные тестовые данные
    test_index, test_words = inverted_index.load_documents(test_doc)
    etalon_index = [0, 1]
    etalon_words = [{'test', 'text', 'number', 'one'},
                    {'test', 'text', 'number', 'two'}]
    assert etalon_index == test_index
    for etalon, test in zip(etalon_words, test_words):
        assert etalon == test
