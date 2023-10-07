import logging
import mysql.connector
from MySQLDatabase import MySQLDatabase


class MySQL_logic:
    
    # Fixed connection details as constants
    HOST = "localhost"
    USER = "root"
    PASSWORD = "12345"
    DATABASE = "tesdatabase"

    # sets up the connection with the SQL server hosted locally on my machine
    # irl implementation is going to be hosted on an online server
    def __init__(self):
        self.db  = mysql.connector.connect(
            host = self.HOST,
            user = self.USER,
            passwd = self.PASSWORD,
            database = self.DATABASE
        )

        #print("I am here at SQL class !")
    
    # This function checks if there's an existing verification smart contract entry for the requestes smart contract by the user.
    # If an entry for vrfSC is found, the address it returned
    # If nothing is found, Null is returned
    def checkForTrgtSC(self, address):
        mycursor = self.db.cursor()# cursour to navigate through our database
        sql_command = "SELECT * FROM SmartContracts WHERE trgtSC ='"+address+"'" # SQL string that we will execute next
        mycursor.execute(sql_command)# executing SQL command
        # Fetch the result
        result = mycursor.fetchone()
        if result is not None:
            return "Found entry"
        else:#this means that the target smart was never previously processed
            print("Entry not found in our db")
            return None


    # This function adds a (Target smart contract address, verification code (file name), ) pair in our DB
    # It takes in trgtSC, and vrfSC
    # Doesnt not return anything, but prints a success or error command 
    def addSC(self, trgtSC):
            mycursor = self.db.cursor()# cursdour to navigate through our database
            sql_command = "INSERT INTO SmartContracts (trgtSC) VALUES (%s)"
            try:
                mycursor.execute(sql_command,(trgtSC,))
                self.db.commit()
                print("Entry added")
                return "[+] Success"
            except mysql.connector.Error as err:
                 print("Could not add entry to table: {err}",err) 
                 self.db.rollback() # undo any changes made in case of an error.
                 return "[-] Addition failed"
            finally:
                mycursor.close()
    
 
           




