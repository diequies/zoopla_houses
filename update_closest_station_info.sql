# SQL script to update zoopla_houses table with closest station information

USE zoopla_houses;

ALTER TABLE zoopla_houses
ADD COLUMN (
	closest_station_name VARCHAR(256),
    closest_station_distance_sec int
);

UPDATE zoopla_houses as t1
INNER JOIN closest_station t2 
ON t1.index = t2.index
SET t1.closest_station_name = t2.closest_station_name, t1.closest_station_distance_sec = t2.closest_station_distance_sec;

DROP TABLE closest_station;

SELECT * FROM zoopla_houses;