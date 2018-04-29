-- Login --
SELECT * 
FROM User
WHERE Username = userName

-- Registration --
SELECT BreezecardNum, BelongsTo
FROM Breezecard 
WHERE BreezecardNum = cardNum

SELECT Username 
FROM User 
WHERE Username = userName

SELECT Email 
FROM Passenger 
WHERE Email = email

INSERT INTO User 
VALUES(%s, %s, %s)

INSERT INTO Passenger 
VALUES(%s, %s)

INSERT INTO Breezecard 
VALUES(%s, %s, %s)

INSERT INTO Conflict 
VALUES(%s, %s, %s)

-- Station Management --
SELECT * 
FROM Station 
WHERE StopId = stopID

SELECT Intersection 
FROM BusStation 
WHERE StopId = stopID

SELECT StopID,Name,EnterFare,ClosedStatus,IsTrain 
FROM Station

-- Create New Station --
SELECT Name 
FROM Station 
WHERE Name = %s AND IsTrain = %s

SELECT StopID 
FROM Station 
WHERE StopID = %s

INSERT INTO Station (StopId, Name, Enterfare, ClosedStatus, IsTrain) 
VALUES (%s, %s, %s, %s, %s)

INSERT INTO BusStationIntersection(StopID, Intersection) 
VALUES (%s, %s)

-- View and Update Station Detail --
UPDATE Station 
SET Enterfare = %s 
WHERE StopId = %s

UPDATE BusStation 
SET Intersection = %s 
WHERE StopID = %s

UPDATE Station 
SET ClosedStatus = %s 
WHERE StopId = %s

-- Suspend Cards --
SELECT 		Conflict.Username as New_Owner, 
			Conflict.BreezecardNum as Card, 
			Conflict.DateTime as DTime, 
			Breezecard.BelongsTo as Old_Owner 
FROM 		Conflict, Breezecard 
WHERE 		Conflict.BreezecardNum = Breezecard.BreezecardNum

-- Assign to New User --
UPDATE Breezecard 
SET BelongsTo = %s 
WHERE BreezecardNum = %s

DELETE FROM Conflict 
WHERE BreezecardNum = %s

-- Assign to Old User --
UPDATE Breezecard 
SET BelongsTo = %s 
WHERE BreezecardNum = %s

DELETE FROM Conflict 
WHERE BreezecardNum = %s

-- Breezecard Management --
SELECT BreezecardNum, Value, BelongsTo 
FROM Breezecard

SELECT BreezecardNum 
FROM Conflict

SELECT DISTINCT BreezecardNum, Value, BelongsTo 
FROM 			Breezecard
WHERE			BelongsTo = thisOwner

-- Transfer Card --
SELECT IsAdmin 
FROM User 
WHERE Username = thisOwner

UPDATE Breezecard 
SET BelongsTo = %s 
WHERE BreezecardNum = %s

-- Card Manage Set Value --
UPDATE Breezecard 
SET Value = %s 
WHERE BreezecardNum = %s




-- Station listing --
SELECT StopID, Name, EnterFare, ClosedStatus,
FROM Station;

-- Suspended cards window --
SELECT Conflict.CardNumber, Conflict.Username, Conflict.DateTime, BreezeCard.Username,
FROM Conflict NATURAL JOIN BreezeCard;

-- At Register -- 
-- The purpose is to validate the input BreezecardNum
SELECT 		BreezecardNum
FROM 		BreezeCard
WHERE 		BreezecardNum = "xxx";

SELECT 		BelongsTo
FROM		Breezecard
WHERE		BreezecardNum = "xxx";

-- Username and Email validation
SELECT		Username
FROM		BreezeCard
WHERE		Username = "xxx";

SELECT 		Email
FROM		BreezeCard
WHERE		Email = "xxx";

-- Flow report --
-- Displays the entire flow report without filter --
SELECT Name AS Station, 
IFNULL(PassengersIn, 0) AS  'Passengers_In', 
IFNULL(PassengersOut, 0) AS  'Passengers_Out',
(IFNULL(PassengersIn, 0) - IFNULL(PassengersOut, 0)) AS Flow,
IFNULL(Revenue, 0) AS Revenue
FROM Station
NATURAL LEFT JOIN (
	SELECT DISTINCT StartsAt AS StopID, 
					COUNT( StartsAt ) AS PassengersIn, 
					SUM( Tripfare ) AS Revenue
	FROM 			Trip
	GROUP BY 		StartsAt
) Passenger_In_Data
NATURAL LEFT JOIN (
	SELECT DISTINCT EndsAt AS StopID, 
					COUNT(EndsAt) AS PassengersOut
	FROM 			Trip
	GROUP BY 		EndsAt
) Passenger_Out_Data
WHERE 	Passenger_In_Data.PassengersIn > 0
OR 		Passenger_Out_Data.PassengersOut > 0

-- Filter flow report according to start time and end time --
SELECT Name AS Station,
IFNULL(PassengersIn, 0) AS  'Passengers_In',
IFNULL(PassengersOut, 0) AS  'Passengers_Out',
(IFNULL(PassengersIn, 0) - IFNULL(PassengersOut, 0)) AS Flow,
IFNULL(Revenue, 0) AS Revenue
FROM Station
NATURAL LEFT JOIN (
SELECT DISTINCT StartsAt AS StopID,
COUNT( StartsAt ) AS PassengersIn,
SUM( Tripfare ) AS Revenue
FROM 			Trip
WHERE Trip.StartTime >= startTime
AND Trip.StartTime <= endTime
GROUP BY 		StartsAt
) Passenger_In_Data
NATURAL LEFT JOIN (
SELECT DISTINCT EndsAt AS StopID,
COUNT(EndsAt) AS PassengersOut
FROM 			Trip
WHERE Trip.StartTime >= startTime
AND Trip.StartTime <= endTime	               
GROUP BY 		EndsAt
) Passenger_Out_Data
WHERE 	Passenger_In_Data.PassengersIn > 0
OR 		Passenger_Out_Data.PassengersOut > 0

-- Passenger Home --
SELECT BreezecardNum 
FROM Breezecard 
WHERE BelongsTo = %s

SELECT BreezecardNum 
FROM Breezecard 
WHERE BelongsTo = %s

SELECT Value 
FROM Breezecard 
WHERE BreezecardNum = %s

SELECT * 
FROM Trip 
WHERE EndsAt is NULL 
AND BreezecardNum = thisCard

-- Passenger Manage Card --
SELECT BreezecardNum, Value 
FROM Breezecard 
WHERE BelongsTo = %s

-- Drop Card --
SELECT BreezecardNum, Value 
FROM Breezecard 
WHERE BelongsTo = %s

SELECT BreezecardNum 
FROM Breezecard 
WHERE BreezecardNum = %s

UPDATE Breezecard 
SET BelongsTo = NULL 
WHERE BreezecardNum = %s

-- Add Card --
SELECT BreezecardNum, Value 
FROM Breezecard 
WHERE BelongsTo = %s

SELECT BreezecardNum, BelongsTo AS Owner 
FROM Breezecard 
WHERE BreezecardNum = %s

INSERT INTO Breezecard 
VALUES(%s, %s, %s)

SELECT BreezecardNum, Value 
FROM Breezecard 
WHERE BelongsTo = %s

UPDATE Breezecard 
SET BelongsTo = %s

INSERT INTO Conflict 
VALUES(%s, %s, %s)

-- Add Value --
SELECT BreezecardNum, Value 
FROM Breezecard 
WHERE BelongsTo = %s

SELECT BreezecardNum 
FROM Breezecard 
WHERE BelongsTo = %s 
AND BreezecardNum = %s

SELECT Value 
FROM Breezecard 
WHERE BreezecardNum = %s

UPDATE Breezecard 
SET Value = %s 
WHERE BreezecardNum = %s

SELECT BreezecardNum, Value 
FROM Breezecard 
WHERE BelongsTo = %s

-- Passenger Start Trip --
SELECT Enterfare 
FROM Station 
WHERE StopId = thisID

INSERT INTO Trip (Tripfare, StartTime, BreezecardNum, StartsAt, EndsAt) 
VALUES (%s, %s, %s, %s, %s)

-- Passenger End Trip --
UPDATE Trip 
SET EndsAt = newEnd
WHERE	BreezecardNum = cardNum

-- Passenger View Trip --
CREATE VIEW SuspendedCards AS
SELECT distinct Breezecard.BreezecardNum AS BreezecardNum 
FROM Breezecard 
NATURAL JOIN Conflict

CREATE VIEW UNSuspendedCards AS 
SELECT distinct Breezecard.BreezecardNum 
FROM Breezecard 
LEFT OUTER JOIN SuspendedCards 
ON Breezecard.BreezecardNum = SuspendedCards.BreezecardNum 
WHERE SuspendedCards.BreezecardNum is NULL

SELECT Tripfare, StartTime, Trip.BreezecardNum AS BreezecardNum, StartsAt, EndsAt 
FROM Trip 
JOIN Breezecard 
ON Trip.BreezecardNum = Breezecard.BreezecardNum 
JOIN UNSuspendedCards 
ON UNSuspendedCards.BreezecardNum = Breezecard.BreezecardNum 
WHERE BelongsTo = %s

DROP VIEW IF EXISTS SuspendedCards

DROP VIEW IF EXISTS UNSuspendedCards

CREATE VIEW SuspendedCards AS 
SELECT distinct Breezecard.BreezecardNum 
AS BreezecardNum 
FROM Breezecard NATURAL JOIN Conflict

CREATE VIEW UNSuspendedCards AS 
SELECT distinct Breezecard.BreezecardNum 
FROM Breezecard 
LEFT OUTER JOIN SuspendedCards 
ON Breezecard.BreezecardNum = SuspendedCards.BreezecardNum 
WHERE SuspendedCards.BreezecardNum is NULL

