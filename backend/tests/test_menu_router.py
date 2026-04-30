import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.store import Store
from app.models.user import User, UserRole
from app.utils.security import hash_password, create_access_token


@pytest_asyncio.fixture
async def store(db_session: AsyncSession) -> Store:
    store = Store(name="테스트매장", code="test-store")
    db_session.add(store)
    await db_session.flush()
    return store


@pytest_asyncio.fixture
async def admin_token(db_session: AsyncSession, store: Store) -> str:
    user = User(
        store_id=store.id,
        username="admin",
        password_hash=hash_password("password"),
        role=UserRole.STORE_ADMIN,
    )
    db_session.add(user)
    await db_session.flush()
    return create_access_token({"user_id": user.id, "store_id": store.id, "role": "store_admin"})


@pytest_asyncio.fixture
async def tablet_token(store: Store) -> str:
    return create_access_token({"table_id": 1, "store_id": store.id, "role": "tablet"})


def auth_header(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


# --- Admin Category API ---


class TestAdminCategoryAPI:
    @pytest.mark.asyncio
    async def test_create_category(self, client: AsyncClient, admin_token):
        resp = await client.post(
            "/api/admin/menu/categories",
            json={"name": "메인메뉴"},
            headers=auth_header(admin_token),
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["name"] == "메인메뉴"

    @pytest.mark.asyncio
    async def test_list_categories(self, client: AsyncClient, admin_token):
        await client.post("/api/admin/menu/categories", json={"name": "메인"}, headers=auth_header(admin_token))
        await client.post("/api/admin/menu/categories", json={"name": "사이드"}, headers=auth_header(admin_token))
        resp = await client.get("/api/admin/menu/categories", headers=auth_header(admin_token))
        assert resp.status_code == 200
        assert len(resp.json()) == 2

    @pytest.mark.asyncio
    async def test_update_category(self, client: AsyncClient, admin_token):
        create_resp = await client.post(
            "/api/admin/menu/categories", json={"name": "원래"}, headers=auth_header(admin_token)
        )
        cat_id = create_resp.json()["id"]
        resp = await client.put(
            f"/api/admin/menu/categories/{cat_id}",
            json={"name": "변경됨"},
            headers=auth_header(admin_token),
        )
        assert resp.status_code == 200
        assert resp.json()["name"] == "변경됨"

    @pytest.mark.asyncio
    async def test_delete_category(self, client: AsyncClient, admin_token):
        create_resp = await client.post(
            "/api/admin/menu/categories", json={"name": "삭제대상"}, headers=auth_header(admin_token)
        )
        cat_id = create_resp.json()["id"]
        resp = await client.delete(f"/api/admin/menu/categories/{cat_id}", headers=auth_header(admin_token))
        assert resp.status_code == 204

    @pytest.mark.asyncio
    async def test_duplicate_category_returns_409(self, client: AsyncClient, admin_token):
        await client.post("/api/admin/menu/categories", json={"name": "중복"}, headers=auth_header(admin_token))
        resp = await client.post("/api/admin/menu/categories", json={"name": "중복"}, headers=auth_header(admin_token))
        assert resp.status_code == 409

    @pytest.mark.asyncio
    async def test_unauthorized_access(self, client: AsyncClient, tablet_token):
        resp = await client.get("/api/admin/menu/categories", headers=auth_header(tablet_token))
        assert resp.status_code == 403


# --- Admin Menu Item API ---


class TestAdminMenuItemAPI:
    @pytest.mark.asyncio
    async def test_create_menu_item(self, client: AsyncClient, admin_token):
        cat_resp = await client.post(
            "/api/admin/menu/categories", json={"name": "메인"}, headers=auth_header(admin_token)
        )
        cat_id = cat_resp.json()["id"]
        resp = await client.post(
            "/api/admin/menu/items",
            data={"category_id": cat_id, "name": "김치찌개", "price": 8000, "description": "맛있는 김치찌개"},
            headers=auth_header(admin_token),
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["name"] == "김치찌개"
        assert data["price"] == 8000

    @pytest.mark.asyncio
    async def test_list_menu_items(self, client: AsyncClient, admin_token):
        cat_resp = await client.post(
            "/api/admin/menu/categories", json={"name": "메인"}, headers=auth_header(admin_token)
        )
        cat_id = cat_resp.json()["id"]
        await client.post(
            "/api/admin/menu/items",
            data={"category_id": cat_id, "name": "메뉴1", "price": 5000},
            headers=auth_header(admin_token),
        )
        resp = await client.get("/api/admin/menu/items", headers=auth_header(admin_token))
        assert resp.status_code == 200
        assert len(resp.json()) >= 1

    @pytest.mark.asyncio
    async def test_delete_menu_item_soft(self, client: AsyncClient, admin_token):
        cat_resp = await client.post(
            "/api/admin/menu/categories", json={"name": "메인"}, headers=auth_header(admin_token)
        )
        cat_id = cat_resp.json()["id"]
        item_resp = await client.post(
            "/api/admin/menu/items",
            data={"category_id": cat_id, "name": "삭제대상", "price": 5000},
            headers=auth_header(admin_token),
        )
        item_id = item_resp.json()["id"]
        resp = await client.delete(f"/api/admin/menu/items/{item_id}", headers=auth_header(admin_token))
        assert resp.status_code == 204


# --- Customer Menu API ---


class TestCustomerMenuAPI:
    @pytest.mark.asyncio
    async def test_get_categories(self, client: AsyncClient, admin_token, tablet_token):
        await client.post("/api/admin/menu/categories", json={"name": "메인"}, headers=auth_header(admin_token))
        resp = await client.get("/api/customer/menu/categories", headers=auth_header(tablet_token))
        assert resp.status_code == 200
        assert len(resp.json()) == 1

    @pytest.mark.asyncio
    async def test_get_menu(self, client: AsyncClient, admin_token, tablet_token):
        cat_resp = await client.post(
            "/api/admin/menu/categories", json={"name": "메인"}, headers=auth_header(admin_token)
        )
        cat_id = cat_resp.json()["id"]
        await client.post(
            "/api/admin/menu/items",
            data={"category_id": cat_id, "name": "김치찌개", "price": 8000},
            headers=auth_header(admin_token),
        )
        resp = await client.get("/api/customer/menu/", headers=auth_header(tablet_token))
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 1
        assert data[0]["category"]["name"] == "메인"
        assert len(data[0]["items"]) == 1
