# Example run command:
# python create_syntax_test.py jbase-basic

import sys
import json


def countLeadingSpaces(text):
	spaces = 0
	for c in text:
		if c == ' ':
			spaces +=1 
		else:
			break
	return spaces

def lenWithoutTrailingSpaces(text):
	for x in reversed(range(len(text))):
		if text[x] == ' ': continue
		return x + 1
	return 0

def field(text, delim, position, count=1):
	field_text = ''
	cur_position = 1
	for c in text:
		if c == delim: 
			cur_position += 1
		if cur_position >= position and cur_position <= (position + count -1): 
			field_text += c
		if cur_position > position + count - 1: 
			break
	return field_text


def assertion(syntax_name, scope, col, repeat=1):
	assert_line = '*'
	if col == 0 or col == '': 
		assert_line += ' <- '
	else:
		assert_line += (' ' * (col - 1)) + ('^' * repeat) + ' '
	assert_line += 'source.' + syntax_name + ' ' + scope + '\n'
	return assert_line

def matchWord(syntax_name, word, scope, indent=3, prefix=''):
	test_lines = ''
	test_lines += prefix + word + '\n'
	test_lines += assertion(syntax_name, scope , countLeadingSpaces(word) + len(prefix))

	indent *= ' '
	test_lines += indent + prefix + word + " \n"
	match_len = len(word.strip()) 
	if word[-2:] == '()': match_len -= 2
	test_lines += assertion(syntax_name, scope , countLeadingSpaces(indent + word) + len(prefix), match_len)
	if indent != '': test_lines += assertion(syntax_name, '' ,countLeadingSpaces(indent + word) + len(prefix) - 1)
	test_lines += assertion(syntax_name, '- ' + scope  ,lenWithoutTrailingSpaces(indent + word) + len(prefix))

	test_lines += '\n'
	return test_lines

syntax_name = sys.argv[1]
if syntax_name == '': syntax_name = 'd3-basic'

path = 'C:\\Users\\ianbe\\AppData\\Roaming\\Sublime Text 3\\Packages\\MultiValue Basic\\'
path += field(syntax_name, '-', 1) + '\\'
print('Test written to: ' + path)
syntax_test_file_name = path + 'syntax_test_' + syntax_name + '_auto_generated.bp'
syntax_test_file = open(syntax_test_file_name, 'w+')

json_elements 	= json.load(open(syntax_name + '.syntax-elements.json'))
constants		= json_elements['constants']
functions		= json_elements['functions']
statements		= json_elements['statements']
flow_control	= json_elements['flow_control']
other			= json_elements['other']
operators		= json_elements['operators']
labels			= json_elements['labels']
# todo: add support for qm builtins

all_words = functions + statements + flow_control + other

syntax_test_file.write('* SYNTAX TEST "' + syntax_name + '.sublime-syntax"\n\n')


syntax_test_file.write('* Constants:\n')
for x in constants:
	syntax_test_file.write(matchWord(syntax_name, x, 'constant.character'))


syntax_test_file.write('* Functions:\n')
for x in functions:
	syntax_test_file.write(matchWord(syntax_name, x + '()', 'support.function.builtin.basicFunction'))


syntax_test_file.write('* Statements:\n')
for x in statements:
	syntax_test_file.write(matchWord(syntax_name, x, 'support.function.builtin.basicStatement'))


syntax_test_file.write('* Flow Control:\n')
for x in flow_control:
	syntax_test_file.write(matchWord(syntax_name, x, 'keyword.control.flow'))


syntax_test_file.write('* Other Keywords:\n')
for x in other:
	syntax_test_file.write(matchWord(syntax_name, x + ' ', 'keyword.other', prefix='word '))


syntax_test_file.write('* Operators:\n')
for x in operators:
	syntax_test_file.write(matchWord(syntax_name, ' ' + x + ' ', 'keyword.operator', prefix='var = 1'))

syntax_test_file.write('* Labels:\n')
for x in labels:
	syntax_test_file.write(matchWord(syntax_name, x, 'entity.name.function.linelabel', 0))

syntax_test_file.write('* Variables: \n')
for x in all_words:
	if '@' in x: continue
	x = x.replace(' ', '.')
	syntax_test_file.write(matchWord(syntax_name, ' ' + x + '.test ', 'variable'))
	syntax_test_file.write(matchWord(syntax_name, x + '.test ', 'variable'))
	syntax_test_file.write(matchWord(syntax_name, ' test.' + x + ' ', 'variable'))
	syntax_test_file.write(matchWord(syntax_name, ' test.' + x, 'variable'))

