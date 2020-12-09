#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0

import sys
import urllib.request
import urllib.parse
import cgi
from collections import namedtuple
from typing import Optional, Tuple

COUNT_DNC = 44053
COUNT_PODESTA = 59028
COUNT_CLINTON = 33727

#USER_AGENT = 'Mozilla/5.0'
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0'


HeadInfo = namedtuple('HeadInfo', ['id', 'name', 'url', 'size'])


def get_clinton_pdf_url(id: int) -> Optional[str]:
	import bs4

	req = urllib.request.Request(
		url=f'https://wikileaks.org/clinton-emails/emailid/{id}',
		headers={'User-Agent': USER_AGENT}
	)

	with urllib.request.urlopen(req) as x:
		html = bs4.BeautifulSoup(x.read().decode('utf-8'), 'html5lib')

	sourcediv = html.find('div', id='source')
	if not sourcediv:
		print(f'{id}: missing source <div>', file=sys.stderr)
		return None

	sourcea = sourcediv.find('a')
	if not sourcea:
		print(f'{id}: missing source <a>', file=sys.stderr)
		return None

	url = sourcea.get('href')
	if not url:
		print(f'{id}: <a> missing href', file=sys.stderr)
		return None

	return urllib.parse.urljoin('https://wikileaks.org/', url)


##
# $ curl --head https://wikileaks.org/clinton-emails/Clinton_Email_August_Release/C05777221.pdf
# HTTP/1.1 200 OK
# Server: nginx
# Date: Tue, 08 Dec 2020 06:34:29 GMT
# Content-Type: application/pdf
# Content-Length: 48833
# Connection: keep-alive
# Last-Modified: Wed, 02 Mar 2016 23:20:46 GMT
# X-Content-Type-Options: nosniff
# X-Cache: 0
# X-Content-Type-Options: nosniff
# X-XSS-PROTECTION: 1; mode=block
# Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
##
# def get_clinton_pdf(url):
# 	req = urllib.request.Request(
# 		url=url,
# 		headers={'User-Agent': USER_AGENT}
# 	)
#
# 	with urllib.request.urlopen(req) as x:
# 		ct = x.getheader('Content-Type')
# 		if ct is None:
# 			print(f'{}')

def get_clinton_pdf(id: int) -> Optional[Tuple[bytes, str]]:
	url = get_clinton_pdf_url(id)

	req = urllib.request.Request(
		url=url,
		headers={'User-Agent': USER_AGENT}
	)

	with urllib.request.urlopen(req) as x:
		ct = x.getheader('Content-Type')
		if ct is None:
			print(f'{id}: Missing Content-Type header', file=sys.stderr)
			return None

		if 'application/pdf' != ct.tolower():
			print(f'{id}: Content-Type is not application/pdf', file=sys.stderr)
			return None

		cl = x.getheader('Content-Length')
		if cl is None:
			print(f'{id}: Missing Content-Length header', file=sys.stderr)
			return None

		cl = int(cl)

	return None


def _head_eml(id: int, urltag: str, logprefix: str) -> Optional[HeadInfo]:
	url=f'https://wikileaks.org/{urltag}/get/{id}'

	req = urllib.request.Request(
		url=url,
		headers={'User-Agent': USER_AGENT},
		method='HEAD'
	)

	with urllib.request.urlopen(req) as x:
		cd = x.getheader('Content-Disposition')
		if cd is None:
			print(f'{logprefix} {id}: Missing Content-Disposition header', file=sys.stderr)
			return None

		value, params = cgi.parse_header(cd)
		if 'filename' not in params:
			print(f'{logprefix} {id}: No filename field in Content-Disposition')
			return None

		size = x.getheader('Contnet-Length')
		if size:
			size = int(size)

		return HeadInfo(id, params["filename"], url, size)


def _get_eml(id: int, urltag: str, logprefix: str) -> Optional[Tuple[bytes, HeadInfo]]:
	url=f'https://wikileaks.org/{urltag}/get/{id}'
	req = urllib.request.Request(
		url=url,
		headers={'User-Agent': USER_AGENT}
	)

	with urllib.request.urlopen(req) as x:
		cd = x.getheader('Content-Disposition')
		if cd is None:
			print(f'{logprefix} {id}: Missing Content-Disposition header', file=sys.stderr)
			return None

		value, params = cgi.parse_header(cd)
		if 'filename' not in params:
			print(f'{logprefix} {id}: No filename field in Content-Disposition')
			return None

		return (x.read(), HeadInfo(id, params["filename"], url))


def get_dnc_eml(id: int) -> Optional[Tuple[bytes, HeadInfo]]:
	return _get_eml(id, 'dnc-emails', 'DNC')


def get_podesta_eml(id: int) -> Optional[Tuple[bytes, HeadInfo]]:
	return _get_eml(id, 'podesta-emails', 'Podesta')


def head_dnc_eml(id: int) -> Optional[HeadInfo]:
	return _head_eml(id, 'dnc-emails', 'DNC')


def head_podesta_eml(id: int) -> Optional[HeadInfo]:
	return _head_eml(id, 'podesta-emails', 'Podesta')
