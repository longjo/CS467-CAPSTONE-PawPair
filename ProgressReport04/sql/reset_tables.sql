USE awsdb;

DROP TABLE IF EXISTS Users;

CREATE TABLE Users (
  user_id INT NOT NULL AUTO_INCREMENT,
  firstname VARCHAR(255) NOT NULL,
  lastname VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL UNIQUE,
  password VARCHAR(255) NOT NULL,
  PRIMARY KEY (user_id)
);


DROP TABLE IF EXISTS Shelters;

CREATE TABLE Shelters (
  shelter_id INT NOT NULL AUTO_INCREMENT,
  sheltername VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL UNIQUE,
  password VARCHAR(255) NOT NULL,
  zip VARCHAR(10) NOT NULL,
  PRIMARY KEY (shelter_id)
);

DROP TABLE IF EXISTS Animals;

CREATE TABLE Animals (
  animal_id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(255) NOT NULL,
  species VARCHAR(255) NOT NULL,
  breed VARCHAR(255) NOT NULL,
  age INT NOT NULL,
  gender VARCHAR(255) NOT NULL,
  image_url VARCHAR(255) NOT NULL,
  description TEXT NOT NULL,
  shelter_id INT NOT NULL,
  FOREIGN KEY (shelter_id) REFERENCES Shelters(shelter_id)
  ON DELETE CASCADE,
  PRIMARY KEY (animal_id)
);
