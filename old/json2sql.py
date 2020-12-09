#!/usr/bin/env python3

import json
import sqlite3
import urllib.parse

with open('clintonurls.json', 'r') as f:
	urls = json.load(f)

with sqlite3.Connection('wikileaks.db') as db:
	cur = db.cursor()
	try:
		cur.execute('DELETE FROM clinton_emails')

		for id, url in urls.items():
			cur.execute('INSERT into clinton_emails(id, path, url) VALUES (?, ?, ?)', (
				id, urllib.parse.urlparse(url).path.lstrip('/'), url
			))
	finally:
		cur.close()

	

	db.commit()