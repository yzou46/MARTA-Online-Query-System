from flask import Flask, render_template, request, session, redirect, url_for
import pymysql 
import re
import bcrypt
from random import randint

## hash 

#mhash = hashlib.md5()
app = Flask(__name__)
## connect to database 
conn = pymysql.connect(host='academic-mysql.cc.gatech.edu',
                       user='cs4400_Group_97',
                       passwd='zWtTC8dv',
                       db='cs4400_Group_97')
app.secret_key = 'Baga Desu'
import time
import datetime

salt = bcrypt.gensalt()
@app.route('/')
def home():
   
   #return redirect(url_for('login'))
   return render_template('home.html')

@app.route('/login/', methods=['GET', 'POST'])
def login():
   session['login_status'] = 0
   session['login_userName'] = ''
   error = None
   print (request.method)
   if request.method == 'POST':
      username = request.form['username']
      password = request.form['password']
      #password_str = password.decode('utf-8')
      #salt = bcrypt.gensalt()
      #hashed = bcrypt.hashpw(password.encode('utf8'), salt)
      #mhash.update(password_str)
      #mhash.digest_size = 4
      #hashed_password = mhash.hexdigest()
      print (username, password)
      #hashed = hash(str(password))
      cur = conn.cursor()
      print ("Opened database successfully")
      cur.execute("SELECT * FROM User WHERE Username = %s", username)
      result = cur.fetchall()
      #conn.close()
      print ("result fetched")
      if not result:
         error = 'Invalid username'
      elif bcrypt.hashpw(password.encode('utf8'), result[0][1]) != result[0][1]: #hashed_password != result[0][1]:
         print("hashed password")
         print(result[0][1])
         print(password)
         error = 'Invalid password'
      else:
         session['login_status'] = result[0][2] + 1
         session['login_userName'] = result[0][0]
         if result[0][2] == 0:
            session['passengerThisCard'] = ''
            print ("redirect to passenger_home")
            return redirect(url_for('passenger_home'))
         else:
            print ("redirect to admin_home")
            return redirect(url_for('admin_home'))
   return render_template('login.html', error=error)


def generateCardNumber():
   ## function to generate 16 digits card number 
   prefix = 3141592653580000 ## 16 digits 
   thousandth = randint(0,9)*1000
   hundredth = randint(0,9)*100
   tenth = randint(0,9)*10
   lsb = randint(0,9)
   cardnumber = prefix+thousandth+hundredth+tenth+lsb
   return str(cardnumber) 


## not finished 
@app.route('/register',methods=['GET', 'POST'])
def register():
   session['login_status'] = 0
   session['login_userName'] = ''
   error = None
   print (request.method)
   if request.method == 'POST':
      username = request.form['username']
      email = request.form['email']
      password1 = request.form['passwordone']
      password2 = request.form['passwordtwo']
      breezecard = request.form['breezecard']
      cardnumber = "" ## breezecard number 
      
      hashed = bcrypt.hashpw(password1.encode('utf8'), salt)
      #password_str = password1.decode('utf-8')
      #mhash.update(password_str)
      #mhash.digest_size = 4
      #hashed_password = mhash.hexdigest()
      ## null value 
      if not username:
         return render_template('register.html', error='Please input valid username')
      if not email:
         return render_template('register.html', error='Please input valid email')
      if not password1:
         return render_template('register.html', error='Please input valid password')
      ## regular expression 
      if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",email):
         return render_template('register.html', error = 'Please input valid email')
      print (username, password1, password2)

      ## integratity check 

      ## password1 and password2 check done in html file 
      cur = conn.cursor()
      print ("Opened database successfully")
      ## breezecard number 
      if breezecard == "old":
         cardnumber = request.form['cardnumber']
         cur.execute("SELECT BreezecardNum FROM Breezecard WHERE BreezecardNum = %s",cardnumber)
         result = cur.fetchall()
         ## validate breezecard here 
         if not result:
            return render_template('register.html', error="Breezecard does not exist")
         '''
         cur.execute("SELECT BelongsTo FROM Breezecard WHERE BreezecardNum = %s",cardnumber)
         result = cur.fetchall()
         if result is "" or username in result:
            print("valid breezecard")
         else:
            return render_template('register.html', error="Breezecard belongs to other people")
      '''
      else:
         ## generate new card from database 
         cardnumber = generateCardNumber()
         cur = conn.cursor()
         cur.execute("SELECT BreezecardNum FROM Breezecard")
         result = cur.fetchall()
         ## avoid duplication 
         while(cardnumber in result):
            cardnumber = generateCardNumber()

      ## username and email validation 
      cur.execute("SELECT Username FROM User WHERE Username = %s", username)
      result = cur.fetchall()
      #conn.close()
      print ("result fetched")
      if result:
         error = 'username existed, please choose another name'
         return render_template('register.html', error=error)
      # check email duplication 
      cur.execute("SELECT Email FROM Passenger WHERE Email = %s", email)
      result = cur.fetchall()
      if result:
         error = 'email existed, please choose another one'
         return render_template('register.html', error=error)
      print(cardnumber)
      ## not consider conflict table 
      if breezecard == "new":
         ## store the record in the database 
         queryString1 = "INSERT INTO User VALUES(%s, %s, %s)"
         cur.execute(queryString1, [username, hashed,0])
         ##conn.commit()
         cur.close()
         conn.commit()
         queryString2 = "INSERT INTO Passenger VALUES(%s, %s)"
         cur = conn.cursor()
         cur.execute(queryString2,[username,email])
         cur.close()
         conn.commit()
         queryString3 = "INSERT INTO Breezecard VALUES(%s, %s, %s)"
         cur=conn.cursor()
         cur.execute(queryString3,[cardnumber,0,username])
         cur.close()
         conn.commit()
      else:
         ## store the record in the database 
         ## Attention: need extra step to check whether this card belongs to this user 
         queryString1 = "INSERT INTO User VALUES(%s, %s, %s)"
         cur.execute(queryString1, [username, hashed,0])
         cur.close()
         conn.commit()
         queryString2 = "INSERT INTO Passenger VALUES(%s, %s)"
         cur = conn.cursor()
         cur.execute(queryString2,[username,email])
         cur.close()
         conn.commit()
         format = '%Y-%m-%d %H:%M:%S'
         currentTimeString = datetime.datetime.now().strftime(format)
         queryString3 = "INSERT INTO Conflict VALUES(%s, %s, %s)"#" SET BelongsTo = %s where BreezecardNum = %s"
         #queryString3 = "UPDATE Breezecard SET BelongsTo = %s where BreezecardNum = %s"
         cur = conn.cursor()
         cur.execute(queryString3,[username, cardnumber,currentTimeString])
         #queryString4 = ""
         cur.close()
         conn.commit()
      return redirect(url_for('newAccount'))
   return render_template('register.html', error=error)

