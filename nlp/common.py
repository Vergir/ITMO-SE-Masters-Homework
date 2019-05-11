def diff(first, second):
    second = set(second)
    return [item for item in first if item not in second]


def pos_tags_dictionary(tokens):
    import nltk
    pos_tags = nltk.pos_tag(tokens)
    tokens_tags = {}
    for token_tag_tuple in pos_tags:
        tokens_tags[token_tag_tuple[0]] = token_tag_tuple[1]

    return tokens_tags
