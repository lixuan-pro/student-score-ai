import os
import pandas as pd
from sqlalchemy import create_engine


def import_to_mysql():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    excel_path = os.path.join(base_dir, "data", "processed", "student_clean_model.xlsx")

    df = pd.read_excel(excel_path)

    bool_cols = df.select_dtypes(include=["bool"]).columns
    for col in bool_cols:
        df[col] = df[col].astype(int)

    print("数据shape:", df.shape)

    engine = create_engine(
        "mysql+pymysql://root:123456@localhost:3306/student_score"
    )

    df.to_sql(
        name="students",
        con=engine,
        if_exists="append",
        index=False
    )

    print("数据导入成功！")


if __name__ == "__main__":
    import_to_mysql()