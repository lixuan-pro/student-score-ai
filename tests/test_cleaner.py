import os
import pandas as pd

#yes/no类型字段,通常转化为0/1
YES_NO_COLUMNS = [
    "schoolsup",
    "famsup",
    "paid",
    "activities",
    "nursery",
    "higher",
    "internet",
    "romantic"
]

#分类字段，为类别，后面通常会对这些做one-hot编码，变成很多0/1列
CATEGORICAL_COLUMNS=[
    "school",
    "sex",
    "address",
    "famsize",
    "pstatus",
    "mjob",
    "fjob",
    "reason",
    "guardian"
]

#数值列
NUMERIC_COLUMNS = [
    "age",
    "Medu",
    "Fedu",
    "traveltime",
    "studytime",
    "failures",
    "famrel",
    "freetime",
    "goout",
    "Dalc",
    "Walc",
    "health",
    "absences",
    "G1",
    "G2",
    "G3"
]
#为每个类别列规定合法取值范围
ALLOWED_CATEGORY_VALUES = {
    "school": {"GP", "MS"},
    "sex": {"F", "M"},
    "address": {"U", "R"},
    "famsize": {"LE3", "GT3"},
    "Pstatus": {"A", "T"},
    "Mjob": {"teacher", "health", "services", "at_home", "other"},
    "Fjob": {"teacher", "health", "services", "at_home", "other"},
    "reason": {"home", "reputation", "course", "other"},
    "guardian": {"mother", "father", "other"},
    "schoolsup": {"yes", "no"},
    "famsup": {"yes", "no"},
    "paid": {"yes", "no"},
    "activities": {"yes", "no"},
    "nursery": {"yes", "no"},
    "higher": {"yes", "no"},
    "internet": {"yes", "no"},
    "romantic": {"yes", "no"}
}

#每个数值列的合理范围
NUMERIC_RANGE_RULES = {
    "age": (10, 30),
    "Medu": (0, 4),
    "Fedu": (0, 4),
    "traveltime": (1, 4),
    "studytime": (1, 4),
    "failures": (0, 4),
    "famrel": (1, 5),
    "freetime": (1, 5),
    "goout": (1, 5),
    "Dalc": (1, 5),
    "Walc": (1, 5),
    "health": (1, 5),
    "absences": (0, 200),
    "G1": (0, 20),
    "G2": (0, 20),
    "G3": (0, 20)
}
#现在是完成了哪些列是什么类型，哪些类别是合法的，哪些数值范围是合理的
#缺失值检查函数
def report_missing_values(df):
    print("\n========缺失值检查========")
    #返回每一列缺失值的数量(布尔值表)
    missing=df.isnull().sum()
    #只保留缺失值大于0的列
    missing=missing[missing>0]
    if missing.empty:
        print("没有缺失值")
    else:
        print("存在缺失值")
        print(missing)
#重复值检查函数
def report_duplicates(df):
    print("\n=======重复值检查=======")
    #检查每一行是不是和前面行重复（一般第一个保留，后面重复的记为TRUE）
    duplicate_count=df.duplicated().sum()
    print("重复行数量:",duplicate_count)

    return duplicate_count

#验证类别值是否合法
def validate_category_values(df):
    print("\n=======类别合法性检查=======")
    #记录非法值
    invalid_columns={}

    #把提前允许的合法字典中的每一列"列名-允许值集合拿出来遍历"
    for col,allowed_values in ALLOWED_CATEGORY_VALUES.items():
        #取出这一列，去除空值，去除列中不重复的值
        actual_values=set(df[col].dropna().unique())
        invalid_values=actual_values-allowed_values
        print(f"{col}唯一值：{sorted(invalid_values)}")
        if invalid_values:
            invalid_columns[col]=invalid_values

    if invalid_columns:
        raise ValueError(f"以下类别列存在非法取值：{invalid_columns}")

    print("类别合法性检查通过")
#把应该是数值的列，统一转化成数值类型
def convert_numeric_columns(df):
    print("\n========== 数值类型转换 ==========")
    for col in NUMERIC_COLUMNS:
        #把这一列强制转化成数值类型,有不合法数据直接报错
        df[col]=pd.to_numeric(df[col],errors='raise')
    print("数值列类型转换完成")
    return df

