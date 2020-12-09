#!/usr/bin/env python3

import wikileaks

with open('dnc.session.aria2', 'w') as f:
    for id in range(1, wikileaks.COUNT_DNC + 1):
        print(f'# --- {id} ---', file=f)
        print(f'https://wikileaks.org/dnc-emails/get/{id}', file=f)
        print('  dir=dnc-emails', file=f)
        print('  max-tries=0', file=f)

with open('podesta.session.aria2', 'w') as f:
    for id in range(1, wikileaks.COUNT_PODESTA + 1):
        print(f'# --- {id} ---', file=f)
        print(f'https://wikileaks.org/podesta-emails/get/{id}', file=f)
        print('  dir=podesta-emails', file=f)
        print('  max-tries=0', file=f)

