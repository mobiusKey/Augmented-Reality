from lxml import html
import requests


page = requests.get('http://sites.psu.edu/easihouse/pointsspreadsheet')
tree = html.fromstring(page.content)

last, first, academic, social, total =tree.xpath('//table/tbody/tr/td/text()')
for x in last:
	print(last + ": " + total)