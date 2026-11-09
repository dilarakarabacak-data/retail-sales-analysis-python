import numpy as np
import pandas as pd
import os

print("Working Directory:", os.getcwd())

df=pd.read_excel("data/raw/online_retail_II.xlsx",sheet_name=0)


df_clean = df.copy()


dropped=df_clean.drop_duplicates()


cminus=dropped.drop(dropped[dropped["Invoice"].astype(str).str.startswith("C")].index)



df_clean=cminus[cminus["Quantity"]>0].copy()


df_clean=df_clean.drop(df_clean[df_clean["Price"]<=0].index)


df_clean["Customer ID"]=df_clean["Customer ID"].astype('Int64')



df_clean["Description"]=df_clean["Description"].fillna("Unknown")


df_clean.insert(loc=6,column="Revenue",value=df_clean["Quantity"]*df_clean["Price"])


df_clean=df_clean.reset_index(drop=True)


df_clean.to_csv("data/cleaned/online_retail_cleaned.csv", index=False)


df2=pd.read_excel("data/raw/online_retail_II.xlsx",sheet_name=1)


df2_clean=df2.copy()


df2_clean=df2_clean.drop_duplicates()


df2_clean=df2_clean.drop(df2_clean[df2_clean["Invoice"].astype(str).str.startswith("C")].index)


df2_clean=df2_clean[df2_clean["Quantity"]>0].copy()



df2_clean=df2_clean.drop((df2_clean[df2_clean["Price"]<=0]).index)


df2_clean["Description"]=df2_clean["Description"].fillna("Unknown")


df2_clean["Customer ID"]=df2_clean["Customer ID"].astype("Int64")



df2_clean.insert(loc=6,column="Revenue",value=df2_clean["Price"]*df2_clean["Quantity"])


df2_clean=df2_clean.reset_index(drop=True)


df2_clean = df2_clean.reset_index(drop=True)


df2_clean.to_csv("data/cleaned/online_retail_2010_2011_cleaned.csv",index=False)


df_final=pd.concat([df_clean,df2_clean],axis=0,ignore_index=True)


df_final_clean=df_final.drop_duplicates()


df_final_clean=df_final_clean.reset_index(drop=True)


df_final_clean.to_csv("data/cleaned/online_retail_final_cleaned.csv",index=False)
