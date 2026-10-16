
from app import app


def test_alice_can_access_own_order():
    client = app.test_client()

    # Iniciar sesión como Alice
    login_response = client.post(
        "/login",
        json={"username": "alice", "password": "alice123"}
    )

    assert login_response.status_code == 200

    # Consultar el pedido de Alice
    response = client.get("/orders/101")

    assert response.status_code == 200

    data = response.get_json()
    assert data["owner"] == "alice"
    assert data["order_id"] == 101





def test_bob_can_access_own_order():
    client = app.test_client()

    # Iniciar sesión como Bob
    login_response = client.post(
        "/login",
        json={"username": "bob", "password": "bob123"}
    )

    assert login_response.status_code == 200

    # Bob consulta su propio pedido
    response = client.get("/orders/102")

    assert response.status_code == 200

    data = response.get_json()
    assert data["owner"] == "bob"
    assert data["order_id"] == 102



def test_alice_cannot_access_bobs_order():
    client = app.test_client()

    # Iniciar sesión como Alice
    login_response = client.post(
        "/login",
        json={"username": "alice", "password": "alice123"}
    )

    assert login_response.status_code == 200

    # Alice intenta consultar el pedido de Bob
    response = client.get("/orders/102")

    # La API debe rechazar el acceso
    assert response.status_code == 404

    data = response.get_json()
    assert data == {"error": "Order not found"}
