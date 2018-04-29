CREATE TABLE User(Username, Password, IsAdmin, PRIMARY KEY(Username));
CREATE TABLE Passenger(Username, Email);
CREATE TABLE Breezecard(BreezecardNum, Value, BelongsTo);
CREATE TABLE Conflict(Username, BreezecardNum, DateTime);
CREATE TABLE Station(StopId, Name, Enterfare, ClosedStatus, IsTrain);
CREATE TABLE Trip(Tripfare, StartTime, BreezecardNum, StartsAt, EndsAt);
CREATE TABLE BusStationIntersection(StopID, Intersection);

INSERT INTO User(Username, Password, IsAdmin) VALUES ('admin', 'a', 1);
INSERT INTO User(Username, Password, IsAdmin) VALUES ('busrider73', 'b', 0);
INSERT INTO Passenger(Username, Email) VALUES ('busrider73', 'lena.wexler@dayrep.com');
INSERT INTO Breezecard(BreezecardNum, Value, BelongsTo) VALUES ('8802558078528210', 42.25, 'busrider73');
INSERT INTO Breezecard(BreezecardNum, Value, BelongsTo) VALUES ('9712526903816770', 68.50, 'busrider73');
INSERT INTO Breezecard(BreezecardNum, Value, BelongsTo) VALUES ('2275718423410130', 168.50, 'commuter14');
INSERT INTO Conflict(Username, BreezecardNum, DateTime) VALUES ('sandrapatel', '9712526903816770', '11/12/2018 12:00:01 AM');
INSERT INTO Station(StopId, Name, Enterfare, ClosedStatus, IsTrain) VALUES ('N11','North Springs',2.50,0,1);
INSERT INTO Station(StopId, Name, Enterfare, ClosedStatus, IsTrain) VALUES ('BUSN11','North Springs',2.00,0,0);
INSERT INTO BusStationIntersection(StopID, Intersection) VALUES ('BUSN11','Peachtree-Dunwoody Road');
INSERT INTO Trip(Tripfare, StartTime, BreezecardNum, StartsAt, EndsAt) VALUES (2.75,'11/05/2017 04:21:49 PM','0524807425551662','N11','N4');
INSERT INTO Trip(Tripfare, StartTime, BreezecardNum, StartsAt, EndsAt) VALUES (2.75,'11/05/2017 04:21:49 PM','0524807425551662','N5','N11');
INSERT INTO Trip(Tripfare, StartTime, BreezecardNum, StartsAt, EndsAt) VALUES (2.75,'11/05/2017 04:21:49 PM','0524807425551662','N5','N4');

