import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from fastapi.testclient import TestClient
from ..init_db import init_database
from ..main import app, db

@pytest_asyncio.fixture
async def db_setup_and_cleanup():
    await init_database(db)
    yield
    print('Limpando banco')
    await db.execute("DROP TABLE IF EXISTS percurso")
    await db.execute("DROP TABLE IF EXISTS telemetria")
    await db.disconnect()

@pytest.mark.asyncio
async def test_get_percurso(db_setup_and_cleanup):
    create_percurso = "INSERT INTO percurso DEFAULT VALUES"
    data = await db.execute(create_percurso)
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/percurso/")
    response_data = response.json()
    assert response.status_code == 200
    assert len(response_data) == 1
    assert response_data[0]['idPercurso'] == data