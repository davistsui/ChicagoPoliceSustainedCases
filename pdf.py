from PyPDF2 import PdfFileReader
from os import listdir

# intentionally left out 2015 because it doesn't have all the months
years = ['2008', '2009', '2010', '2011', '2012', '2013', '2014']
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
months_2015 = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep']

# reads in the pdf file and returns the pdf 'pages' object
def read_pdf(pdf_filename):
	pdf = PdfFileReader(pdf_filename, 'r')
	pages = pdf.pages
	return pages

def get_log_id(log):
	# log could start with: 'No. 1009073......'
	# or '311248...'
	l = list(log)

	if l[0] == 'N' or l[1] == 'N':
		log = log.replace('No. ', '')
		log = log.replace('No.', '')
		log = log.replace('NO.', '')
		log_id = log.split(' ')[0]
	else:
		log_id = log.strip(' ').split(' ')[0]

	print log_id
	return log_id

# builds the dict for the specified year, month and the corresponding pages
def extract_text(pages, year, month, d):
	d[year][month] = {}
	# text is the total text file for all the page texts
	text = ''
	for page in pages:
		# each page is just one text
		page_text = page.extractText().encode('utf-8')
		page_text = page_text.replace('\n', '')

		# combine all the texts on each page first
		text += page_text + ' '

	logs = text.split('C.R. ')

	# remove the first element because it is just the header of the pdf file
	# each of the rest of the elements is an individual log
	del logs[0]

	for log in logs:
		# getting the log_id is tricky heade
		log_id = get_log_id(log)
		d[year][month][log_id] = log

def build_d():
	d = {}

	y = ['2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']

	# iterate through each year folder now
	for year in y:
		d[year] = {}
		year_total_pdf = listdir('data/' + year)
		for month_pdf in year_total_pdf:
			if month_pdf == '.DS_Store':
				continue
			else:
				month = month_pdf.split('.')[0]
				PATH_TO_PDF = 'data/' + year + '/' + month_pdf
				pages = read_pdf(PATH_TO_PDF)
				extract_text(pages, year, month, d)

	return d

def write_output_file(d):
	# write the output file now
	# 'a' opens the file for appending
	f = open('output.txt', 'a')

	for year in years:
		s = '\n************************************************************\n'
		f.write(s)
		s = '************************************************************\n'
		f.write(s)
		s = '************************    ' + year + '    ************************\n'
		f.write(s)
		s = '************************************************************\n'
		f.write(s)
		s = '************************************************************\n\n'
		f.write(s)

		for month in months:
			s = '--------------------------  ' + month + '  --------------------------' + '\n\n'
			f.write(s)
			for log_id in d[year][month]:
				s = 'Log_ID: ' + log_id + '\n'
				f.write(s)
				s = '--SUSTAIN--\n'
				f.write(s)
				log = d[year][month][log_id]
				sentences = log.split('.')
				for sentence in sentences:
					if 'SUSTAIN' in sentence:
						s = sentence + '\n\n'
						f.write(s)

				# take care of mediation now
				s = '--mediation--\n'
				f.write(s)
				for sentence in sentences:
					if 'mediation' in sentence:
						s = sentence + '\n\n'
						f.write(s)
				f.write('\n')


	# take care of the year 2015 year
	year = '2015'
	s = '\n************************************************************\n'
	f.write(s)
	s = '************************************************************\n'
	f.write(s)
	s = '************************    ' + year + '    ************************\n'
	f.write(s)
	s = '************************************************************\n'
	f.write(s)
	s = '************************************************************\n\n'
	f.write(s)

	for month in months_2015:
		s = '--------------------------  ' + month + '  --------------------------' + '\n\n'
		f.write(s)
		for log_id in d[year][month]:
			s = 'Log_ID: ' + log_id + '\n'
			f.write(s)
			s = '--SUSTAIN--\n'
			f.write(s)
			log = d[year][month][log_id]
			sentences = log.split('.')
			for sentence in sentences:
				if 'SUSTAIN' in sentence:
					s = sentence + '\n\n'
					f.write(s)

			# take care of mediation now
			s = '--mediation--\n'
			f.write(s)
			for sentence in sentences:
				if 'mediation' in sentence:
					s = sentence + '\n\n'
					f.write(s)
			f.write('\n')

	f.close()

def calc_mediation_perc(d):
	sustain = 0
	mediation = 0

	for year in d.keys():
		for month in d[year].keys():
			for log_id in d[year][month]:
				log = d[year][month][log_id]
				sustain += 1
				if 'mediation' in log:
					mediation +=1

	print 'mediation: ' + str(mediation) + '\n'
	print 'sustain: ' + str(sustain) + '\n'




if __name__ == '__main__':
	d = build_d()
	write_output_file(d)
	calc_mediation_perc(d)










