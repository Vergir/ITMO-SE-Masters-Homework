READ_FILENAME = 'ru_ar_cut.txt'
WRITE_FILENAME = 'ru_ar_cut_formatted.txt'

file = open(READ_FILENAME, 'rt')
text = file.read()
file.close()

rows = text.split('\n')
formatted_text = ''
for row in rows:
    if (row == '<s>'):
        formatted_text += '\n'
        continue
    label = row.split('	')[0]
    if (label == '.' or ('<' in label and '>' in label)):
        continue
    formatted_text += ' ' + label

print(formatted_text[:1000])

file = open(WRITE_FILENAME, 'w')
file.write(formatted_text)
file.close()