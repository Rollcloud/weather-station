DROP TABLE IF EXISTS weather;

CREATE TABLE weather (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  timestamp TIMESTAMP NOT NULL, 
  temperature REAL NOT NULL,
  pressure INTEGER NOT NULL,
  humidity INTEGER NOT NULL,
  air_quality INTEGER NOT NULL,
  eCO2 INTEGER NOT NULL
);