@app.route('/newAccount/')
def newAccount():
   
   return render_template('login.html')

@app.route('/admin_home')
def admin_home():
   if session['login_status'] != 2:
      return render_template('login.html', error='Please login first')
   session['BreezeCardManagementNumber'] = ''
   session['BreezeCardManagementOwner'] = ''
   session['BreezeCardManagementLower'] = ''
   session['BreezeCardManagementUpper'] = ''
   session['BreezeCardManagementSuspendended'] = 1
   session['BreezePassengerFlowStart'] = ''
   session['BreezePassengerFlowEnd'] = ''
   return render_template('admin_home.html')

@app.route('/logout/')
def logout():
   session['login_status'] = 0
   session['login_userName'] = ''
   error = ""
   return render_template('login.html', error=error)


@app.route('/StationManagement/', methods=['GET', 'POST'])
def StationManagement():
   if session['login_status'] != 2:
      return render_template('login.html', error='Please login first')
   
   if request.method == 'POST':
      thisStopID = request.form['StopID']
      session['currentStopID'] = thisStopID
      #conn = sql.connect('database.db')
      #conn.row_factory = pymysql.Row
      cur = conn.cursor()
      sqlStr = 'SELECT * FROM Station where StopId = \'' + thisStopID + '\''
      print (sqlStr)
      cur.execute(sqlStr)
      result = cur.fetchall()
      session['currentStopIsTrain'] = result[0][4]
      if result[0][4] == 0:
         cur.execute("SELECT Intersection from BusStation where StopId = \'" + thisStopID + '\'')
         intersectionArg = cur.fetchall()
         if not intersectionArg:
            intersection = ''
         else:
            intersection = intersectionArg[0][0]
      else:
         intersection = ''

      if result[0][3] == 0:
         x = 'Open'
      else:
         x = 'Close'

      return render_template('ViewStationDetail.html', x = x, info = result[0], intersection = intersection)
   
   
   session['currentStopID'] = ''
   session['currentStopIsTrain'] = 0
   #conn = sql.connect('database.db')
   #conn.row_factory = sql.Row
   cur = conn.cursor()
   cur.execute("SELECT StopID,Name,EnterFare,ClosedStatus,IsTrain FROM Station")
   result = cur.fetchall()
   print (result)
   return render_template('StationManagement.html', rows = result)

#StationManagement
@app.route('/CreateNewStation/', methods=['GET', 'POST'])
def CreateNewStation():
   if session['login_status'] != 2:
      return render_template('login.html', error='Please login first')
   print ("CreateNewStation",request.method)
   if request.method == 'POST':
      thisStationName = request.form['StationName']
      thisStopID = request.form['StopID']
      thisFare = request.form['Fare']
      thisIsTrain = request.form['isTrain']

      ## validate input 
      if thisStationName == "":
         return render_template('CreateNewStation.html', error = "Input valid station name")
      if thisStopID == "":
         return render_template('CreateNewStation.html', error = "Input valid stop ID")
      if thisFare == "":
         return render_template('CreateNewStation.html', error = "Input valid fare between 0 and 50")
      num_fare = float(thisFare)
      print(thisFare, num_fare)
      if num_fare < 0 or num_fare > 50:
         print("here fare wrong")
         return render_template('CreateNewStation.html', error = "Input valid fare between 0 and 50")
      ## check station Name and stopID 
      cur = conn.cursor()
      cur.execute("SELECT Name from Station where Name = %s AND IsTrain = %s", [thisStationName, int(thisIsTrain)])
      result = cur.fetchall()
      if not result:
         print("valid station name")
      else:
         return render_template('CreateNewStation.html', error = "Station Name existed")

      cur.execute("SELECT StopID from Station where StopID = %s", thisStopID)
      result = cur.fetchall()
      if not result:
         print("valid stop ID")
      else:
         return render_template('CreateNewStation.html', error = "Stop ID existed")


      if thisIsTrain == 1:
         thisIntersection = ''
      else:
         thisIntersection = request.form['Intersection']
      thisClosed = request.form['Closed']
      #conn = sql.connect('database.db')
      cur = conn.cursor()
      print ("CreateNewStation, database connected successfully")
      cur.execute("INSERT INTO Station (StopId, Name, Enterfare, ClosedStatus, IsTrain) VALUES (%s, %s, %s, %s, %s)", [thisStopID, thisStationName, thisFare,thisClosed, thisIsTrain])
      conn.commit()
      if thisIsTrain == 0:
         print ("CreateNewStation this is a BusStationIntersection")
         cur.execute("INSERT INTO BusStationIntersection(StopID, Intersection) VALUES (%s, %s)", [thisStopID, thisIntersection])
         conn.commit()
      #conn.close()
      return redirect(url_for('StationManagement'))
   return render_template('CreateNewStation.html')

