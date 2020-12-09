#!/usr/bin/env python3

import sqlite3
import os.path
import os
import re
import hashlib

with sqlite3.Connection('wikileaks.db') as db:
	try:
		cur = db.cursor()
		
		##
		# Add the original_name field
		##

		# for r in cur.execute('SELECT * FROM podesta_emails').fetchall():
		# 	cur.execute('INSERT INTO podesta_emails2(id, path, url, original_name, size, md5, sha1, sha256) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (
		# 		r[0], # id
		# 		r[1], # path
		# 		r[2], # url
		# 		os.path.basename(r[1]), # original_name
		# 		r[3], # size
		# 		r[4], # md5
		# 		r[5], # sha1
		# 		r[6]  # sha256
		# 	))

		##
		# Fix the podesta paths
		##

		# for r in cur.execute('SELECT id, original_name FROM podesta_emails').fetchall():
		# 	cur.execute('UPDATE podesta_emails SET path = ? WHERE id = ?', (
		# 		'podesta-emails/{0:0>5}_{1}'.format(r[0], r[1]),
		# 		r[0]
		# 	))


		##
		# Read a dnc/ folder produced by WikileaksEmailDownloader.py
		##

		# pattern = re.compile(r'^(\d{5})_(.+)$')
		# for f in os.listdir('dnc/'):
		# 	m = pattern.match(f)
		# 	id, name = m.groups()
		# 	id = int(id)
		# 	url = f'https://wikileaks.org/dnc-emails/get/{id}'
		# 	size = os.path.getsize(f'dnc/{f}')
		# 	path = f'dnc-emails/{f}'

		# 	with open(f'dnc/{f}', 'rb') as f:
		# 		data = f.read()
		# 		md5sum = hashlib.md5(data).hexdigest()
		# 		sha1sum = hashlib.sha1(data).hexdigest()
		# 		sha256sum = hashlib.sha256(data).hexdigest()

		# 	cur.execute('INSERT INTO dnc_emails(id, path, url, original_name, size, md5, sha1, sha256) VALUES(?, ?, ?, ?, ?, ?, ?, ?)', (
		# 		id, path, url, name, size, md5sum, sha1sum, sha256sum
		# 	))
		db.commit()

	finally:
		cur.close()