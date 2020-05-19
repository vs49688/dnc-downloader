#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0

import os
import errno
import argparse
import urllib.request
import sys

email_db = {
	"podesta": {
		"download-id":"podesta-emails",
		"count":59028
    },
	"dnc": {
		"download-id":"dnc-emails",
		"count":44053
	},
	# Clinton emails use a different format, will implement later
	#"clinton": {
	#	"download-id":"clinton-emails",
	#	"count":30945
	#}
}

#curl -OJL https://wikileaks.org/dnc-emails//get/<id-here>
parser = argparse.ArgumentParser(description="Download emails from wikileaks.")
parser.add_argument('set', type=str, help="The email set.",	choices=["podesta", "dnc"])
parser.add_argument('--start', type=int, default=1, help="The email index to start from (default: 1)")
parser.add_argument('--end', type=int, default=-1, help="The email index to stop at. -1 = all of them (default: -1)")
parser.add_argument('--retries', type=int, default=5, help="The retry count if downloading fails (default: 5)")

args = parser.parse_args()

if args.retries < -1:
	args.retries = 0

email_set = email_db[args.set]

if args.start > email_set["count"] or args.start < 1:
	print("Invalid value for start. {0} >= {1} or {0} < 0".format(args.start, email_set["count"]))
	exit(1)

if args.end < 1:
	args.end = email_set["count"]

if args.end > email_set["count"]:
	print("Invalid value for end. {0} >= {1}".format(args.end, email_set["count"]))
	exit(1)

print("Parameters: {0}".format(args))
print("Email Set:  {0}".format(email_set))

base_url = "https://wikileaks.org/{0}//get".format(email_set["download-id"])

os.makedirs(args.set, exist_ok=True)

for i in range(args.start, args.end + 1):
	print("Downloading {0}".format(i))

	for r in range(0, args.retries + 1):
		print("* Try {0}...".format(r + 1))
		try:
			email_url = "{0}/{1}".format(base_url, i)

			req = urllib.request.Request(
				url=email_url,
				headers={'User-Agent': 'Mozilla/5.0'},
				method='GET'
			)

			with urllib.request.urlopen(req) as x:
				email_name = x.getheader('Content-Disposition').split('filename=')[1]

				if email_name[0] in ["\"", "'"]:
					email_name = email_name[1:-1]

				file_name = "{0}/{1:05d}_{2}".format(args.set, i, email_name)

				with open(file_name, "wb") as f:
					f.write(x.read())

			break
		except Exception as e:
			print(" * Failed to download: {0}".format(e))

