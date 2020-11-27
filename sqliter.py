import sqlite3


class SQLiter:
    def __init__(self, database):
        """Подключаемся к БД и сохраняем курсор соединения"""
        self.connection = sqlite3.connect(database, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def add_user(self, user_id, status=False):
        """Добавляем пользователя в БД без активации подписки"""
        with self.connection:
            return self.cursor.execute('INSERT INTO `subscription` (`user_id`, `status`) VALUES(?,?)', (user_id, status))

    def users_exists(self, user_id):
        """Проверяем, есть ли уже юзер в базе"""
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `subscription` WHERE `user_id` = ?', (user_id,)).fetchall()
            return bool(len(result))

    def get_subscriptions(self, status=True):
        """Получаем всех активных подписчиков бота"""
        with self.connection:
            return self.cursor.execute('SELECT * FROM `subscription` WHERE `status` = ?', (status,)).fetchall()

    def subscriber_exist(self, user_id, status=True):
        """Проверяем, активна ли подписка"""
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `subscription` WHERE `user_id` = ? AND `status` = ?',
                                         (user_id, status)).fetchall()
            return bool(len(result))

    def update_subscription(self, user_id, status):
        """Обновляем статус подписки пользователя"""
        with self.connection:
            return self.cursor.execute('UPDATE `subscription` SET `status` = ? WHERE `user_id` = ?', (status, user_id))

    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()