import subprocess
import re


class WaterQuality:
	def __init__(self):
		self.url = 'https://www.sdcoastkeeper.org/beach-advisories'


	# Disable refresh when referencing a predownloaded site, mostly used for debugging
	def grabLines(self, refresh = True):
		if refresh:
			subprocess.call('curl ' + self.url + ' -o SDBeachAdvisory.html')
		with open('SDBeachAdvisory.html') as f:
			return f.readlines()


	def cleanText(self, text):
		return text.group().replace('sans-serif;">', '').replace('</span>', '').replace('&#8217;', "'")


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
					locations.append(self.cleanText(loc))
				text = re.search('sans-serif;">.+</span>', html[x+3]) # Three lines below the <tr> tag is the location text
				if text is not None:
					locationText.append(self.cleanText(text))

		# Essentially pops first value in list to remove column title
		locations = locations[1:]

		# Essentially pops first value in list to remove column title
		locationText = locationText[3:]


		for x in range(0, len(locationText)):
			print(locations[x])
			print(locationText[x])
			print('\n')


if __name__ == '__main__':
	WaterQuality().start()