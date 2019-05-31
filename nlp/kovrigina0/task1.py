import re
import nltk
nltk.download('punkt')

FILENAME = 'task1_text.txt'

file = open(FILENAME, 'rt')
text = file.read()
file.close()

formatted_text = text
print(formatted_text)

print('replace \begin & \end blocks with contents')
formatted_text = re.sub(r"\\begin{(.*?)}(.*?)\\end{(.*?)}", r"\2", formatted_text, flags=re.M | re.S)
print(formatted_text)

print('replace \tt links with url')
formatted_text = re.sub(r"{\\tt (.*?)}", r"\1", formatted_text, flags=re.M | re.S)
print(formatted_text)

print('replace \section with section names')
formatted_text = re.sub(r"\\section{(.*?)}", r"\1.", formatted_text, flags=re.M | re.S)
print(formatted_text)

print('delete redundant tags')
formatted_text = re.sub(r"(\\ref{.*?}|\[ht\]|\\maketitle|\\includegraphics.*?})", r"", formatted_text, flags=re.M | re.S)
print(formatted_text)

print('replace all other tags as tag_name: tag_content')
formatted_text = re.sub(r"\\(.*?){(.*?)}", r"\1: \2", formatted_text, flags=re.M | re.S)
print(formatted_text)

print('overall text')
formatted_text = formatted_text.replace('\n', ' ')
print(formatted_text)

print('tokenization')
tokens = nltk.tokenize.word_tokenize(formatted_text)
#выводим все словоупотребления в тексте:
print(tokens)