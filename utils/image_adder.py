import sys
sys.path.insert(1, 'modules')

from im2tx import obtain_df_with_text
from iris_db import IrisDB
import pandas as pd
from openai import OpenAI

def add_images(openai_client : OpenAI, folderpath : str, csvpath : str = 'Data/version2.csv'):
    DB = IrisDB(Openai_client = openai_client)
    if not DB.table_exists():
            df = pd.read_csv(csvpath)
            df.columns = ['image_path', 'description']

            DB.init_table()
            DB.insert_df_to_table(df)
    
    df = obtain_df_with_text(folderpath)
    df.to_csv(csvpath, mode="a", header=False)

    df.columns = ['image_path', 'description']
    DB.insert_df_to_table(df)
