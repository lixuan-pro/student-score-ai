import os
#用来加载保存的模型
import joblib
#要把用户传来的json转化成dataframe再喂给模型
import pandas as pd
#Flask创建flask对象，request获取用户发来的数据请求，jsonify把python字典变成json响应返回给前端
from flask import Flask,request,jsonify

#创建一个flask网站/服务对象
app=Flask(__name__)
#获取根目录地址和训练好的模型位置
BASE_DIR=os.path.abspath(os.path.join(os.path.dirname(__file__),"../../"))
MODEL_PATH=os.path.join(BASE_DIR,"model","student_model_simple.pkl")

#把训练好的模型从磁盘读到内存中
model=joblib.load(MODEL_PATH)
#因为模型训练时是固定的列且顺序一致，明确模型需要哪些输入字段,所以预测时列必须一致
FEATURE_COLUMNS = ["G1", "G2", "studytime", "failures", "absences"]

@app.route("/")
def home():
    return "Flask API is running"

@app.route("/api/test")
def api_test():
    return jsonify({
        "message":"test ok",
        "status":200
    })

@app.route("/api/predict",methods=["POST"])
def predict():
    try:
        #获取前端发来的json数据，转化成字典
        data=request.get_json()
        if data is None:
            return jsonify({
                "error":"输入请求提交不合法"

            }),400

        #加[]是变成列表转化成dataframe类型，？？
        input_df=pd.DataFrame([data])

        #检查前端发来的json数据是否包含模型所需要的所有特征，如果缺少则返回错误，停止预测
        missing_cols=[col for col in FEATURE_COLUMNS if col not in input_df.columns]
        if missing_cols:
            return jsonify({
                "error":"缺少必要字段",
                "missing_cols":missing_cols
            }),400
        #清洗+排序输入数据（上一步已经保证了不会少列，这一步就是保证不会多列和重排序成模型可以使用的）
        input_df=input_df[FEATURE_COLUMNS]
        #模型预测返回数组，取第一条结果
        predition=model.predict(input_df)[0]

        return jsonify({
            "predicted_G3":round(float(predition),2),
        })

    except Exception as e:
        return jsonify({
            "error":str(e)
        }),500

if __name__ == "__main__":
    app.run(debug=True)







