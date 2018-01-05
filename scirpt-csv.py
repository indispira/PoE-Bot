import string
import re

f = open('List_currencies.csv', 'r')
text = f.read()
text = string.split(text, '\n')
result = '"value";"language"'
for line in text:
	result += '\n"'
	result += line
	result += '";"en"'
print result
r = open('list.csv', 'w')
r.write(result)
r.close()
f.close()