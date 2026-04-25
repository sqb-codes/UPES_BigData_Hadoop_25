import streamlit as st
# To call backend API
import requests
from kafka import KafkaProducer
import json
import time

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v : json.dumps(v).encode()
)

# Setup UI with Streamlit
st.set_page_config(page_title="E-comm Recommendation System",
                   layout="wide")

st.title("E-commerce Real Time Recommendation System")
# users = [101,102,103,104,105]
# products = [9001,9002,9003,9004,9005]
# events = ["view", "click", "add_to_cart", "search"]
products = [
    {"id": 101, "name": "Apple Macbook", "price": 76000},
    {"id": 102, "name": "Apple IPhone 17", "price": 96000},
    {"id": 103, "name": "Boat headphones", "price": 4000},
    {"id": 104, "name": "Adidas shoes", "price": 6500},
    {"id": 105, "name": "Puma shoes", "price": 7800},
]

user_id = 1001

st.subheader("Browse Products")
cols = st.columns(len(products))

# for item in products:
#     print(item)

# for i in range(len(products)):
#     print(i, products[i])

for i, item in enumerate(products):
    with cols[i]:
        st.write(f"## {item['name']}")
        st.write(f"## {item['price']}")
        # View Button
        if st.button(f"View {item['name']}", key=f"view_{item['id']}"):
            event = {
                "user_id": user_id,
                "product_id": item['id'],
                "event_type": "view",
                "timestamp": time.time()
            }
            producer.send("clickstream", value=event)
            st.success(f"Viewed : {item['name']}")

        # Add to Cart Button
        if st.button(f"Add to Cart", key=f"cart_{item['id']}"):
            event = {
                "user_id": user_id,
                "product_id": item['id'],
                "product_name": item['name'],
                "event_type": "add_to_cart",
                "timestamp": time.time()
            }
            producer.send("clickstream", value=event)
            st.success(f"Added to Cart : {item['name']}")


# Trending Products
st.subheader("Trending Products")
try:
    URL = "http://localhost:8000/trending"
    response = requests.get(URL)
    data = response.json()

    if data['trending']:
        for item in data['trending'][:5]:
            product_id = item.get('product_id')
            for product in products:
                if product['id'] == product_id:
                    name = product['name']
                    price = product['price']
                    st.write(f"Product name : {name}")
                    st.write(f"Product price : {price}")
    else:
        st.write("No recommendations yet...")
except Exception as ex:
    print("Error while fetching trending products :",ex)
