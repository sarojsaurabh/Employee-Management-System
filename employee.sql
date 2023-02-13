use employee;
create table emp_data(emp_id varchar(255) unique not null,emp_name varchar(255),emp_email varchar(255) unique not null,emp_phone varchar(255) unique not null,emp_address mediumtext,emp_post varchar(255),emp_salary int,emp_join_date date,primary key(emp_id,emp_name));
insert into emp_data values("A001","Mansi Bajaj","mansi156@gmail.com","9475809777","Block 110 H.no 212,vikas nagar lko, Up,India","Analyst",45000,'2016-01-22');
drop table emp_data;
select * from emp_data;

create table founders(founder_id varchar(255), passcode varchar(255),primary key(founder_id));
drop table founders;
insert into founders values("renuka@mycompanyltd","renuka20");
select * from founders;

create table emp_pass(emp_id varchar(255) unique not null,pass varchar(255),primary key(emp_id));
insert into emp_pass values("A003","mansiwonder18");
create table new_project(pname varchar(255));
select * from emp_pass;

create table working_projects(empl_id varchar(255)unique not null,pname varchar(255) unique not null,p_comp varchar(255),primary key(empl_id));
insert into working_projects values("A003","Employee System","0");
update working_projects set p_comp=23 where pname="EmployeeSystem";
select * from working_projects;
drop table working_projects;

create table new_projects(npname varchar(255));
insert into new_projects values("Organization Website Development");
select * from new_projects;

create table message_to_emp(employ_id varchar(255),message mediumtext,date_time datetime default );
insert into message_to_emp values("A003","please sumbit your project in 10 days",now());
drop table message_to_emp;
select * from message_to_emp order by date_time DESC;

create table message_to_admin(employee_id varchar(255),employee_name varchar(255),employee_post varchar(255),emp_message mediumtext,date_time datetime);
drop table message_to_admin;

create table message_to_other_emp(sent_to varchar(255),sent_from varchar(255),employee_name varchar(255),employee_post varchar(255),emp_message mediumtext,date_time datetime );
drop table message_to_other_emp
 