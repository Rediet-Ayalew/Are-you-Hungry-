


CREATE TABLE App_users (
	user_id INT IDENTITY(1,1) PRIMARY KEY,
	name NVARCHAR(100) NOT NULL,
	email NVARCHAR(100) UNIQUE NOT NULL, 
	preferences NVARCHAR(MAX) NULL,
);

CREATE TABLE Restaurants (
	name NVARCHAR(100) NOT NULL,
	address NVARCHAR(MAX) NOT NULL,
	cuisine NVARCHAR(50) NOT NULL,
	rating FLOAT NULL,
	phone NVARCHAR(15) NULL,
	website NVARCHAR(MAX) NULL
	PRIMARY KEY (name, address)
);

CREATE TABLE SearchHistory (
	search_id INT IDENTITY(1,1) PRIMARY KEY,
	user_id INT FOREIGN KEY REFERENCES App_users(user_id),
	search_term NVARCHAR(100) NOT NULL,
	latitude FLOAT NOT NULL,
	longitude FLOAT NOT NULL,
	radius INT NOT NULL,
	limit INT NOT NULL, 
	search_timestamp DATETIME DEFAULT GETDATE()
);

CREATE TABLE SearchResults (
	search_id INT FOREIGN KEY REFERENCES SearchHistory(search_id),
	restaurant_name NVACHAR(100),
	restaurant_address NVACHAR(MAX),
	added_at DATETIME DEFAULT GETDATE(),
	PRIMARY KEY (search_id, restaurant_name, restaurant_address), 
	FOREIGN KEY (restaurant_name, restaurant_address) REFERENCES Restaurants(name, address)
);
 