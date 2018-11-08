import sqlite3
"""
try:
    cursor.execute(sql_statement)
    result = cursor.fetchall()
except sqlite3.DatabaseError as err:
    print("Error: ", err)
else:
    conn.commit()


"""


class DB:

    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def get_all_dannie(self) -> list:
        self.cursor.execute("SELECT * FROM commands")
        results = self.cursor.fetchall()
        return results

    def get_action(self, command: str) -> list:
        result = self.cursor.execute(
            "SELECT * FROM commands where command = ?", command)
        result = self.cursor.fetchone()
        return result[2]  # возвращает action

    def get_commands(self) -> list:
        results = self.get_all_dannie()
        res = []
        for asd in results:
            res.append(asd[1])
        return res

    def get_description(self, command):
        result = self.cursor.execute(
            "SELECT * FROM commands where command = :command",
            {'command': command}
            )
        result = self.cursor.fetchone()
        return result[6]

    def create_new_command(self, command: str, action: str, description: str,
                           notsmile=True, private=False):
        """
        command - ну сама команда очевидно типа !help
        action - что должен отправить бот
        notsmile(default = True) - нужен типа для того чтобы
        если челик шлет смайл то на это что - то отвечается
        типа для того чтобы не было проверки на ! (очевидно)
        private(default = False) - если True то action будет отправлен в лс
        """
        letters = list(command)
        words = command.split()
        error = "error: "
        if notsmile:
            if letters[0] != "!":
                error += "! should be first\n"
        if len(words) > 1:
            error += "it should be one word\n"
        if error != "error: ":
            return error
        if not command or not action or not description:
            error += "что - то не заполнено"
            return error
        # lets check if this command already exist
        coms = self.get_commands()
        for com in coms:
            if command == com:
                error = "this command already existss"
                return error

        # if len(list(action)) > 500:
        #     error += "you action is too big"
        # на твиче нет ограничения на кол-во символов(можно больше 900)
        if notsmile and not private:
            try:
                self.cursor.execute("""
                    INSERT INTO commands (command, action) VALUES(?,?)
                    """, (command, action))
            except sqlite3.DatabaseError as err:
                print("Error: ", err)
            else:
                print("Команда %s добавлена" % command)
                self.conn.commit()
        elif not notsmile:
            try:
                self.cursor.execute(
                    """
                    INSERT INTO commands (command, action, notsmile)
                    VALUES(?,?, 0)
                    """, (command, action))
            except sqlite3.DatabaseError as err:
                print("Error: ", err)
            else:
                print("Команда smile %s добавлена" % command)
                self.conn.commit()
        elif private:
            try:
                self.cursor.execute(
                    """
                    INSERT INTO commands (command, action, private)
                    VALUES(?,?, 1)
                    """, (command, action))
            except sqlite3.DatabaseError as err:
                print("Error: ", err)
            else:
                print("Команда smile %s добавлена" % command)
                self.conn.commit()

    def close_connection(self):
        self.conn.close()


# def check_command(command, commands):
#     for asd in commands:
#         if command == asd:
#             print(db.get_action(command))
#             break


if __name__ == '__main__':
    db = DB('twitch.db')

    commands = db.get_commands()
    message = "commands:"

    for com in commands:
        action = db.get_action(com)
        message += """
        %s = %s
        """ % (com, action)

    db.close_connection()

