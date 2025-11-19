def make_censor(bad_words):
    bad_words = set(bad_words)

    def add_word(word):
        bad_words.add(word)

    def censor(text):
        words = text.split()
        result = [
            "*" * len(w) if w in bad_words else w
            for w in words
        ]
        return " ".join(result)

    return censor, add_word

censor, add_word = make_censor(["kot"])

print(censor("kot"))

print(censor("pies"))    # ***
add_word("pies")
print(censor("pies"))    # ****


