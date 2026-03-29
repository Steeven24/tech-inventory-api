from conftest import get_auth_headers


def test_inventory_and_sales_flow(client, admin_user):
    admin_headers = get_auth_headers(client, admin_user.email, "Admin123!")

    create_product_response = client.post(
        "/products",
        headers=admin_headers,
        json={
            "name": "Gaming Laptop",
            "category": "Computers",
            "brand": "ASUS",
            "sku": "LAPTOP-001",
            "price": 1500.0,
            "stock": 10,
        },
    )
    assert create_product_response.status_code == 201
    product_id = create_product_response.json()["id"]

    movement_response = client.post(
        "/inventory-movements",
        headers=admin_headers,
        json={
            "product_id": product_id,
            "movement_type": "in",
            "quantity": 5,
            "note": "Supplier restock",
        },
    )
    assert movement_response.status_code == 201

    product_after_restock = client.get(f"/products/{product_id}", headers=admin_headers)
    assert product_after_restock.status_code == 200
    assert product_after_restock.json()["stock"] == 15

    sale_response = client.post(
        "/sales",
        headers=admin_headers,
        json={
            "discount": 100.0,
            "items": [
                {
                    "product_id": product_id,
                    "quantity": 2,
                }
            ],
        },
    )
    assert sale_response.status_code == 201
    sale_payload = sale_response.json()
    assert sale_payload["subtotal"] == 3000.0
    assert sale_payload["total"] == 2900.0

    product_after_sale = client.get(f"/products/{product_id}", headers=admin_headers)
    assert product_after_sale.status_code == 200
    assert product_after_sale.json()["stock"] == 13

    movement_history = client.get(
        f"/inventory-movements/product/{product_id}",
        headers=admin_headers,
    )
    assert movement_history.status_code == 200
    assert len(movement_history.json()) == 2


def test_sale_fails_with_insufficient_stock(client, admin_user):
    admin_headers = get_auth_headers(client, admin_user.email, "Admin123!")

    create_product_response = client.post(
        "/products",
        headers=admin_headers,
        json={
            "name": "Console",
            "category": "Consoles",
            "brand": "Sony",
            "sku": "CONSOLE-001",
            "price": 499.0,
            "stock": 1,
        },
    )
    product_id = create_product_response.json()["id"]

    sale_response = client.post(
        "/sales",
        headers=admin_headers,
        json={
            "discount": 0,
            "items": [
                {
                    "product_id": product_id,
                    "quantity": 3,
                }
            ],
        },
    )

    assert sale_response.status_code == 400
    assert "Insufficient stock" in sale_response.json()["detail"]
