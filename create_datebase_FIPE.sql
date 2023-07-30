drop table if exists FIPE;

create table if not exists FIPE(
	ID SERIAL PRIMARY key,
	COD_BRAND INT2,
	NAME_BRAND VARCHAR(30),
	COD_CAR INT2,
	NAME_CAR VARCHAR(244),
	VALUE INT4,
	MODEL_YEAR INT2,
	DATE_REFERENCE VARCHAR(50)
)