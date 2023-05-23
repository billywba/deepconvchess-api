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
    
    def check_fen_already_has_move(self, fen, move):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM positions WHERE fen = %s AND move = %s", (fen, move, ))

        results = cursor.fetchall()
        cursor.close()
        
        return len(results) > 0

    def insert_statistic(self, fen, move, winner):
        cursor = self.connection.cursor()

        if self.check_fen_already_has_move(fen, move):
            query = ""
            if winner == "black":
                query = "UPDATE positions SET black_won = black_won + 1 WHERE fen = %s AND move = %s"
            elif winner == "white":
                query = "UPDATE positions SET white_won = white_won + 1 WHERE fen = %s AND move = %s"
            elif winner == "draw":
                query = "UPDATE positions SET draw = draw + 1 WHERE fen = %s AND move = %s"

            cursor.execute(query, (fen, move, ))

        else:
            query = ""
            if winner == "black":
                query = "INSERT INTO positions (fen, move, black_won, white_won, draw) VALUES (%s, %s, 1, 0, 0)"
            elif winner == "white":
                query = "INSERT INTO positions (fen, move, black_won, white_won, draw) VALUES (%s, %s, 0, 1, 0)"
            elif winner == "draw":
                query = "INSERT INTO positions (fen, move, black_won, white_won, draw) VALUES (%s, %s, 0, 0, 1)"

            cursor.execute(query, (fen, move, ))

        self.connection.commit()

        cursor.close()
