CREATE TABLE App_users (
	user_id INT IDENTITY(1,1) PRIMARY KEY,
	name NVARCHAR(100) NOT NULL,
	email NVARCHAR(100) UNIQUE NOT NULL, 
	preferences NVARCHAR(MAX) NULL,
);

CREATE TABLE Restaurants (
	restaurant_id NVACHAR(50) PRIMARY KEY,
	name NVACHAR(100) NOT NULL,
	address NVACHAR(MAX) NOT NULL,
	cuisine NVACHAR(50) NOT NULL,
	rating FLOAT NULL,
	phone NVACHAR(15) NULL,
	website NVACHAR(MAX) NULL
);

CREATE TABLE SearchHistory (
	search_id INT IDENTITY(1,1) PRIMARY KEY,
	user_id INT FOREIGN KEY REFERENCES App_users(user_id),
	search_term NVACHAR(100) NOT NULL,
	latitude FLOAT NOT NULL,
	longitude FLOAT NOT NULL,
	radius INT NOT NULL,
	limit INT NOT NULL, 
	search_timestamp DATETIME DEFAULT GETDATE()
);

CREATE TABLE SearchResults (
	search_id INT FOREIGN KEY REFERENCES SearchHistory(search_id),
	restaurant_id NVACHAR(50) FOREIGN KEY REFERENCES Restaurants(restaurant_id),
	added_at DATETIME DEFAULT GETDATE(),
	PRIMARY KEY (search_id, restaurant_id)
);