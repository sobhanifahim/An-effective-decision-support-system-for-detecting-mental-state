create database if not exists dssms default character set utf8 collate utf8_general_ci;
use dssms;

create table patientinfo(
pid int not null auto_increment,
pname varchar(50) not null,
gender varchar(7) not null,
Age varchar(4) not null,
la varchar(10) not null,
ha varchar(10) not null, 
lb varchar(10) not null,
hb varchar(10) not null,
lg varchar(10) not null,
hg varchar(10) not null,
state varchar(15) not null,
ref varchar(50) not null,
primary key(pid)
) engine=InnoDB auto_increment=1 default charset=utf8;

select * from patientinfo;

delete from patientinfo where pid=12;
create table uaccount(
   uid int not null auto_increment,
   uname varchar(50),
   email varchar(50),
   upassword varchar(50),
   primary key(uid)
)engine=InnoDB auto_increment=1 default charset=utf8;

select * from uaccount;

create table adminaccount(
   aid int not null auto_increment,
   aname varchar(50),
   apassword varchar(50),
   primary key(aid)
)engine=InnoDB auto_increment=1 default charset=utf8;

insert into adminaccount(aname,apassword) values('sobhanifahim','654321');
select * from adminaccount;

