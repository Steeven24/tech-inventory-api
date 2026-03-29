from conftest import get_auth_headers


def test_root_health(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "API working"}


def test_public_signup_forces_seller_role(client):
    signup_response = client.post(
        "/users",
        json={
            "name": "New User",
            "email": "new-user@test.com",
            "password": "Secure123!",
            "role": "admin",
        },
    )

    assert signup_response.status_code == 201
    assert signup_response.json()["role"] == "seller"

    headers = get_auth_headers(client, "new-user@test.com", "Secure123!")
    me_response = client.get("/auth/me", headers=headers)

    assert me_response.status_code == 200
    assert me_response.json()["role"] == "seller"


def test_seller_cannot_access_admin_reports(client, seller_user):
    headers = get_auth_headers(client, seller_user.email, "Seller123!")

    response = client.get("/reports/dashboard-overview", headers=headers)

    assert response.status_code == 403


def test_admin_can_access_admin_reports(client, admin_user):
    headers = get_auth_headers(client, admin_user.email, "Admin123!")

    response = client.get("/reports/dashboard-overview", headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert "products_count" in data
    assert "sales_count" in data
