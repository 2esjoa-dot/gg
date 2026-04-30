import pytest
import pytest_asyncio
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.store import Store
from app.services.menu_service import MenuService


@pytest_asyncio.fixture
async def store(db_session: AsyncSession) -> Store:
    store = Store(name="테스트매장", code="test-store")
    db_session.add(store)
    await db_session.flush()
    return store


@pytest_asyncio.fixture
async def menu_service(db_session: AsyncSession) -> MenuService:
    return MenuService(db_session)


class TestMenuServiceCategory:
    @pytest.mark.asyncio
    async def test_create_category(self, store, menu_service):
        cat = await menu_service.create_category(store.id, "메인메뉴")
        assert cat.name == "메인메뉴"
        assert cat.store_id == store.id

    @pytest.mark.asyncio
    async def test_create_duplicate_category_raises(self, store, menu_service):
        await menu_service.create_category(store.id, "메인메뉴")
        with pytest.raises(HTTPException) as exc_info:
            await menu_service.create_category(store.id, "메인메뉴")
        assert exc_info.value.status_code == 409

    @pytest.mark.asyncio
    async def test_get_categories(self, store, menu_service):
        await menu_service.create_category(store.id, "메인")
        await menu_service.create_category(store.id, "사이드")
        categories = await menu_service.get_categories(store.id)
        assert len(categories) == 2

    @pytest.mark.asyncio
    async def test_update_category(self, store, menu_service):
        cat = await menu_service.create_category(store.id, "원래이름")
        updated = await menu_service.update_category(store.id, cat.id, "새이름")
        assert updated.name == "새이름"

    @pytest.mark.asyncio
    async def test_update_category_not_found(self, store, menu_service):
        with pytest.raises(HTTPException) as exc_info:
            await menu_service.update_category(store.id, 9999, "이름")
        assert exc_info.value.status_code == 404

    @pytest.mark.asyncio
    async def test_delete_category(self, store, menu_service):
        cat = await menu_service.create_category(store.id, "삭제대상")
        await menu_service.delete_category(store.id, cat.id)
        categories = await menu_service.get_categories(store.id)
        assert len(categories) == 0

    @pytest.mark.asyncio
    async def test_delete_category_with_items_raises(self, store, menu_service):
        cat = await menu_service.create_category(store.id, "메뉴있음")
        await menu_service.create_menu_item(store.id, cat.id, "테스트메뉴", 5000)
        with pytest.raises(HTTPException) as exc_info:
            await menu_service.delete_category(store.id, cat.id)
        assert exc_info.value.status_code == 400


class TestMenuServiceMenuItem:
    @pytest.mark.asyncio
    async def test_create_menu_item(self, store, menu_service):
        cat = await menu_service.create_category(store.id, "메인")
        item = await menu_service.create_menu_item(
            store.id, cat.id, "김치찌개", 8000, description="맛있는 김치찌개"
        )
        assert item.name == "김치찌개"
        assert item.price == 8000
        assert item.is_active is True

    @pytest.mark.asyncio
    async def test_create_menu_item_invalid_category(self, store, menu_service):
        with pytest.raises(HTTPException) as exc_info:
            await menu_service.create_menu_item(store.id, 9999, "메뉴", 5000)
        assert exc_info.value.status_code == 404

    @pytest.mark.asyncio
    async def test_update_menu_item(self, store, menu_service):
        cat = await menu_service.create_category(store.id, "메인")
        item = await menu_service.create_menu_item(store.id, cat.id, "원래", 5000)
        updated = await menu_service.update_menu_item(
            store.id, item.id, name="변경됨", price=7000
        )
        assert updated.name == "변경됨"
        assert updated.price == 7000

    @pytest.mark.asyncio
    async def test_update_menu_item_not_found(self, store, menu_service):
        with pytest.raises(HTTPException) as exc_info:
            await menu_service.update_menu_item(store.id, 9999, name="이름")
        assert exc_info.value.status_code == 404

    @pytest.mark.asyncio
    async def test_delete_menu_item_soft(self, store, menu_service):
        cat = await menu_service.create_category(store.id, "메인")
        item = await menu_service.create_menu_item(store.id, cat.id, "삭제대상", 5000)
        await menu_service.delete_menu_item(store.id, item.id)
        # soft delete이므로 include_inactive=True로 조회 가능
        menu = await menu_service.get_menu_by_store(store.id, active_only=False)
        items = menu[0]["items"]
        assert len(items) == 1
        assert items[0].is_active is False

    @pytest.mark.asyncio
    async def test_get_menu_by_store_active_only(self, store, menu_service):
        cat = await menu_service.create_category(store.id, "메인")
        await menu_service.create_menu_item(store.id, cat.id, "활성", 5000)
        item2 = await menu_service.create_menu_item(store.id, cat.id, "비활성", 6000)
        await menu_service.delete_menu_item(store.id, item2.id)

        menu = await menu_service.get_menu_by_store(store.id, active_only=True)
        assert len(menu) == 1
        assert len(menu[0]["items"]) == 1
        assert menu[0]["items"][0].name == "활성"

    @pytest.mark.asyncio
    async def test_update_menu_order(self, store, menu_service):
        cat = await menu_service.create_category(store.id, "메인")
        item1 = await menu_service.create_menu_item(store.id, cat.id, "메뉴1", 5000)
        item2 = await menu_service.create_menu_item(store.id, cat.id, "메뉴2", 6000)
        await menu_service.update_menu_order(store.id, [
            {"menu_item_id": item1.id, "display_order": 2},
            {"menu_item_id": item2.id, "display_order": 1},
        ])
        menu = await menu_service.get_menu_by_store(store.id)
        items = menu[0]["items"]
        assert items[0].name == "메뉴2"
        assert items[1].name == "메뉴1"
