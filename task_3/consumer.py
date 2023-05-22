import json
import os
import pika
import time
from datetime import datetime
from pathlib import Path


def main():
    delete_files = set()
    credentials = pika.PlainCredentials('rmuser', 'rmpassword')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host='localhost',
            port=5672,
            credentials=credentials,
        )
    )
    channel = connection.channel()
    channel.queue_declare(queue='for_result')

    def callback(ch, method, properties, body):
        """
        Если надо все документы собрать в один то можно использовать этот код
        routing_key = method.routing_key
        if not os.path.isfile(f'result/{routing_key}.txt'):
            with open(f'result/{routing_key}.txt', 'w') as file:
                file.write(all_text)
        else:
            with open(f'result/{routing_key}.txt', 'r') as file:
                prev_text = file.read()
            prev_text += all_text
            with open(f'result/{routing_key}.txt', 'w') as file:
                file.write(prev_text)
        """
        start_time = int(datetime.now().timestamp())
        all_text = ''
        files_list = json.loads(body)
        delivery_tag = method.delivery_tag
        print(f'Получен список файлов: {files_list}'
              f'\nИдентификатор сообщения: {delivery_tag}')
        if files_list:
            for txt_file in files_list:
                if txt_file not in delete_files:
                    with open(f'data/{txt_file}', 'r') as file:
                        all_text += file.read() + '\n'
            if not Path('result').exists():
                os.makedirs('result')
            if all_text:
                with open(f'result/{delivery_tag}.txt', 'w') as file:
                    file.write(all_text)
            for txt_file in files_list:
                if txt_file not in delete_files:
                    os.remove(f'data/{txt_file}')
                    delete_files.add(txt_file)
            end_time = int(datetime.now().timestamp())
            time.sleep(35-(end_time-start_time))
        channel.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(queue='for_result', on_message_callback=callback)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
