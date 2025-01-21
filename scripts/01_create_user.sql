-- create the user for test database
CREATE USER 'kupidon'@'%' IDENTIFIED BY 'kupidon';
GRANT CREATE, ALTER, INDEX, LOCK TABLES, REFERENCES, UPDATE, DELETE, DROP, SELECT, INSERT ON `kupidon`.* TO 'kupidon'@'%';

FLUSH PRIVILEGES;
