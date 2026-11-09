import pandas as pd


df_final_clean=pd.read_csv("data/cleaned/online_retail_final_cleaned.csv",parse_dates=["InvoiceDate"], dtype={"Customer ID": "Int64", "Invoice": "string", "StockCode": "string"})


#1. Sales Performance Analysis

print("Mean of Revenue:",df_final_clean["Revenue"].mean())


print("Average of Revenue by Unique Invoices:",df_final_clean.groupby("Invoice")["Revenue"].sum().mean())


pd.set_option('display.float_format', lambda x: f'{x:.2f}')
highest_revenue_by_countries=df_final_clean.groupby("Country")["Revenue"].sum().sort_values(ascending=False).head(10)
print("Highest Revenue by Countries:",highest_revenue_by_countries)


print("Yearly Revenue:",df_final_clean.groupby(df_final_clean["InvoiceDate"].dt.year)["Revenue"].sum())


print("Monthly Revenue:",df_final_clean.groupby(df_final_clean["InvoiceDate"].dt.to_period("M"))["Revenue"].sum())


print("Highest Monthly Revenue:",df_final_clean.groupby(df_final_clean["InvoiceDate"].dt.to_period("M"))["Revenue"].sum().sort_values(ascending=False).head(1))


print("Lowest Monthly Revenue:",df_final_clean.groupby(df_final_clean["InvoiceDate"].dt.to_period("M"))["Revenue"].sum().sort_values(ascending=True).head(1))


print("MoM Growth Monthly:",(df_final_clean.groupby(df_final_clean["InvoiceDate"].dt.to_period("M"))["Revenue"].sum().pct_change()*100))


#2. Product and Country Analysis

print("Top 10 Products with Quantities",df_final_clean.groupby(df_final_clean["StockCode"])["Quantity"].sum().sort_values(ascending=False).head(10))


print("Top 10 Products with Revenues",df_final_clean.groupby(df_final_clean["StockCode"])["Revenue"].sum().sort_values(ascending=False).head(10))


print("Unique StockCodes by Countries",df_final_clean.groupby(df_final_clean["Country"])["StockCode"].nunique(dropna=True).sort_values(ascending=False).head(10))


print("Top 10 Products by Revenue (Excluding Special Codes):",df_final_clean.loc[(~df_final_clean["StockCode"].isin(["M","DOT","POST","m","TEST001","TEST002","S"])) & (~df_final_clean["StockCode"].str.startswith("gift_",na=False))].groupby(df_final_clean["StockCode"])["Revenue"].sum().sort_values(ascending=False).head(10))



#3. Customer Analysis

print("Top 10 Highest Spending Customers:",df_final_clean.loc[~df_final_clean["Customer ID"].isnull()].groupby(df_final_clean["Customer ID"])["Revenue"].sum().sort_values(ascending=False).head(10))


print("Top 10 Customers who Purchased the most:",df_final_clean.loc[~df_final_clean["Customer ID"].isnull()].groupby(df_final_clean["Customer ID"])["Invoice"].nunique().sort_values(ascending=False).head(10))


revsum=(df_final_clean.loc[~df_final_clean["Customer ID"].isnull()].groupby(df_final_clean["Customer ID"])["Revenue"].sum()).sum()
customersum=df_final_clean["Customer ID"].nunique()
avg=revsum/customersum
print("Average Revenue by Customer:",avg)


customersvsinvoice=df_final_clean.loc[df_final_clean["Customer ID"].notnull()].groupby(df_final_clean["Customer ID"])["Invoice"].nunique().reset_index()
invoicecounter=customersvsinvoice.loc[customersvsinvoice["Invoice"]>=2]


customercount=len(invoicecounter)
totalcount=df_final_clean["Customer ID"].nunique()
percent=(customercount/totalcount)*100
print("Total of customers who purchased at least 2 times:",customercount)
print("Repeat Purchase Rate:",percent)


invoicecounter2=customersvsinvoice.loc[customersvsinvoice["Invoice"]==1]
print("Customers who only purchased only once:",len(invoicecounter2))


segmentcounter=df_final_clean.loc[df_final_clean["Customer ID"].notnull()].groupby(df_final_clean["Customer ID"])["Revenue"].sum().reset_index()
print("Low:",len(segmentcounter[segmentcounter["Revenue"]<1000]))
print("Medium:",len(segmentcounter.loc[(segmentcounter["Revenue"]>=1000) & (segmentcounter["Revenue"]<5000)]))
print("High:",len(segmentcounter[segmentcounter["Revenue"]>=5000]))


#4. RFM Segmentation

getdate=df_final_clean.loc[df_final_clean["Customer ID"].notnull()].groupby(df_final_clean["Customer ID"])["InvoiceDate"].max().reset_index()
refdate=pd.to_datetime("2011/12/10")
getdate["Recency"]=(refdate-getdate["InvoiceDate"]).dt.days


frequency_df=df_final_clean.loc[df_final_clean["Customer ID"].notnull()].groupby(df_final_clean["Customer ID"])["Invoice"].nunique().reset_index()
frequency_df.rename(columns={"Invoice":"Frequency"},inplace=True)



monetary_df=df_final_clean.loc[df_final_clean["Customer ID"].notnull()].groupby(df_final_clean["Customer ID"])["Revenue"].sum().reset_index()
monetary_df.rename(columns={"Revenue":"Monetary"},inplace=True)


getdate.drop(columns="InvoiceDate",inplace=True)
rfm_df=getdate.merge(frequency_df, on="Customer ID").merge(monetary_df, on="Customer ID")


rfm_df["R_Score"]=pd.qcut(rfm_df["Recency"], q=5, labels=[5, 4, 3, 2, 1])


rfm_df["F_Score"]=(pd.qcut(rfm_df["Frequency"], q=5, labels=False,duplicates="drop")+1)


rfm_df["M_Score"]=pd.qcut(rfm_df["Monetary"], q=5, labels=[1, 2, 3, 4, 5])


rfm_df["RFM_Total"] = rfm_df["R_Score"].astype("int64")+rfm_df["F_Score"].astype("int64")+rfm_df["M_Score"].astype("int64")


def rfm_segmenter(row):
    if (row["RFM_Total"]>=3) & (row["RFM_Total"]<=6):
        return "Low Value"
    elif (row["RFM_Total"]>=7) & (row["RFM_Total"]<=10):
        return "Medium Value"
    else:
        return "High Value"
rfm_df["RFM_Segment"]=rfm_df.apply(rfm_segmenter,axis=1)
print("RFM Segment Distribution:",rfm_df["RFM_Segment"].value_counts())


monetaryrate=rfm_df.groupby(rfm_df["RFM_Segment"])["Monetary"].sum()
monetaryrate2=(monetaryrate/rfm_df["Monetary"].sum())*100
monetaryrate3=monetaryrate.to_frame().merge(monetaryrate2,on="RFM_Segment")
monetaryrate3.columns=["Monetary Sum","Monetary Rate"]
print("Revenue Contribution by RFM Segment:",monetaryrate3)


recency_mean=rfm_df.groupby(rfm_df["RFM_Segment"])["Recency"].mean()
frequency_mean=rfm_df.groupby(rfm_df["RFM_Segment"])["Frequency"].mean()
monetary_mean=rfm_df.groupby(rfm_df["RFM_Segment"])["Monetary"].mean()
mean_calc=recency_mean.to_frame().merge(frequency_mean,on="RFM_Segment").merge(monetary_mean,on="RFM_Segment")
mean_calc.columns=["Recency Mean","Frequency Mean","Monetary Mean"]
print("Average RFM Metrics by Segment:",mean_calc)
