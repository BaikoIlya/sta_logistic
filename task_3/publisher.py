import json
import os
import time
import pika


def main():
    last = []
    credentials = pika.PlainCredentials('rmuser', 'rmpassword')
    try:
        while True:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host='localhost',
                    port=5672,
                    credentials=credentials
                )
            )
            channel = connection.channel()
            channel.queue_declare(queue='for_result')
            files_list = [
                file_name for file_name in os.listdir('data')
                if file_name.endswith('.txt')
            ]
            if last != files_list:
                for_send = json.dumps(files_list)
                channel.basic_publish(
                    exchange='',
                    routing_key='for_result',
                    body=for_send
                )
                last = files_list
            time.sleep(15)
            connection.close()

    except KeyboardInterrupt:
        connection.close()


if __name__ == '__main__':
    main()
