"""
Tests de API contra https://jsonplaceholder.typicode.com
Cubre: GET, POST, DELETE y encadenamiento de peticiones (Clases 11 y 12).
"""
import pytest
import requests

BASE = "https://jsonplaceholder.typicode.com"


# ─── GET ─────────────────────────────────────────────────────────────────────

@pytest.mark.api
def test_get_lista_usuarios():
    """GET /users — valida status, cantidad y estructura de cada usuario."""
    r = requests.get(f"{BASE}/users")
    assert r.status_code == 200
    data = r.json()
    assert len(data) > 0
    campos_requeridos = {"id", "name", "username", "email"}
    for usuario in data:
        assert campos_requeridos <= set(usuario.keys()), f"Faltan campos en usuario: {usuario}"


@pytest.mark.api
def test_get_usuario_individual():
    """GET /users/2 — valida status, id y presencia de email."""
    r = requests.get(f"{BASE}/users/2")
    assert r.status_code == 200
    usuario = r.json()
    assert usuario["id"] == 2
    assert "@" in usuario["email"]
    assert r.elapsed.total_seconds() < 3


@pytest.mark.api
def test_get_usuario_no_encontrado():
    """GET /users/9999 — valida que la API devuelve 404 para recursos inexistentes."""
    r = requests.get(f"{BASE}/users/9999")
    assert r.status_code == 404


# ─── POST ────────────────────────────────────────────────────────────────────

@pytest.mark.api
def test_post_crear_post():
    """POST /posts — crea un recurso y valida los campos devueltos."""
    payload = {"title": "QA Automation", "body": "automation tester", "userId": 1}
    r = requests.post(f"{BASE}/posts", json=payload)
    assert r.status_code == 201
    body = r.json()
    assert body["title"] == payload["title"]
    assert body["body"] == payload["body"]
    assert body["userId"] == payload["userId"]
    assert "id" in body


@pytest.mark.api
def test_post_crear_comentario():
    """POST /comments — crea un comentario y valida la estructura devuelta."""
    payload = {
        "postId": 1,
        "name": "Test QA",
        "email": "qa@test.com",
        "body": "Comentario de prueba automatizada",
    }
    r = requests.post(f"{BASE}/comments", json=payload)
    assert r.status_code == 201
    body = r.json()
    assert body["postId"] == payload["postId"]
    assert body["email"] == payload["email"]
    assert "id" in body


@pytest.mark.api
def test_post_crear_sin_campos_requeridos():
    """POST /posts con body vacío — valida que la API acepta y responde con id."""
    r = requests.post(f"{BASE}/posts", json={})
    assert r.status_code == 201
    assert "id" in r.json()


# ─── DELETE ──────────────────────────────────────────────────────────────────

@pytest.mark.api
def test_delete_post():
    """DELETE /posts/1 — valida que la eliminación devuelve 200."""
    r = requests.delete(f"{BASE}/posts/1")
    assert r.status_code == 200


# ─── ENCADENAMIENTO ──────────────────────────────────────────────────────────

@pytest.mark.api
def test_crear_y_verificar_post():
    """Encadenamiento: POST para crear un post y verifica que los datos devueltos coinciden."""
    payload = {"title": "Chain Test", "body": "qa engineer", "userId": 1}
    r_crear = requests.post(f"{BASE}/posts", json=payload)
    assert r_crear.status_code == 201

    creado = r_crear.json()
    assert creado["title"] == payload["title"]
    assert creado["body"] == payload["body"]
    assert creado["id"] is not None

    print(f"\nPost creado con id={creado['id']}")