@app.route('/ViewStationDetail/', methods=['GET', 'POST'])
def ViewStationDetail():
   if session['login_status'] != 2:
      return render_template('login.html', error='Please login first') 

   if request.method == 'POST':
      thisFare = request.form['fare']
      thisIntersection = request.form['Intersection']
      thisClosed = request.form['Closed']
      cur = conn.cursor()
      if thisFare != '':
         cur.execute("UPDATE Station SET Enterfare = %s WHERE StopId = %s", [thisFare, session['currentStopID']])
         conn.commit()
      if session['currentStopIsTrain'] == 0 and thisIntersection != '':
         cur.execute("UPDATE BusStation SET Intersection = %s WHERE StopID = %s", [thisIntersection, session['currentStopID']])
         conn.commit()
      cur.execute("UPDATE Station SET ClosedStatus = %s WHERE StopId = %s", [thisClosed, session['currentStopID']])
      return redirect(url_for('StationManagement'))

@app.route('/SuspendedCards/', methods=['GET', 'POST'])
def SuspendedCards():
   if session['login_status'] != 2:
      return render_template('login.html', error='Please login first')
   #conn = sql.connect('database.db')
   #conn.row_factory = sql.Row
   cur = conn.cursor()
   cur.execute("SELECT Conflict.Username as New_Owner, Conflict.BreezecardNum as Card, Conflict.DateTime as DTime, Breezecard.BelongsTo as Old_Owner FROM Conflict, Breezecard WHERE Conflict.BreezecardNum = Breezecard.BreezecardNum")
   result = cur.fetchall()
   return render_template('SuspendedCards.html', rows = result)


@app.route('/AssignToNew/', methods=['GET', 'POST'])
def AssignToNew():
   if session['login_status'] != 2:
      return render_template('login.html', error='Please login first')
   
   thisUser = request.form['User']
   thisCard = request.form['Card']
   #conn = sql.connect('database.db')
   cur = conn.cursor()
   cur.execute("UPDATE Breezecard SET BelongsTo = %s WHERE BreezecardNum = %s", [thisUser, thisCard])
   conn.commit()
   cur.execute("DELETE FROM Conflict WHERE BreezecardNum = %s", thisCard)
   conn.commit()
   #conn.close()
   return redirect(url_for('SuspendedCards'))


@app.route('/AssignToOld/', methods=['GET', 'POST'])
def AssignToOld():
   if session['login_status'] != 2:
      return render_template('login.html', error='Please login first')
   print ("!!!!!AssignToOld")
   thisUser = request.form['User']
   thisCard = request.form['Card']
   #conn = sql.connect('database.db')
   cur = conn.cursor()
   cur.execute("UPDATE Breezecard SET BelongsTo = %s WHERE BreezecardNum = %s", [thisUser, thisCard])
   cur = conn.cursor()
   cur.execute("DELETE FROM Conflict WHERE BreezecardNum = %s", thisCard)
   conn.commit()
   #conn.close()
   return redirect(url_for('SuspendedCards'))


@app.route('/BreezeCardManagement/<error>', methods=['GET', 'POST'])
def BreezeCardManagement(error):
   if session['login_status'] != 2:
      return render_template('login.html', error='Please login first')
   if error == 'default':
      error = ''
   if request.method == 'GET':
      session['BreezeCardManagementNumber'] = ''
      session['BreezeCardManagementOwner'] = ''
      session['BreezeCardManagementLower'] = ''
      session['BreezeCardManagementUpper'] = ''
      session['BreezeCardManagementSuspendended'] = 1
      #conn = sql.connect('database.db')
      #conn.row_factory = sql.Row
      
      cur = conn.cursor()
      '''
      cur.execute("DROP TABLE IF EXISTS TEMP_CARD")
      conn.commit()
      cur.execute("CREATE TABLE TEMP_CARD AS SELECT BreezecardNum, Value, BelongsTo FROM Breezecard")
      conn.commit()
      cur.execute("UPDATE TEMP_CARD AS T SET BelongsTo = %s WHERE EXISTS (SELECT BreezecardNum FROM Conflict AS C WHERE T.BreezecardNum= C.BreezecardNum)", "Suspended")
      conn.commit()
      cur.execute("SELECT BreezecardNum,Value,BelongsTo FROM TEMP_CARD")
      result = cur.fetchall()
      cur.execute("DROP TABLE TEMP_CARD")
      conn.commit()
      '''
      cur = conn.cursor()
      cur.execute("SELECT BreezecardNum, Value, BelongsTo FROM Breezecard")
      result = cur.fetchall()
      cur.execute("SELECT BreezecardNum FROM Conflict")
      sus = cur.fetchall()
      cur.close()
      #conn.close()

  ## 
      re = []
      new_result = ()
      print(result[0])
      print(list(result[0]))
      for row in result:
      #print (row)
         row_list = list(row)
         #print(row_list)
         for card in sus:
            if row_list[0] == card[0]:
               row_list[2] = "Suspended"
               print("sus")
               print(row_list)
         re.append(row_list)
   #print(re)
      new_result = tuple(re)
      for row in new_result:
         row = tuple(row)
      #print(new_result)
      print(sus)
      rows = new_result
      #cookies part
      cks =[session['BreezeCardManagementNumber'],session['BreezeCardManagementOwner'],session['BreezeCardManagementLower'],session['BreezeCardManagementUpper']]
      return render_template('BreezeCardManagement.html', rows=rows, ck=cks, error = error)

   if request.method == 'POST':
      print ("POOOOOOOOOOOOst")
      thisOwner = request.form['Username']
      thisNumber = request.form['Card']
      thisLower = request.form['LowerValue']
      thisUpper = request.form['UpperValue']
      thisSuspendened = request.form['Suspended']
      session['BreezeCardManagementNumber'] = thisNumber
      session['BreezeCardManagementOwner'] = thisOwner
      session['BreezeCardManagementLower'] = thisLower
      session['BreezeCardManagementUpper'] = thisUpper
      session['BreezeCardManagementSuspendended'] = thisSuspendened
      
      cur = conn.cursor()
      #cur = conn.cursor()
      '''
      cur.execute("DROP TABLE IF EXISTS TEMP_CARD")
      conn.commit()
      cur.execute("CREATE TABLE TEMP_CARD AS SELECT BreezecardNum, Value, BelongsTo FROM Breezecard")
      conn.commit()
      cur.execute("UPDATE TEMP_CARD AS T SET BelongsTo = %s WHERE EXISTS (SELECT BreezecardNum FROM Conflict AS C WHERE T.BreezecardNum= C.BreezecardNum)", "Suspended")
      conn.commit()
      cur.execute("SELECT BreezecardNum,Value,BelongsTo FROM TEMP_CARD")
      '''
      #form string
      queryString = "SELECT DISTINCT BreezecardNum, Value, BelongsTo FROM Breezecard"
      attributes = ['BelongsTo = ', 'BreezecardNum = ', 'Value >= ', 'Value <= ']
      thisStrings = ['\'' + thisOwner + '\'', '\'' + thisNumber + '\'', thisLower, thisUpper]
      array = []
      if thisOwner != '':
         array.append(0)
      if thisNumber != '':
         array.append(1)
      if thisLower != '':
         array.append(2)
      if thisUpper != '':
         array.append(3)
      for i in range(len(array)):
         if i == 0:
            queryString = queryString + " WHERE " + attributes[array[0]] + thisStrings[array[0]]
         else:
            queryString = queryString + " and " + attributes[array[i]] + thisStrings[array[i]]
      cur = conn.cursor()
      print(queryString)
      cur.execute(queryString)
      result = cur.fetchall()
      new_result = ()
      if thisSuspendened == "yes":
         cur.execute("SELECT BreezecardNum FROM Conflict")
         sus = cur.fetchall()
         re = []
         
         #print(result[0])
         #print(list(result[0]))
         for row in result:
         #print (row)
            row_list = list(row)
            #print(row_list)
            for card in sus:
               if row_list[0] == card[0]:
                  row_list[2] = "Suspended"
                  print("sus")
                  print(row_list)
                  re.append(row_list)
      #print(re)
         new_result = tuple(re)
         for row in new_result:
            row = tuple(row)
            #print(new_result)
         print(sus)
      else:
         sus = []
      cur.close()
      #conn.close()

  ##  
      
      if thisSuspendened == "yes": 
         rows = new_result
      else:
         rows = result
      cur.close()
      #conn.close()

      cks =[session['BreezeCardManagementNumber'],session['BreezeCardManagementOwner'],session['BreezeCardManagementLower'],session['BreezeCardManagementUpper'], session['BreezeCardManagementSuspendended']]
      
      return render_template('BreezeCardManagement.html', rows=rows, ck=cks, error = error)



