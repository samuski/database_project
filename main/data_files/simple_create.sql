CREATE TABLE location (
    locationid INTEGER PRIMARY KEY,
    city STRING,
    area STRING,
    latitude INTEGER,
    longitude INTEGER
);

CREATE TABLE timeinfo (
    timeid INTEGER PRIMARY KEY,
    crimetime STRING
);

CREATE TABLE crimecategory (
    categoryid INTEGER PRIMARY KEY,
    categoryname STRING
);

CREATE TABLE crimetype (
    crimetypeid INTEGER PRIMARY KEY,
    crimedesc STRING,
    categoryid INTEGER,
    FOREIGN KEY (categoryid) REFERENCES crimecategory(categoryid)
);

CREATE TABLE premisetype (
    premisid INTEGER PRIMARY KEY,
    premisdesc STRING
);

CREATE TABLE crime (
    crimeid INTEGER PRIMARY KEY,
    locationid INTEGER,
    timeid INTEGER,
    crimetypeid INTEGER,
    premisid INTEGER,
    arrestmade STRING,
    FOREIGN KEY (locationid) REFERENCES location(locationid),
    FOREIGN KEY (timeid) REFERENCES timeinfo(timeid),
    FOREIGN KEY (crimetypeid) REFERENCES crimetype(crimetypeid),
    FOREIGN KEY (premisid) REFERENCES premisetype(premisid)
);

CREATE TABLE 1k_i (
    id INTEGER PRIMARY KEY,
    col1 INTEGER,
    col2 INTEGER
);

CREATE TABLE 1k_1 (
    id INTEGER PRIMARY KEY,
    col1 INTEGER,
    col2 INTEGER
);

CREATE TABLE 100k_i (
    id INTEGER PRIMARY KEY,
    col1 INTEGER,
    col2 INTEGER
);

CREATE TABLE 100k_1 (
    id INTEGER PRIMARY KEY,
    col1 INTEGER,
    col2 INTEGER
);

CREATE TABLE 1m_i (
    id INTEGER PRIMARY KEY,
    col1 INTEGER,
    col2 INTEGER
);

CREATE TABLE 1m_1 (
    id INTEGER PRIMARY KEY,
    col1 INTEGER,
    col2 INTEGER
);