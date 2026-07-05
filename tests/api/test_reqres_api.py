"""
Tests de API contra https://reqres.in/api
Cubre: GET, POST, DELETE y encadenamiento de peticiones (Clases 11 y 12).
"""
import pytest
import requests

BASE = "https://reqres.in/api"


# ─── GET ─────────────────────────────────────────────────────────────────────

@pytest.mark.api
def test_get_lista_usuarios():
    """GET /users?page=2 — valida status, paginación y estructura de cada usuario."""
    r = requests.get(f"{BASE}/users?page=2")
    assert r.status_code == 200
    data = r.json()
    assert data["page"] == 2
    assert len(data["data"]) > 0
    campos_requeridos = {"id", "email", "first_name", "last_name", "avatar"}
    for usuario in data["data"]:
        assert campos_requeridos <= set(usuario.keys()), f"Faltan campos en usuario: {usuario}"


@pytest.mark.api
def test_get_usuario_individual():
    """GET /users/2 — valida status, id y dominio de email."""
    r = requests.get(f"{BASE}/users/2")
    assert r.status_code == 200
    usuario = r.json()["data"]
    assert usuario["id"] == 2
    assert "@reqres.in" in usuario["email"]
    assert r.elapsed.total_seconds() < 2


@pytest.mark.api
def test_get_usuario_no_encontrado():
    """GET /users/999 — valida que la API devuelve 404 para recursos inexistentes."""
    r = requests.get(f"{BASE}/users/999")
    assert r.status_code == 404


# ─── POST ────────────────────────────────────────────────────────────────────

@pytest.mark.api
def test_post_crear_usuario():
    """POST /users — crea un usuario y valida los campos devueltos."""
    payload = {"name": "Esteban QA", "job": "automation tester"}
    r = requests.post(f"{BASE}/users", json=payload)
    assert r.status_code == 201
    body = r.json()
    assert body["name"] == payload["name"]
    assert body["job"] == payload["job"]
    assert "id" in body
    assert "createdAt" in body


@pytest.mark.api
def test_post_login_exitoso():
    """POST /login — valida que un login exitoso devuelve un token."""
    r = requests.post(
        f"{BASE}/login",
        json={"email": "eve.holt@reqres.in", "password": "cityslicka"},
    )
    assert r.status_code == 200
    assert "token" in r.json()


@pytest.mark.api
def test_post_login_sin_password():
    """POST /login — escenario negativo: falta el campo password."""
    r = requests.post(f"{BASE}/login", json={"email": "eve.holt@reqres.in"})
    assert r.status_code == 400
    assert "error" in r.json()


# ─── DELETE ──────────────────────────────────────────────────────────────────

@pytest.mark.api
def test_delete_usuario():
    """DELETE /users/2 — valida que la eliminación devuelve 204 sin cuerpo."""
    r = requests.delete(f"{BASE}/users/2")
    assert r.status_code == 204
    assert r.text == ""


# ─── ENCADENAMIENTO ──────────────────────────────────────────────────────────

@pytest.mark.api
def test_crear_y_verificar_usuario():
    """Encadenamiento: POST para crear un usuario y verifica que los datos devueltos coinciden."""
    payload = {"name": "Chain Test", "job": "qa engineer"}
    r_crear = requests.post(f"{BASE}/users", json=payload)
    assert r_crear.status_code == 201

    creado = r_crear.json()
    assert creado["name"] == payload["name"]
    assert creado["job"] == payload["job"]
    assert creado["id"] is not None
    assert "createdAt" in creado

    print(f"\nUsuario creado con id={creado['id']} en {creado['createdAt']}")
