import os
import pandas as pd
import sys

def convert_txt_xlsx(log_performance):
    dirname = os.path.dirname(log_performance)
    output_file = os.path.join(dirname, "performance.xlsx")

    data = pd.read_csv(log_performance, sep=' ')

    cols = list(data.columns)
    cols.remove('#')
    cols.append(None)
    data.columns = cols

    data.to_excel(output_file, index=False)

convert_txt_xlsx(sys.argv[1])
