import pika
import json
from conf import get_config


def send_message(data, queue_name):
    # 建立连接
    mq_conf = get_config("rabbitmq")
    user = pika.PlainCredentials(mq_conf['username'], str(mq_conf['password']))
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(mq_conf['host'], int(mq_conf['port']), mq_conf['route'], credentials=user))

    # 开辟管道
    channel = connection.channel()
    channel.queue_declare(queue=queue_name, durable=True, passive=True)
    channel.basic_publish(exchange='',
                          routing_key=queue_name,
                          body=json.dumps(data))
    print(" [x] Sent " + json.dumps(data))
    connection.close()
