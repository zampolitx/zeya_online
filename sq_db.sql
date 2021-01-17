CREATE TABLE IF NOT EXISTS holidays (
id integer PRIMARY KEY AUTOINCREMENT,
name text NOT NULL,
description text NOT NULL,
photo BLOB,
hol_date text NOT NULL
);

CREATE TABLE IF NOT EXISTS mainmenu (
id integer PRIMARY KEY AUTOINCREMENT,
title text NOT NULL,
url text NOT NULL
);

CREATE TABLE IF NOT EXISTS posts (
id integer PRIMARY KEY AUTOINCREMENT,
title text NOT NULL,
text text NOT NULL,
time integer NOT NULL
);