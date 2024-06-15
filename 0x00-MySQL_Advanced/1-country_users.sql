-- Script to create a 'users' table with id, email, and name attributes.
-- The table includes constraints for id (PRIMARY KEY, AUTO_INCREMENT),
-- email (UNIQUE, NOT NULL), name and country.
-- The script ensures the table is created only if it does not already exist.
CREATE TABLE IF NOT EXISTS users (
	id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	email VARCHAR(255) NOT NULL UNIQUE,
	name VARCHAR(255),
    country ENUM ('US', 'CO', 'TN') DEFAULT 'US'
);
