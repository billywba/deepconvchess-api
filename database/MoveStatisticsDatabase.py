import mysql.connector


class MoveStatisticsDatabase():
    def __init__(self, host, port, username, password, database):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.database = database
        self.connection = None

        self.connect()

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.username,
                password=self.password,
                database=self.database
            )
            print("Connected to MySQL database successfully")
        except mysql.connector.Error as error:
            print("Error connecting to MySQL database:", error)

    def disconnect(self):
        if self.connection:
            self.connection.close()
            print("Disconnected from MySQL database")

    def get_statistics(self, fen):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM positions")

        move_statistics = []

        results = cursor.fetchall()
        for row in results:
            move_statistics.append({
                "move": row[2],
                "black_won": row[3],
                "white_won": row[4],
                "draw": row[5]
            })

        cursor.close()
        return move_statistics
