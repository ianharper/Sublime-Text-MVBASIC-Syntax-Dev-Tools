import xml.etree.ElementTree as ET
import os


def convertToUpper(path, ext_len):
	tree = ET.parse(path)
	root = tree.getroot()
	root.find('content').text = root.find('content').text.upper() 
	root.find('tabTrigger').text = root.find('tabTrigger').text.upper() 
	out_path = path[:-ext_len] + ' (upper)' + path[-ext_len:]
	tree.write(out_path)
	print(out_path)

def parseDir(directory):
	directory = os.fsencode(directory)
	for file in os.listdir(directory):
		filename = os.fsdecode(file)
		if filename[-ext_len:] == ext and 'upper' not in filename:
			convertToUpper( os.fsdecode(directory) + '\\' + filename, ext_len )

ext = '.sublime-snippet'
ext_len = len(ext)

parseDir('C:\\Users\\ianbe\\AppData\\Roaming\\Sublime Text 3\\Packages\\MVBasic-Syntax\\d3\\snippets')
parseDir('C:\\Users\\ianbe\\AppData\\Roaming\\Sublime Text 3\\Packages\\MVBasic-Syntax\\qm\\snippets')

