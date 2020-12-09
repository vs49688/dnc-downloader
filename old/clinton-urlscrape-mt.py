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

try:
	with open('clintonurls.json', 'r') as f:
		urls = json.load(f)
except FileNotFoundError as e:
	urls = {}

done = False
mutex = threading.Lock()

def get_url_proc(id: int, pool: concurrent.futures.Executor):
	while True:
		try:
			url = wikileaks.get_clinton_pdf_url(id)
			break
		except urllib.error.HTTPError as e:
			print(f'{id}: Caught exception {e}, retrying')
			#pool.submit(get_url_proc, id, pool)
			#return
		except:
			traceback.print_exc()
			return

	print(f'{id}: {url}')

	mutex.acquire()
	try:
		urls[id] = url
	finally:
		mutex.release()


def checkpoint():
	while not done:
		time.sleep(10)
		print('~10 seconds passed, checkpointing')
		with open('clintonurls.json', 'w') as f:
			mutex.acquire()
			try:
				json.dump(urls, f, indent=4)
			finally:
				mutex.release()


cpthread = threading.Thread(target=checkpoint, daemon=False)
cpthread.start()

with concurrent.futures.ThreadPoolExecutor(max_workers=15) as pool:
	for i in range(1, wikileaks.COUNT_CLINTON + 1):
		if str(i) in urls:
			continue

		pool.submit(get_url_proc, i, pool)

done = True
cpthread.join()

#print('Done')
with open('clintonurls.json', 'w') as f:
	json.dump(urls, f, indent=4)


dirs = set(os.path.dirname(urllib.parse.urlparse(url).path).lstrip('/') for url in urls.values())

# aria2c --save-session=clinton.session.aria2 --save-session-interval=10 --continue=true -i clinton.session.aria2
with open('clinton.session.aria2', 'w') as f:
	for(id, url) in urls.items():
		x = urllib.parse.urlparse(url).path.lstrip('/')

		print(f'# --- {id} ---', file=f)
		print(url, file=f)
		print(f'  dir={os.path.dirname(x)}', file=f)
		print(f'  out={os.path.basename(x)}', file=f)
		print('  max-tries=0', file=f)

exit(0)