#数值范围检查函数
def validate_numeric_ranges(df):

    print("\n========== 数值范围检查 ==========")
    #空字典，记录超出合理范围的数据
    invalid_info = {}
    for col, (min_value, max_value) in NUMERIC_RANGE_RULES.items():
        #找出这一列里所有“小于最小值”或“大于最大值”的行
        invalid_rows = df[(df[col] < min_value) | (df[col] > max_value)]

        if len(invalid_rows) > 0:
            invalid_info[col] = len(invalid_rows)
        #这列在真实数据里的最小值和最大值
        print(f"{col} 范围：最小值={df[col].min()}，最大值={df[col].max()}")

    if invalid_info:
        raise ValueError(f"以下数值列存在超出合理范围的数据：{invalid_info}")

    print("数值范围检查通过。")

#用 IQR 方法报告异常值情况
def report_iqr_outliers(df, columns=None):
    print("\n========== IQR异常值检测 ==========")

    if columns is None:
        columns = ["absences", "G1", "G2", "G3"]

    for col in columns:
        #数据从小到大排列后，前 25% 的分界点
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        #中间 50% 数据的跨度（四分位距）
        iqr = q3 - q1
        #计算下界
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        #iqr方法认为小于下界大于上界的可能是异常值
        outlier_count = ((df[col] < lower_bound) | (df[col] > upper_bound)).sum()

        print(
            f"{col}: Q1={q1}, Q3={q3}, IQR={iqr}, "
            f"下界={lower_bound}, 上界={upper_bound}, 异常值数量={outlier_count}"
        )


#生成analysis版本的数据方便查看分析
def clean_analysis_version(df: pd.DataFrame):
    df_analysis = df.copy()
    print("原始数据 shape:", df_analysis.shape)

    # 缺失值检查
    report_missing_values(df_analysis)

    # 重复值检查（如果有重复，删除）
    duplicate_count = report_duplicates(df_analysis)
    if duplicate_count > 0:
        #删除重复行，只保留第一次出现的那条
        df_analysis = df_analysis.drop_duplicates()
        print("已删除重复行，当前 shape:", df_analysis.shape)

    # 类别合法性检查
    validate_category_values(df_analysis)

    # 数值列转换
    df_analysis = convert_numeric_columns(df_analysis)

    #  数值范围检查
    validate_numeric_ranges(df_analysis)

    #  yes/no -> bin
    for col in YES_NO_COLUMNS:
        df_analysis[f"{col}_bin"] = (df_analysis[col] == "yes").astype(int)

    #  IQR异常值检测（只报告，不直接删）
    report_iqr_outliers(df_analysis, columns=["absences", "G1", "G2", "G3"])

    print("\nanalysis 版本 shape:", df_analysis.shape)

    return df_analysis


def clean_model_version(df_analysis: pd.DataFrame) -> pd.DataFrame:
    """
    生成 model 版本数据（机器学习使用）
    - 删除原始 yes/no 列
    - 对分类列做 one-hot
    - 不允许存在 object 类型
    """
    df_model = df_analysis.copy()

    # 删除原始 yes/no 列（保留 _bin）
    df_model = df_model.drop(columns=YES_NO_COLUMNS)

    # one-hot 编码，把类别列转换成机器学习可以使用的 0/1 列
    df_model = pd.get_dummies(
        df_model,
        columns=CATEGORICAL_COLUMNS,
        drop_first=True,
        dtype=int
    )
    #避免共线性，为了矩阵求逆

    # 检查是否仍存在 object 类型
    object_cols = df_model.select_dtypes(include="object").columns.tolist()
    if len(object_cols) > 0:
        raise ValueError(f"模型数据中仍然存在 object 类型列: {object_cols}")

    print("model 版本 shape:", df_model.shape)

    return df_model



if __name__ == "__main__":
    from src.ingestion.loader import load_data

    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    raw_path = os.path.join(BASE_DIR, "data", "raw", "student-mat.csv")
    processed_dir = os.path.join(BASE_DIR, "data", "processed")

    df_raw = load_data(raw_path)

    # analysis 版本
    df_analysis = clean_analysis_version(df_raw)
    analysis_path = os.path.join(processed_dir, "student_clean_analysis.xlsx")
    df_analysis.to_excel(analysis_path, index=False)

    # model 版本
    df_model = clean_model_version(df_analysis)
    model_path = os.path.join(processed_dir, "student_clean_model.xlsx")
    df_model.to_excel(model_path, index=False)

    print("\n数据清洗流程完成！")








