import itertools
import math
import pprint
import nltk
nltk.download('punkt')

READ_FILENAME = 'ru_ar_cut_formatted.txt'

file = open(READ_FILENAME, 'rt')
text = file.read()
file.close()

tokens = nltk.tokenize.word_tokenize(text, 'russian', True)
print('Tokens')
print(tokens[:100])
print()

trigrams = list(nltk.trigrams(tokens))
print('Trigrams')
print(trigrams[:25])
print()

trigram_pmi = nltk.collocations.TrigramAssocMeasures().pmi
finder = nltk.collocations.TrigramCollocationFinder.from_words(nltk.Text(tokens))
nltk_best = finder.nbest(trigram_pmi, 50)
print('NLTK pmi')
print(nltk_best)
print()

words_counts = {}
for word in tokens:
    if (word not in words_counts):
        words_counts[word] = 0
    words_counts[word] += 1
print('words_counts')
print(dict(itertools.islice(words_counts.items(), 50)))
print()

trigrams_counts = {}
for trigram in trigrams:
    tri_key = str(trigram)
    if (tri_key not in trigrams_counts):
        trigrams_counts[tri_key] = {'trigram': trigram, 'count': 0}
    trigrams_counts[tri_key]['count'] += 1
print('trigrams_count')
print(dict(itertools.islice(trigrams_counts.items(), 50)))
print()

all_count = len(tokens)

trigrams_pmi = []
for trigram_key, trigram_object in trigrams_counts.items():
    count1 = words_counts[trigram_object['trigram'][0]]
    count2 = words_counts[trigram_object['trigram'][1]]
    count3 = words_counts[trigram_object['trigram'][2]]
    p1 = count1 / all_count
    p2 = count2 / all_count
    p3 = count3 / all_count
    p_all = trigram_object['count'] / all_count
    pmi_score = math.log2(p_all / (p1 * p2 * p3))
    trigrams_pmi.append((trigram_key, pmi_score, count1, count2, count3, trigram_object['count']))

trigrams_pmi.sort(key=lambda tuple: tuple[1], reverse=True)
print('Self-made PMI')
pprint.pprint(trigrams_pmi[:50])
print()

