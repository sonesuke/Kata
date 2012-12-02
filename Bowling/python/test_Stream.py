from Archive import TextArchive
import pytest
import io


def test_create():
    stream = io.StringIO()
    a = TextArchive(stream)


def test_write_header():
    stream = io.StringIO()
    a = TextArchive(stream)
    a.write_header("hoge")
    stream.seek(0)
    assert stream.readline() == "hoge\n"


def test_write_footer():
    stream = io.StringIO()
    a = TextArchive(stream)
    a.write_footer("hoge")
    stream.seek(0)
    assert stream.readline() == "/hoge\n"


def test_write_count():
    stream = io.StringIO()
    a = TextArchive(stream)
    a.write_count(3)
    stream.seek(0)
    assert stream.readline() == "3\n"


def test_write_body():
    stream = io.StringIO()
    a = TextArchive(stream)
    a.write_body(3)
    stream.seek(0)
    assert stream.readline() == "3\n"


def test_load_header():
    stream = io.StringIO()
    a = TextArchive(stream)
    a.write_header("hoge")
    stream.seek(0)
    assert a.load_header() == "hoge"


def test_load_footer():
    stream = io.StringIO()
    a = TextArchive(stream)
    a.write_footer("hoge")
    stream.seek(0)
    assert a.load_footer() == "hoge"


def test_load_count():
    stream = io.StringIO()
    a = TextArchive(stream)
    a.write_count(3)
    stream.seek(0)
    assert a.load_count() == 3


def test_load_count():
    stream = io.StringIO()
    a = TextArchive(stream)
    a.write_body(3)
    stream.seek(0)
    assert a.load_body() == 3
