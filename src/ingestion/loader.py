import pandas as pd
import os


def load_data(file_path: str) -> pd.DataFrame:
    """
    读取原始成绩数据
    """
    print("正在读取数据...")
    df = pd.read_csv(file_path)
    print("数据读取完成！")
    return df


def explore_data(df: pd.DataFrame):
    """
    打印数据基本信息
    """
    print("\n数据前5行：")
    print(df.head())

    print("\n数据形状：")
    print(df.shape)

    print("\n数据类型：")
    print(df.dtypes)

    print("\n缺失值统计：")
    print(df.isnull().sum())


def export_to_excel(df: pd.DataFrame, output_path: str):
    """
    导出为 Excel 文件
    """
    print("\n正在导出为 Excel...")
    df.to_excel(output_path, index=False)
    print("导出完成！")


if __name__ == "__main__":
    # 获取项目根目录
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))

    raw_path = os.path.join(BASE_DIR, "data", "raw", "student-mat.csv")
    processed_path = os.path.join(BASE_DIR, "data", "processed", "student-mat.xlsx")

    if not os.path.exists(raw_path):
        print("找不到原始数据文件！请检查路径。")
        print("当前尝试路径为：", raw_path)
    else:
        data = load_data(raw_path)
        explore_data(data)
        export_to_excel(data, processed_path)