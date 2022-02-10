from hailtop.utils import (partition, url_basename, url_join, url_scheme,
                           url_and_params, parse_docker_image_reference, grouped)
                        


def test_partition_zero_empty():
    assert list(partition(0, [])) == []


def test_partition_even_small():
    assert list(partition(3, range(3))) == [range(0, 1), range(1, 2), range(2, 3)]


def test_partition_even_big():
    assert list(partition(3, range(9))) == [range(0, 3), range(3, 6), range(6, 9)]


def test_partition_uneven_big():
    assert list(partition(2, range(9))) == [range(0, 5), range(5, 9)]


def test_partition_toofew():
    assert list(partition(6, range(3))) == [range(0, 1), range(1, 2), range(2, 3),
                                            range(3, 3), range(3, 3), range(3, 3)]


def test_url_basename():
    assert url_basename('/path/to/file') == 'file'
    assert url_basename('https://hail.is/path/to/file') == 'file'


def test_url_join():
    assert url_join('/path/to', 'file') == '/path/to/file'
    assert url_join('/path/to/', 'file') == '/path/to/file'
    assert url_join('/path/to/', '/absolute/file') == '/absolute/file'
    assert url_join('https://hail.is/path/to', 'file') == 'https://hail.is/path/to/file'
    assert url_join('https://hail.is/path/to/', 'file') == 'https://hail.is/path/to/file'
    assert url_join('https://hail.is/path/to/', '/absolute/file') == 'https://hail.is/absolute/file'


def test_url_scheme():
    assert url_scheme('https://hail.is/path/to') == 'https'
    assert url_scheme('/path/to') == ''

def test_url_and_params():
    assert url_and_params('https://example.com/') == ('https://example.com/', {})
    assert url_and_params('https://example.com/foo?') == ('https://example.com/foo', {})
    assert url_and_params('https://example.com/foo?a=b&c=d') == ('https://example.com/foo', {'a': 'b', 'c': 'd'})

def test_parse_docker_image_reference():
    x = parse_docker_image_reference('animage')
    assert x.domain is None
    assert x.path == 'animage'
    assert x.tag is None
    assert x.digest is None
    assert x.name() == 'animage'
    assert str(x) == 'animage'

    x = parse_docker_image_reference('hailgenetics/animage')
    assert x.domain == 'hailgenetics'
    assert x.path == 'animage'
    assert x.tag is None
    assert x.digest is None
    assert x.name() == 'hailgenetics/animage'
    assert str(x) == 'hailgenetics/animage'

    x = parse_docker_image_reference('localhost:5000/animage')
    assert x.domain == 'localhost:5000'
    assert x.path == 'animage'
    assert x.tag is None
    assert x.digest is None
    assert x.name() == 'localhost:5000/animage'
    assert str(x) == 'localhost:5000/animage'

    x = parse_docker_image_reference('localhost:5000/a/b/name')
    assert x.domain == 'localhost:5000'
    assert x.path == 'a/b/name'
    assert x.tag is None
    assert x.digest is None
    assert x.name() == 'localhost:5000/a/b/name'
    assert str(x) == 'localhost:5000/a/b/name'

    x = parse_docker_image_reference('localhost:5000/a/b/name:tag')
    assert x.domain == 'localhost:5000'
    assert x.path == 'a/b/name'
    assert x.tag == 'tag'
    assert x.digest is None
    assert x.name() == 'localhost:5000/a/b/name'
    assert str(x) == 'localhost:5000/a/b/name:tag'

    x = parse_docker_image_reference('localhost:5000/a/b/name:tag@sha256:abc123')
    assert x.domain == 'localhost:5000'
    assert x.path == 'a/b/name'
    assert x.tag == 'tag'
    assert x.digest == 'sha256:abc123'
    assert x.name() == 'localhost:5000/a/b/name'
    assert str(x) == 'localhost:5000/a/b/name:tag@sha256:abc123'

    x = parse_docker_image_reference('localhost:5000/a/b/name@sha256:abc123')
    assert x.domain == 'localhost:5000'
    assert x.path == 'a/b/name'
    assert x.tag is None
    assert x.digest == 'sha256:abc123'
    assert x.name() == 'localhost:5000/a/b/name'
    assert str(x) == 'localhost:5000/a/b/name@sha256:abc123'

    x = parse_docker_image_reference('name@sha256:abc123')
    assert x.domain is None
    assert x.path == 'name'
    assert x.tag is None
    assert x.digest == 'sha256:abc123'
    assert x.name() == 'name'
    assert str(x) == 'name@sha256:abc123'

    x = parse_docker_image_reference('gcr.io/hail-vdc/batch-worker:123fds312')
    assert x.domain == 'gcr.io'
    assert x.path == 'hail-vdc/batch-worker'
    assert x.tag == '123fds312'
    assert x.digest is None
    assert x.name() == 'gcr.io/hail-vdc/batch-worker'
    assert str(x) == 'gcr.io/hail-vdc/batch-worker:123fds312'

    x = parse_docker_image_reference('us-docker.pkg.dev/my-project/my-repo/test-image')
    assert x.domain == 'us-docker.pkg.dev'
    assert x.path == 'my-project/my-repo/test-image'
    assert x.tag is None
    assert x.digest is None
    assert x.name() == 'us-docker.pkg.dev/my-project/my-repo/test-image'
    assert str(x) == 'us-docker.pkg.dev/my-project/my-repo/test-image'




def test_grouped_1():
    try:
        actual = list(grouped(0, [1,2,3,4,5,6,7,8,9]))
        expected = [ 1,2,3,4,5,6,7,8,9]
        assert actual == expected
    except ValueError:
        pass

def test_grouped_2():
    actual = list(grouped(1, [1,2,3,4,5,6,7,8,9]))
    expected = [[1], [2], [3], [4], [5], [6], [7], [8], [9]]
    assert actual == expected

def test_grouped_3():
    actual = list(grouped(5, [1,2,3,4,5,6,7,8,9]))
    expected = [[1, 2, 3, 4, 5], [6, 7, 8, 9]]
    assert actual == expected

def test_grouped_4():
    actual = list(grouped(3,[]))
    expected = []
    assert actual == expected

def test_grouped_5():
    actual = list(grouped(2,[1]))
    expected = [[1]]
    assert actual == expected

def test_grouped_6():
    actual = list(grouped(1,[0]))
    expected = [[0]]
    assert actual == expected

def test_grouped_7():
    actual = list(grouped(1,['abc', 'def', 'ghi', 'jkl', 'mno']))
    expected = [['abc'], ['def'], ['ghi'], ['jkl'], ['mno']]
    assert actual == expected

def test_grouped_8():
    actual = list(grouped(2,['abc', 'def', 'ghi', 'jkl', 'mno']))
    expected = [['abc', 'def'], ['ghi', 'jkl'], ['mno']]
    assert actual == expected

def test_grouped_9():
    actual = list(grouped(3,['abc', 'def', 'ghi', 'jkl', 'mno', '']))
    expected = [['abc', 'def', 'ghi'], ['jkl', 'mno', '']]
    assert actual == expected


def test_grouped_10():
    actual = list(grouped(3,['abc', 'def', 'ghi', 'jkl', 'mno', 'pqr', 'stu']))
    expected = [['abc', 'def', 'ghi'], ['jkl', 'mno', 'pqr'], ['stu']]
    assert actual == expected
