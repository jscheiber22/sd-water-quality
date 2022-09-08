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



	# Curl the site and decipher the pulled table
	def start(self):
		html = self.grabLines(False)

		# Gathers list of location titles
		locations = []
		for x in range(0, len(html)):
			if '<tr' in html[x]:
				loc = re.search('sans-serif;">.+</span>', html[x+2])
				if loc is not None:
					# <strong> tag is used for column title, ie "Beach" which is not wanted
					if '<strong>' not in loc.group():
						loc = loc.group().replace('sans-serif;">', '').replace('</span>', '')
						locations.append(loc)

		# Gathers the text associated with each location
		locationText = []
		for x in range(0, len(html)):
			if '<tr' in html[x]:
				loc = re.search('sans-serif;">.+</span>', html[x+3])
				if loc is not None:
					# <strong> tag is used for column title, ie "Beach" which is not wanted
					if '<strong>' not in loc.group():
						loc = loc.group().replace('sans-serif;">', '').replace('</span>', '')
						locationText.append(loc)

		for location in locationText:
			print(location + '\n')


if __name__ == '__main__':
	WaterQuality().start()