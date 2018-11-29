import pytest
import python_cpp_skel as m
import datetime

def test_verison():
    assert m.__version__ == '0.0.1'

def test_add():
    assert m.add(1, 2) == 3

def test_subtract():
    assert m.subtract(1, 2) == -1

def test_date():
    assert m.date() == datetime.datetime.today().strftime('%Y-%m-%d')
