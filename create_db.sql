CREATE TABLE IF NOT EXISTS donors (
  user_id INT,
  name TEXT,
  type TEXT,
  sex TEXT,
  city TEXT,
  region TEXT
);

.mode csv
CREATE TABLE IF NOT EXISTS parties (
  party_id INT,
  name TEXT);

.mode csv

CREATE TABLE IF NOT EXISTS donations (
  donate_id INT,
  party_id INT,
  date TEXT,
  user_id INT,
  user_type TEXT,
  sex TEXT,
  city TEXT,
  region TEXT,
  income_type TEXT,
  amount INT,
  flag TEXT,
  source TEXT
  );
.mode csv

