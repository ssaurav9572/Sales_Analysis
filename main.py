import pandas as pd
import os
import matplotlib.pyplot as plt
path = "./Sales_Data"
files = [file for file in os.listdir(path) if not file.startswith('.')] # Ignore hidden files

all_months_data = pd.DataFrame()

for file in files:
    current_data = pd.read_csv(path+"/"+file)
    all_months_data = pd.concat([all_months_data, current_data])
    
all_months_data.to_csv("all_data_copy.csv", index=False)
all_data = pd.read_csv("all_data_copy.csv")
'''

Clean up the data!

The first step in this is figuring out what we need to clean. I have found in practice, that you find things we need to 
clean as you perform operations and get errors. Based on the error, we decide how we should go about cleaning the data
'''

nan_df = all_data[all_data.isna().any(axis=1)]
#print(nan_df.head())

all_data = all_data.dropna(how='all')
all_data.head()

#Get rid of text in order date column
all_data = all_data[all_data['Order Date'].str[0:2]!='Or']


#Make columns correct type

all_data['Quantity Ordered'] = pd.to_numeric(all_data['Quantity Ordered'])
all_data['Price Each'] = pd.to_numeric(all_data['Price Each'])

#Add month column

all_data['Month'] = all_data['Order Date'].str[0:2]
all_data['Month'] = all_data['Month'].astype('int32')

#Add city column

def get_city(address):
    return address.split(",")[1].strip(" ")

def get_state(address):
    return address.split(",")[2].split(" ")[1]

all_data['City'] = all_data['Purchase Address'].apply(lambda x: f"{get_city(x)}  ({get_state(x)})")

# Data Exploration

# What was the best month for sales? How much was earned that month?

all_data['sales']=all_data['Quantity Ordered']*all_data['Price Each'].astype(float)
month=all_data.groupby('Month').sum('sales')
print(month)

#plotting graph
months = range(1,13)
print(months)

plt.bar(months,all_data.groupby(['Month']).sum()['sales'])
plt.xticks(months)
plt.ylabel('Sales in USD ($)')
plt.xlabel('Month number')
plt.show()


#What city sold the most product?

cities=all_data.groupby('City')['Quantity Ordered'].sum()
print(cities)

city_names = cities.index
quantities_ordered = cities.values

# Plotting graph

plt.bar(city_names, quantities_ordered, color='skyblue')
plt.xlabel('City')
plt.ylabel('Total Quantity Ordered')
plt.title('Total Quantity Ordered per City')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()


# What time should we display advertisements to maximize likelihood of customer's buying product?

all_data['Hour'] = pd.to_datetime(all_data['Order Date']).dt.hour
all_data['Minute'] = pd.to_datetime(all_data['Order Date']).dt.minute
all_data['Count'] = 1
print(all_data.head())

#plotting graph

hours = all_data.groupby('Hour')['Count'].sum()

# Extract hours and order counts
hour = hours.index
order_count = hours.values

# Plotting the graph
plt.figure(figsize=(10, 6))
plt.bar(hour, order_count, color='skyblue')
plt.xlabel('Hour of the Day')
plt.ylabel('Number of Orders')
plt.title('Number of Orders per Hour')
plt.xticks(hour)  # Ensure all hours are shown on the x-axis
plt.grid(True)
plt.tight_layout()
plt.show()


# What products are most often sold together?

# https://stackoverflow.com/questions/43348194/pandas-select-rows-if-id-appear-several-time
df = all_data[all_data['Order ID'].duplicated(keep=False)]

# Referenced: https://stackoverflow.com/questions/27298178/concatenate-strings-from-several-rows-using-pandas-groupby
df['Grouped'] = df.groupby('Order ID')['Product'].transform(lambda x: ','.join(x))
df2 = df[['Order ID', 'Grouped']].drop_duplicates()

# Referenced: https://stackoverflow.com/questions/52195887/counting-unique-pairs-of-numbers-into-a-python-dictionary
from itertools import combinations
from collections import Counter

count = Counter()

for row in df2['Grouped']:
    row_list = row.split(',')
    count.update(Counter(combinations(row_list, 2)))

for key,value in count.most_common(10):
    print(key, value)



# What product sold the most? 

products = all_data.groupby('Product')['Quantity Ordered'].sum()
print(products)
product=products.index
sold_items=products.values
plt.bar(product,sold_items)
plt.xlabel('Name of products')
plt.ylabel('Quantity Sold')
plt.xticks(product, rotation=90, ha='right')
plt.tight_layout()
plt.show()


