import pandas as pd
from time import sleep as s
for page in range(1, 12):
    df = pd.read_html(f'https://developers.whatismybrowser.com/useragents/explore/software_name/chrome/{str(page)}', header=0)[0]
    with pd.ExcelWriter('output.xlsx', mode='a', engine="openpyxl") as writer: # pylint: disable=abstract-class-instantiated
        df.to_excel(writer)
    s(2)