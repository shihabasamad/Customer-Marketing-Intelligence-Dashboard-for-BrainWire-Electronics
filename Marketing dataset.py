import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta
import os

# Create 'data' directory if it doesn't exist
os.makedirs('data', exist_ok=True)


fake = Faker()
Faker.seed(42)
np.random.seed(42)
random.seed(42)

# Parameters
n_customers = 4000
n_orders = 10000
start_date = datetime(2020, 4, 1).date()
end_date = datetime(2023, 4, 1).date()
countries = ['Germany', 'France', 'Spain', 'Italy', 'Netherlands', 'Poland', 'Sweden', 'Belgium']
channels = ['Facebook', 'Instagram', 'Reddit', 'Google Ads', 'Web Ads', 'Influencer']

# Product Catalog
products = [
    {'ProductID': 1, 'Name': 'AI Keyboard', 'Category': 'AI Device', 'Price': 129.99},
    {'ProductID': 2, 'Name': 'Multi-language Earbud', 'Category': 'AI Device', 'Price': 199.99},
    {'ProductID': 3, 'Name': 'Smart Glasses', 'Category': 'Wearable', 'Price': 179.99},
    {'ProductID': 4, 'Name': 'Wireless Charger', 'Category': 'Accessories', 'Price': 39.99},
    {'ProductID': 5, 'Name': 'Portable Projector', 'Category': 'Gadgets', 'Price': 249.99},
    {'ProductID': 6, 'Name': 'Smartwatch Pro', 'Category': 'Wearable', 'Price': 149.99},
    {'ProductID': 7, 'Name': 'Voice Assistant Lamp', 'Category': 'Home Tech', 'Price': 89.99},
    {'ProductID': 8, 'Name': 'AI Pen Translator', 'Category': 'AI Device', 'Price': 99.99}
]
products_df = pd.DataFrame(products)

# Customer Table
def generate_customers(n):
    customers = []
    for i in range(1, n + 1):
        reg_date = fake.date_between(start_date, end_date)
        segment = np.random.choice(['Premium', 'Regular', 'Discount Seeker', 'One-Time'], p=[0.2, 0.5, 0.2, 0.1])
        customers.append({
            'CustomerID': i,
            'Name': fake.name(),
            'Email': fake.email(),
            'Country': random.choice(countries),
            'Gender': random.choice(['Male', 'Female', 'Other']),
            'Age': random.randint(18, 65),
            'Segment': segment,
            'RegistrationDate': reg_date
        })
    return pd.DataFrame(customers)

customers_df = generate_customers(n_customers)

# Order Table
def generate_orders(n):
    orders = []
    for i in range(1, n + 1):
        customer = customers_df.sample(1).iloc[0]
        product = random.choice(products)
        order_date = fake.date_between(start_date, end_date)
        quantity = random.randint(1, 3)
        
        # Trend simulation: 1st 6 months low, mid 2 years growth, last 6 months dip
        if order_date < datetime(2020, 10, 1).date():
            if random.random() > 0.4: continue  # simulate slow start
        elif order_date > datetime(2022, 10, 1).date():
            if random.random() > 0.7: continue  # simulate turbulence

        total_amount = product['Price'] * quantity
        orders.append({
            'OrderID': i,
            'CustomerID': customer.CustomerID,
            'ProductID': product['ProductID'],
            'OrderDate': order_date,
            'Quantity': quantity,
            'UnitPrice': product['Price'],
            'TotalAmount': total_amount
        })
    return pd.DataFrame(orders)

orders_df = generate_orders(n_orders)

# Campaign Table
campaigns = []
for i in range(1, 61):
    start = fake.date_between(start_date, end_date)
    end = start + timedelta(days=random.randint(5, 30))
    campaigns.append({
        'CampaignID': i,
        'Name': f"{random.choice(['Winter', 'Summer', 'New Product', 'Holiday'])} Campaign {i}",
        'Channel': random.choice(channels),
        'StartDate': start,
        'EndDate': end,
        'Budget': round(random.uniform(1000, 10000), 2)
    })
campaigns_df = pd.DataFrame(campaigns)

# Campaign Responses
responses = []
for i in range(5000):
    cust = customers_df.sample(1).iloc[0]
    camp = campaigns_df.sample(1).iloc[0]
    response_date = fake.date_between(camp.StartDate, camp.EndDate)
    responses.append({
        'ResponseID': i+1,
        'CustomerID': cust.CustomerID,
        'CampaignID': camp.CampaignID,
        'ResponseDate': response_date,
        'Action': random.choice(['Clicked', 'Purchased', 'Ignored', 'Visited Website'])
    })
responses_df = pd.DataFrame(responses)

# Web Behavior
web_data = []
for i in range(1, 5001):
    cust = customers_df.sample(1).iloc[0]
    session_date = fake.date_between(start_date, end_date)
    sessions = random.randint(1, 5)
    web_data.append({
        'SessionID': i,
        'CustomerID': cust.CustomerID,
        'SessionDate': session_date,
        'PageViews': random.randint(1, 10),
        'BounceRate': round(random.uniform(0.1, 0.9), 2),
        'TimeOnSite_Min': round(random.uniform(1, 15), 2)
    })
web_df = pd.DataFrame(web_data)

# Returns Table
returns = []
returned_orders = orders_df.sample(frac=0.06)
for i, row in returned_orders.iterrows():
    returns.append({
        'ReturnID': i+1,
        'OrderID': row.OrderID,
        'CustomerID': row.CustomerID,
        'ReturnDate': row.OrderDate + timedelta(days=random.randint(2, 20)),
        'Reason': random.choice(['Defective', 'Not Satisfied', 'Wrong Item', 'No Longer Needed'])
    })
returns_df = pd.DataFrame(returns)

# Date Table
date_range = pd.date_range(start=start_date, end=end_date)
date_table = pd.DataFrame({
    'Date': date_range,
    'Year': date_range.year,
    'Month': date_range.month,
    'MonthName': date_range.strftime('%B'),
    'Day': date_range.day,
    'Weekday': date_range.strftime('%A'),
    'Quarter': date_range.quarter
})

# Save all as CSV
customers_df.to_csv('data/Customers.csv', index=False)
products_df.to_csv('data/Products.csv', index=False)
orders_df.to_csv('data/Orders.csv', index=False)
campaigns_df.to_csv('data/Campaigns.csv', index=False)
responses_df.to_csv('data/CampaignResponses.csv', index=False)
web_df.to_csv('data/WebBehavior.csv', index=False)
returns_df.to_csv('data/Returns.csv', index=False)
date_table.to_csv('data/DateTable.csv', index=False)

print("All CSVs generated successfully!")
