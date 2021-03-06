CREATE TABLE User(
	Username 		varchar(50),
	Password 		CHAR(32) NOT NULL,
	IsAdmin 		boolean NOT NULL,
	PRIMARY KEY (Username)
) ENGINE=InnoDB;

INSERT INTO User (Username, Password, IsAdmin) VALUES
('admin', 'admin123', TRUE),
('kparker', 'imtheCEO', TRUE),
('eoneil', 'interimCEO', TRUE),
('commuter14', 'choochoo', FALSE),
('busrider73', 'roundandround', FALSE),
('sandrapatel', 'iphonex', FALSE),
('ignacio.john', 'tohellwga', FALSE),
('riyoy1996', 'Riyo4LIFE', FALSE),
('kellis', 'martapassword', FALSE),
('ashton.woods', '2Factor', FALSE),
('adinozzo', 'V3rySpecialAgent', FALSE);

---------------------- Passenger Table ----------------------------

CREATE TABLE Passenger(
	Username 		varchar(50),
	Email 			varchar(50) NOT NULL,
	PRIMARY KEY (Username),
	UNIQUE (Email),
	FOREIGN KEY (Username) REFERENCES User(Username) 
		ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

INSERT INTO Passenger (Username, Email) VALUES
('commuter14', 'LeonBarnes@superrito.com'),
('busrider73', 'lena.wexler@dayrep.com'),
('sandrapatel', 'sandra74@jourrapide.com'),
('ignacio.john', 'john@iconsulting.com'),
('riyoy1996', 'yamada.riyo@navy.mil.gov'),
('kellis', 'kateellis@gatech.edu'),
('ashton.woods', 'awoods30@gatech.edu'),
('adinozzo', 'anthony.dinozzo@ncis.mil.gov');

---------------------- Breezecard Table ----------------------------

CREATE TABLE Breezecard(
	BreezecardNum 	char(16),
	Value 			decimal(6,2) NOT NULL,
	BelongsTo		varchar(50),
	PRIMARY KEY (BreezecardNum),
	FOREIGN KEY (BelongsTo) REFERENCES Passenger(Username) -- <====(Can also reference Email)
		ON DELETE SET NULL ON UPDATE CASCADE, -- <== Must be SET NULL
	CHECK (Value >= 0.00 AND Value <= 1000.00)
) ENGINE=InnoDB;

INSERT INTO Breezecard (BreezecardNum, Value, BelongsTo) VALUES
('919948381768459', 126.50, 'commuter14'),
('1788613719481390', 177.00, 'busrider73'),
('2792083965359460', 20.00, 'sandrapatel'),
('524807425551662', 59.50, 'ignacio.john'),
('7792685035977770', 80.25, 'riyoy1996'),
('1325138309325420', 97.00, 'kellis'),
('6411414737900960', 41.00, 'ashton.woods'),
('9248324548250130', 12.75, 'sandrapatel'),
('8753075721740010', 110.00, 'sandrapatel'),
('7301442590825470', 6.00, 'sandrapatel'),
('4769432303280540', 68.50, 'sandrapatel'),
('4902965887533820', 79.75, 'sandrapatel'),
('475861680208144', 35.25, 'commuter14'),
('5943709678229760', 133.50, 'commuter14'),
('2613198031233340', 45.00, 'commuter14'),
('2286669536044610', 0.50, 'commuter14'),
('6424673176102560', 27.00, 'commuter14'),
('4792323707679860', 34.00, 'commuter14'),
('2006517782865770', 127.25, 'commuter14'),
('3590098235166490', 16.25, 'commuter14'),
('2275718423410130', 143.25, 'commuter14'),
('8802558078528210', 42.25, 'busrider73'),
('9712526903816770', 68.50, 'busrider73'),
('6603808416168570', 41.50, 'busrider73'),
('9286930794479390', 116.25, 'kellis'),
('123456780987654', 140.25, NULL),
('9876543212345670', 92.50, NULL),
('7534785562588930', 85.50, 'adinozzo'),
('3346822267258650', 113.00, NULL),
('1258825691462690', 144.75, NULL),
('4156771407939460', 110.50, NULL),
('1156635952683150', 141.00, NULL);


---------------------- Conflict Table ----------------------------

CREATE TABLE Conflict(
	Username 		varchar(50),
	BreezecardNum 	char(16),
	DateTime 		TIMESTAMP NOT NULL,
	CONSTRAINT Pk_Conflict PRIMARY KEY (Username, BreezecardNum),
	FOREIGN KEY (Username) REFERENCES Passenger(Username)
		ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (BreezecardNum) REFERENCES Breezecard(BreezecardNum) 
		ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

INSERT INTO Conflict (Username, BreezecardNum, DateTime) VALUES
('sandrapatel', '475861680208144', '2018-11-12 00:00:01'),
('kellis', '4769432303280540', '2017-10-23 16:21:49'),
('riyoy1996', '4769432303280540', '2017-10-24 07:31:12');



---------------------- Station Table ----------------------------

CREATE TABLE Station(
	StopID 			varchar(50),
	Name 			varchar(50) NOT NULL,
	EnterFare 		decimal(4,2) NOT NULL,
	ClosedStatus 	boolean NOT NULL,
	IsTrain 		boolean NOT NULL,
	PRIMARY KEY (StopID),
	UNIQUE (Name, IsTrain),
	CHECK (EnterFare >= 0.00 AND EnterFare <= 50.00)
) ENGINE=InnoDB;

INSERT INTO Station (StopID, Name, EnterFare, ClosedStatus, IsTrain) VALUES
('N11', 'North Springs', 2.50, FALSE, TRUE),
('BUSN11', 'North Springs', 2.00, FALSE, FALSE),
('N10', 'Sandy Springs', 2.00, FALSE, TRUE),
('N9', 'Dunwoody', 3.00, FALSE, TRUE),
('N8', 'Medical Center', 4.00, FALSE, TRUE),
('N7', 'Buckhead', 1.00, FALSE, TRUE),
('N6', 'Lindbergh Center', 2.00, FALSE, TRUE),
('N5', 'Arts Center', 4.00, FALSE, TRUE),
('N4', 'Midtown', 5.00, FALSE, TRUE),
('BUSN4', 'Midtown', 5.00, FALSE, FALSE),
('N3', 'North Avenue', 3.00, FALSE, TRUE),
('N2', 'Civic Center', 4.00, FALSE, TRUE),
('N1', 'Peachtree Center', 6.00, FALSE, TRUE),
('FP', 'Five Points', 8.00, FALSE, TRUE),
('S1', 'Garnett', 10.00, FALSE, TRUE),
('S2', 'West End', 25.00, FALSE, TRUE),
('BUSS2', 'West End', 2.50, FALSE, FALSE),
('S3', 'Oakland City', 5.00, FALSE, TRUE),
('S4', 'Lakewood/Ft. McPherson', 2.50, TRUE, TRUE),
('S5', 'East Point', 2.50, FALSE, TRUE),
('S6', 'College Park', 2.50, FALSE, TRUE),
('S7', 'Atlanta Airport', 2.50, FALSE, TRUE),
('W5', 'Hamilton E.Holmes', 2.50, TRUE, TRUE),
('W4', 'West Lake', 2.50, FALSE, TRUE),
('W3', 'Ashby', 2.50, FALSE, TRUE),
('W2', 'Vine City', 2.50, FALSE, TRUE),
('W1', 'GA Dome, GA World Congress Center, Phillips Arena, CNN Center', 2.50, FALSE, TRUE),
('BUSDOME', 'Georgia Dome Bus Station', 4.00, FALSE, FALSE),
('E1', 'Georgia State', 2.50, FALSE, TRUE),
('E2', 'King Memorial', 2.50, FALSE, TRUE),
('E3', 'Inman Park/Reynolds Town', 2.50, FALSE, TRUE),
('E4', 'Edgewood/Candler Park', 2.50, FALSE, TRUE),
('E5', 'East Lake', 3.00, FALSE, TRUE),
('E6', 'Decatur', 2.50, FALSE, TRUE),
('E7', 'Avondale', 2.50, FALSE, TRUE),
('E8', 'Kensington', 3.00, FALSE, TRUE),
('E9', 'Indian Creek', 2.50, FALSE, TRUE),
('P4', 'Bankhead', 1.00, TRUE, TRUE),
('35161', 'Old Milton Pkwy - Park Bridge Pkwy', 2.00, TRUE, FALSE),
('31955', 'Old Milton Pkwy - North Point Pkwy', 2.00, FALSE, FALSE),
('95834', 'Old Milton Pkwy - Haynes Bridge Pkwy', 2.00, FALSE, FALSE),
('46612', 'Alpharetta Hwy - Commerce Pkwy', 2.00, FALSE, FALSE);


---------------------- BusStation Table ----------------------------

CREATE TABLE BusStation(
	StopID 			varchar(50),
	Intersection 	varchar(255),
	PRIMARY KEY (StopID),
	FOREIGN KEY (StopID) REFERENCES Station(StopID)
		ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

INSERT INTO BusStation(StopID, Intersection) VALUES
('BUSN11', 'Peachtree-Dunwoody Road'),
('BUSDOME', NULL),
('BUSN4', '10th Street'),
('BUSS2', NULL),
('35161', 'Park Bridge Pkwy'),
('31955', 'North Point Pkwy'),
('95834', 'Haynes Bridge Pkwy'),
('46612', 'Commerce Pkwy');


---------------------- Trip Table ----------------------------
CREATE TABLE Trip(
	Tripfare 		decimal(4,2) NOT NULL,
	StartTime 		TIMESTAMP,
	BreezecardNum 	char(16),
	StartsAt 		varchar(50) NOT NULL,
	EndsAt 			varchar(50),
	CONSTRAINT Pk_Trip PRIMARY KEY (StartTime, BreezecardNum),
	FOREIGN KEY (BreezecardNum) REFERENCES Breezecard(BreezecardNum) 
		ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (StartsAt) REFERENCES Station(StopID)
		ON DELETE RESTRICT ON UPDATE CASCADE,
	FOREIGN KEY (EndsAt) REFERENCES Station(StopID)
		ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB;

INSERT INTO Trip(Tripfare, StartTime, BreezecardNum, StartsAt, EndsAt) VALUES
(2.75, '2017-11-05 16:21:49', '524807425551662', 'N11', 'N4'),
(1.50, '2017-11-03 09:44:11', '524807425551662', 'N4', 'N11'),
(10.50, '2017-11-02 13:11:11', '1788613719481390', 'BUSDOME', 'BUSN11'),
(4.00, '2017-11-02 13:11:11', '2792083965359460', '31955', '46612'),
(2.00, '2017-10-31 22:33:10', '524807425551662', 'S7', 'N4'),
(3.50, '2017-10-31 22:31:10', '7792685035977770', 'E1', 'N3'),
(1.00, '2017-10-31 21:30:00', '1325138309325420', 'FP', NULL),
(3.50, '2017-10-28 22:30:10', '6411414737900960', 'N11', 'N4'),
(1.50, '2017-10-28 22:11:13', '9248324548250130', 'N4', 'N11'),
(1.00, '2017-10-27 09:40:11', '8753075721740010', 'N3', 'N4'),
(9.00, '2017-10-27 04:31:30', '7301442590825470', 'N4', 'S7'),
(1.50, '2017-10-10 00:00:00', '7534785562588930', 'BUSS2', 'BUSDOME');
