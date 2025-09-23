import requests
#发送一个get请求
response = requests.get('http://localhost:5000/')
print(response.json())
#发送一个post请求
data = {"name": "Alice", "age": 30}
response = requests.post('http://localhost:5000/', json=data)
print("没有传location参数时的响应:")
print(response.json())
data2 = {"name": "Alice", "location": "Wonderland", "age": 30}
response = requests.post('http://localhost:5000/', json=data2)
print("传入所有参数时的响应:")
print(response.json())