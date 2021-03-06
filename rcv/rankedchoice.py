from typing import List, Dict, Optional, Set


# todo: add report for each round
# todo: add more tests for calculate_winner
# todo: add tie-breaking strategies

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
    print(least_popular_count)
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
