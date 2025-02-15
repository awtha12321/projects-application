from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knight_A_says = Symbol("I am both a knight and a knave.")
knowledge0 = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Biconditional(AKnight, knight_A_says),
    Biconditional(AKnave, Not(knight_A_says)),
    Not(knight_A_says)
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knight_A_says = Symbol("We are both knaves.")
knowledge1 = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Biconditional(AKnight, knight_A_says),
    Biconditional(AKnave, Not(knight_A_says)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    Implication(knight_A_says, BKnave),
    Implication(AKnave, BKnight),
    Not(knight_A_says)
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knight_A_says = Symbol("We are the same kind.")
knight_B_says = Symbol("We are of different kinds.")
knowledge2 = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Biconditional(AKnight, knight_A_says),
    Biconditional(AKnave, Not(knight_A_says)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    Biconditional(BKnight, knight_B_says),
    Biconditional(BKnave, Not(knight_B_says)),
    Implication(knight_A_says, Or(And(AKnight, BKnight), And(AKnave, BKnave))),
    Implication(knight_B_says, Or(Not(And(AKnight, BKnight)), Not(And(AKnave, BKnave)))),
    Not(knight_A_says),
    knight_B_says
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knight_A_says = Symbol("I am a knight.' or 'I am a knave.', but you don't know which.")
knight_B_says = Symbol("A said 'I am a knave'.")
knight_B_says_2 = Symbol("C is a knave.")
knight_C_says = Symbol("A is a knight.")
knowledge3 = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Biconditional(AKnight, knight_A_says),
    Biconditional(AKnave, Not(knight_A_says)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    Biconditional(BKnight, knight_B_says),
    Biconditional(BKnave, Not(knight_B_says)),
    Implication(Not(knight_B_says), Not(knight_B_says_2)),
    Or(CKnight, CKnave),
    Not(And(CKnight, CKnave)),
    Biconditional(CKnight, knight_C_says),
    Biconditional(CKnave, Not(knight_C_says)),
    Implication(knight_A_says, Or(AKnight, AKnave)),
    Implication(knight_B_says, BKnave),
    Implication(knight_B_says_2,  CKnave),
    Implication(knight_C_says, AKnight),
    knight_A_says,
    Not(knight_B_says),
    Not(knight_B_says_2),
    knight_C_says
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
