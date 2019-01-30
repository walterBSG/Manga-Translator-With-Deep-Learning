#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 14:36:49 2019

@author: walter
"""

import numpy as np
import textwrap
import cv2

def fit_text(x,y,text, color = (255,255,255)):
	img = np.zeros([x,y,3],dtype=np.uint8)
	img[:] = color
	
	text = textwrap.wrap(text, width=int(y/7))
	text = '\n'.join(t for t in text)
	
	font = cv2.FONT_HERSHEY_SIMPLEX
	height = 15
	
	for i, line in enumerate(text.split('\n')):
		img = cv2.putText(img,line,(0,height), font, 0.4,(0,0,0))
		height += 15
	return img