@app.route('/TransferCard/', methods=['GET', 'POST'])
def TransferCard():
   if session['login_status'] != 2:
      return render_template('login.html', error='Please login first')
   session['BreezeCardManagementNumber'] = ''
   session['BreezeCardManagementOwner'] = ''
   session['BreezeCardManagementLower'] = ''
   session['BreezeCardManagementUpper'] = ''
   session['BreezeCardManagementSuspendended'] = 1
   thisOwner = request.form['Owner']
   thisNumber = request.form['Card']
   #conn = sql.connect('database.db')
   cur = conn.cursor()
   print (thisOwner)
   print ('SELECT IsAdmin FROM User WHERE Username = \'' + thisOwner + '\'')

   ## data validation, cannot assign to admin user or the user has to be existed 
   cur.execute("SELECT IsAdmin FROM User WHERE Username = %s" ,thisOwner)
   temp = cur.fetchall()
   print (temp)
   if not temp:
      return redirect(url_for('BreezeCardManagement', error = "User does not exist"))

   if temp[0][0] == 1:
      return redirect(url_for('BreezeCardManagement', error = "Cannot assign to admin user"))
   print ('UPDATE SUSSSS')

   
   
   cur.execute("UPDATE Breezecard SET BelongsTo = %s WHERE BreezecardNum = %s", [thisOwner, thisNumber])
   conn.commit()
   #conn.close()
   return redirect(url_for('BreezeCardManagement', error = "default"))



@app.route('/CardManageSetValue/', methods=['GET', 'POST'])
def CardManageSetValue():
   if session['login_status'] != 2:
      return render_template('login.html', error='Please login first')
   thisValue = float(request.form['Value'])
   thisNumber = request.form['Card']

   if thisValue > 1000:
      return redirect(url_for('BreezeCardManagement', error = "Invalid Value Assigned, should < 1000"))
   #conn = sql.connect('database.db')
   cur = conn.cursor()
   cur.execute("UPDATE Breezecard SET Value = %s WHERE BreezecardNum = %s", [thisValue, thisNumber])
   conn.commit()
   #conn.close()
   session['BreezeCardManagementNumber'] = ''
   session['BreezeCardManagementOwner'] = ''
   session['BreezeCardManagementLower'] = ''
   session['BreezeCardManagementUpper'] = ''
   session['BreezeCardManagementSuspendended'] = 1
   return redirect(url_for('BreezeCardManagement', error = "default"))


