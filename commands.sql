CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    password VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS users_backup (
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) PRIMARY KEY,
    password VARCHAR(50) NOT NULL
);

CREATE TRIGGER IF NOT EXISTS User_Del
AFTER DELETE ON Users
FOR EACH ROW
INSERT INTO users_backup (username,email,password) VALUES(old.username, old.email, old.password);