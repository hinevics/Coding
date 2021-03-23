import pytest
import inverted_index


def test_can_import_inverted_index_module1():
    import inverted_index


def test_can_load_load_documents2():
    assert inverted_index.load_documents


def test_len_document3():
    """Unit Testing"""
    # Проверка длины документы
    test_link = inverted_index.work_links['dataset']
    with open(file=test_link, mode='r', encoding='utf-8') as file:
        data = file.readlines()
        assert len(data) == 4100


def test_work_function_load_documents_with_one_doc4(tmpdir):
    test_doc = tmpdir.join('datatest.txt')  # создаю временный тестовый документ
    # временные тестовые данные
    test_doc.write('0\tTest text testing, my work now! Train testing this, working, bool?')
    test_index, test_words = inverted_index.load_documents(test_doc)
    etalon_index = [0]
    etalon_words = [{'test', 'text', 'testing', 'my', 'work', 'now', 'train', 'this', 'working', 'bool'}]
    assert etalon_index == test_index
    assert etalon_words == test_words


def test_work_function_load_documents_with_lot_doc5(tmpdir):
    test_doc = tmpdir.join('datatest.txt')  # создаю временный тестовый документ
    test_doc.write('0\tTest text! test number one...\n1\tTest text... number two!')
    test_index, test_words = inverted_index.load_documents(test_doc)
    etalon_index = {0, 1}
    etalon_words = {0: {'test', 'text', 'number', 'one'},
                    1: {'test', 'number', 'two', 'text'}}
    assert etalon_index == set(test_index)
    for text, index in zip(test_words, test_index):
        assert text == etalon_words[index]


def test_work_function_load_documents_with_an_extra_newline_character6(tmpdir):
    test_doc = tmpdir.join('datatest.txt')  # создаю временный тестовый документ
    test_doc.write('0\tTest text! test number one...\n1\tTest text... number two!\n')
    test_index, test_words = inverted_index.load_documents(test_doc)
    etalon_index = {0, 1}
    etalon_words = {0: {'test', 'text', 'number', 'one'},
                    1: {'test', 'number', 'two', 'text'}}
    assert etalon_index == set(test_index)
    for text, index in zip(test_words, test_index):
        assert text == etalon_words[index]


def test_work_function_load_documents_with_lot_doc7(tmpdir):
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


def test_load_stop_words8(tmpdir):
    test_doc = tmpdir.join('datatest.txt')
    test_doc.write('Test\ntext\ntest\nnumber\none\nTe\ntext\nnumber2\ntwo')
    test_words = inverted_index.load_stop_words(test_doc)
    etalon_words = {'test', 'text', 'number', 'one', 'te', 'number2', 'two'}
    assert etalon_words == test_words


def test_load_stop_words_with_an_extra_newline_character9(tmpdir):
    test_doc = tmpdir.join('datatest.txt')  # создаю временный тестовый документ
    test_doc.write('Test\ntext\ntest\nnumber\none\nTe\ntext\nnumber2\ntwo\n')
    test_words = inverted_index.load_stop_words(test_doc)
    etalon_words = {'test', 'text', 'number', 'one', 'te', 'number2', 'two'}
    assert etalon_words == test_words


def test_build_inverted_index10():
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


def test_build_inverted_index12():
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


def test_build_inverted_index13(tmp_path):
    f1 = tmp_path / 'temp'
    test_index = [0, 1, 3]
    test_words = [{'test', 'null', 'hi'}, {'test', 'one', 'lol'}, {'test', 'two', 'cant'}]
    test_stop_words = {'hi', 'cant', 'lol'}
    test_result = inverted_index.build_inverted_index(indexs=test_index, stop_words=test_stop_words,
                                                      words=test_words)
    test_result.dump(filepath=f1)
    result = inverted_index.InvertedIndex.load(filepath=f1)
    assert result == {
        'test': {0, 1, 3},
        'null': {0},
        'one': {1},
        'two': {3}
    }


def test_build_inverted_index14(tmp_path):
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

    result = inverted_index.InvertedIndex.load(filepath=f1)
    assert result == {
        'test': {0, 1, 3},
        'null': {0},
        'one': {1, 15},
        'two': {3, 25}
    }
