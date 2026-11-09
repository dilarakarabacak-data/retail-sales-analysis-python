import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from retail_analysis import rfm_df
import pandas as pd
from pathlib import Path

figures_dir = Path("figures")
figures_dir.mkdir(parents=True, exist_ok=True)
df_final_clean=pd.read_csv("data/cleaned/online_retail_final_cleaned.csv",parse_dates=["InvoiceDate"], dtype={"Customer ID": "Int64", "Invoice": "string", "StockCode": "string"})

#1. Monthly Revenue Trend

monthly_rev=df_final_clean.groupby(df_final_clean["InvoiceDate"].dt.to_period("M"))["Revenue"].sum().to_frame(name="Total Revenue")
monthly_rev.index=monthly_rev.index.to_timestamp()
monthly_rev.index.rename("Month",inplace=True)
monthly_rev=monthly_rev.sort_index()
filtered_rev=monthly_rev.loc["2009-12":"2011-12"]
plt.figure(1,figsize=(10,5))
sns.set_style(style="whitegrid")
sns.lineplot(data=filtered_rev.reset_index(),x="Month",y="Total Revenue",marker="o",linewidth=2.5,color="green")
ax=plt.gca()
plt.title("Monthly Revenue Trend", fontsize=14, fontweight="bold", pad=15)
plt.ylabel("Total Revenue (£)", fontsize=12)
plt.xlabel("Month", fontsize=12)
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
plt.xticks(rotation=45)
plt.savefig(figures_dir/"monthly_revenue_trend.png",dpi=300, bbox_inches="tight")

#2. Top 10 Products by Revenue

top10products=df_final_clean.loc[(~df_final_clean["StockCode"].isin(["M","DOT","POST","m","TEST001","TEST002","S"])) & (~df_final_clean["StockCode"].str.startswith("gift_",na=False))].groupby(df_final_clean["StockCode"])["Revenue"].sum().sort_values(ascending=False).head(10).to_frame(name="Total Revenue").reset_index()
top10products.columns=["Product","Total Revenue"]
plt.figure(2,figsize=(10,6))
sns.barplot(x="Total Revenue",y="Product",data=top10products,orient="h",color="royalblue")
plt.title("Top 10 Products by Total Revenue", fontsize=14, fontweight="bold", pad=15)
plt.xlabel("Total Revenue (£)", fontsize=12)
plt.ylabel("StockCode", fontsize=12)
plt.tight_layout()
plt.savefig(figures_dir/"top10_products_by_revenue.png",dpi=300, bbox_inches="tight")


#3. Top 10 Countries by Revenue

top10countries=df_final_clean.groupby(df_final_clean["Country"])["Revenue"].sum().sort_values(ascending=False).head(10).to_frame(name="Total Revenue").reset_index()
plt.figure(3,figsize=(10,6))
sns.barplot(x="Country",y="Total Revenue",data=top10countries,orient="v",color="orange")
plt.title("Top 10 Countries by Revenue",fontsize=14, fontweight="bold", pad=15)
plt.ylabel("Total Revenue (£)", fontsize=12)
plt.xlabel("Country", fontsize=12)
plt.tight_layout()
plt.savefig(figures_dir/"top10_countries_by_revenue.png",dpi=300, bbox_inches="tight")


#4. Customer Distribution by RFM Segment

order=["Low Value","Medium Value","High Value"]
customervsrfmseg=rfm_df.groupby(rfm_df["RFM_Segment"])["Customer ID"].count().to_frame(name="Number of Customers").reset_index()
plt.figure(4,figsize=(10,6))
sns.barplot(x="RFM_Segment",y="Number of Customers",order=order,data=customervsrfmseg,color="purple")
plt.title("Customer Distribution by RFM Segment",fontsize=14, fontweight="bold", pad=15)
plt.xlabel("RFM Segment", fontsize=12)
plt.ylabel("Number of Customers", fontsize=12)
plt.tight_layout()
plt.savefig(figures_dir/"customer_distributions_by_rfmsegment.png",dpi=300, bbox_inches="tight")


#5. Revenue Contribution by RFM Segment

totalmonetary=rfm_df.groupby(rfm_df["RFM_Segment"])["Monetary"].sum().to_frame(name="Total Monetary").reset_index()
plt.figure(5,figsize=(6,6))
colors=sns.color_palette("pastel")
labels=totalmonetary["RFM_Segment"]
plt.pie(totalmonetary["Total Monetary"],labels=labels,colors=colors,autopct="%1.2f%%",startangle=90)
plt.title("Revenue Contribution by RFM Segment",fontsize=14, fontweight="bold", pad=15)
plt.savefig(figures_dir/"revenue_contribution_by_rfmsegment.png",dpi=300, bbox_inches="tight")


#6. Average Monetary Value by RFM Segment

avgmonetary=rfm_df.groupby(rfm_df["RFM_Segment"])["Monetary"].mean().to_frame(name="Average Monetary").reset_index()
plt.figure(6,figsize=(10,6))
sns.barplot(data=avgmonetary,x="RFM_Segment",order=order,y="Average Monetary",color="pink")
plt.title("Average Monetary Value by RFM Segment",fontsize=14, fontweight="bold", pad=15)
plt.xlabel("RFM Segment", fontsize=12)
plt.ylabel("Average Monetary Value (£)", fontsize=12)
plt.tight_layout()
plt.savefig(figures_dir/"avg_monetary_by_rfmsegments.png",dpi=300, bbox_inches="tight")
plt.show()