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
        """
        get info from DB by ID
        return dict first_name, last_name, username, date
        """
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

    def add_deathlist(self, chat_id, **kwargs):
        chatid = chat_id
        data = {'user_id': None,
                'first_name': None,
                'last_name': None,
                'username': None,
                'decl_user_id': None,
                'decl_first_name': None,
                'decl_last_name': None,
                'decl_username': None,
                }
        data.update(kwargs)

        with self.connection.cursor() as cursor4:
            cursor4.execute('''INSERT INTO botdata.deathlist (chat_id, user_id, first_name, last_name, username,
                                decl_user_id, decl_first_name, decl_last_name, decl_username)
                                    VALUES  (%s, %s, %s, %s, %s,
                                    %s, %s, %s, %s)
                                ON CONFLICT DO NOTHING
            ''', (str(chatid), str(data['user_id']), str(data['first_name']), str(data['last_name']),
                  str(data['username']),
                  str(data['decl_user_id']), str(data['decl_first_name']),
                  str(data['decl_last_name']), str(data['decl_username']))
                            )
            self.connection.commit()
        return cursor4.statusmessage

    def get_deathlist(self, chat_id):
        with self.connection.cursor() as cursor5:  # FIXME дубликаты имени добавителей
            cursor5.execute('''
                SELECT count(user_id),
                first_name || ', ' || last_name AS first_name, 
                string_agg(decl_first_name || ' ' || decl_last_name, ', ') AS decl_nickname,
                string_agg(decl_user_id, ', ') AS decl_id
                    FROM botdata.deathlist
                    WHERE chat_id = '%s'
                    GROUP BY 2
                    ORDER BY count(user_id) DESC
            ''' % str(chat_id)
                            )

            names = {0: 'score',
                     1: 'first_name',
                     2: 'decl_first_name',
                     3: 'decl_user_id'}

            dictionary = {}
            result = cursor5.fetchall()
            if result:
                for i, row in enumerate(result):
                    dictionary[i] = {}
                    for j, string in enumerate(row):
                        dictionary[i].update({names[j]: string})
                return dictionary
            return None


if __name__ == '__main__':
    from bottoken import *

    data = {'user_id': '234',
            'first_name': 'Vasya',
            'last_name': 'Pumpir',
            'username': 'Pupochkiiin',
            'decl_user_id': '3445',
            'decl_last_name': None,
            'decl_username': 'Snippy',
            }

    sqldb = SqlData(dbname=postgresql_bd, user=postgresql_username,
                    password=postgresql_password, host=postgresql_host)
    sqldb.db_connect()
    # test add string
    # print(sqldb.update_user(user_id='555', first_name='Petya', last_name='Volodin', username='Volodyaaa'))
    # i = sqldb.user('555')
    # i = sqldb.add_deathlist(33333, **data)
    i = sqldb.get_deathlist(161613125)
    print(i)
    sqldb.db_disconnect()
