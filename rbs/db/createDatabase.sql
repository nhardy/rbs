DROP TABLE IF EXISTS faculties;
DROP TABLE IF EXISTS rooms;
DROP TABLE IF EXISTS resourcetypes;
DROP TABLE IF EXISTS resources;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS bookings;

CREATE TABLE faculties (
	fid INTEGER PRIMARY KEY,
	name TEXT NOT NULL,
	UNIQUE (name)
);

CREATE TABLE rooms (
	fid INTEGER NOT NULL,
	rid INTEGER PRIMARY KEY,
	code TEXT NOT NULL,
	capacity INTEGER NOT NULL,
	UNIQUE (code),
--	PRIMARY KEY (fid, rid), -- Restriction of SQLite, cannot have composite autoincrementing primary key
	FOREIGN KEY (fid) REFERENCES faculties(fid)
);

CREATE TABLE resourcetypes (
	type INTEGER PRIMARY KEY,
	name TEXT NOT NULL
);

CREATE TABLE resources (
	fid INTEGER NOT NULL,
	rid INTEGER NOT NULL,
	type INTEGER NOT NULL,
	quantity INTEGER NOT NULL,
	PRIMARY KEY (fid, rid, type),
	FOREIGN KEY (fid) REFERENCES rooms(fid),
	FOREIGN KEY (rid) REFERENCES rooms(rid),
	FOREIGN KEY (type) REFERENCES resourcetypes(type)
);

CREATE TABLE users (
	uid INTEGER PRIMARY KEY,
	username TEXT NOT NULL,
	utype INTEGER NOT NULL,
	password TEXT NOT NULL,
	salt TEXT NOT NULL,
	UNIQUE (username)
);

CREATE TABLE bookings (
	bid INTEGER PRIMARY KEY,
	fid INTEGER NOT NULL,
	rid INTEGER NOT NULL,
	uid INTEGER NOT NULL,
	stime INTEGER NOT NULL,
	etime INTEGER NOT NULL,
--	TODO: Booking resource requirements for shuffling bookings
	FOREIGN KEY (fid) REFERENCES rooms(fid),
	FOREIGN KEY (rid) REFERENCES rooms(rid),
	FOREIGN KEY (uid) REFERENCES users(uid)
);
