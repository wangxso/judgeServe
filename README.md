# judgeServe

### Centos 下使用会发生错误
```shell
/usr/bin/ld: cannot find -lm\n
```
#### 解决要安装静态库
```shell
yum install glibc-static
```
