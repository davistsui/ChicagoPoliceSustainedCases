from lxml import html
import requests

years = ['2010', '2011', '2012', '2013', '2014', '2015']


def read_page():

	website = 'http://iprachicago.org/sustained_cases_' + '2011' + '.html'
	page = requests.get(website)
	# tree containes the whole HTML file in a nice tree structure
	tree = html.fromstring(page.content)
	# use xpath to parse through the tree
	monthly_pdfs = tree.xpath('//div[]')

