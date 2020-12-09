
CREATE TABLE clinton_emails(
	id     INTEGER NOT NULL PRIMARY KEY,
	path   TEXT NOT NULL UNIQUE,
	url    TEXT NOT NULL UNIQUE,
	size   INTEGER,
	md5    VARCHAR(32),
	sha1   VARCHAR(40),
	sha256 VARCHAR(64)
);


CREATE TABLE dnc_emails(
	id            INTEGER NOT NULL PRIMARY KEY,
	path          TEXT NOT NULL UNIQUE,
	url           TEXT NOT NULL UNIQUE,
	original_name TEXT NOT NULL,
	size          INTEGER,
	md5           VARCHAR(32),
	sha1          VARCHAR(40),
	sha256        VARCHAR(64)
);


CREATE TABLE podesta_emails(
	id            INTEGER NOT NULL PRIMARY KEY,
	path          TEXT NOT NULL UNIQUE,
	url           TEXT NOT NULL UNIQUE,
	original_name TEXT NOT NULL,
	size          INTEGER,
	md5           VARCHAR(32),
	sha1          VARCHAR(40),
	sha256        VARCHAR(64)
);
