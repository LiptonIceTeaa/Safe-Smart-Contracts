import mysql.connector

class MySQLDatabase:

    def __init__(self, host, user, password, database):
        self.db = mysql.connector.connect(
            host=host,
            user=user,
            passwd=password,
            database=database
        )
        self.mycursor = self.db.cursor()

    # creates a table in our database
    def create_table(self, table_name, columns):
        create_table_query = f"CREATE TABLE {table_name} ({', '.join(columns)})"
        self.mycursor.execute(create_table_query)

    def describe_table(self, table_name):
        self.mycursor.execute(f"DESCRIBE {table_name}")
        for column_info in self.mycursor:
            print(column_info)

    def insert_data(self, table_name, values):
        insert_query = f"INSERT INTO {table_name} VALUES ({', '.join(['%s'] * len(values))})"
        self.mycursor.execute(insert_query, values)
        self.db.commit()

    def select_all(self, table_name):
        self.mycursor.execute(f"SELECT * FROM {table_name}")
        for row in self.mycursor:
            print(row)

    def close_connection(self):
        self.db.close()

# Usage example:
if __name__ == "__main__":
    db = MySQLDatabase(
        host="localhost",
        user="root",
        password="12345",
        database="tesdatabase"
    )

    # Create a table (uncomment if needed)
    # db.create_table("SmartContracts", ["trgtSC VARCHAR(43)", "vrfSC VARCHAR(43)"])

    # Describe the table (uncomment if needed)
    # db.describe_table("SmartContracts")

    # Insert data into the table (uncomment if needed)
    # db.insert_data("SmartContracts", ("x437543", "x0xOsama"))

    # Select and print all data from the table
    db.select_all("SmartContracts")

    # Close the database connection
    db.close_connection()
