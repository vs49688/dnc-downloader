#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0

import os.path
import urllib.parse
import json
import concurrent.futures

with open('clintonurls.json', 'r') as f:
	urls = json.load(f)

dirs = set()

for (id, url) in urls.items():
	x = urllib.parse.urlparse(url)
	dirs.add(os.path.dirname(x.path).lstrip('/'))

for d in dirs:
	os.makedirs(d, exist_ok=True)



def downloadproc(url):
	pass


with concurrent.futures.ThreadPoolExecutor(max_workers=15) as pool:
	for (id, url) in urls.items():
		pool.submit(downloadproc, url)



#print('mkdir -p $PWD')
# for (id, url) in urls.items():
# 	print(url)
