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

