import psycopg2


class SqlData:
    def __init__(self, **kwargs):
        self.__connect_data = kwargs
        self.connection = None

    def db_connect(self):
        """
        Connect to DB
        """
        try:
            if bool(not self.connection.closed):
                # print('connection active')
                return 'connection active'
        except:
            pass
            # print('open connection')
        self.connection = psycopg2.connect(**self.__connect_data)
        return self.connection

    def db_disconnect(self):
        """
        Disconnect with DB
        """
        if not self.connection.closed:
            return
        self.connection.close()
        return bool(self.connection.closed)

    def message_logger(self, message):
        if not message.content_type == 'text':
            return None
        with self.connection.cursor() as cursor1:
            reply_to = 0
            try:
                reply_to = message.reply_to_message.message_id
            except AttributeError:
                pass
            cursor1.execute('''
            INSERT INTO botdata.messages (chat_id, user_id, message_id, time_stamp, text, reply_to) 
            VALUES (%s, %s, %s, (TIMESTAMPTZ 'epoch' + %s * '1 second'::interval), %s, %s) 
            ''', (str(message.chat.id), str(message.from_user.id), str(message.message_id),
                  str(message.date), str(message.text), str(reply_to)))
            self.connection.commit()
        return cursor1.statusmessage

    def update_user(self, user_id, first_name=None, last_name=None, username=None):
        """
        :param user_id: user ID'
        :param first_name: first name
        :param last_name: last name
        :param username: nickname
        """

        with self.connection.cursor() as cursor2:
            cursor2.execute('''INSERT INTO botdata.users (user_id, first_name, last_name, username)
                VALUES (%s, ARRAY[%s], ARRAY[%s], ARRAY[%s])
                    ON CONFLICT (user_id)
                    DO UPDATE 
                        SET first_name = users.first_name || EXCLUDED.first_name,
                        last_name = users.last_name || EXCLUDED.last_name,
                        username = users.username || EXCLUDED.username
            ''', (str(user_id), str(first_name), str(last_name), str(username))
                            )
            self.connection.commit()
        return cursor2.statusmessage

    def user(self, user_id):
        with self.connection.cursor() as cursor3:
            cursor3.execute('''SELECT first_name, last_name, username, extract(epoch from date)
                            FROM botdata.users
                            WHERE user_id = '%s'
            ''' % str(user_id)
                            )
            names = {0: 'first_name',
                     1: 'last_name',
                     2: 'username',
                     3: 'date'}
            dictionary = {}
            result = cursor3.fetchone()
            if result:
                for i, row in enumerate(result):
                    dictionary[names[i]] = row
                return dictionary
            return None


if __name__ == '__main__':
    from bottoken import *
    sqldb = SqlData(dbname=postgresql_bd, user=postgresql_username,
                                    password=postgresql_password, host=postgresql_host)
    sqldb.db_connect()
    # test add string
    # print(sqldb.update_user(user_id='555', first_name='Petya', last_name='Volodin', username='Volodyaaa'))
    i = sqldb.user('555')
    print(i)
    sqldb.db_disconnect()