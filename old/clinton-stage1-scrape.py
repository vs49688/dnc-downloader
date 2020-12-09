#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0

import urllib.parse
import json
import wikileaks

try:
	with open('clintonurls.json', 'r') as f:
		urls = json.load(f)
except FileNotFoundError as e:
	urls = {}

#print(urls)
#exit(0)
i = 1
while i <= 33727:

	if str(i) in urls:
		url = urls[str(i)]
		if url.startswith('/'):
			urls[str(i)] = urllib.parse.urljoin('https://wikileaks.org/', url)

		print(f'{i}: Skipping...')
		i += 1
		continue

	try:
		urls[i] = wikileaks.get_clinton_pdf_url(i)
	except urllib.error.HTTPError as e:
		print(f'{i}: Caught exception {e}, retrying')
		continue
		
	print(f'{i}: {urls[i]}')

	if i % 10 == 0:
		print(f'Dumping at {i}')
		with open('clintonurls.json', 'w') as f:
			json.dump(urls, f, indent=4)

	i += 1

print('Done')
with open('clintonurls.json', 'w') as f:
	json.dump(urls, f, indent=4)
