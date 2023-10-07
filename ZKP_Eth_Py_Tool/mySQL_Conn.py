
import mysql.connector

db  = mysql.connector.connect(

    host = "localhost",
    user = "root",
    passwd = "12345",
    database = "tesdatabase"

)

mycursor = db.cursor() #navigate through the db

#mycursor.execute("CREATE TABLE SmartContracts (trgtSC VARCHAR(43), vrfSC VARCHAR(43) ) ")

#mycursor.execute("DESCRIBE SmartContracts")

#mycursor.execute("INSERT INTO SmartContracts VALUES (%s,%s)",("x437543","x0xOsama"))
#db.commit()

mycursor.execute("SELECT * FROM SmartContracts")

for x in mycursor:
    print(x)


#