@app.route('/PassengerFlow/', methods=['GET', 'POST'])
def PassengerFlow():
   if session['login_status'] != 2:
      return render_template('login.html', error='Please login first')
   if request.method == 'GET':
      session['BreezePassengerFlowStart'] = ''
      session['BreezePassengerFlowEnd'] = ''
      cur = conn.cursor()

      cur.execute("SELECT Name AS Station,\
                   IFNULL(PassengersIn, 0) AS  'Passengers_In',\
                   IFNULL(PassengersOut, 0) AS  'Passengers_Out',\
                  (IFNULL(PassengersIn, 0) - IFNULL(PassengersOut, 0)) AS Flow,\
                   IFNULL(Revenue, 0) AS Revenue\
                   FROM Station\
                   NATURAL LEFT JOIN (\
	               SELECT DISTINCT StartsAt AS StopID,\
				   COUNT( StartsAt ) AS PassengersIn,\
				   SUM( Tripfare ) AS Revenue\
	               FROM 			Trip\
	               GROUP BY 		StartsAt\
                  ) Passenger_In_Data\
                  NATURAL LEFT JOIN (\
	              SELECT DISTINCT EndsAt AS StopID,\
				  COUNT(EndsAt) AS PassengersOut\
	              FROM 			Trip\
	              GROUP BY 		EndsAt\
                  ) Passenger_Out_Data\
                  WHERE 	Passenger_In_Data.PassengersIn > 0\
                  OR 		Passenger_Out_Data.PassengersOut > 0")
      conn.commit()

      result = cur.fetchall()

      cks = [session['BreezePassengerFlowStart'], session['BreezePassengerFlowEnd']]
      return render_template('PassengerFlow.html', rows = result, ck = cks)

   if request.method == 'POST':
      thisStart = request.form['Start']
      thisEnd = request.form['End']
      print ("passenger flow", thisStart, thisEnd)
      session['BreezePassengerFlowStart'] = thisStart
      session['BreezePassengerFlowEnd'] = thisEnd
      cur = conn.cursor()


      cur.execute("SELECT Name AS Station,\
                   IFNULL(PassengersIn, 0) AS  'Passengers_In',\
                   IFNULL(PassengersOut, 0) AS  'Passengers_Out',\
                  (IFNULL(PassengersIn, 0) - IFNULL(PassengersOut, 0)) AS Flow,\
                   IFNULL(Revenue, 0) AS Revenue\
                   FROM Station\
                   NATURAL LEFT JOIN (\
	               SELECT DISTINCT StartsAt AS StopID,\
				   COUNT( StartsAt ) AS PassengersIn,\
				   SUM( Tripfare ) AS Revenue\
	               FROM 			Trip\
	               GROUP BY 		StartsAt\
                  ) Passenger_In_Data\
                  NATURAL LEFT JOIN (\
	              SELECT DISTINCT EndsAt AS StopID,\
				  COUNT(EndsAt) AS PassengersOut\
	              FROM 			Trip\
	              GROUP BY 		EndsAt\
                  ) Passenger_Out_Data\
                  WHERE 	Passenger_In_Data.PassengersIn > 0\
                  OR 		Passenger_Out_Data.PassengersOut > 0")
      conn.commit()

      if thisStart == '' and thisEnd == '':
      	cur.execute("SELECT Name AS Station,\
                   IFNULL(PassengersIn, 0) AS  'Passengers_In',\
                   IFNULL(PassengersOut, 0) AS  'Passengers_Out',\
                  (IFNULL(PassengersIn, 0) - IFNULL(PassengersOut, 0)) AS Flow,\
                   IFNULL(Revenue, 0) AS Revenue\
                   FROM Station\
                   NATURAL LEFT JOIN (\
	               SELECT DISTINCT StartsAt AS StopID,\
				   COUNT( StartsAt ) AS PassengersIn,\
				   SUM( Tripfare ) AS Revenue\
	               FROM 			Trip\
	               GROUP BY 		StartsAt\
                  ) Passenger_In_Data\
                  NATURAL LEFT JOIN (\
	              SELECT DISTINCT EndsAt AS StopID,\
				  COUNT(EndsAt) AS PassengersOut\
	              FROM 			Trip\
	              GROUP BY 		EndsAt\
                  ) Passenger_Out_Data\
                  WHERE 	Passenger_In_Data.PassengersIn > 0\
                  OR 		Passenger_Out_Data.PassengersOut > 0")
      elif thisStart != ''  and thisEnd == '':
          s = "SELECT Name AS Station,\
      	       IFNULL(PassengersIn, 0) AS  'Passengers_In',\
      	       IFNULL(PassengersOut, 0) AS  'Passengers_Out',\
      	       (IFNULL(PassengersIn, 0) - IFNULL(PassengersOut, 0)) AS Flow,\
      	        IFNULL(Revenue, 0) AS Revenue\
      	        FROM Station\
      	        NATURAL LEFT JOIN (\
      	        SELECT DISTINCT StartsAt AS StopID,\
      	        COUNT( StartsAt ) AS PassengersIn,\
      	        SUM( Tripfare ) AS Revenue\
      	        FROM 			Trip\
      	        WHERE Trip.StartTime >= " + '\'' + thisStart + '\'' + \
              "GROUP BY 		StartsAt\
              ) Passenger_In_Data\
              NATURAL LEFT JOIN (\
              SELECT DISTINCT EndsAt AS StopID,\
              COUNT(EndsAt) AS PassengersOut\
              FROM 			Trip\
              WHERE Trip.StartTime >= " + '\'' + thisStart + '\'' + \
              "GROUP BY 		EndsAt\
              ) Passenger_Out_Data\
              WHERE 	Passenger_In_Data.PassengersIn > 0\
              OR 		Passenger_Out_Data.PassengersOut > 0"
          cur.execute(s)
      elif thisStart == ''  and thisEnd != '':
          s = "SELECT Name AS Station,\
                       IFNULL(PassengersIn, 0) AS  'Passengers_In',\
                           IFNULL(PassengersOut, 0) AS  'Passengers_Out',\
                          (IFNULL(PassengersIn, 0) - IFNULL(PassengersOut, 0)) AS Flow,\
                           IFNULL(Revenue, 0) AS Revenue\
                           FROM Station\
                           NATURAL LEFT JOIN (\
        	               SELECT DISTINCT StartsAt AS StopID,\
        				   COUNT( StartsAt ) AS PassengersIn,\
        				   SUM( Tripfare ) AS Revenue\
        	               FROM 			Trip\
                           WHERE Trip.StartTime <= " + '\'' + thisEnd + '\'' + \
                          "GROUP BY 		StartsAt\
                          ) Passenger_In_Data\
                          NATURAL LEFT JOIN (\
                          SELECT DISTINCT EndsAt AS StopID,\
                          COUNT(EndsAt) AS PassengersOut\
                          FROM 			Trip\
                          WHERE Trip.StartTime <= " + '\'' + thisEnd + '\'' + \
                          "GROUP BY 		EndsAt\
                          ) Passenger_Out_Data\
                          WHERE 	Passenger_In_Data.PassengersIn > 0\
                          OR 		Passenger_Out_Data.PassengersOut > 0"
          cur.execute(s)
      else:
        s = "SELECT Name AS Station,\
               IFNULL(PassengersIn, 0) AS  'Passengers_In',\
                   IFNULL(PassengersOut, 0) AS  'Passengers_Out',\
                  (IFNULL(PassengersIn, 0) - IFNULL(PassengersOut, 0)) AS Flow,\
                   IFNULL(Revenue, 0) AS Revenue\
                   FROM Station\
                   NATURAL LEFT JOIN (\
	               SELECT DISTINCT StartsAt AS StopID,\
				   COUNT( StartsAt ) AS PassengersIn,\
				   SUM( Tripfare ) AS Revenue\
	               FROM 			Trip\
                   WHERE Trip.StartTime >= " + '\'' + thisStart + '\'' + \
                   " AND Trip.StartTime <= " + '\'' + thisEnd + '\'' + \
                   "GROUP BY 		StartsAt\
                   ) Passenger_In_Data\
                   NATURAL LEFT JOIN (\
                   SELECT DISTINCT EndsAt AS StopID,\
                   COUNT(EndsAt) AS PassengersOut\
                   FROM 			Trip\
                   WHERE Trip.StartTime >= "  + '\'' + thisStart + '\'' +\
                   " AND Trip.StartTime <= " + '\'' + thisEnd + '\'' +\
	               "GROUP BY 		EndsAt\
                   ) Passenger_Out_Data\
                   WHERE 	Passenger_In_Data.PassengersIn > 0\
                   OR 		Passenger_Out_Data.PassengersOut > 0"
        cur.execute(s)
      result = cur.fetchall()

      cks = [session['BreezePassengerFlowStart'], session['BreezePassengerFlowEnd']]
      print(result)
      return render_template('PassengerFlow.html', rows = result, ck = cks)

