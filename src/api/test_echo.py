import requests
#发送HTTP请求的库

#要访问的接口地址
url="http://127.0.0.1:5000/api/echo"

payload={
    "name":"Li Xuan",
    "G1":12,
    "G2":14,
    "studytime":2
}

response=requests.post(url,json=payload)

#查看请求是否成功
print("状态码：",response.status_code)
print("返回内容：",response.json())

