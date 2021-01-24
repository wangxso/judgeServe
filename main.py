from send import send_message

body = {
    "code": '#include<stdio.h>\nint main(){\nprintf("hello world");\nreturn 0;\n}',
    "input": '',
    "output": 'hello world',
    'type': 1
}
send_message(data=body, queue_name="judge")
