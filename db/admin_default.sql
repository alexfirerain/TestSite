-- # SQL-запрос создания таблицы командировочных в базе:
-- CREATE TABLE IF NOT EXISTS users (
--     trip_id    INTEGER PRIMARY KEY AUTOINCREMENT,
--     name       TEXT    NOT NULL,
--     city       TEXT    NOT NULL,
--     per_diem   REAL    NOT NULL,
--     date_first DATE    NOT NULL,
--     date_last  DATE    NOT NULL
-- );

INSERT INTO users (name,city,per_diem,date_first,date_last) VALUES
	('Баранов П.Е.','Воронеж',450.00,'2020-07-19','2020-07-25')
