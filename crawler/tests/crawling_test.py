#!/usr/bin/env python3


import requests as req
from reppy.cache import RobotsCache


from crawler.swiftea_bot.data import HEADERS
from crawler.crawling import data_processing
from crawler.crawling import searches
from crawler.crawling.web_connection import WebConnection
from crawler.crawling.site_informations import SiteInformations
from crawler.crawling import parsers
import crawler.tests.test_data as test_data


class CrawlingBaseTest(object):
	"""Base class for all crawler test classes."""
	def setup_method(self, _):
		"""Configure the app."""
		self.url = "http://aetfiws.ovh"
		self.code1 = test_data.CODE1
		self.code2 = test_data.CODE2
		self.code3 = test_data.CODE3
		self.parser = parsers.ExtractData()
		self.parser_encoding = parsers.ExtractEncoding()
		self.STOPWORDS = {'fr':('mot', 'pour', 'de')}
		self.BADWORDS = {'fr': ('pipe', 'xxx')}
		self.is_title = True
		self.title = 'letter'
		self.headers = {'status': '200 OK', 'content-type': 'text/html; charset=utf-8', 'vary': 'X-PJAX, Accept-Encoding'}
		self.reqrobots = RobotsCache(capacity=100)


class TestConnection(CrawlingBaseTest):
	def test_check_connection(self):
		assert data_processing.check_connection(self.url) == False
		assert data_processing.check_connection() == True

	def test_is_nofollow(self):
		nofollow, url = data_processing.is_nofollow(self.url + '!nofollow!')
		assert nofollow == True
		assert url == self.url
		nofollow, url = data_processing.is_nofollow(self.url)
		assert nofollow == False
		assert url == self.url

	def test_duplicate_content(self):
		assert data_processing.duplicate_content('un premier code', 'un deuxieme code') == True  # percent >= 65 and percent < 95 and size_code1 <= size_code2
		assert data_processing.duplicate_content('un premier code         ', 'un deuxieme code') == False  # percent >= 65 and percent < 95 and size_code1 <= size_code2
		assert data_processing.duplicate_content('un deuxieme code', 'un premier code') == True  # percent >= 65 and percent < 95 and size_code1 > size_code2
		assert data_processing.duplicate_content('un deuxieme code', 'un premier code         ') == False  # percent >= 65 and percent < 95 and size_code1 > size_code2
		assert data_processing.duplicate_content('le meme code', 'le meme code') == True  # code1 == code2
		t1 = 'le meme code le meme code le meme code le meme code le meme code'
		t2 = 'le meme code le meme code le meme code le meme code le meme code0'
		assert data_processing.duplicate_content(t1, t2) == True  # size_code1 < size_code2
		t3 = 'le meme0 code le meme0 code le meme0 code le meme code le meme0 code'
		t4 = 'le meme code le meme code le meme code le meme code le meme code'
		assert data_processing.duplicate_content(t3, t4) == True  # percent >= 95
		assert data_processing.duplicate_content('un premier code un peu plus grand', 'un deuxieme code') == False  # persont < 65

	def test_all_urls(self):
		request = req.get("https://fr.wikipedia.org")
		assert data_processing.all_urls(request) == ["https://fr.wikipedia.org/wiki/Wikip%C3%A9dia:Accueil_principal", "https://fr.wikipedia.org"]
		request = req.get("https://choosealicense.com/")
		assert data_processing.all_urls(request) == ["https://choosealicense.com"]


class TestWebConnection(CrawlingBaseTest):
	def test_search_encoding(self):
		assert WebConnection.search_encoding(self, {}, self.code3) == ('utf-8', 0)
		assert WebConnection.search_encoding(self, self.headers, self.code3) == ('utf-8', 1)
		assert WebConnection.search_encoding(self, {}, self.code1) == ('utf-8', 1)
		assert WebConnection.search_encoding(self, {}, self.code2) == ('UTF-16 LE', 1)

	def test_check_robots_perm(self):
		assert WebConnection.check_robots_perm(self, 'https://zestedesavoir.com') == True
		assert WebConnection.check_robots_perm(self, 'https://www.facebook.com') == False
		assert WebConnection.check_robots_perm(self, self.url) == False
		assert WebConnection.check_robots_perm(self, 'http://premium.lefigaro.fr') == True

	def test_send_request(self):
		WebConnection.send_request(self, 'https://zestedesavoir.com')
		assert WebConnection.send_request(self, 'https://uneurlbidon.com') == None

	def test_duplicate_content(self):
		request = req.get('https://zestedesavoir.com')
		WebConnection.duplicate_content(self, request, 'https://zestedesavoir.com')


class TestSearches(CrawlingBaseTest):
	def test_clean_text(self):
		text = searches.clean_text('Sample text with non-desired \r whitespaces \t chars \n')
		assert '\n' not in text and '\r' not in text and '\t' not in text

	def test_get_base_url(self):
		assert searches.get_base_url(self.url + '/page1.php') == self.url

	def test_is_homepage(self):
		assert searches.is_homepage('http://www.bfmtv.com') == True
		assert searches.is_homepage('http://www.bfmtv.com/page.html') == False
		assert searches.is_homepage('https://github.com') == True
		assert searches.is_homepage('http://bfmbusiness.bfmtv.com') == False

	def test_capitalize(self):
		assert searches.capitalize('ceci est un Titre') == 'Ceci est un Titre'
		assert searches.capitalize('') == ''

	def test_clean_link(self):
		assert searches.clean_link('http://www.example.fr?w=word#big_title') == 'http://www.example.fr?w=word'

	def test_stats_links(self):
		searches.stats_links(50)


