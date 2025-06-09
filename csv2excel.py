import pandas as pd

def csv_to_excel(FILE_PATH):
  df = pd.read_csv(FILE_PATH)
  df.to_excel("file.xlsx", index=False)
try:
    csv_to_excel("disk_usage.csv")
    print("File Created")
except:
    print("Something wrong")
