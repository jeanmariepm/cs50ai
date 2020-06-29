from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

exclusive = And(
    Or(AKnight, AKnave),
    Implication(AKnight, Not(AKnave)),
    Or(BKnight, BKnave),
    Implication(BKnight, Not(BKnave)),
    Or(CKnight, CKnave),
    Implication(CKnight, Not(CKnave)),
)
# Puzzle 0
# A says "I am both a knight and a knave."
claim1 = And(AKnight, AKnave)
knowledge0 = And(
    # TODO
    exclusive,
    Implication(AKnight, claim1),
    Implication(AKnave, Not(claim1))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
claim1 = And(AKnave, BKnave)
knowledge1 = And(
    # TODO
    exclusive,
    Implication(AKnight, claim1),
    Implication(AKnave, Not(claim1))

)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
claim1 = Or(And(AKnight, BKnight), And(AKnave, BKnave))
claim2 = Or(And(AKnight, BKnave), And(AKnave, BKnight))
knowledge2 = And(
    # TODO
    exclusive,
    Implication(AKnight, claim1),
    Implication(AKnave, Not(claim1)),
    Implication(BKnight, claim2),
    Implication(BKnave, Not(claim2))

)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
claim1 = AKnight  # since A did say something
claim2 = BKnave  # since A could not have said what B says that A said
claim3 = CKnave  # claim by B
claim4 = AKnight  # claim by C
knowledge3 = And(
    # TODO
    exclusive,
    claim1,
    claim2,
    Implication(BKnight, claim3),
    Implication(BKnave, Not(claim3)),
    Implication(CKnight, claim4),
    Implication(CKnave, Not(claim4))

)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
