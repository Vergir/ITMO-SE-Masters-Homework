import nltk.book
import nltk.corpus
import nltk.tokenize
import string
import common


def freq_dist(corpus, n_words=50, plot=True):
    dist = nltk.book.FreqDist(corpus)
    if plot:
        dist.plot(n_words, cumulative=False)

    most_common_tuples = dist.most_common(n_words)
    most_common_words = [word_freq[0] for word_freq in most_common_tuples]

    return most_common_words


def search_index(index, word1, word2):
    result_docs = set()

    word1_docs = index[word1]
    word2_docs = index[word2]

    common_docs = word1_docs.keys() & word2_docs.keys()

    if common_docs:
        for doc_id in common_docs:
            for w1 in word1_docs[doc_id]:
                if not w1[1].startswith('N') and not w1[1].startswith('J'):
                    continue
                for w2 in word2_docs[doc_id]:
                    if not w2[1].startswith('N') and not w2[1].startswith('J'):
                        continue
                    if w1[0] + len(word1) + 1 == w2[0]:
                        result_docs.add((doc_id, w1[0]))

    return result_docs


def clean_and_lemmatize(tokens, tags):
    processed_tokens = tokens

    # clean punctuation
    processed_tokens = common.diff(processed_tokens, string.punctuation)

    # clean stopwords
    stopwords = nltk.corpus.stopwords.words('english')
    processed_tokens = common.diff(processed_tokens, stopwords)

    # lemmatize
    lemmatizer = nltk.stem.WordNetLemmatizer()
    lemmatized_tokens = []
    for token in processed_tokens:
        lemma_tag = nltk.corpus.wordnet.NOUN
        if tags[token].startswith('J'):
            lemma_tag = nltk.corpus.wordnet.ADJ
        elif tags[token].startswith('V'):
            lemma_tag = nltk.corpus.wordnet.VERB
        elif tags[token].startswith('R'):
            lemma_tag = nltk.corpus.wordnet.ADV
        lemmatized_tokens.append(lemmatizer.lemmatize(token, pos=lemma_tag))
    processed_tokens = lemmatized_tokens

    return processed_tokens


def plot_and_diff_most_common_words(tokens1, tokens2):
    tokens1_common_words = freq_dist(tokens1)
    tokens2_common_words = freq_dist(tokens2)

    tokens1_diff = common.diff(tokens1_common_words, tokens2_common_words)
    print("Words in tokens1 list but not in tokens2 list")
    print(tokens1_diff)
    print()

    tokens2_diff = common.diff(tokens2_common_words, tokens1_common_words)
    print("Words in tokens2 list but not in tokens1 list")
    print(tokens2_diff)
    print()


def create_pos_index(unique_tokens, documents, documents_tokens, tokens_tags):
    pos_index = {}
    for token in unique_tokens:
        if token not in pos_index:
            pos_index[token] = {}
        for doc_id, doc in enumerate(documents):
            cnt = documents_tokens[doc_id].count(token)
            token_position = -1
            str_position = -1
            for i in range(0, cnt):
                try:
                    token_position = documents_tokens[doc_id].index(token, token_position + 1)
                    str_position = doc.index(token, str_position + 1)
                    while (
                            (doc[str_position - 1] != ' ' and doc[str_position - 1] not in string.punctuation)
                            or
                            (
                                    len(doc) != str_position + len(token) and
                                    doc[str_position + len(token)] != ' ' and
                                    doc[str_position + len(token)] not in string.punctuation
                            )
                    ):
                        str_position = doc.index(token, str_position + 1)

                    if doc_id not in pos_index[token]:
                        pos_index[token][doc_id] = set()
                    pos_index[token][doc_id].add((str_position, tokens_tags[token]))
                except ValueError:
                    pass

    return pos_index
