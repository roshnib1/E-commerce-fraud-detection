drop database db;
create database db;
use db;

CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT, 
    name VARCHAR(30), 
    email VARCHAR(50) UNIQUE, 
    password VARCHAR(40), 
    age INT, 
    gender VARCHAR(30)
    );


CREATE TABLE products (
    id INT PRIMARY KEY AUTO_INCREMENT, 
    name VARCHAR(100), 
    price INT, 
    path VARCHAR(500)
    );


CREATE TABLE cart (
    id INT PRIMARY KEY AUTO_INCREMENT, 
    product_id INT, 
    user_id INT
    );


CREATE TABLE purchases (
    id INT PRIMARY KEY AUTO_INCREMENT, 
    product_id INT, 
    quantity int, 
    amount int, 
    user_id INT
    );


CREATE TABLE users_data (
    user_id INT PRIMARY KEY AUTO_INCREMENT, 
    age_group_18_25 BOOLEAN, 
    age_group_26_35 BOOLEAN, 
    age_group_36_45 BOOLEAN, 
    age_group_46_55 BOOLEAN, 
    age_group_56_65 BOOLEAN, 
    gender_female BOOLEAN, 
    gender_male BOOLEAN, 
    avg_transaction_amount FLOAT DEFAULT 0, 
    add_to_cart INT DEFAULT 0, 
    browse INT DEFAULT 0, 
    login INT DEFAULT 0, 
    purchase INT DEFAULT 0
    );


insert into products (name, price, path) values ("example", 100, "static/images/p1.png");
insert into products (name, price, path) values ("example", 100, "static/images/p2.png");
insert into products (name, price, path) values ("example", 100, "static/images/p3.png");
insert into products (name, price, path) values ("example", 100, "static/images/p4.png");
insert into products (name, price, path) values ("example", 100, "static/images/p5.png");
insert into products (name, price, path) values ("example", 100, "static/images/p6.png");
insert into products (name, price, path) values ("example", 100, "static/images/p7.png");
insert into products (name, price, path) values ("example", 100, "static/images/p8.png");