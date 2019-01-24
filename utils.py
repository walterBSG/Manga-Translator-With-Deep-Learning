#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  8 14:04:55 2018

@author: walter
"""
import os
import shutil
from PIL import Image
from fnmatch import fnmatch

def takeFilesByExtension(folder, pattern):
	paths = []
	for path, subdirs, files in os.walk(folder):
	    for name in files:
	        if fnmatch(name, pattern):
	            paths.append(os.path.join(path, name))

	return paths

def takeAllFiles(folder):
	paths = []
	for path, subdirs, files in os.walk(folder):
		for name in files:
			paths.append(os.path.join(path, name))
	return paths

def list_paths(folder):
	names = []
	for filename in os.listdir(folder):
		filename = os.path.join(folder,filename)
		names.append(filename)
	names = sorted(names, key=str.lower)
	return names

def loadImages(paths):
	images = []
	for path in paths:
		images.append(Image.open(path))
	
	return images

def copy(folder,dest):
	
	files = os.listdir(folder)
	files = sorted(files, key=str.lower)
	
	for idx, n in enumerate(files):
		if not (os.path.isdir(folder+n)):
			shutil.copyfile(os.path.join(folder,n), os.path.join(dest,n))

def move_percentage(folder,dest, percentage):
	files = os.listdir(folder)
	files = sorted(files, key=str.lower)
	
	amount = 100/percentage
	
	for idx, n in enumerate(files):
		if ((idx%amount) == 0):
			shutil.move(os.path.join(folder,n), os.path.join(dest,n))
			
def remove(original, target):
	files = os.listdir(original)
	for file in files:
		   os.remove(os.path.join(target,file))
   
def clean(folder):
	files = os.listdir(folder)
	for file in files:
		os.remove(os.path.join(folder,file))   

"""
dest= '/home/walter/Documents/models/research/object_detection/data/images/'
utils.clean(dest)

folders = utils.list_paths('/home/walter/Downloads/mangaDataset')

for folder in folders:
	new = folder.replace('chapter','')
	new = new.replace(' ','_')
	os.rename(folder,new)
	folder = new
	name = os.path.basename(folder)
	for filename in utils.list_paths(folder):
		name2 = os.path.basename(filename)
		new = filename.replace(name2,(name+name2))
		os.rename(os.path.join(folder, filename),(new))
		
"""