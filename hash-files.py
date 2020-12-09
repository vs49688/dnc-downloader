#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0

import sqlite3
import hashlib
import os.path
import sys

if len(sys.argv) != 2:
	print(f'Usage: {sys.argv[0]} <dnc|podesta|clinton>')
	exit(2)

if sys.argv[1] not in ['dnc', 'podesta', 'clinton']:
	print(f'Usage: {sys.argv[0]} <dnc|podesta|clinton>')
	exit(2)

table_name = f'{sys.argv[1]}_emails'

with sqlite3.Connection('wikileaks.db') as db:
	cur = db.cursor()

	for r in cur.execute(f'SELECT id, path FROM {table_name} ORDER BY id').fetchall():
		with open(r[1], 'rb') as f:
			data = f.read()
			md5sum = hashlib.md5(data).hexdigest()
			sha1sum = hashlib.sha1(data).hexdigest()
			sha256sum = hashlib.sha256(data).hexdigest()
			size = os.path.getsize(r[1])

			cur.execute(f'UPDATE {table_name} SET size = ?, md5 = ?, sha1 = ?, sha256 = ? WHERE id = ?', (
				size, md5sum, sha1sum, sha256sum, r[0]
			))
	db.commit()