@app.route('/passenger_home', methods=['GET', 'POST'])
def passenger_home():
   if session['login_status'] != 1:
      return render_template('login.html', error='Please login first')
   
   if request.method == 'GET':
      cks={}
      cur = conn.cursor()
      if session['passengerThisCard'] == '':
         cur.execute("SELECT BreezecardNum from Breezecard WHERE BelongsTo = %s", session['login_userName'])
         temp = cur.fetchone()
         if not temp:
            thisCard = ''
         else:
            thisCard = temp[0]
      else:
         thisCard = session['passengerThisCard']
      cur.execute("SELECT BreezecardNum from Breezecard WHERE BelongsTo = %s", session['login_userName'])
      Cards = cur.fetchall() 
      print (thisCard)
      if thisCard != '':
         cur.execute("SELECT Value from Breezecard WHERE BreezecardNum = %s", thisCard)
         value = cur.fetchone()[0]
      else:
         value = ''
      cks["CardNumber"] = thisCard
      cur.execute("SELECT * FROM Trip WHERE EndsAt is NULL and BreezecardNum = \'" + thisCard + '\'')
      temp = cur.fetchall()
      if not temp:
         inTrip = False
         StartStation = ""
      else:
         inTrip = True
         StartStation = temp[0][3]
      cks["CardInTrip"] = inTrip
      cks["StartStation"] = StartStation
      cur.execute("SELECT Name, StopID FROM Station")
      Stations = cur.fetchall()
      session['passengerThisCard'] = thisCard
      print (session['passengerThisCard'])
      return render_template('passenger_home.html', Cards=Cards, cks = cks, value = value, Stations=Stations)
      
   if request.method == 'POST':
      thisCard = request.form.get('Cards')
      cks={}
      cur = conn.cursor()
      cur.execute("SELECT BreezecardNum from Breezecard WHERE BelongsTo = %s", session['login_userName'])
      Cards = cur.fetchall() 
      cur.execute("SELECT Value from Breezecard WHERE BreezecardNum = %s", thisCard)
      value = cur.fetchone()[0]
      cks["CardNumber"] = thisCard
      cur.execute("SELECT * FROM Trip WHERE EndsAt is NULL and BreezecardNum = \'" + thisCard + '\'')
      temp = cur.fetchall()
      if not temp:
         inTrip = False
      else:
         inTrip = True
      cks["CardInTrip"] = inTrip
      if inTrip:
         StartStation = temp[0][3]
      else:
         StartStation = ""
      cks["StartStation"] = StartStation
      cur.execute("SELECT Name, StopID FROM Station")
      Stations = cur.fetchall()
      session['passengerThisCard'] = thisCard
      return render_template('passenger_home.html', Cards=Cards, cks = cks, value = value, Stations=Stations)



@app.route('/passengerManageCard/<error>', methods=['GET', 'POST'])
def passengerManageCard(error):
   if session['login_status'] != 1:
      return render_template('login.html', error='Please login first')
   if error == 'default':
      error = ''
   #conn = sql.connect('database.db')
   #conn.row_factory = sql.Row
   cur = conn.cursor()
   cur.execute("SELECT BreezecardNum, Value from Breezecard WHERE BelongsTo = %s", session['login_userName'])
   rows = cur.fetchall()
   #rows = rows[:][1:-2]
   return render_template('passengerManageCard.html', rows = rows, error = error)
   
