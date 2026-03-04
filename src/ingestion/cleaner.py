import pandas as pd


def clean_analysis_version(df:pd.DataFrame):
    df_analysis=df.copy()
    print("原始数据shape：",df_analysis.shape)
    #yes/no列
    yes_no_columns = [
        "schoolsup",
        "famsup",
        "paid",
        "activities",
        "nursery",
        "higher",
        "internet",
        "romantic"
    ]

    for col in yes_no_columns:
        df_analysis[f"{col}_bin"] =(df_analysis[col]=="yes").astype(int)

    #成绩列转化成int,防止成绩列为字符串“100”
    grade_columns=["G1","G2","G3"]
    for col in grade_columns:
        df_analysis[col] = pd.to_numeric(df_analysis[col], errors="raise")
        #pd.to_numeric的作用是将df中的某一列强制转换成数值类型,errors=raise是为了将错误暴露出来

    print("analysis 版本 shape:", df_analysis.shape)

    return df_analysis

def clean_model_version(df_analysis:pd.DataFrame)->pd.DataFrame:
    """
    生成model版本数据（机器使用）
    删除yes/no列
    对指定分类列做one-hot
    不允许存在object类型（机器使用）
    保留G1 G2用于预测G3

    """
    #删除原始yes/no列（保留_bin）
    yes_no_columns = [
        "schoolsup",
        "famsup",
        "paid",
        "activities",
        "nursery",
        "higher",
        "internet",
        "romantic"
    ]
    df_model=df_analysis.drop(columns=yes_no_columns)

    #需要one-hot分类的列
    categorical_columns = [
        "school",
        "sex",
        "address",
        "famsize",
        "Pstatus",
        "Mjob",
        "Fjob",
        "reason",
        "guardian"
    ]

    df_model=pd.get_dummies(
        df_model,
        columns=categorical_columns,
        drop_first=True)
    #drop_first是为了避免共线性，为了矩阵求逆

    #对清洗后的类型进行检查，不允许存在object类型
    object_cols=df_model.select_dtypes(include='object').columns.tolist()
    if len(object_cols)>0:
        raise ValueError(f"模型数据中仍然存在 object 类型列: {list(object_cols)}")

    print("model 版本 shape:", df_model.shape)

    return df_model



#模块加可独立测试（模块自测能力）
if __name__ == "__main__":
    from src.ingestion.loader import load_data
    import os

    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__),"../../"))

    raw_path=os.path.join(BASE_DIR,"data","raw","student-mat.csv")
    processed_dir = os.path.join(BASE_DIR, "data", "processed")

    df_raw = load_data(raw_path)

    #analysis
    df_analysis=clean_analysis_version(df_raw)
    analysis_path=os.path.join(processed_dir, "student_clean_analysis.xlsx")
    df_analysis.to_excel(analysis_path, index=False)

    #model
    df_model=clean_model_version(df_analysis)
    model_path=os.path.join(processed_dir, "student_clean_model.xlsx")
    df_model.to_excel(model_path, index=False)

    print("数据清洗流程完成！")



