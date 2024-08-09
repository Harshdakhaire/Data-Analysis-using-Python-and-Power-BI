#!/usr/bin/env python
# coding: utf-8
#Importing all the packages and libraries 

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#Importing the Data file for analysis

file_path = r'F:/Solidcam Assignment/Synthetic_Software_Sales_Data.csv'
data = pd.read_csv(file_path)


data.head()

#Data Cleaning and Preparation
# In[4]:


#Convert 'Date of Sale' to datetime format
data['Date of Sale'] = pd.to_datetime(data['Date of Sale'], format='%d-%m-%Y')


# In[5]:


# Drop rows with missing values
data_cleaned = data.dropna().copy()  # Make a copy to avoid modifying the original DataFrame


# In[6]:


# Set 'Date of Sale' as index
data_cleaned.set_index('Date of Sale', inplace=True)


# In[7]:


# Extract month from Date of Sale
data_cleaned['Month'] = data_cleaned.index.month


# In[8]:


# Descriptive Analysis
# Descriptive analysis for numerical columns
numeric_summary = data_cleaned.describe()
print("Numeric Summary:")
print(numeric_summary)


# In[9]:


# Descriptive analysis for categorical columns
categorical_summary = data_cleaned.describe(include=['object'])
print("\nCategorical Summary:")
print(categorical_summary)

#Analysis of the various attributes
# In[10]:


# Sales Trends Over Time (Region-wise)
# Group by both 'Date of Sale' and 'Region', sum sales and units
monthly_sales_region = data_cleaned.groupby([pd.Grouper(freq='M'), 'Region']).sum().reset_index()


# In[11]:


# Plot sales trends over time for each region
plt.figure(figsize=(14, 7))
for region in monthly_sales_region['Region'].unique():
    region_data = monthly_sales_region[monthly_sales_region['Region'] == region]
    plt.plot(region_data['Date of Sale'], region_data['Sales Amount in US$'], label=f'{region} Sales')

plt.title('Sales Trends Over Time (Region-wise)')
plt.xlabel('Date')
plt.ylabel('Sales Amount in US$')
plt.legend()
plt.show()


# In[13]:


# Best-Performing Regions
region_sales = data_cleaned.groupby('Region')['Sales Amount in US$'].sum().sort_values(ascending=False)


# In[14]:


# Plot best-performing regions based on total sales
plt.figure(figsize=(10, 6))
sns.barplot(x=region_sales.values, y=region_sales.index, palette='viridis')
plt.title('Best-Performing Regions by Total Sales')
plt.xlabel('Total Sales Amount in US$')
plt.ylabel('Region')
plt.show()


# In[15]:


# Region-wise Sales Trends Over Time
plt.figure(figsize=(14, 10))
for i, region in enumerate(region_sales.index, start=1):
    plt.subplot(len(region_sales)//2 + len(region_sales)%2, 2, i)
    region_data = data_cleaned[data_cleaned['Region'] == region]
    monthly_sales = region_data.resample('M')['Sales Amount in US$'].sum()
    plt.plot(monthly_sales.index, monthly_sales.values, label=f'{region} Sales')
    plt.title(f'Sales Trends Over Time - {region}')
    plt.xlabel('Date')
    plt.ylabel('Sales Amount in US$')
    plt.legend()

plt.tight_layout()
plt.show()


# In[16]:


# Customer Purchase Patterns (Region-wise)
# Customer type distribution by region
customer_type_distribution = data_cleaned.groupby('Region')['Customer Type'].value_counts().unstack().fillna(0)
print("\nCustomer Type Distribution by Region:")
print(customer_type_distribution)


# In[17]:


# Returning customer distribution by region
returning_customer_distribution = data_cleaned.groupby('Region')['Returning Customer'].value_counts().unstack().fillna(0)
print("\nReturning Customer Distribution by Region:")
print(returning_customer_distribution)

#Cohort Analysis
# In[18]:


# Region-wise Cohort Analysis
# Extract year of first purchase by region
data_cleaned['Year of First Purchase'] = data_cleaned.index.year


# In[19]:


# Group by region, year of first purchase, and returning customer
cohort_data = data_cleaned.groupby(['Region', 'Year of First Purchase', 'Returning Customer']).size().unstack().fillna(0)


# In[20]:


print("\nCohort Analysis (Region, Year of First Purchase vs Returning Customer):")
print(cohort_data)


# In[21]:


# Region-wise Product Performance (Month-wise)
# Group by Region, Product Type, and Month, summing up the sales
region_product_sales_month = data_cleaned.groupby(['Region', 'Product Type', 'Month'])['Sales Amount in US$'].sum().reset_index()


# In[22]:


# Plotting product sales month-wise in each region
plt.figure(figsize=(14, 10))
for i, region in enumerate(region_product_sales_month['Region'].unique(), start=1):
    plt.subplot(len(region_product_sales_month['Region'].unique())//2 + len(region_product_sales_month['Region'].unique())%2, 2, i)
    region_data = region_product_sales_month[region_product_sales_month['Region'] == region]
    
    for product_type in region_data['Product Type'].unique():
        product_data = region_data[region_data['Product Type'] == product_type]
        plt.plot(product_data['Month'], product_data['Sales Amount in US$'], marker='o', label=f'{product_type}')
    
    plt.title(f'Product Sales Month-wise in {region}')
    plt.xlabel('Month')
    plt.ylabel('Sales Amount in US$')
    plt.xticks(range(1, 13))
    plt.legend()

plt.tight_layout()
plt.show()

