import json
from os import path
from urllib.parse import urlparse


from crawler.swiftea_bot.data import DIR_LINKS, FILE_LINKS


LINK_FILE_MAX_SIZE = 50000

def get_already_done(domain, level):
	domains = get_domains()
	done = False
	for key, d in enumerate(domains):
		if (d['domain'] == domain
			and d['level'] == level
			and d['completed']):
			done = True
	return done

def filter_links(links, crawl_option):
	if crawl_option['domain'] == '':
		return links, []

	domain_links = []
	next_level_links = []

	for link in links:
		if crawl_option['sub-domain']:
			if crawl_option['domain'] in urlparse(link).netloc:
				domain_links.append(link)
			else:
				next_level_links.append(link)
		else:
			if crawl_option['domain'] == urlparse(link).netloc:
				domain_links.append(link)
			else:
				next_level_links.append(link)

	return domain_links, next_level_links

def get_filename(domains, crawl_option, LINK_FILE_MAX_SIZE=50000):
	"""
	level_filename_ptr: 11,
	domains:
	[
		{'domain': 'idesys.org', 'level': 5, 'completed': 0}
	]
	"""
	save = False  # if we need to save the json file at the end
	max_ptr = len(domains)
	level_filename_ptr = -1;  # returned result
	next_level_filename_ptr = -1;
	domain_ptr = -1;  # related to the given domain
	no_domain_ptr = -1;  # the max no domain file

	for key, d in enumerate(domains):
		if (d['domain'] == crawl_option['domain']
			and d['level'] == crawl_option['level']
			and not d['completed']):
			domain_ptr = key
		if (d['domain'] == crawl_option['domain']
			and d['level'] == (crawl_option['level'] + 1)
			and not d['completed']):
			next_level_filename_ptr = key
		if d['domain'] == '' or d['level'] == -1:
			no_domain_ptr = key

	if crawl_option['domain'] == '' or crawl_option['level'] == -1:
		# this is a no domain crawl
		filename = DIR_LINKS + str(domain_ptr)
		level_filename_ptr = no_domain_ptr
		no_domain_ptr = -1
		if path.exists(filename):
			if path.getsize(filename) > LINK_FILE_MAX_SIZE:
				domains.append({
					'domain': '',
					'level': -1,
					'completed': 0,
					'file': max_ptr,
					'line': 1
				})
				level_filename_ptr = max_ptr
				no_domain_ptr = -1
				save = True
		if domain_ptr == -1:
			# not found
			domains.append({
				'domain': '',
				'level': -1,
				'completed': 0,
				'file': max_ptr,
				'line': 1
			})
			level_filename_ptr = 0
			save = True
		next_level_filename_ptr = no_domain_ptr
	else:
		# this is a domain crawl
		if domain_ptr == -1:
			# domain not found
			domain_info = {
				'domain': crawl_option['domain'],
				'level': crawl_option['level'],
				'completed': 0,
				'file': max_ptr,
				'line': 1
			}
			domains.append(domain_info)
			level_filename_ptr = max_ptr
			max_ptr += 1
			save = True
		else:
			level_filename_ptr = domain_ptr

		if next_level_filename_ptr == -1:
			domains.append({
				'domain': crawl_option['domain'],
				'level': crawl_option['level'] + 1,
				'completed': 0,
				'file': max_ptr,
				'line': 1
			})
			next_level_filename_ptr = max_ptr
			save = True

	return level_filename_ptr, save, domains, next_level_filename_ptr

def get_filename_read(domains, crawl_option):
	domain_ptr = -1;  # related to the given domain
	no_domain_ptr = -1;  # the max no domain file

	for key, d in enumerate(domains):
		if (d['domain'] == crawl_option['domain']
			and d['level'] == crawl_option['level']):
			domain_ptr = key
		if (d['domain'] == '' or d['level'] == -1) and no_domain_ptr == -1:
			# modify no_domain_ptr once
			no_domain_ptr = key

	if crawl_option['domain'] == '' or crawl_option['level'] == -1:
		domain_ptr = no_domain_ptr if no_domain_ptr != -1 else 0

	reading_line_number = domains[domain_ptr]['line']
	domains[domain_ptr]['line'] += 1
	save_domains(domains)

	return domain_ptr, reading_line_number

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

def get_domains():
	if path.exists(FILE_LINKS):
		with open(FILE_LINKS) as json_file:
			domains = json.load(json_file)
	else:
		domains = []
	return domains

def save_domains(domains):
	with open(FILE_LINKS, 'w') as json_file:
		json.dump(domains, json_file, indent=2)

def add_domain(domain):
	domains = get_domains()
	exists = False
	for key, d in enumerate(domains):
		if d['domain'] == domain:
			exists = True

	if not exists:
		domains.append({
			'domain': domain,
			'level': 0,
			'completed': 0,
			'line': 1
		})
		save_domains(domains)


def save_links(links, crawl_option, LINK_FILE_MAX_SIZE=2):
	domains = get_domains()
	# read link files index

	level_filename_ptr, save, domains, next_level_filename_ptr = get_filename(
		domains, crawl_option, LINK_FILE_MAX_SIZE)

	domain_links, next_level_links = filter_links(links, crawl_option)
	store_link(domain_links, level_filename_ptr)
	if crawl_option['domain'] != '':
		store_link(next_level_links, next_level_filename_ptr)

	if save:
		save_domains(domains)

	return domains
