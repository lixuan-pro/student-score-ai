import matplotlib
matplotlib.use("TkAgg")

import pandas as pd
import matplotlib.pyplot as plt
import os
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
analysis_path = os.path.join(BASE_DIR, "data", "processed", "student_clean_analysis.xlsx")

df = pd.read_excel(analysis_path)

print("G3 描述统计：")
print(df["G3"].describe())
print(df[["G1", "G2", "G3"]].corr())

plt.hist(df["G3"], bins=15)
plt.title("Distribution of Final Grade (G3)")
plt.xlabel("G3")
plt.ylabel("Frequency")
plt.show()