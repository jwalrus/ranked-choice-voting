from dataclasses import dataclass
from typing import List, Dict, Optional, Set


# todo: add report for each round
# todo: add more tests for calculate_winner
# todo: add tie-breaking strategies
def load_votes(f: str) -> List[List[str]]:
    return []


@dataclass
class RankedChoiceElectionRound:

    def __init__(self, _round: int, votes: List[List[str]], eliminated: Set[str] = frozenset()):
        self.round = _round
        self.votes = votes
        self.tally = count_first_choice_votes(votes)
        self._eliminated = eliminated

    @property
    def winner(self) -> Optional[str]:
        return winner(self.tally)

    @property
    def eliminated(self) -> Set[str]:
        return candidates_to_eliminate(self.tally).union(self._eliminated)

    @property
    def report(self) -> str:
        return '\n'.join([
            f'Round {self.round}',
            '-' * 50,
            f'Winner:     {self.winner}',
            f'Eliminated: {self.eliminated}',
            f'Tally:      {self.tally}',
            '-' * 50,
        ])


@dataclass
class RankedChoiceElectionOutcome:

    def __init__(self, rounds: List[RankedChoiceElectionRound]):
        self.rounds = rounds

    @property
    def winner(self) -> str:
        return self.rounds[-1].winner

    @property
    def report(self) -> str:
        return '\n\n'.join([r.report for r in self.rounds])


@dataclass
class RankedChoiceElection:

    def __init__(self, votes: List[List[str]]):
        self.votes = votes

    def run(self) -> RankedChoiceElectionOutcome:

        def go(num, vs, eliminated, acc) -> List[RankedChoiceElectionRound]:
            rnd = RankedChoiceElectionRound(num, vs, eliminated)
            if rnd.winner:
                return acc + [rnd]
            else:
                return go(num + 1, update_votes(vs, rnd.eliminated), rnd.eliminated, acc + [rnd])

        return RankedChoiceElectionOutcome(go(1, self.votes, set(), []))


def main():
    votes = load_votes('some/file/path.csv')
    election = RankedChoiceElection(votes)
    outcome = election.run()  # type: RankedChoiceElectionOutcome
    print(outcome.winner)
    print(outcome.report)


def count_first_choice_votes(votes: List[List[str]]) -> Dict[str, int]:
    d = {}  # type: Dict[str, int]
    for vote in votes:
        if vote:
            choice = vote[0]
            d.setdefault(choice, 0)
            d[choice] = d[choice] + 1
    return d


def winner(vote_tally: Dict[str, int], threshold: float = 0.5) -> Optional[str]:
    total_votes = sum(vote_tally.values())
    for candidate, vote_count in vote_tally.items():
        if vote_count / total_votes > threshold:
            return candidate
    return None


def candidates_to_eliminate(vote_tally: Dict[str, int]) -> Set[str]:
    least_popular_count = min(vote_tally.values())
    return {candidate for candidate, tally in vote_tally.items() if tally == least_popular_count}


def update_votes(votes: List[List[str]], eliminated: Set[str]) -> List[List[str]]:
    xs = [[candidate for candidate in vote if candidate not in eliminated] for vote in votes]
    return [x for x in xs if x]


def calculate_winner(votes: List[List[str]]) -> str:
    counts = count_first_choice_votes(votes)
    first = winner(counts)
    if first:
        return first
    else:
        eliminated = candidates_to_eliminate(counts)
        updated_votes = update_votes(votes, eliminated)
        return calculate_winner(updated_votes)
