"""
Ensure executor follows the script correctly
"""
from datetime import datetime
from unittest import mock

from ..script import executor
from .script_data import TEST_SCRIPT


@mock.patch('src.script.fields.get_input')
def test_executor__doesnt_like_running(mock_input):
    mock_input.side_effect = [
        'Matt',
        'mattdsegal@gmail.com',
        'n',
        '\n'
    ]
    data = executor.execute(TEST_SCRIPT)
    assert data == {
        'NAME': 'Matt',
        'EMAIL': 'mattdsegal@gmail.com',
        'LIKES_RUNNING': False,
        'LAST_RAN': None,
        'RUNS_PER_WEEK': None,
        'FAVOURITE_SHOE': None,
        'RUNNING_SURFACES': None,
    }


@mock.patch('src.script.fields.get_input')
def test_executor__happy_path(mock_input):
    mock_input.side_effect = [
        'Matt',
        'mattdsegal@gmail.com',
        'y',
        '01/01/2018',
        '12',
        'A',
        '\n',
        'B',
        '\n'
    ]
    data = executor.execute(TEST_SCRIPT)
    assert data == {
        'NAME': 'Matt',
        'EMAIL': 'mattdsegal@gmail.com',
        'LIKES_RUNNING': True,
        'LAST_RAN': datetime(2018, 1, 1, 0, 0),
        'RUNS_PER_WEEK': 12,
        'FAVOURITE_SHOE': 'Nike',
        'RUNNING_SURFACES': ['Asphalt'],
    }
