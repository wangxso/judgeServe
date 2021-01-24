import yaml
import os


def get_config(key):
    # 获取当前文件路径
    file_path = os.path.dirname(__file__)
    print(file_path)
    # 获取当前文件的Realpath
    file_name_path = os.path.split(os.path.realpath(__file__))[0]
    print(file_name_path)
    # 获取配置文件的路径
    yaml_path = os.path.join(file_name_path, 'config.yaml')
    # 加上 ,encoding='utf-8'，处理配置文件中含中文出现乱码的情况。
    f = open(yaml_path, 'r', encoding='utf-8')
    cont = f.read()
    r = yaml.full_load(cont)
    conf = r.get("rabbitmq")
    return conf
