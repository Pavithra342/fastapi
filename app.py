"""
Streanlit - An E-commerce Product Display App using Streamlit

This module fetches product data from two APIs (FakeStore and Platzi) and displays the products in a 
Streamlit web application. The products can be filtered by category and viewed with pagination.
"""

import io
import random
from PIL import Image
import requests
import streamlit as st
import pandas as pd
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Disable SSL certificate verification warning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Constants
PER_PAGE = 9
PLACEHOLDER_IMAGE_URL = 'https://picsum.photos/200'
PRODUCTS_COUNT = 10000

# Function to fetch products from the FakeStore API
def fetch_fakestore_products(timeout=10):
    """
    Fetch products from the FakeStore API.

    Parameters:
        timeout (int): Timeout for the request in seconds.

    Returns:
        list: List of products from the API.
    """
    url = "https://fakestoreapi.com/products"
    response = requests.get(url, verify=False, timeout=timeout)
    return response.json()

# Function to fetch products from the Platzi Fake Store API
def fetch_platzi_products(timeout=10):
    """
    Fetch products from the Platzi Fake Store API.

    Parameters:
        timeout (int): Timeout for the request in seconds.

    Returns:
        list: List of products from the API.
    """
    url = "https://api.escuelajs.co/api/v1/products"
    response = requests.get(url, verify=False, timeout=timeout)
    return response.json()

# Function to resize images
def resize_image(image_url, size=(200, 200), timeout=10):
    """
    Resize image from the provided URL.

    Parameters:
        image_url (str): URL of the image to fetch and resize.
        size (tuple): Size to resize the image to.
        timeout (int): Timeout for the request in seconds.

    Returns:
        Image: Resized PIL Image object.
    """
    try:
        response = requests.get(image_url, verify=False, timeout=timeout)
        response.raise_for_status()
        img = Image.open(io.BytesIO(response.content))
    except requests.RequestException:
        response = requests.get(PLACEHOLDER_IMAGE_URL, stream=True, timeout=timeout)
        img = Image.open(io.BytesIO(response.content))
    return img.resize(size)

# Fetch product data from both APIs
fakestore_products = fetch_fakestore_products()
platzi_products = fetch_platzi_products()

# Normalize Platzi products to match FakeStore product structure
for product in platzi_products:
    product['image'] = product.get('images', [PLACEHOLDER_IMAGE_URL])[0]
    product['price'] = product.get('price', 0)
    product['title'] = product.get('title', 'No title')
    product['description'] = product.get('description', 'No description')
    product['category'] = product.get('category', {}).get('name', 'No category')

# Combine both datasets
all_products = fakestore_products + platzi_products

# Prepare DataFrame
df = pd.DataFrame(all_products)

# Simulate more products by repeating the existing products
multiplier = (PRODUCTS_COUNT // len(df)) + 1
df = pd.concat([df] * multiplier, ignore_index=True).head(PRODUCTS_COUNT)

# Ensure length of offers and reviews matches the length of the DataFrame
num_products = len(df)
offers = ['10% off', '15% off', '20% off', '25% off', '30% off', '35% off', '40% off', '45% off', '50% off', '55% off'] * (num_products // 10 + 1)
reviews = [
    'Excellent product!', 'Good value for money.', 'Highly recommended.', 'Superb quality.', 'Will buy again.',
    'Best product ever.', 'Amazing product.', 'Fantastic value.', 'Top-notch product.', 'Highly satisfied.'
] * (num_products // 10 + 1)

# Simulate ratings (1 to 5 stars)
ratings = [random.randint(1, 5) for _ in range(num_products)]

# Slice to match the length of the DataFrame
df['offer'] = offers[:num_products]
df['review'] = reviews[:num_products]
df['rating'] = ratings

# Adding Categories
categories = df['category'].unique() if 'category' in df else ['Electronics', 'Jewelery', 'Men\'s clothing', 'Women\'s clothing']

# Streamlit UI - Set page title and icon
st.set_page_config(page_title="Aureate", page_icon=":shopping_cart:")

# Header - Navigation bar
st.subheader("Our Awesome Products")
st.write(" ")
st.sidebar.title("Navigation")

# Sidebar - Category selection
selected_category = st.sidebar.selectbox("Select Category", ["All Products"] + list(categories))

# Filter products based on category selection
filtered_df = df if selected_category == "All Products" else df[df['category'] == selected_category]

# Pagination setup
total_pages = (len(filtered_df) // PER_PAGE) + (1 if len(filtered_df) % PER_PAGE > 0 else 0)

# Session state to store current page number
if "page_number" not in st.session_state:
    st.session_state.page_number = 1

# Input for current page number
current_page = st.sidebar.number_input('Page', min_value=1, max_value=total_pages, step=1, value=st.session_state.page_number)

# Calculate start and end indices for current page
start_idx = (current_page - 1) * PER_PAGE
end_idx = start_idx + PER_PAGE
current_products = filtered_df.iloc[start_idx:end_idx]

# Display products in rows of three
for i in range(0, len(current_products), 3):
    cols = st.columns(3)
    for col, (_, product) in zip(cols, current_products.iloc[i:i+3].iterrows()):
        with col:
            try:
                img = resize_image(product['image'])
            except requests.RequestException:
                img = Image.open(requests.get(PLACEHOLDER_IMAGE_URL, stream=True).raw).resize((200, 200))
            st.image(img, width=200)
            st.subheader(product['title'])
            st.write(product['description'])
            st.write(f"**Price:** ${product['price']}")
            st.write(f"**Offer:** {product['offer']}")
            st.write(f"**Review:** {product['review']}")
            st.write(f"**Rating:** {'⭐' * product['rating']}")
            st.write("---")

# Pagination controls at the bottom
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    if current_page > 1:
        if st.button("Previous"):
            st.session_state.page_number -= 1
            st.experimental_rerun()
with col2:
    st.write(f"Page {current_page} of {total_pages}")
with col3:
    if current_page < total_pages:
        if st.button("Next"):
            st.session_state.page_number += 1
            st.experimental_rerun()
