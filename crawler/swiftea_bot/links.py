import json
from os import path
from urllib.parse import urlparse


from swiftea_bot.data import DIR_LINKS, FILE_LINKS

LINK_FILE_MAX_SIZE = 50000

def get_level(domaine=''):
	if domaine == '':
		return -1
	domaines = get_domaines()

	domaine_info = {}
	for key, d in enumerate(domaines):
		if d['domaine'] == domaine:
			domaine_info = d

	if domaine_info == {}:
		return 0
	return domaine_info['level']

def filter_links(links, crawl_option):
	if crawl_option['domaine'] == '':
		return links

	domaine_links = []
	next_level_links = []

	for link in links:
		if crawl_option['sub-domaine']:
			if crawl_option['domaine'] in urlparse(link).netloc:
				domaine_links.append(link)
			else:
				next_level_links.append(link)
		else:
			if crawl_option['domaine'] == urlparse(link).netloc:
				domaine_links.append(link)
			else:
				next_level_links.append(link)

	return domaine_links, next_level_links

def get_filename(domaines, crawl_option, LINK_FILE_MAX_SIZE=50000):
	"""
	level_filename_ptr: 11,
	domaines:
	[
		{'domaine': 'idesys.org', 'level': 5, 'completed': 0}
	]
	"""
	save = False  # if we need to save the json file at the end
	max_ptr = len(domaines)
	level_filename_ptr = -1;  # returned result
	next_level_filename_ptr = -1;
	domaine_ptr = -1;  # related to the given domaine
	no_domaine_ptr = -1;  # the max no domaine file

	for key, d in enumerate(domaines):
		if (d['domaine'] == crawl_option['domaine']
			and d['level'] == crawl_option['level']
			and not d['completed']):
			domaine_ptr = key
		if (d['domaine'] == crawl_option['domaine']
			and d['level'] == (crawl_option['level'] + 1)
			and not d['completed']):
			next_level_filename_ptr = key
		if d['domaine'] == '' or d['level'] == -1:
			no_domaine_ptr = key

	if crawl_option['domaine'] == '' or crawl_option['level'] == -1:
		# this is a no domaine crawl
		filename = DIR_LINKS + str(domaine_ptr)
		level_filename_ptr = no_domaine_ptr
		no_domaine_ptr = -1
		if path.exists(filename):
			if path.getsize(filename) > LINK_FILE_MAX_SIZE:
				domaines.append({'domaine': '', 'level': -1, 'completed': 0})
				level_filename_ptr = max_ptr
				no_domaine_ptr = -1
				save = True
		if domaine_ptr == -1:
			# not found
			domaines.append({'domaine': '', 'level': -1, 'completed': 0})
			level_filename_ptr = 0
			save = True
		next_level_filename_ptr = no_domaine_ptr
	else:
		# this is a domaine crawl
		if domaine_ptr == -1:
			# domaine not found
			domaine_info = {
				'domaine': crawl_option['domaine'],
				'level': crawl_option['level'],
				'completed': 0
			}
			domaines.append(domaine_info)
			level_filename_ptr = max_ptr
			max_ptr += 1
			save = True
		else:
			level_filename_ptr = domaine_ptr

		if no_domaine_ptr == -1 and False:  # TODO: if target almost reach,
			domaines.append({'domaine': '', 'level': -1, 'completed': 0})
			next_level_filename_ptr = max_ptr
			save = True
		elif next_level_filename_ptr == -1:
			domaines.append({
				'domaine': crawl_option['domaine'],
				'level': crawl_option['level'] + 1,
				'completed': 0
			})
			next_level_filename_ptr = max_ptr
			save = True

	return level_filename_ptr, save, domaines, next_level_filename_ptr

def get_filename_read(domaines, crawl_option):
	save = False  # if we need to save the json file at the end
	max_ptr = len(domaines)
	level_filename_ptr = -1;  # returned result
	next_level_filename_ptr = -1;
	domaine_ptr = -1;  # related to the given domaine
	no_domaine_ptr = -1;  # the max no domaine file

	for key, d in enumerate(domaines):
		if (d['domaine'] == crawl_option['domaine']
			and d['level'] == crawl_option['level']):
			domaine_ptr = key
		if (d['domaine'] == crawl_option['domaine']
			and d['level'] == (crawl_option['level'] + 1)):
			next_level_filename_ptr = key
		if d['domaine'] == '' or d['level'] == -1:
			no_domaine_ptr = key

	if crawl_option['domaine'] == '' or crawl_option['level'] == -1:
		return no_domaine_ptr
	else:
		return domaine_ptr

def store_link(links, level_filename_ptr):
	filename = DIR_LINKS + str(level_filename_ptr)
	if path.exists(filename):
		with open(filename, 'r', errors='replace', encoding='utf8') as myfile:
			list_links = myfile.read().splitlines()  # List of urls
		for link in links:
			if link not in list_links:
				list_links.append(link)
	else:
		list_links = links
	with open(filename, 'w', errors='replace', encoding='utf8') as myfile:
		myfile.write('\n'.join(list_links) + '\n')

def get_domaines():
	if path.exists(FILE_LINKS):
		with open(FILE_LINKS) as json_file:
			domaines = json.load(json_file)
	else:
		domaines = []
	return domaines

def save_domaines(domaines):
	with open(FILE_LINKS, 'w') as json_file:
		json.dump(domaines, json_file, indent=2)

def add_domaine(domaine):
	domaines = get_domaines()
	exists = False
	for key, d in enumerate(domaines):
		if d['domaine'] == domaine:
			exists = True

	if not exists:
		with open(FILE_LINKS, 'w') as link_file:
			json.dump([{
				'domaine': domaine,
				'level': 0,
				'completed': 0
			}], link_file)


def save_links(links, crawl_option, LINK_FILE_MAX_SIZE=2):
	# read link files index
	domaines = get_domaines()

	level_filename_ptr, save, domaines, next_level_filename_ptr = get_filename(
		domaines, crawl_option, LINK_FILE_MAX_SIZE)

	domaine_links, next_level_links = filter_links(links, crawl_option)
	store_link(domaine_links, level_filename_ptr)
	if crawl_option['domaine'] != '':
		store_link(next_level_links, next_level_filename_ptr)

	if save:
		save_domaines(domaines)

	return domaines
