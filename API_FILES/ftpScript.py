from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

# Create an authorizer with a single user
authorizer = DummyAuthorizer()
authorizer.add_user("username", "password", r"C:\Users\Osama Assem\API_FILES\DB_files", perm="elradfmw")

# Create an FTP handler with the authorizer
handler = FTPHandler
handler.authorizer = authorizer

# Create and start the FTP server
server = FTPServer(("127.0.0.1", 21), handler)
server.serve_forever()