SET FOREIGN_KEY_CHECKS = 0;

USE awsdb;

-- Users Table -------------------------------------------------------

DROP TABLE IF EXISTS Users;

CREATE TABLE Users (
  user_id INT NOT NULL AUTO_INCREMENT,
  first_name VARCHAR(255) NOT NULL,
  last_name VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL UNIQUE,
  password VARCHAR(255) NOT NULL,

  PRIMARY KEY (user_id)
);

INSERT INTO Users (first_name, last_name, email, password)
VALUES
('Test', 'User', 'please.dont@delete.me', 'password4+6489oiemm'),
('Bobo', 'Gobo', 'b@g.com', 'ham');


-- Shelters Table ---------------------------------------------------

DROP TABLE IF EXISTS Shelters CASCADE;

CREATE TABLE Shelters (
  shelter_id INT NOT NULL AUTO_INCREMENT,
  shelter_name VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL UNIQUE,
  zip VARCHAR(10) NOT NULL,
  password VARCHAR(255) NOT NULL,

  PRIMARY KEY (shelter_id)
);

INSERT INTO Shelters (shelter_name, email, zip, password) VALUES
('Test Shelter', 'please.dont@delete.me2', '02468', 'password4+6489oiemm'),
('OSU Capstone', 'aaa@bbb.ccc', '13579', 'aaa');


-- Animals Table ----------------------------------------------------

DROP TABLE IF EXISTS Animals;

CREATE TABLE Animals (
  animal_id INT NOT NULL AUTO_INCREMENT,
  animal_name VARCHAR(255) NOT NULL,
  type_id INT NOT NULL,
  breed_id INT NOT NULL,

  age VARCHAR(255) NOT NULL,
  -- Newborn, Young, Adult, Senior
  gender VARCHAR(255) NOT NULL,
  -- Male, Female, Unknown

  image_url VARCHAR(255),
  description TEXT NOT NULL,
  news_item TEXT,

  shelter_id INT NOT NULL,
  availability VARCHAR(255) NOT NULL,
  -- Available, Not Available, Pending, Adopted
  reserved_by INT,

  date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

  PRIMARY KEY (animal_id),

  FOREIGN KEY (type_id) REFERENCES Animal_Types(type_id)
  ON DELETE RESTRICT,

  FOREIGN KEY (breed_id) REFERENCES Animal_Breeds(breed_id)
  ON DELETE RESTRICT,

  FOREIGN KEY (shelter_id) REFERENCES Shelters(shelter_id)
  ON DELETE CASCADE,

  FOREIGN KEY (reserved_by) REFERENCES Users(user_id)
  ON DELETE SET NULL
);

INSERT INTO Animals (animal_name, type_id, breed_id, age, gender, 
                    image_url,
                    description,
                    news_item,
                    shelter_id, availability)
VALUES 
('Lady Bird', 1, 15, 'Senior', 'Female', 
'https://www.dogbreeds-and-doggie.com/image-files/bloodhound.jpg',
'A friendly dog looking for a loving home',
'Newly Added!',
1, 'Available'),

('Jynx', 2, 27, 'Adult', 'Female',
'https://thumb1.shutterstock.com/thumb_large/702739/187288940/stock-photo-black-cat-187288940.jpg',
'A spooky black cat looking for a new home',
NULL,
1, 'Available'),

('Yuki', 2, 23, 'Young', 'Male', 
'https://thumb9.shutterstock.com/image-photo/redirected-150nw-269516942.jpg',
'A hungry orange cat looking for a forever home',
'Just adopted!',
2, 'Available'),

('Birdy', 3, 33, 'Newborn', 'Unknown', 
NULL,
'A newborn bird almost ready for adoption',
NULL,
2, 'Available');

-- Animal Types Table -----------------------------------------------

DROP TABLE IF EXISTS Animal_Types;

CREATE TABLE Animal_Types (
  type_id INT NOT NULL AUTO_INCREMENT,
  type_name VARCHAR(255) NOT NULL,

  PRIMARY KEY (type_id)
);

INSERT INTO Animal_Types (type_name) VALUES
('Dog'),
('Cat'),
('Other');


-- Animal Breeds Table ----------------------------------------------

DROP TABLE IF EXISTS Animal_Breeds;

CREATE TABLE Animal_Breeds (
  breed_id INT NOT NULL AUTO_INCREMENT,
  breed_name VARCHAR(255) NOT NULL,
  type_id INT NOT NULL,
  PRIMARY KEY (breed_id),

  FOREIGN KEY (type_id) REFERENCES Animal_Types(type_id)
  ON DELETE CASCADE
);

INSERT INTO Animal_Breeds (breed_name, type_id) VALUES 
('Beagle', 1),
('Chihuahua', 1),
('Dachshund', 1),
('English Bulldog', 1),
('French Bulldog', 1),
('German Shepherd', 1),
('German Shorthaired Pointer', 1),
('Golden Retriever', 1),
('Labrador Retriever', 1),
('Pit Bull', 1),
('Poodle', 1),
('Rottweiler', 1),
('Siberian Husky', 1),
('Mixed Breed', 1),
('Other', 1),

('Abyssinian', 2),
('Bombay', 2),
('Calico', 2),
('Devon Rex', 2),
('Domestic Longhair', 2),
('Domestic Shorthair', 2),
('Exotic Shorthair', 2),
('Maine Coon', 2),
('Persian', 2),
('Ragdoll', 2),
('Russian Blue', 2),
('Siamese', 2),
('Sphynx', 2),
('Tabby', 2),
('Tuxedo', 2),
('Mixed Breed', 2),
('Other', 2),

('Bird', 3),
('Fish/Aquatic', 3),
('Hamster/Gerbil', 3),
('Rabbit', 3),
('Unknown', 3);


-- Dispositions Table -----------------------------------------------

DROP TABLE IF EXISTS Dispositions;

CREATE TABLE Dispositions (
  disposition_id INT NOT NULL AUTO_INCREMENT,
  disposition_name VARCHAR(255) NOT NULL,
  
  PRIMARY KEY (disposition_id)
);

INSERT INTO Dispositions (disposition_name) VALUES
('Affectionate'),
('Independent'),
('Energetic'),
('Laid-back'),
('Good with children'),
('Good with other animals'),
('Must be leashed at all times');


-- Animal Dispositions Table ----------------------------------------

DROP TABLE IF EXISTS Animal_Dispositions;

CREATE TABLE Animal_Dispositions (
  animal_id INT NOT NULL,
  disposition_id INT NOT NULL,
  
  PRIMARY KEY (animal_id, disposition_id),
  
  FOREIGN KEY (animal_id) REFERENCES Animals(animal_id)
  ON DELETE CASCADE,
  
  FOREIGN KEY (disposition_id) REFERENCES Dispositions(disposition_id)
  ON DELETE CASCADE
);

INSERT INTO Animal_Dispositions (animal_id, disposition_id) VALUES
(1, 2),
(1, 4),
(1, 5),
(1, 6),
(2, 2),
(2, 7),
(3, 1),
(3, 3);

SET FOREIGN_KEY_CHECKS=1;