class TestSiteInformations(CrawlingBaseTest):
	def test_set_listswords(self):
		var = SiteInformations()
		var.set_listswords({'en': ['then', 'already']}, {'en': ['verybadword']})
		assert var.STOPWORDS == {'en': ['then', 'already']}
		assert var.BADWORDS == {'en': ['verybadword']}

	def test_get_info(self):
		site_informations = SiteInformations()
		site_informations.set_listswords(stopwords={'en': []}, badwords={'en':[]})
		site_informations.get_infos('http://aetfiws.ovh', test_data.CODE1, True, 0)

	def test_clean_links(self):
		links = ['page.php', 'http://aetfiws.ovh/', 'mailto:test@test.fr',
			'//www.example.fr?w=word', 'http://aetfiws.ovh/page1/index.html',
			'/page1', 'http:/', '://www.sportetstyle.fr']
		links = data_processing.clean_links(links, self.url)
		assert links == ['http://aetfiws.ovh/page.php', self.url,
			'http://www.example.fr?w=word', 'http://aetfiws.ovh/page1',
			'http://www.sportetstyle.fr']

	def test_clean_keywords(self):
		base_keywords = ['le', 'mot', '2015', 'bureau', 'word\'s', 'l\'example', 'l’oiseau',
		'quoi...', '*****', 'epee,...', '2.0', 'o\'clock', '[çochon$¤', '#{[|µ£%]}', '12h|(']
		keywords = SiteInformations.clean_keywords(self, base_keywords, 'fr')
		assert keywords == test_data.CLEANED_KEYWORDS

	def test_sane_search(self):
		assert SiteInformations.sane_search(self, ['car'], 'fr') == False
		assert SiteInformations.sane_search(self, ['cigare', 'pipe', 'cigarette', 'fumer', 'tue', 'santé'], 'fr') == False
		assert SiteInformations.sane_search(self, ['pipe', 'xxx', 'voiture'], 'fr') == True
		assert SiteInformations.sane_search(self, [], 'fr') == False

	def test_detect_language(self):
		keywords = "un texte d'exemple pour tester la fonction".split()
		assert SiteInformations.detect_language(self, keywords) == 'fr'
		keywords = "un texte d'exemple sans stopwords".split()
		assert SiteInformations.detect_language(self, keywords) == ''

	def test_clean_favicon(self):
		favicon = 'http://aetfiws.ovh/icon.ico'
		assert SiteInformations.clean_favicon(self, '/icon.ico', self.url) == favicon
		assert SiteInformations.clean_favicon(self, '//aetfiws.ovh/icon.ico', self.url) == favicon
		assert SiteInformations.clean_favicon(self, 'icon.ico', self.url) == favicon


class TestParsers(CrawlingBaseTest):
	def test_can_append(self):
		assert parsers.can_append('about/ninf.php', 'noindex, nofollow') == None
		assert parsers.can_append('about/ninf.php', 'nofollow') == 'about/ninf.php!nofollow!'
		assert parsers.can_append('about/ninf.php', '') == 'about/ninf.php'
		assert parsers.can_append(None, '') is None

	def test_meta(self):
		language, description = parsers.meta([('name', 'description'), ('content', 'Communauté du Libre partage')])
		assert description == 'Communauté du Libre partage'
		language, description = parsers.meta([('name', 'language'), ('content', 'fr')])
		assert language == 'fr'
		language, description = parsers.meta([('http-equiv', 'content-language'), ('content', 'en')])
		assert language == 'en'

	def test_handle_entityref(self):
		parsers.ExtractData.handle_entityref(self, 'eacute')
		assert self.title == 'letteré'
		parsers.ExtractData.handle_entityref(self, 'agrave')
		assert self.title == 'letteréà'

	def test_parser(self):
		self.parser.feed(self.code1)
		assert self.parser.links == ['demo', 'index', 'about/nf.php!nofollow!']
		assert searches.clean_text(self.parser.first_title) == 'Gros titre🤣'
		keywords = 'une CSS Demo ici! Gros titre🤣 Moyen titre petit titre strong em Why use Swiftea ?1 Why use Swiftea ?2 Why use Swiftea ?3 © >'
		assert searches.clean_text(self.parser.keywords) == keywords
		assert self.parser.css == True
		assert self.parser.description == 'Moteur de recherche'
		assert self.parser.language == 'en'
		assert self.parser.favicon == 'public/favicon.ico'
		assert self.parser.title == 'Swiftea'

		self.parser.feed(self.code2)
		assert self.parser.language == 'en'
		assert self.parser.favicon == 'public/favicon2.ico'

		self.parser.feed(self.code3)
		assert self.parser.language == 'fr'

	def test_parser_encoding(self):
		self.parser_encoding.feed(self.code1)
		assert self.parser_encoding.encoding == 'utf-8'
		self.parser_encoding.feed(self.code2)
		assert self.parser_encoding.encoding == 'UTF-16 LE'
