drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  text text not null
);

create table admin (
  id integer primary key autoincrement,
  status text not null
);