@app.route('/DropCard', methods=['GET', 'POST'])
def DropCard():
   if session['login_status'] != 1:
      return render_template('login.html', error='Please login first')
   thisCard = request.form.get('Card')
   
   if request.method == 'POST':
      cur = conn.cursor()
      cur.execute("SELECT BreezecardNum, Value from Breezecard WHERE BelongsTo = %s", session['login_userName'])
      rows = cur.fetchall()
      if thisCard == "":
         return redirect(url_for('passengerManageCard', rows = rows, error = "Please input breezecard number"))
      ## check card 
      cur = conn.cursor()
      cur.execute("SELECT BreezecardNum FROM Breezecard WHERE BreezecardNum = %s", thisCard)
      result = cur.fetchall()
      if not result:
         return redirect(url_for('passengerManageCard', rows = rows, error = "This breezecard does not exist in our system, please check your breezecard number"))
      #conn = sql.connect('database.db')
      cur = conn.cursor()
      cur.execute("UPDATE Breezecard SET BelongsTo = NULL WHERE BreezecardNum = %s", thisCard)
      conn.commit()
      return redirect(url_for('passengerManageCard', rows = rows, error = "default"))
   
@app.route('/AddCard', methods=['GET', 'POST'])
def AddCard():
   if session['login_status'] != 1:
      return render_template('login.html', error='Please login first')
   thisCard = request.form['Card']
   #conn = sql.connect('database.db')
   if request.method == 'POST':
      ## validate card 
      cur = conn.cursor()
      cur.execute("SELECT BreezecardNum, Value from Breezecard WHERE BelongsTo = %s", session['login_userName'])
      rows = cur.fetchall()
      if thisCard == "":
         return redirect(url_for('passengerManageCard', rows = rows, error = "Breezecard number cannot be empty"))
      cur = conn.cursor()
      cur.execute("SELECT BreezecardNum, BelongsTo as Owner FROM Breezecard WHERE BreezecardNum = %s", thisCard)
      result = cur.fetchall()
      print(result)
      if not result: 
         cardnumber = thisCard
         print (cardnumber)
         if len(cardnumber) != 16:
            return redirect(url_for('passengerManageCard', rows = rows, error = "Breezecard number must be 16 digits long"))
            #return passengerManageCard('default')
         else:
            ## this card does not in the database, store it and set initial value to 0
            cur.execute("INSERT INTO Breezecard VALUES(%s, %s, %s)", [thisCard, 0, session['login_userName']])
            conn.commit()
            cur = conn.cursor()
            cur.execute("SELECT BreezecardNum, Value from Breezecard WHERE BelongsTo = %s", session['login_userName'])
            rows = cur.fetchall()
            return redirect(url_for('passengerManageCard', rows = rows, error = "default"))
      else:
         ## this card is already in use 
         thisUser = result[0][1]
         print(thisUser)
         print(session['login_userName'])
         if not thisUser:
            #print()
            cur.execute("UPDATE Breezecard SET BelongsTo = %s WHERE BreezecardNum = %s", [session['login_userName'], thisCard])
            conn.commit()
            cur = conn.cursor()
            cur.execute("SELECT BreezecardNum, Value from Breezecard WHERE BelongsTo = %s", session['login_userName'])
            rows = cur.fetchall()
            print("debug here card already in use")
            print(session['login_userName'])
            print(rows)
            return redirect(url_for('passengerManageCard', rows = rows, error = 'default'))
         if thisUser == session['login_userName']:
            return redirect(url_for('passengerManageCard', rows = rows, error = "This card already exists"))
         if thisUser != session['login_userName']:
            format = '%Y-%m-%d %H:%M:%S'
            currentTimeString = datetime.datetime.now().strftime(format)
            cur.execute("INSERT INTO Conflict VALUES(%s, %s, %s)", [session['login_userName'],thisCard, currentTimeString])
            conn.commit()
            cur.execute("SELECT BreezecardNum, Value from Breezecard WHERE BelongsTo = %s", session['login_userName'])
            rows = cur.fetchall()
            return redirect(url_for('passengerManageCard', rows=rows, error = "default"))

@app.route('/AddValue', methods=['GET', 'POST'])
def AddValue():
   if session['login_status'] != 1:
      return render_template('login.html', error='Please login first')
   if request.method == 'POST':
      thisCard = request.form['Card']
      thisCredit = request.form['CreditCard']
      thisValue = request.form['Value']

      #conn = sql.connect('database.db')
      cur = conn.cursor()
      ## check this card 
      cur.execute("SELECT BreezecardNum FROM Breezecard WHERE BelongsTo = %s", session['login_userName'])
      result = cur.fetchall()
      #cur = conn.cursor()
      cur.execute("SELECT BreezecardNum, Value from Breezecard WHERE BelongsTo = %s", session['login_userName'])
      rows = cur.fetchall()
      if not thisCredit: 
         return redirect(url_for('passengerManageCard', rows=rows, error = 'Invalid credit card'))

      if not result:
         return redirect(url_for('passengerManageCard', rows = rows, error = "This breezecard does not exist"))
      else:
         #cur.execute("SELECT")
         cur.execute("SELECT BreezecardNum FROM Breezecard where BelongsTo = %s and BreezecardNum = %s", [session['login_userName'], thisCard])
         temp_result = cur.fetchall()
         if temp_result:
             ## update value     
            cur.execute("SELECT Value FROM Breezecard WHERE BreezecardNum = %s", thisCard)
            nextValue = float(cur.fetchall()[0][0]) + float(thisValue)
            if nextValue > 1000:
               return redirect(url_for('passengerManageCard'), rows = rows, error = "Maximum balance is 1000")
            cur.execute("UPDATE Breezecard SET Value = %s WHERE BreezecardNum = %s", [nextValue, thisCard])
            conn.commit()
            cur = conn.cursor()
            cur.execute("SELECT BreezecardNum, Value from Breezecard WHERE BelongsTo = %s", session['login_userName'])
            rows = cur.fetchall()
            return redirect(url_for('passengerManageCard', rows = rows, error = "default"))
            
         else:
            print(result)
            print(thisCard)
            return redirect(url_for('passengerManageCard', rows = rows, error = "This breezecard is not valid"))
        
   

