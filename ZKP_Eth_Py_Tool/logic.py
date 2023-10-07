import requests
import mysql.connector


# 1- Ask user for trgt smart contract address
# 2- Check if already processed it, by checking if the trgt sc addr exists in the SQL db
# 3- If no, call the Ethersacn.io api to retrieve the trgt sc src code. If yes,
# 4- Store the src code in a variable or file
# 5- Interact with ZoKrates

# Prompt the user to enter the smart contract they want to view
trgtSCAddress = input("Please enter the target smart contract address")

# initiate connection with the SQL database hosted on local server.
# In real world scenario, it will be hosted on an external server
db  = mysql.connector.connect(

    host = "localhost",
    user = "root",
    passwd = "12345",
    database = "tesdatabase"

)


mycursor = db.cursor() #navigate through the db
#mycursor.execute("DESCRIBE SmartContracts")
mycursor.execute("SELECT * FROM SmartContracts WHERE trgtSC ='"+trgtSCAddress+"'")
#mycursor.execute("SELECT * FROM SmartContracts")
#x437543
#cursour_ln = int(len(mycursor.fetchall()))

# Fetch the result
result = mycursor.fetchone()
if result is not None:
    vrfSC_value = result[1]
    #print("vrfSC value:", vrfSC_value)
    print("Smart contract found and its verifcation samrt contract address is: ", vrfSC_value)
else:#this means that the target smart was never previously processed
    print("Entry not found")
    # retrieve the source code smart contract from Etherscan.io
    # might be available or might not be
    # if not available exit the program
    # if available continue as below
    # call a function that interacts with the ZoKrates platform
    # get the verification smart contract
    # use truffle suite to deploy it
    # add the trgtSC and vrfSC entry in our DB



api_key = 'SP7W6K1G5RDYIC6ZRXSCGXJ651HRDBPMMN'
#contract_address = '0x6e1BD5971d8C07Ac042bfe8d4ae60276C8777c92'

url = f"https://api.etherscan.io/api?module=contract&action=getsourcecode&address={trgtSCAddress}&apikey={api_key}"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    # Parse and extract the source code from the response JSON.
    source_code = data['result'][0]['SourceCode']
    if source_code == '':
        print("No source code found. \nPlease request the original creators to verify them on Etherscan.io")
    else:
        print("Source code found")
else:
    print("Error: Unable to fetch source code.")