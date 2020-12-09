#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0

##
# Scrape the actual PDF url from
# https://wikileaks.org/clinton-emails/emailid/{id}
#
# Stored results in clintonurls.json. This is idempotent, just
# restart it if it fails.
#
# At the end, it will spit out an aria2 input file to download
# everything.
##

import os.path
import urllib.parse
import json
import concurrent.futures
import traceback
import threading
import time
import wikileaks
import shlex
import sqlite3
from typing import Optional

db = sqlite3.Connection('wikileaks.db', check_same_thread=False)

done = False
mutex = threading.Lock()


class Shit(object):
	def get_info(self, id: int) -> Optional[wikileaks.HeadInfo]:
		pass

	def insert(self, info: wikileaks.HeadInfo, cur: sqlite3.Cursor):
		pass


class DNC(Shit):
	def get_info(self, id: int) -> Optional[wikileaks.HeadInfo]:
		return wikileaks.head_dnc_eml(id)


	def insert(self, info: wikileaks.HeadInfo, cur: sqlite3.Cursor):
		cur.execute('INSERT INTO dnc_emails(id, path, url, original_name, size) VALUES (?, ?, ?, ?, ?)', (
			info.id,
			'dnc-emails/{0:0>5}_{1}'.format(info.id, info.name),
			info.url,
			info.name,
			info.size
		))


class Podesta(Shit):
	def get_info(self, id: int) -> Optional[wikileaks.HeadInfo]:
		return wikileaks.head_podesta_eml(id)


	def insert(self, info: wikileaks.HeadInfo, cur: sqlite3.Cursor):
		cur.execute('INSERT INTO podesta_emails(id, path, url, original_name, size) VALUES (?, ?, ?, ?, ?)', (
			info.id,
			'podesta-emails/{0:0>5}_{1}'.format(info.id, info.name),
			info.url,
			info.name,
			info.size
		))


class Clinton(Shit):
	def get_info(self, id: int) -> Optional[wikileaks.HeadInfo]:
		url = wikileaks.get_clinton_pdf_url(id)
		return wikileaks.HeadInfo(id, urllib.parse.urlparse(url).path.lstrip('/'), url, size=None)


	def insert(self, info: wikileaks.HeadInfo, cur: sqlite3.Cursor):
		cur.execute('INSERT INTO clinton_emails(id, path, url, size) VALUES (?, ?, ?, ?)', info)


def get_url_proc(id: int, shit: Shit, pool: concurrent.futures.Executor):
	while True:
		try:
			info = shit.get_info(id)
			print(f'{id}: {info}')
			break
		except urllib.error.HTTPError as e:
			print(f'{id}: Caught exception {e}, retrying')
			#pool.submit(get_url_proc, id, pool)
			#return
		except:
			traceback.print_exc()
			return

	mutex.acquire()
	try:
		cur = db.cursor()
		shit.insert(info, cur)
	except:
		traceback.print_exc()
		return
	finally:
		cur.close()
		mutex.release()


needed_podesta = set()
needed_dnc = set()
needed_clinton = set()
cur = db.cursor()
try:
	for i in range(1, wikileaks.COUNT_PODESTA + 1):
		if not cur.execute('SELECT id FROM podesta_emails WHERE id = ?', (i,)).fetchone():
			needed_podesta.add(i)

	for i in range(1, wikileaks.COUNT_DNC + 1):
		if not cur.execute('SELECT id FROM dnc_emails WHERE id = ?', (i,)).fetchone():
			needed_dnc.add(i)

	for i in range(1, wikileaks.COUNT_CLINTON + 1):
		if not cur.execute('SELECT id FROM clinton_emails WHERE id = ?', (i,)).fetchone():
			needed_clinton.add(i)
finally:
	cur.close()


def checkpoint():
	while not done:
		time.sleep(10)
		print('~10 seconds passed, checkpointing')
		mutex.acquire()
		try:
			db.commit()
		finally:
			mutex.release()

cpthread = threading.Thread(target=checkpoint, daemon=False)
cpthread.start()


pshit = Podesta()
dshit = DNC()
cshit = Clinton()

with concurrent.futures.ThreadPoolExecutor(max_workers=50) as pool:
	for i in needed_podesta:
		pool.submit(get_url_proc, i, pshit, pool)

	for i in needed_dnc:
		pool.submit(get_url_proc, i, dshit, pool)

	for i in needed_clinton:
		pool.submit(get_url_proc, i, cshit, pool)

done = True
cpthread.join()
db.close()
