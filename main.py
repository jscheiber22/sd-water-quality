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
			subprocess.call('curl ' + self.url + ' -o SDBeachAdvisory.html')
		try:
			with open('SDBeachAdvisory.html') as f:
				return f.readlines()
		except FileNotFoundError:
			print('FileNotFoundError. Could not locate html file.')


	def cleanText(self, text):
		return text.group().replace('sans-serif;">', '').replace('</span>', '').replace('&#8217;', "'")


	# Curl the site and decipher the pulled table
	def start(self):
		html = self.grabLines(False)

		# Gathers list of location titles
		self.locations = []
		# Gathers the text associated with each location
		self.locationText = []
		for x in range(0, len(html)):
			if '<tr' in html[x]:
				loc = re.search('sans-serif;">.+</span>', html[x+2]) # Two lines below the <tr> tag is the location title
				if loc is not None:
					self.locations.append(self.cleanText(loc))
				text = re.search('sans-serif;">.+</span>', html[x+3]) # Three lines below the <tr> tag is the location text
				if text is not None:
					self.locationText.append(self.cleanText(text))

		# Creates a dictionary out of the cleaned up lists w title as key and text as value
		# It is wrapped within another list for API purposes
		self.info = { 'qualities':dict(zip(self.locations[1:], self.locationText[3:])) }


if __name__ == '__main__':
	WaterQuality().start()