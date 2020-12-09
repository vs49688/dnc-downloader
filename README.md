# Wikileaks DNC/Podesta/Clinton Email Downloader

Scripts that download DNC, Podesta, and Clinton emails from Wikileaks
into their original format so they can be loaded into an email
client for further perusal.

## Legacy Version(s)
  * `dncdownload.sh` - The original version, written for bash. Only supports DNC.
  * `WikileaksEmailDownloader.py` - The second version, written for Python3. Supports DNC + Podesta.

## Downloading

This repository contains pregenerated [metalink](https://tools.ietf.org/id/draft-bryan-metalink-28.html) files for each set of emails. Use [aria2](https://aria2.github.io/) to download them.

Emails will be written in their respective `{dnc,podesta,clinton}-emails` subdirectory. DNC and Podesta emails have their 0-padded ID prefixed to the file name as some have duplicate names.

### To download
```bash
$ aria2c \
    --save-session=dnc.session.aria2 \
    --save-session-interval=10 \
    --continue=true \
    --max-concurrent-downloads=50 \
    --max-tries=0 \
    --retry-wait=5 \
    --allow-overwrite=true \
    --always-resume=true \
    --auto-file-renaming=false \
    dnc-emails.metalink # or podesta-emails.metalink or clinton-emails.metalink
```

### To resume
```bash
$ aria2c \
    --save-session=dnc.session.aria2 \
    --save-session-interval=10 \
    --continue=true \
    --max-concurrent-downloads=50 \
    --max-tries=0 \
    --retry-wait=5 \
    --allow-overwrite=true \
    --always-resume=true \
    --auto-file-renaming=false \
    -i dnc.session.aria2
```

## Generating the metalinks

Use `metagen.py <dnc|podesta|clinton>`. This requires `wikileaks.db` to be completed. A compressed version
is provided in the repository. See `wikileaks.db.zst`. If you'd like to generate from scratch, continue reading.

## Creating wikileaks.db

This is a bit of a painful process:
1. Create the database. 
   ```bash
   $ sqlite3 wikileaks.db < schema.db
   ```
2. Scrape the email metadata (filenames, etc.)
   ```bash
   $ ./urlscrape.mt2.py
   ```
   This will take awhile. Wikileaks likes to 503/504 a lot, so be patient. If interrupted, this will pick up where it left off.
3. Generate "stage 1" metalinks.
   ```
   ./metagen.py dnc > dnc.stage1.metalink
   ./metagen.py podesta > podestea.stage1.metalink
   ./metagen.py clinton > clinton.stage1.metalink
   ```
   These are metalink files without file sizes or hashes, only URLs and names.
4. Download the files. This is the most fragile part as there's nothing to verify against.
   ```bash
   $ aria2c \
      --save-session=dnc.session.aria2 \
      --save-session-interval=10 \
      --continue=true \
      --max-concurrent-downloads=50 \
      --max-tries=0 \
      --retry-wait=5 \
      --allow-overwrite=true \
      --always-resume=true \
      --auto-file-renaming=false \
      dnc.stage1.metalink # also do podesta and clinton
   ```

5. Hash the downloaded files
   ```bash
   $ ./hash-files.py
   ```

`wikileaks.db` should now contain all the information required to generate the
completed metalink files.

## License

[CC0-1.0](./LICENSE).
