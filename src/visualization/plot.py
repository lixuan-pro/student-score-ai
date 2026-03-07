import matplotlib.pyplot as plt
#高级可视化库，视图更好看，适合数据分析
import seaborn as sns
import os


#画G3成绩分布直方图，
def plot_score_distribution(df,save_path):
    #创建一个新的图像，如果不创建的活，多个图会在一起
    plt.figure()
    #画直方图，取G3列，分成15个区间：可以看出成绩集中在哪里，分布是否正常
    plt.hist(df['G3'],bins=15)
    plt.title("期末成绩G3的分布")
    plt.xlabel("G3")
    plt.ylabel("人数")

    #保存图像...
    plt.savefig(save_path)
    plt.close()

#预测和真实数据的散点图.
def plot_prediction_vs_true(y_test,y_pred,save_path):
    plt.figure()
    #x轴为真实成绩，y轴为预测成绩，如果模型好，图像会接近45°直线。~
    plt.scatter(y_test,y_pred)
    plt.xlabel("真实G3")
    plt.ylabel("预测G3")
    plt.savefig(save_path)
    plt.close()

#画特征重要性图，看看什么最牛,解释模型为什么这样预测
def plot_feature_importance(feature_df,save_path):
    plt.figure()
    #排序，按照系数排序，取前10个,降序
    feature_df=feature_df.sort_values(by="coefficients",ascending=False).head(10)
    #柱状图，
    plt.barh(feature_df["feature"],feature_df["coefficients"])
    plt.title("特征重要程度")
    plt.xlabel("coefficient")

    plt.savefig(save_path)
    plt.close()




































