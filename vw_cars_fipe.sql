drop view if exists VW_CARS_FIPE;

create view VW_CARS_FIPE as
	SELECT 
		f.id, f.cod_brand, f.cod_car, cm.id model_id,
		round(f.value,2) value, f.model_year, f.date_reference
	FROM fipe AS f
	JOIN car_model AS cm ON f.name_car like concat(cm.name, '%');
	

drop view if exists VW_CARS;

create view VW_CARS as
	SELECT 
		c.*, cm.id model_id
	FROM cars AS c
	JOIN car_model AS cm ON c.title like concat('%', concat(cm.name, '%'));