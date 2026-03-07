import matplotlib
matplotlib.use("TkAgg")

import pandas as pd
import matplotlib.pyplot as plt
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
analysis_path = os.path.join(BASE_DIR, "data", "processed", "student_clean_analysis.xlsx")

df = pd.read_excel(analysis_path)

# 描述统计
print("G3 描述统计：")
print(df["G3"].describe())

# 成绩相关性
print(df[["G1", "G2", "G3"]].corr())

# 成绩分布
plt.hist(df["G3"], bins=15)
plt.title("Distribution of Final Grade (G3)")
plt.xlabel("G3")
plt.ylabel("Frequency")
plt.show()

# G2 与 G3 的关系
plt.scatter(df["G2"], df["G3"])
plt.title("Relationship between G2 and G3")
plt.xlabel("G2 (Second Period Grade)")
plt.ylabel("G3 (Final Grade)")
plt.show()