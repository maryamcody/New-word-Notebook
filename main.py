
TEXT = "the cat sat on the mat and the cat ate the fish and the dog sat on the rug"
WORDS = TEXT.split()

TEST_WORDS = [
    ("the", "cat"),
    ("sat", "on"),
    ("and", "the"),
    ("dog", "sat"),
    ("pizza", "the"),
    ("cat", "ate"),
]


def build_bigrams(words):
    model = {}
    for current, following in zip(words, words[1:]):
        if current not in model:
            model[current] = {}
        model[current][following] = model[current].get(following, 0) + 1
    return model

BIGRAMS = build_bigrams(WORDS)
print("PART 1: Bigrams")
print(BIGRAMS.get("the"), BIGRAMS.get("pizza", "not found"))


def probabilities(word):
    counts = BIGRAMS.get(word, {})
    total = sum(counts.values())
    result = {}
    for following, count in counts.items():
        result[following] = count / total
    return result

print("\nPART 2: Probabilities")
print({w: round(p, 2) for w, p in probabilities("the").items()})


def predict(word):
    chances = probabilities(word)
    if not chances:
        return "the"
    return max(chances, key=chances.get)

print("\nPART 3: Predict")
print(predict("the"), "|", predict("pizza"))


print("\nPART 4: Test all words")
mistakes = 0
for word, wanted in TEST_WORDS:
    answer = predict(word)
    if answer != wanted:
        mistakes += 1
    print(word, "->", answer)
print("Mistakes:", mistakes, "out of", len(TEST_WORDS))


if __name__ == "__main__":
    print("NEXT WORD NOTEBOOK")
    print("==================")

    print("\nPART 1: Bigrams")
    print(BIGRAMS.get("the"), BIGRAMS.get("pizza", "not found"))

    print("\nPART 2: Probabilities")
    print({
        w: round(p, 2)
        for w, p in probabilities("the").items()
    })

    print("\nPART 3: Predict")
    print(predict("the"), "|", predict("pizza"))

    print("\nPART 4: Test all words")
    mistakes = 0

    for word, wanted in TEST_WORDS:
        answer = predict(word)

        if answer != wanted:
            mistakes += 1

        print(word, "->", answer)

    print("Mistakes:", mistakes, "out of", len(TEST_WORDS))