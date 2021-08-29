import pytest

from rcv.rankedchoice import *


@pytest.mark.parametrize(
    'votes,expected_counts', [
        ([], {}),
        ([[]], {}),
        ([['a'], []], {'a': 1}),
        ([['a']], {'a': 1}),
        ([['a'], ['a']], {'a': 2}),
        ([['a', 'b'], ['b', 'a']], {'a': 1, 'b': 1}),
        ([['a', 'b'], ['b', 'a', 'c'], ['b', 'a']], {'a': 1, 'b': 2})
    ]
)
def test_count_first_choice_votes(votes, expected_counts):
    assert count_first_choice_votes(votes) == expected_counts


@pytest.mark.parametrize(
    'vote_tally,expected_winner', [
        ({}, None),
        ({'a': 1}, 'a'),
        ({'a': 1, 'b': 2}, 'b'),
        ({'a': 1, 'b': 1, 'c': 1}, None),
        ({'a': 1, 'b': 1}, None)
    ]
)
def test_winner(vote_tally, expected_winner):
    assert winner(vote_tally) == expected_winner


@pytest.mark.parametrize(
    'vote_tally,expected_eliminated', [
        ({'a': 1}, {'a'}),
        ({'a': 1, 'b': 2}, {'a'}),
        ({'a': 1, 'b': 1, 'c': 1}, {'a', 'b', 'c'})
    ]
)
def test_candidate_to_eliminate(vote_tally, expected_eliminated):
    assert candidates_to_eliminate(vote_tally) == expected_eliminated


@pytest.mark.parametrize(
    'votes,eliminated,expected_votes', [
        ([], {}, []),
        ([['b', 'a'], ['b', 'a'], ['a']], {'a'}, [['b'], ['b']]),
        ([['a', 'b', 'c'], ['b', 'c', 'a']], {'c'}, [['a', 'b'], ['b', 'a']])
    ]
)
def test_update_votes(votes, eliminated, expected_votes):
    assert update_votes(votes, eliminated) == expected_votes


def test_calculate_winner():
    votes = [
        ['a', 'b', 'c'],
        ['b', 'c', 'a'],
        ['c', 'b', 'a'],
        ['b', 'c', 'a'],
        ['c', 'b', 'a']
    ]

    assert calculate_winner(votes) == 'b'

