import utils
import cv2
import os
import pytesseract
import balloonDetector as detector
import fit_text
import translator_module as tr


print('ok')

def translate(folder = 'test'):
	
	model, tokenizer, x, y = tr.load_all()
	print('translator loaded')
	
	paths = utils.takeFilesByExtension(folder, '*.jpg')
	print('paths taken')
	
	ballons, locations, pages = detector.detectFromPaths(paths)
	
	path = pages[0]
	img = cv2.imread(path)
	
	for ballon, location, page in zip(ballons, locations, pages):
		if path != page:
			cv2.imwrite(os.path.join('translated',os.path.basename(path)), img)
			path = page
			img = cv2.imread(path)
		result = pytesseract.image_to_string(ballon)
		result = tr.translate(model, result, tokenizer, x, y)
		fited_text = fit_text.fit_text(ballon.shape[0],ballon.shape[1],result)
		img[location[0]:location[1],location[2]:location[3]] = fited_text

translate()