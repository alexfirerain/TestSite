import sqlite3


class TripRepository:
    def __init__(self, db_path, table_name):
        self._table_name = table_name
        self._connection = sqlite3.connect(db_path, check_same_thread=False)
        self._cursor = self._connection.cursor()
        print(f'подключение к СУБД "{db_path}", репозиторий работает с таблицей "{table_name}"')

    def __del__(self):
        self._cursor.close()
        self._connection.close()
        print(f'закрытие соединения с СУБД')

    def read_all(self):
        return self._cursor.execute(f'SELECT * FROM {self._table_name}').fetchall()

    def read_by_id(self, trip_id):
        return self._cursor.execute(f'SELECT * FROM {self._table_name} WHERE trip_id = {trip_id}').fetchone()

    def delete_by_id(self, id_num):
        self._cursor.execute(f'DELETE from {self._table_name} WHERE trip_id={id_num}')
        self._connection.commit()

