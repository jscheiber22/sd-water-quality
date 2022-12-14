import subprocess
import re
from flask import Flask


app = Flask(__name__)


@app.get('/sdwaterquality')
def waterquality():
	WQ = WaterQuality()
	WQ.start()
	return {"water":list(WQ.info.values())}


class WaterQuality:
	def __init__(self):
		self.url = 'https://www.sdcoastkeeper.org/beach-advisories'
		self.info = {}


	# Disable refresh when referencing a predownloaded site, mostly used for debugging
	def grabLines(self, refresh = True):
		if refresh:
			subprocess.call('curl ' + self.url + ' -o SDBeachAdvisory.html', shell=True)
		try:
			with open('SDBeachAdvisory.html') as f:
				lines =  f.readlines()
		except FileNotFoundError:
			print('FileNotFoundError. Could not locate html file.')

		if lines is not None:
			return lines
		else:
			print('Preventing a TypeError. An html file was evidently found but seems to be empty and returned type None. Probably need to redonwload the site :).')
			exit()


	# Renoves leftover regex text as well as anything else that ends up getting kept
	def cleanText(self, text):
		textToReplace = [
			'sans-serif;">',
			'</span>',
			'&#8217;',
			'<span style="color: #ff0000;"><span style="font-size: 10pt; font-family: arial, helvetica, sans-serif; color: #000000;">',
			'<span style="color: #ff0000;"><span style="color: #000000;">',
			'sans-serif; font-size: 10pt;">',
			'<span style="color: #ff0000;">',
			'<strong>',
			'</strong>'
		]

		for value in textToReplace:
			text = text.replace(value, '')

		return text

	# Curl the site and decipher the pulled table
	def start(self):
		html = self.grabLines(False)

		# Gathers list of location titles
		locations = []
		# Gathers the text associated with each location
		locationText = []
		for x in range(0, len(html)):
			if '<tr' in html[x]:
				loc = re.search('sans-serif;">.+</span>', html[x+2]) # Two lines below the <tr> tag is the location title
				if loc is not None:
					locations.append(self.cleanText(loc.group()))
				else:
					# If loc is None, the text was not found, but evidently there can be different html attributes around the text so this looks for another kind
					loc = re.search('sans-serif; font-size: 10pt;">.+</span>', html[x+2])
					if loc is not None:
						locations.append(self.cleanText(loc.group()))
				text = re.search('sans-serif;">.+</span>', html[x+3]) # Three lines below the <tr> tag is the location text
				if text is not None:
					locationText.append(self.cleanText(text.group()))
				else:
					text = re.search('sans-serif; font-size: 10pt;">.+</span>', html[x+3])
					if text is not None:
						locationText.append(self.cleanText(text.group()))


		# Creates a dictionary out of the cleaned up lists w title as key and text as value
		# It is wrapped within another list for API purposes
		self.info = { 'qualities': dict(zip(locations[1:], locationText[1:])) } # locationText was previously [3:] until they only had 1 listed beach ("all beaches") but now it only works with [1:] which makes more sense anyway


if __name__ == '__main__':
	WaterQuality().start()
