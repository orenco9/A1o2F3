from game import Session
# from strategies.random_strategy import RandomStrategy
# from strategies.rank_only_strategy import RankOnlyStrategy
from strategies.binary_strategy import BinaryStrategy

N_PLAYERS = 2
N_LOOP = 30000

N_BBS = 8
BB_SIZE = 3
RAKE_SIZE = 0  # OCOC1

def main():
    strategies = list()
    strategies.append(BinaryStrategy(True))
    strategies.append(BinaryStrategy(True))
    strategies.append(BinaryStrategy(True))
    strategies.append(BinaryStrategy(True))
    session = Session(N_BBS, BB_SIZE, RAKE_SIZE, strategies)

    session.run(5)

if __name__ == "__main__":
    main()

# python -m cProfile -s cumtime main2.py
