from NounPhrasesExtractor import get_nouns_phrases

noun_phrases = get_nouns_phrases("Michael Jackson was a great musician.")

for term in noun_phrases:
    for word in term:
        print(word,)
    print('\n')
