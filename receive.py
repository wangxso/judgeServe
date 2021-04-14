import os, stat
import subprocess
import uuid
import pika
import ujson
from conf import get_config
from send import send_message
import shutil
# 建立连接
mq_conf = get_config("rabbitmq")
user = pika.PlainCredentials(mq_conf['username'], str(mq_conf['password']))
connection = pika.BlockingConnection(
    pika.ConnectionParameters(mq_conf['host'], int(mq_conf['port']), mq_conf['route'], credentials=user))
channel = connection.channel()

channel.queue_declare(queue='hello')

result = {
    "Accepted": 1,
    "Wrong Answer": 2,
    "Runtime Error": 3,
    "Output Limit Exceeded": 4,
    "Memory Limit Exceeded": 5,
    "Time Limit Exceeded": 6,
    "Presentation Error": 7,
    "System Error": 8,
    "Compile Error": 9
}


def judge(suid, file_name):
    path = fr"./dist/{suid}"
    cmd = fr"./Core -c {path}/{file_name} -t 1000 -m 65535 -d {path}"
    print(cmd)
    os.system(cmd)


def get_result(path, suid):
    with open(fr"{path}/result.txt", "r") as fp:
        # [:-1] 去除换行符
        res = fp.readline()[:-1]
        time = fp.readline()[:-1]
        mem = fp.readline()[:-1]
        err = fp.readlines()[:-1]
        if len(err) == 0:
            err = ""
        data = {
            "sid": suid,
            "result": result[res],
            "timeCost": time,
            "memoryCost": mem,
            "error": err
        }
        fp.close()
    send_message(ujson.dumps(data), "result")
    shutil.rmtree(path)
    print(data)


def callback(ch, method, properties, body):
    print(body)
    data = ujson.loads(body)
    suid = data['sid']
    print(" [x] Received %r" % suid)
    path = fr'./dist/{suid}/'
    type = data['language']
    file_name = ""
    if type == '0':
        file_name = "test.c"
    elif type == '1':
        file_name = "test.cpp"
    elif type == '2':
        file_name = "Main.java"
    else:
        file_name = "test.c"
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
    judge(suid, file_name)
    get_result(path, suid)


channel.basic_consume(queue='judge', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
