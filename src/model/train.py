import os
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

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
    feature_name=x.columns
    coefficients=model.coef_
    coef_df=pd.DataFrame({
        'feature':feature_name,
        'coefficients':coefficients
    })
    #按照系数值进行排序
    coef_df=coef_df.sort_values(by='coefficients',ascending=False)
    print("特征对G3的影响：")
    print(coef_df.head(10))

    return model

if __name__=='__main__':
    BASE_DIR=os.path.abspath(os.path.join(os.path.dirname(__file__),"../../"))
    model_path=os.path.join(BASE_DIR,"data","processed","student_clean_model.xlsx")

    df_model=pd.read_excel(model_path)

    print("读取model版本的数据完成,shape:",df_model.shape)
    train_linear_regression(df_model)













