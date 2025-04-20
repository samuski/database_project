CREATE TABLE location (
    locationid INTEGER PRIMARY KEY,
    city STRING,
    area STRING,
    latitude STRING,
    longitude STRING
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

-- For Rel-i-i-1000.csv
CREATE TABLE thousand_i (
    col1 INTEGER,
    col2 INTEGER
);

-- For Rel-i-1-1000.csv
CREATE TABLE thousand_1 (
    col1 INTEGER,
    col2 INTEGER
);

-- For Rel-i-i-1000000.csv
CREATE TABLE hun_thousand_i (
    col1 INTEGER,
    col2 INTEGER
);

-- For Rel-i-1-1000000.csv
CREATE TABLE hun_thousand_1 (
    col1 INTEGER,
    col2 INTEGER
);

CREATE TABLE million_i (
    col1 INTEGER,
    col2 INTEGER
);

CREATE TABLE million_1 (
    col1 INTEGER,
    col2 INTEGER
);