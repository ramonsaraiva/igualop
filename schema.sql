drop table if exists upload;
create table upload
(
	id integer primary key autoincrement,
	title text not null,
	description text null,
	filename varchar(32) not null 
);
