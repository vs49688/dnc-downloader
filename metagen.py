#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0

import sys
import sqlite3
from xml.etree.ElementTree import ElementTree, Element, SubElement, tostring

if len(sys.argv) != 2:
	print(f'Usage: {sys.argv[0]} <dnc|podesta|clinton>')
	exit(2)

if sys.argv[1] not in ['dnc', 'podesta', 'clinton']:
	print(f'Usage: {sys.argv[0]} <dnc|podesta|clinton>')
	exit(2)

table_name = f'{sys.argv[1]}_emails'

# https://tools.ietf.org/id/draft-bryan-metalink-28.html
metalink = Element('metalink')
metalink.set('xmlns', 'urn:ietf:params:xml:ns:metalink')
with sqlite3.Connection('wikileaks.db') as db:
	for id, url, path, size, md5, sha1, sha256 in db.execute(f'SELECT id, url, path, size, md5, sha1, sha256 FROM {table_name}'):
		file = SubElement(metalink, 'file')
		file.set('name', path)

		SubElement(file, 'url').text = url
		if size:
			SubElement(file, 'size').text = str(size)

		# https://www.iana.org/assignments/hash-function-text-names/hash-function-text-names.xml
		if md5:
			h = SubElement(file, 'hash')
			h.set('type', 'md5')
			h.text = md5

		if sha1:
			h = SubElement(file, 'hash')
			h.set('type', 'sha-1')
			h.text = sha1

		if sha256:
			h = SubElement(file, 'hash')
			h.set('type', 'sha-256')
			h.text = sha256

from xml.dom import minidom


print(minidom.parseString(tostring(metalink, encoding='UTF-8', xml_declaration=True)).toprettyxml(), end='')
#ElementTree(metalink).write(sys.stdout.buffer, encoding='UTF-8', xml_declaration=True)
exit(0)