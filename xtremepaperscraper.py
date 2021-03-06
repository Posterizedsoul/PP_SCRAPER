from bs4 import BeautifulSoup
import multiprocessing
from functools import partial
import time
import requests
import urllib
import os

''' define global variables'''

url_list = {

	'9231': 'http://papers.xtremepapers.com/CIE/Cambridge International A and AS Level/Mathematics - Further (9231)/',
	'9608': 'http://papers.xtremepapers.com/CIE/Cambridge International A and AS Level/Computer Science (9608)/',
	'9691': 'http://papers.xtremepapers.com/CIE/Cambridge International A and AS Level/Computing (9691)/',
	'9698': 'http://papers.xtremepapers.com/CIE/Cambridge International A and AS Level/Psychology (9698)/',
	'9700': 'http://papers.xtremepapers.com/CIE/Cambridge International A and AS Level/Biology (9700)/',
	'9701': 'http://papers.xtremepapers.com/CIE/Cambridge International A and AS Level/Chemistry (9701)/',
	'9702': 'https://papers.xtremepape.rs/CAIE/AS%20and%20A%20Level/Physics%20(9702)/',
	'9706': 'http://papers.xtremepapers.com/CIE/Cambridge International A and AS Level/Accounting (9706)/',
	'9707': 'http://papers.xtremepapers.com/CIE/Cambridge International A and AS Level/Business Studies (9707)/',
	'9708': 'http://papers.xtremepapers.com/CIE/Cambridge International A and AS Level/Economics (9708)/',
	'9709': 'http://papers.xtremepapers.com/CIE/Cambridge International A and AS Level/Mathematics (9709)/'
}


online_url = 'https://papers.xtremepapers.com/CIE/Cambridge International A and AS Level/'

url_online = {}


def down_paper(href, folder_p):
	''' given url, download the pdf at that url '''

	time.sleep(0.5)  # please do not delete this
	filename = href.split('/')[-1]
	# print(href,filename,sep='-----') # test only

	# if the file already exists
	try:
		with open(folder_p+filename, 'r') as code:
			print('file already exists {}'.format(filename))
			return 1
	# otherwise creating new file
	except FileNotFoundError:
		print('detected new file.', end=' ')
		try:
			# try to open new file
			with open(folder_p+filename, 'wb') as code:
				r = requests.get(href)
				code.write(r.content)
				print('successfully downloaded {}'.format(filename))
				return 0
		# if cannot open/download
		except Exception:
			print(
				'lost connections to the file {} or cannot i/o in the directory provided.'.format(filename))
			return -1


def get_code():
	''' get the syllabus code for every subject on xtremepaper'''

	html = requests.get(online_url)
	soup = BeautifulSoup(html.text, 'lxml')
	datas = soup.select('td.autoindex_td > a ')
	if datas != []:
		# get rid of parent dir
		datas.pop(0)
		#
		for data in datas:
			# multi = 0
			href_code = data.get('href')
			code = str(data.get_text().split('(')[-1].strip(')'))
			if not code.isdigit():
				# multi = 1
				url_online[code[:4]
						   ] = 'http://papers.xtremepapers.com' + href_code
				url_online[code[-4:]
						   ] = 'http://papers.xtremepapers.com' + href_code
			else:
				url_online[code] = 'http://papers.xtremepapers.com' + href_code

		# print(url_online)
	else:
		print('NetWork error')
		return -1


def get_papers(url):
	'''download all the files at the url provided'''
	new_hrefs = []
	# obatin url
	html = requests.get(url)
	soup = BeautifulSoup(html.text, 'lxml')
	hrefs = soup.select('td.autoindex_td > a')

	if hrefs == []:
		print('wrong url provided')
		return -1
	hrefs.pop(0)
	print('Now starts to download, this may (defintely) take some times so you may want to go and grab yourself some drink and let this programe run alone.')

	# create folder
	folder_path = '.\\'+url.split('/')[-2]+'\\'

	print(folder_path)

	if os.path.isdir(folder_path):
		print('folder {} already exists'.format(folder_path))
		pass
	else:
		print('creating new folder {}'.format(folder_path))
		os.mkdir(folder_path)

	for href in hrefs:
		href = 'http://papers.xtremepapers.com/'+href.get('href').strip('/.')
		new_hrefs.append(href)
	# print(new_hrefs)

	# dowload file
	with multiprocessing.Pool() as pool:
		results = pool.map(
			partial(down_paper, folder_p=folder_path), new_hrefs)

	print('1 - already downloaded, -1 - cannot download, 0 - successfully download.')

	print(results)

	print('successfully downloaded all the files available at {}'.format(url))
	return 0


def main():
	''' handles input and outputs '''

	# get code
	print('please provide the syllabus number of the papers you wants to download:', end='')
	url_key = input()

	# local code
	if url_key in url_list:

		print('detected syllabus code, processing...')
		get_papers(url_list[url_key])

	# online code
	elif url_key.isdigit():
		print('syllabus code did not match local database, do you wish to get online database for syllabus code?')

		ans = input()
		if ans == 'y' or ans == 'yes':
			# seraching online
			print('Searching at online data base at {}'.format(online_url))
			get_code()
			if url_key in url_online:
				print('detected syllabus code, processing...')
				get_papers(url_online[url_key])
			else:
				print('invalid syllabus code.')
		else:
			print('invalid syllabus code.')
	# provide url
	elif url_key.startswith('http://') or url_key.startswith('https://'):

		print('url detected')
		print('downloading form the website {}'.format(url_key))
		get_papers(url_key)

	else:
		print('invalid input please check your syllabus code / start your url with http')

if __name__ == '__main__':
	main()
