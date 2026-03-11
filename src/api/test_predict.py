#发送HTTP请求的库
import requests

url="http://127.0.0.1:5000/api/predict"

#提交内容
payload = {
    "G1": 11,
    "G2": 11,
    "studytime": 2,
    "failures": 0,
    "absences": 4
}

#提交json数据，接收返回结果
response=requests.post(url,json=payload)

print("状态码：",response.status_code)
print("返回内容：",response.json())











