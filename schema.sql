drop table if exists entries;
create table entries (
	registered date unique,
	weight real,
	bodyfat real
)
