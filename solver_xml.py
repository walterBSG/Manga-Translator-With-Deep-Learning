#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 12 13:32:27 2018

@author: walter
"""
import re
import os
from fnmatch import fnmatch

def takeFilesByExtension(folder, pattern):
	paths = []
	for path, subdirs, files in os.walk(folder):
	    for name in files:
	        if fnmatch(name, pattern):
	            paths.append(os.path.join(path, name))

	return paths

def fileSolver(file):
	with open(file, 'r+') as f:
		text = f.read()
		filename = os.path.basename(file)
		filename = filename.replace('.xml','.jpg')
		path = file.replace('.xml','.jpg')
		text = re.sub('<folder>.*?</folder>','<folder>images</folder>',text, flags=re.DOTALL)
		text = re.sub('<filename>.*?</filename>',('<filename>'+filename+'</filename>'),text, flags=re.DOTALL)
		text = re.sub('<path>.*?</path>',('<path>'+path+'</path>'),text, flags=re.DOTALL)
	with open(file, 'w+') as f:
		f.write(text)
		
paths = takeFilesByExtension('/home/walter/Documents/models/research/object_detection/data/images','*.xml')
print(paths)
for path in paths:
	fileSolver(path)