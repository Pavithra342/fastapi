import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Helper function to create a product
def create_test_product():
    """
    Helper function to create a test product via API.
    Returns:
        Response object from the API call.
    """
    product = {
        "name": "Test Product",
        "description": "This is a test product",
        "price": 19.99,
        "created_by": "tester"
    }
    response = client.post("/products", json=product)
    return response

# Helper function to create a review
def create_test_review(product_id):
    """
    Helper function to create a test review for a product via API.
    Args:
        product_id (str): ID of the product for which the review is being created.
    Returns:
        Response object from the API call.
    """
    review = {
        "product_id": product_id,
        "review": "Great product!",
        "rating": 5,
        "created_by": "tester"
    }
    response = client.post(f"/products/{product_id}/reviews", json=review)
    return response

# Helper function to create an offer
def create_test_offer(product_id):
    """
    Helper function to create a test offer for a product via API.
    Args:
        product_id (str): ID of the product for which the offer is being created.
    Returns:
        Response object from the API call.
    """
    offer = {
        "product_id": product_id,
        "description": "20% off",
        "discount": 20.0,
        "created_by": "tester"
    }
    response = client.post(f"/products/{product_id}/offers", json=offer)
    return response

# Test cases for create_product
def test_create_product():
    """
    Test case to verify creation of a product via API.
    """
    response = create_test_product()
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Product"
    assert data["description"] == "This is a test product"
    assert data["price"] == 19.99

def test_create_product_missing_name():
    """
    Test case to verify API response when creating a product without a name.
    """
    product = {
        "description": "This is a test product",
        "price": 19.99,
        "created_by": "tester"
    }
    response = client.post("/products", json=product)
    assert response.status_code == 422

def test_create_product_invalid_price():
    """
    Test case to verify API response when creating a product with an invalid price.
    """
    product = {
        "name": "Test Product",
        "description": "This is a test product",
        "price": "invalid_price",
        "created_by": "tester"
    }
    response = client.post("/products", json=product)
    assert response.status_code == 422

# Test cases for fetch_product
def test_fetch_product():
    """
    Test case to verify fetching a product by ID via API.
    """
    product_response = create_test_product()
    product_id = product_response.json()["product_id"]
    response = client.get(f"/products/{product_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["product_id"] == product_id

def test_fetch_product_not_found():
    """
    Test case to verify API response when fetching a non-existent product.
    """
    response = client.get("/products/nonexistent_id")
    assert response.status_code == 404

def test_fetch_product_invalid_id():
    """
    Test case to verify API response when fetching a product with an invalid ID format.
    """
    response = client.get("/products/invalid_id")
    assert response.status_code == 404

# Test cases for update_product
def test_update_product():
    """
    Test case to verify updating a product via API.
    """
    product_response = create_test_product()
    product_id = product_response.json()["product_id"]
    update_data = {
        "name": "Updated Product",
        "description": "This is an updated test product",
        "price": 29.99,
        "created_by": "tester",
        "updated_by": "updater"
    }
    response = client.put(f"/products/{product_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Product"

def test_update_product_not_found():
    """
    Test case to verify API response when updating a non-existent product.
    """
    update_data = {
        "name": "Updated Product",
        "description": "This is an updated test product",
        "price": 29.99,
        "created_by": "tester",
        "updated_by": "updater"
    }
    response = client.put("/products/nonexistent_id", json=update_data)
    assert response.status_code == 404

def test_update_product_invalid_price():
    """
    Test case to verify API response when updating a product with an invalid price.
    """
    product_response = create_test_product()
    product_id = product_response.json()["product_id"]
    update_data = {
        "name": "Updated Product",
        "description": "This is an updated test product",
        "price": "invalid_price",
        "created_by": "tester",
        "updated_by": "updater"
    }
    response = client.put(f"/products/{product_id}", json=update_data)
    assert response.status_code == 422

# Test cases for create_product_review
def test_create_product_review():
    """
    Test case to verify creating a product review via API.
    """
    product_response = create_test_product()
    product_id = product_response.json()["product_id"]
    review_response = create_test_review(product_id)
    assert review_response.status_code == 200
    data = review_response.json()
    assert data["review"] == "Great product!"

def test_create_product_review_not_found():
    """
    Test case to verify API response when creating a review for a non-existent product.
    """
    review = {
        "product_id": "nonexistent_id",
        "review": "Great product!",
        "rating": 5,
        "created_by": "tester"
    }
    response = client.post("/products/nonexistent_id/reviews", json=review)
    assert response.status_code == 404

def test_create_product_review_invalid_rating():
    """
    Test case to verify API response when creating a review with an invalid rating.
    """
    product_response = create_test_product()
    product_id = product_response.json()["product_id"]
    review = {
        "product_id": product_id,
        "review": "Great product!",
        "rating": "invalid_rating",
        "created_by": "tester"
    }
    response = client.post(f"/products/{product_id}/reviews", json=review)
    assert response.status_code == 422

# Test cases for create_offer
def test_create_offer():
    """
    Test case to verify creating an offer for a product via API.
    """
    product_response = create_test_product()
    product_id = product_response.json()["product_id"]
    offer_response = create_test_offer(product_id)
    assert offer_response.status_code == 200
    data = offer_response.json()
    assert data["description"] == "20% off"

def test_create_offer_not_found():
    """
    Test case to verify API response when creating an offer for a non-existent product.
    """
    offer = {
        "product_id": "nonexistent_id",
        "description": "20% off",
        "discount": 20.0,
        "created_by": "tester"
    }
    response = client.post("/products/nonexistent_id/offers", json=offer)
    assert response.status_code == 404
