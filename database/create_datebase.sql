DROP TABLE IF EXISTS CARS CASCADE;

CREATE TABLE IF NOT EXISTS CARS(
	ID SERIAL PRIMARY KEY,
	PRICE INT4,
	REGION VARCHAR(244),
	KM INT4,
	YEAR INT2,
	DATE VARCHAR(18),
	LINK VARCHAR(244),
	TITLE VARCHAR(244),
	DESCRIPTION VARCHAR(5000),
	MODEL VARCHAR(80),
	POWER VARCHAR(16),
	COLOR VARCHAR(20),
	DOORS INT2,
	STEERING VARCHAR(20),
	TYPE_CAR VARCHAR(20),
	OPTIONAL VARCHAR(244),
	CEP INT4,
	CITY VARCHAR(244));
	

ALTER TABLE CARS ALTER COLUMN DESCRIPTION TYPE VARCHAR(5000);