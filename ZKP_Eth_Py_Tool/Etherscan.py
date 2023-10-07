import requests

class EtherRetreiver:


    
    def __init__(self):
        self.API_KEY = "SP7W6K1G5RDYIC6ZRXSCGXJ651HRDBPMMN"
    

    # This function retrieves a verified source code of a smart contract from Etherscan.io using their provided API
    # It takes the target smart contract address as input
    # Returns the requested source code if found, if not, returns None
    def retrieveSrcCode(self,contract_address):
        url = f"https://api.etherscan.io/api?module=contract&action=getsourcecode&address={contract_address}&apikey={self.API_KEY}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            # Parse and extract the source code from the response JSON.
            source_code = data['result'][0]['SourceCode']
            if source_code == '':
                return None
            else:
                return source_code
        else:
            print("Internal Error: Unable to fetch source code.")
            return None
    