from send import send_message

body = {
    "sid": "123456",
    "code": '#include<stdio.h>\nint main(){\nprintf("hello world");\nreturn 0;\n}',
    "input": '',
    "output": 'hello world',
    'language': 0
}
send_message(data=body, queue_name="judge")
