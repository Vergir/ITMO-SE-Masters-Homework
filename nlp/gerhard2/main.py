import common
import gerhard2.functions
import nltk.book

if __name__ == '__main__':
    # 1. Download the text you selected
    file_name = 'text.txt'
    with open(file_name, 'r') as book_file:
        lines = book_file.read()

    # 2. Apply word and sentence tokenization
    # 7. Split your assigned gutenberg book into paragraphs
    sent_tokens = nltk.tokenize.sent_tokenize(lines)
    document_size = 50
    documents = [' '.join(sent_tokens[n:n + document_size]) for n in range(0, len(sent_tokens), document_size)]
    documents_tokens = [[token for token in nltk.tokenize.word_tokenize(document)] for document in documents]
    all_tokens = [token for document_tokens in documents_tokens for token in document_tokens]
    unique_tokens = set(all_tokens)

    # 3. Convert to a nltk Text
    nltk_text = nltk.Text(all_tokens)

    # 4. Use NLTK FreqDist to print and plot the most common words in your book
    # 5. Compare the frequency to “Moby Dick” book in NLTK, What are the differences in the 50 most frequent words?
    my_text_raw = all_tokens
    example_text_raw = nltk.book.text1.tokens
    print("Analysing My book and Example book (raw)")
    gerhard2.functions.plot_and_diff_most_common_words(my_text_raw, example_text_raw)

    # 6. Repeat step 5, but first remove all stopwords, and apply lemmatization to the list of tokens
    tokens_tags = common.pos_tags_dictionary(unique_tokens)
    my_text_clean = gerhard2.functions.clean_and_lemmatize(all_tokens, tokens_tags)
    example_text_clean = gerhard2.functions.clean_and_lemmatize(example_text_raw, common.pos_tags_dictionary(example_text_raw))
    print("Analysing My book and Example book (cleaned)")
    gerhard2.functions.plot_and_diff_most_common_words(my_text_clean, example_text_clean)

    # 8. Now create a positional index, with the paragraphs being the documents
    pos_index = gerhard2.functions.create_pos_index(unique_tokens, documents, documents_tokens, tokens_tags)

    # 9. Implement simple search for 2 word phrase queries
    # 10. Do some example searches to show that the positional index works
    # 11. Bonus (optional for extra points): Apply POS (part-of-speech) tagging to the text,
    # and search only for nouns and adjectives in the text.
    print('Results of search "simple story":')
    print(gerhard2.functions.search_index(pos_index, 'simple', 'story'))  # should output {(80, 2729)}
    print()
    print('Results of search "Martin drank":')
    print(gerhard2.functions.search_index(pos_index, 'Martin', 'drank'))
    print()

    print("Text at document 80, words 2720 and beyond")  # as a proof for 'simple story' earlier
    print("'" + documents[80][2720:] + "'")
