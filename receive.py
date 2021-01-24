import os, stat
import subprocess
import uuid
import pika
import json
from conf import get_config
from send import send_message
# 建立连接
mq_conf = get_config("rabbitmq")
user = pika.PlainCredentials(mq_conf['username'], str(mq_conf['password']))
connection = pika.BlockingConnection(
    pika.ConnectionParameters(mq_conf['host'], int(mq_conf['port']), mq_conf['route'], credentials=user))
channel = connection.channel()

channel.queue_declare(queue='hello')


def judge(suid, file_name):
    path = fr"./dist/{suid}"
    cmd = fr"sudo Core -c {path}/{file_name} -t 1000 -m 65535 -d {path}"
    print(cmd)
    os.system(cmd)


def get_result(path, suid):
    with open(fr"{path}/result.txt", "r") as fp:
        # [:-1] 去除换行符
        res = fp.readline()[:-1]
        time = fp.readline()[:-1]
        mem = fp.readline()[:-1]
        err = fp.readlines()[:-1]
        data = {
            "sid": suid,
            "res": res,
            "time": time,
            "mem": mem,
            "err": err
        }
        fp.close()
    send_message(json.dumps(data), "result")
    print(data)


def callback(ch, method, properties, body):
    data = json.loads(body)
    uid = str(uuid.uuid4())
    suid = ''.join(uid.split('-'))
    print(" [x] Received %r" % suid)
    path = fr'./dist/{suid}/'
    type = data['type']
    file_name = ""
    if type == 1:
        file_name = "test.c"
    elif type == 2:
        file_name = "test.cpp"
    elif type == 3:
        file_name = "Main.java"
    if not os.path.isdir(path):
        os.mkdir(fr"./dist/{suid}")
    # 测试样例写入文件
    print(data)
    with open(file=fr"{path}in.in", mode="w") as fp:
        fp.write(str(data['input']))
        fp.close()
    with open(file=fr"{path}out.out", mode="w") as fp:
        fp.write(str(data["output"]))
        fp.close()
    # 源代码写入文件
    with open(file=fr"{path}{file_name}", mode="w") as fp:
        fp.write(str(data['code']))
        fp.close()
    os.chmod(fr"{path}{file_name}", stat.S_IRWXO)
    judge(suid, file_name)
    get_result(path, suid)


channel.basic_consume(queue='judge', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()