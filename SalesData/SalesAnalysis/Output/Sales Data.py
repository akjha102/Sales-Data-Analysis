#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import os


# <b>Merge the 12 months sales data into a single CSV</b>

# In[3]:


df=pd.read_csv("Desktop/Sales_Data/Sales_April_2019.csv")
files=[file for file in os.listdir('Desktop/Sales_Data')]
all_months_data=pd.DataFrame()

for file in files:
    df=pd.read_csv("Desktop/Sales_Data/"+file)
    all_months_data = pd.concat( [all_months_data,df] )
    
all_months_data.to_csv("all_data.csv",index=False)


# <b>Read in Updated DataFrame</b>

# In[4]:


all_data=pd.read_csv("all_data.csv")
all_data.head()


# <b>Clean up the data</b>

# In[5]:


all_data.isna().sum()


# In[6]:


all_data.shape


# In[7]:


all_data=all_data.dropna(how='all')


# In[8]:


all_data.isna().sum()


# <b>Find 'Or' and delete it</b>

# In[9]:


temp_df=all_data[all_data['Order Date'].str[0:2]=='Or']
temp_df.head()


# In[10]:


temp_df.shape


# In[11]:


all_data=all_data[all_data['Order Date'].str[0:2]!='Or']


# <b>Adding Month Column</b>

# In[12]:


all_data['Month']=all_data['Order Date'].str[0:2]
all_data['Month']=pd.to_numeric(all_data['Month'])
all_data


# In[13]:


all_data['Quantity Ordered'] = pd.to_numeric(all_data['Quantity Ordered'])
all_data['Price Each'] = pd.to_numeric(all_data['Price Each'])


# In[14]:


all_data.info()


# <b>Adding a Sales Column</b>

# In[15]:


all_data['Sales']=all_data['Quantity Ordered']*all_data['Price Each']
all_data


# In[16]:


all_data.info()


# <b>Best month of sales</b>

# In[17]:


g1=all_data.groupby('Month').sum()
g1


# In[18]:


months=range(1,13)
plt.bar(months,g1['Sales'])
plt.xticks(months)
plt.ylabel('Sales in USD ($)')
plt.xlabel('Month Number')
plt.show()


# <b>City wise sales</b>

# Adding City column

# In[20]:


def get_state(address):
    return address.split(',')[2].split(" ")[1]

all_data['City']=all_data['Purchase Address'].apply(lambda x: x.split(',')[1] + ' '+'('+get_state(x)+')')
all_data


# In[21]:


g2=all_data.groupby('City').sum()
g2


# In[22]:


all_data2=all_data


# In[23]:


cities = [city for city,df in all_data.groupby('City')]
#cities=all_data['City'].unique()
plt.bar(cities,g2['Sales'])
plt.xticks(cities,rotation='vertical')
plt.ylabel('Sales in USD ($)')
plt.xlabel('City Name')
plt.show()


# <b>At What time should advertisments be displayed in order to Increase liklihood of customers bying the products.</b>

# In[24]:


all_data['Order Date']=pd.to_datetime(all_data['Order Date'])


# In[25]:


all_data


# In[26]:


all_data['Hour']=all_data['Order Date'].dt.hour


# In[28]:


all_data.head()


# In[29]:


all_data['Minute']=all_data['Order Date'].dt.minute
all_data.head()


# In[40]:


hours= [hour for hour,df in all_data.groupby('Hour')]
g3=all_data.groupby('Hour')
plt.plot(hours,g3['Hour'].count())
plt.xticks(hours)
plt.xlabel('Hour')
plt.ylabel('Number of Orders')
plt.grid()
plt.show()


# <b>Just before 11 Am or around 6 Pm is the right time for advertisment because peak is at 11-12 Hours and at 7 Pm</b>

# <h4>Are there any kind of product(s) which are sold together</h4>

# In[49]:


df=all_data[all_data['Order ID'].duplicated(keep=False)]
df['Grouped']=df.groupby('Order ID')['Product'].transform(lambda x: ','.join(x))
df=df[['Order ID','Grouped']].drop_duplicates()
df.head(10)


# <h2>Count of Items which are purchesed together</h2>

# In[59]:


count=df['Grouped'].value_counts().sort_index(ascending=False).sort_values(ascending=False)
count.head(30)


# <b>Number of times a Product is brought</b> 

# In[61]:


g4=all_data.groupby('Product').sum()['Quantity Ordered']
g4


# In[72]:


product_group=all_data.groupby('Product')
quantity_ordered=product_group.sum()['Quantity Ordered']
products= [product for product,df in product_group]
plt.bar(products,quantity_ordered)

plt.ylabel('Quantity Ordered')
plt.xlabel('Product')
plt.xticks(products,rotation='vertical')
plt.show()


# In[75]:


prices = all_data.groupby('Product').mean()['Price Each']

fig, ax1 = plt.subplots()

ax2 = ax1.twinx()
ax1.bar(products, quantity_ordered, color='g')
ax2.plot(products, prices, color='b')

ax1.set_xlabel('Product Name')
ax1.set_ylabel('Quantity Ordered', color='g')
ax2.set_ylabel('Price ($)', color='b')
ax1.set_xticklabels(products, rotation='vertical', size=8)

fig.show()


# In[ ]:




