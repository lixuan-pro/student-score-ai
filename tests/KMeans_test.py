#处理表格数据常用库
import pandas as pd
#用来做数值计算
import numpy as np
#从sklearn.cluster中导入聚类算法
from sklearn.cluster import KMeans

#读取数据文件
df=pd.read_csv("井区年度投入情况.csv",encoding="gbk")

#显示前五行数据，检查是否读取成功
print(df.head())
#查看表的列名
print(df.columns)

#从表中取出这一列
area=df["井区"]
#从df中取。。到。。之间的所有列，做聚类的真正输入
data=df.loc[:,"钻井":"其他"]
print(area)
print(data.head())

#先创建一个聚类模型，参数的意思为把井区分成4类，让结果更稳定，选10组不同初始中心尝试聚类选效果最好的那次
model=KMeans(n_clusters=4,random_state=42,n_init=10)
#先让模型看看31个井区在8个方向的投入情况，一边学习，一边返回分类结果
labels=model.fit_predict(data)
#每个井区所属的簇标签打印出来
print(labels)
#labels是一个numpy数组，理解为一串按照顺序存放类别编号的数字序列
print(type(labels))
#看看标签数量有多少个
print(len(labels))

#列表套列表结构
area_cluster=[[],[],[],[]]

for i in range(len(labels)):
    cluster_id=labels[i]
    area_name=area.iloc[i]
    area_cluster[cluster_id].append(area_name)

print(area_cluster)

for i in range(len(area_cluster)):
    print(f"第{i}类井区：{area_cluster[i]}")


avg_invest = np.sum(model.cluster_centers_, axis=1)

print(model.cluster_centers_)
print(avg_invest)

for i in range(len(avg_invest)):
    print(f"第{i}类平均总投入：{avg_invest[i]:.2f}")