@app.route('/passengerStartTrip', methods=['GET', 'POST'])
def passengerStartTrip():
   if session['login_status'] != 1:
      return render_template('login.html', error='Please login first')
   if session['passengerThisCard'] == '':
      return redirect(url_for('passenger_home'))
   thisStart = request.form['Start']
   print ('passengerStarttrip  ', thisStart)
   #conn = sql.connect('database.db')

   print(session['passengerThisCard'])
   cur = conn.cursor()
   format = '%Y-%m-%d %H:%M:%S'
   currentTimeString = datetime.datetime.now().strftime(format)
   cur.execute("SELECT Enterfare FROM Station WHERE StopId = \'" + thisStart + '\'')
   thisFare = cur.fetchone()[0]
   sqlstr = "INSERT INTO Trip (Tripfare, StartTime, BreezecardNum, StartsAt, EndsAt) VALUES (" + str(thisFare) + ',\'' + currentTimeString + '\',' + '\'' + str(session['passengerThisCard']) + '\'' + ',\'' + thisStart + '\', NULL)' 
   
   print("sql statement")
   print(sqlstr)
   cur.execute(sqlstr)
   conn.commit()
   return redirect(url_for('passenger_home'))


@app.route('/passengerEndTrip', methods=['GET', 'POST'])
def passengerEndTrip():
   if session['login_status'] != 1:
      return render_template('login.html', error='Please login first')
   if session['passengerThisCard'] == '':
      return redirect(url_for('passenger_home'))
   thisEnd = request.form['End']
   #conn = sql.connect('database.db')
   cur = conn.cursor()
   sqlstr = "UPDATE Trip SET EndsAt = \'" + thisEnd + '\' WHERE BreezecardNum = ' + '\'' + session['passengerThisCard'] + '\''+  ' and EndsAt IS NULL'
   print (sqlstr)
   cur.execute(sqlstr)
   conn.commit()
   return redirect(url_for('passenger_home'))

@app.route('/passengerViewTrip', methods=['GET', 'POST'])
def passengerViewTrip():
   if session['login_status'] != 1:
      return render_template('login.html', error='Please login first')
  
   if request.method == 'GET':
      session['BreezePassengerTripStart'] = ''
      session['BreezePassengerTripEnd'] = ''
      cur = conn.cursor()

      cur.execute("DROP VIEW IF EXISTS SuspendedCards")
      conn.commit()
      cur.execute("DROP VIEW IF EXISTS UNSuspendedCards")
      conn.commit()

      cur.execute("CREATE VIEW SuspendedCards AS SELECT distinct Breezecard.BreezecardNum as BreezecardNum FROM Breezecard NATURAL JOIN Conflict")
      cur.execute("CREATE VIEW UNSuspendedCards AS SELECT distinct Breezecard.BreezecardNum FROM Breezecard LEFT OUTER JOIN SuspendedCards on Breezecard.BreezecardNum = SuspendedCards.BreezecardNum where SuspendedCards.BreezecardNum is NULL")

      cur.execute("SELECT Tripfare, StartTime, Trip.BreezecardNum as BreezecardNum, StartsAt, EndsAt FROM Trip JOIN Breezecard ON Trip.BreezecardNum = Breezecard.BreezecardNum JOIN UNSuspendedCards on UNSuspendedCards.BreezecardNum = Breezecard.BreezecardNum WHERE BelongsTo = \'" + session['login_userName'] + '\'')
      conn.commit()

      rows = cur.fetchall()
      print (rows)

      cur.execute("DROP VIEW IF EXISTS SuspendedCards")
      conn.commit()
      cur.execute("DROP VIEW IF EXISTS UNSuspendedCards")
      conn.commit()

      cks = [session['BreezePassengerTripStart'], session['BreezePassengerTripEnd']]
      return render_template('passengerViewTrip.html', rows = rows, ck = cks)

   if request.method == 'POST':
      thisStart = request.form['Start']
      thisEnd = request.form['End']
      session['BreezePassengerTripStart'] = thisStart
      session['BreezePassengerTripEnd'] = thisEnd
      #conn = sql.connect('database.db')
      #conn.row_factory = sql.Row
      cur = conn.cursor()

      cur.execute("DROP VIEW IF EXISTS SuspendedCards")
      conn.commit()
      cur.execute("DROP VIEW IF EXISTS UNSuspendedCards")
      conn.commit()

      cur.execute("CREATE VIEW SuspendedCards AS SELECT distinct Breezecard.BreezecardNum as BreezecardNum FROM Breezecard NATURAL JOIN Conflict")
      cur.execute("CREATE VIEW UNSuspendedCards AS SELECT distinct Breezecard.BreezecardNum FROM Breezecard LEFT OUTER JOIN SuspendedCards on Breezecard.BreezecardNum = SuspendedCards.BreezecardNum where SuspendedCards.BreezecardNum is NULL")

      sqlstr = "SELECT Tripfare, StartTime, Trip.BreezecardNum as BreezecardNum, StartsAt, EndsAt FROM Trip JOIN Breezecard ON Trip.BreezecardNum = Breezecard.BreezecardNum JOIN UNSuspendedCards on UNSuspendedCards.BreezecardNum = Breezecard.BreezecardNum WHERE BelongsTo = \'" + session['login_userName'] + '\''
      
      if thisStart == '' and thisEnd == '':
      	cur.execute(sqlstr)
      elif thisStart != ''  and thisEnd == '':
      	cur.execute(sqlstr + ' and StartTime >= \'' + thisStart + '\'')
      elif thisStart == ''  and thisEnd != '':
      	cur.execute(sqlstr + ' and StartTime <= \'' + thisEnd + '\'')
      else:
      	cur.execute(sqlstr + ' and StartTime >= \'' + thisStart + '\' and StartTime <= \'' + thisEnd + '\'')
      result = cur.fetchall()

      cur.execute("DROP VIEW IF EXISTS SuspendedCards")
      conn.commit()
      cur.execute("DROP VIEW IF EXISTS UNSuspendedCards")
      conn.commit()


      cks = [session['BreezePassengerTripStart'], session['BreezePassengerTripEnd']]
      return render_template('passengerViewTrip.html', rows = result, ck = cks)
 
if __name__ == '__main__':
    app.run(debug = True)
