CREATE DATABASE `bank_final_project`;
USE `bank_final_project`;
CREATE TABLE `customers`(
	`age` int(4),
    `job` varchar(20),
    `marital` varchar(20),
    `education` varchar(20),
    `default` varchar(20),
    `balance` int(10),
    `housing` varchar(20),
    `loan` varchar(20),
    `contact` varchar(20),
    `duration` int(10),
    `campaign` int(20),
    `pdays` int(20),
    `previous` int(20),
    `time_inserted` datetime,
    `predicted` int(10)
    );
    
    
drop table `customers`;

    
SELECT NOW();
    
select * from customers;

SELECT * FROM (SELECT * FROM customers ORDER BY time_inserted ASC LIMIT 10) AS T
ORDER BY time_inserted DESC LIMIT 10;

SELECT * FROM customers
ORDER BY date_inserted ASC;