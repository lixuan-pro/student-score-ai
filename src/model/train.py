import os
import pandas as pd
import matplotlib
import joblib
matplotlib.use("TkAgg")

import matplotlib.pyplot as plt

from src.visualization.plot import plot_feature_importance,plot_prediction_vs_true
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False

def train_linear_regression(df_model):
    #意思是训练一个线性回归的模型
    #先定义一个目标变量y
    y=df_model['G3']
    #定义一个特征矩阵x(去掉目标列)
    x=df_model.drop(columns=['G3'])
    #划分训练集和测试集
    x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=42)

    #先创建一个新模型
    model=LinearRegression()

    #先放入训练参数
    model.fit(x_train,y_train)

    #在测试集上放入x_test得到y_pred
    y_pred=model.predict(x_test)
    y_pred_train=model.predict(x_train)
    #用y_pred计算R2
    r2=r2_score(y_test,y_pred)
    r2_train=r2_score(y_train,y_pred_train)

    print("训练集样本数：",len(x_train))
    print("测试集样本数：",len(x_test))
    print("训练集r2:",r2_train)
    print("测试集r2:",r2)


    #模型解释
    #取出所有列的名字（特征名称）
    feature_name=x.columns
    #取出所有特征的系数
    coefficients=model.coef_
    coef_df=pd.DataFrame({
        'feature':feature_name,
        'coefficients':coefficients
    })
    #按照系数值进行排序
    coef_df=coef_df.sort_values(by='coefficients',ascending=False)
    print("特征对G3的影响：")
    print(coef_df.head(10))

    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    model_save_path = os.path.join(BASE_DIR, "model", "student_model.pkl")

    joblib.dump(model, model_save_path)

    print("模型已保存:", model_save_path)

    return model,y_test,y_pred,coef_df

#去除G2后的预测
def train_without_g2(df_model):
    print("\n=======模型B:删除G2=======")
    y=df_model['G3']

    x=df_model.drop(columns=['G3','G2'])
    x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=42)
    model=LinearRegression()
    model.fit(x_train,y_train)
    y_pred=model.predict(x_test)
    r2=r2_score(y_test,y_pred)
    print("删除G2后的R2:",r2)

#去除G2和G3后的预测
def train_without_g1_g2(df_model):
    print("\n=======模型c:删除G1 G2=======")

    y=df_model['G3']
    x=df_model.drop(columns=['G3','G2','G1'])

    x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=42)
    model=LinearRegression()
    model.fit(x_train,y_train)
    y_pred=model.predict(x_test)
    r2=r2_score(y_test,y_pred)

    print("删除G1 G2后的R2:",r2)

#训练的简化模型
def train_simple_model(df_model):
    print("\n======简化模型：G1 G2 studytime failures absences======")
    #特征列
    feature_columns=["G1","G2","studytime","failures","absences"]
    #目标变量
    y=df_model["G3"]
    #特征量x
    x=df_model[feature_columns]

    #划分训练集和测试集
    x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=42)

    #啥，创建模型
    model=LinearRegression()
    model.fit(x_train,y_train)
    #开始预测
    y_pred_train=model.predict(x_train)
    y_pred=model.predict(x_test)

    #计算R2
    r2=r2_score(y_test,y_pred)
    r2_train=r2_score(y_train,y_pred_train)

    print("简化模型使用的特征：",feature_columns)
    print("训练集样本数：",len(x_train))
    print("测试集样本数：",len(x_test))
    print("简化模型训练集r2:",r2_train)
    print("简化模型测试集r2:",r2)

    #模型解释
    coef_df=pd.DataFrame({
        "feature":feature_columns,
        "coefficients":model.coef_
    })
    coef_df=coef_df.sort_values(by='coefficients',ascending=False)

    print("简化模型特征系数：")
    print(coef_df)

    # 保存模型
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    simple_model_save_path = os.path.join(BASE_DIR, "model", "student_model_simple.pkl")

    joblib.dump(model, simple_model_save_path)
    print("简化模型已经保存：", simple_model_save_path)

    return model,y_test,y_pred,coef_df




if __name__=='__main__':
    BASE_DIR=os.path.abspath(os.path.join(os.path.dirname(__file__),"../../"))
    model_path=os.path.join(BASE_DIR,"data","processed","student_clean_model.xlsx")
    figures_dir = os.path.join(BASE_DIR, "outputs", "figures")
    df_model=pd.read_excel(model_path)

    print("读取model版本的数据完成,shape:",df_model.shape)
    model, y_test, y_pred,coef_df= train_linear_regression(df_model)
    #生成预测和真实图保存地址
    prediction_plot_path=os.path.join(figures_dir, "prediction_vs_true.png")
    #调用visualization里的plot_prediction_vs_true函数来画预测和真实情况的散点图
    plot_prediction_vs_true(y_test,y_pred, prediction_plot_path)

    #生成特征重要性图保存地址
    feature_plot_path=os.path.join(figures_dir,"feature_importance.png")
    #调用visualization里的plot_feature_importance函数来画柱状图
    plot_feature_importance(coef_df,feature_plot_path)



    #去除G2
    train_without_g2(df_model)
    #去除G3
    train_without_g1_g2(df_model)

    #训练简化模型
    simple_model,y_test_simple,y_pred_simple,coef_df_simple=train_simple_model(df_model)

    #简化模型的预测值，vs真实值
    simple_prediction_plot_path=os.path.join(figures_dir,"prediction_vs_true_simple.png")
    plot_prediction_vs_true(y_test_simple,y_pred_simple,simple_prediction_plot_path)

    #简化模型：特征重要性图
    simple_feature_plot_path=os.path.join(figures_dir,"feature_importance_simple.png")
    plot_feature_importance(coef_df_simple,simple_feature_plot_path)




















