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
        cursor.execute("SELECT * FROM positions WHERE fen = %s", (fen, ))

        move_statistics = []

        results = cursor.fetchall()
        if len(results) == 0:
            move_statistics.append({
                "No statistics available"
            })

        else:
            for row in results:
                black_won = row[3]
                white_won = row[4]
                draw = row[5]
                total_games = black_won + white_won + draw

                black_win_percentage = (black_won / total_games) * 100
                white_win_percentage = (white_won / total_games) * 100
                draw_percentage = (draw / total_games) * 100

                move_statistics.append({
                    "move": row[2],
                    "black_won": f"{black_win_percentage}%",
                    "white_won": f"{white_win_percentage}%",
                    "draw": f"{draw_percentage}%"
                })

        cursor.close()
        return move_statistics
