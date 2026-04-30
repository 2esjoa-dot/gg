import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.store import Store
from app.models.category import Category
from app.models.menu_item import MenuItem
from app.repositories.category_repository import CategoryRepository
from app.repositories.menu_repository import MenuRepository


@pytest_asyncio.fixture
async def store(db_session: AsyncSession) -> Store:
    store = Store(name="테스트매장", code="test-store")
    db_session.add(store)
    await db_session.flush()
    return store


@pytest_asyncio.fixture
async def category_repo(db_session: AsyncSession) -> CategoryRepository:
    return CategoryRepository(db_session)


@pytest_asyncio.fixture
async def menu_repo(db_session: AsyncSession) -> MenuRepository:
    return MenuRepository(db_session)


@pytest_asyncio.fixture
async def category(db_session: AsyncSession, store: Store, category_repo: CategoryRepository) -> Category:
    return await category_repo.create(store.id, "메인메뉴")


# --- CategoryRepository Tests ---


class TestCategoryRepository:
    @pytest.mark.asyncio
    async def test_create_category(self, store, category_repo):
        cat = await category_repo.create(store.id, "사이드메뉴")
        assert cat.id is not None
        assert cat.name == "사이드메뉴"
        assert cat.store_id == store.id
        assert cat.display_order == 1

    @pytest.mark.asyncio
    async def test_create_multiple_categories_increments_order(self, store, category_repo):
        cat1 = await category_repo.create(store.id, "메인")
        cat2 = await category_repo.create(store.id, "사이드")
        assert cat2.display_order == cat1.display_order + 1

    @pytest.mark.asyncio
    async def test_get_by_store(self, store, category_repo):
        await category_repo.create(store.id, "메인")
        await category_repo.create(store.id, "사이드")
        categories = await category_repo.get_by_store(store.id)
        assert len(categories) == 2

    @pytest.mark.asyncio
    async def test_get_by_id(self, store, category_repo):
        cat = await category_repo.create(store.id, "메인")
        found = await category_repo.get_by_id(store.id, cat.id)
        assert found is not None
        assert found.name == "메인"

    @pytest.mark.asyncio
    async def test_get_by_id_wrong_store(self, store, category_repo):
        cat = await category_repo.create(store.id, "메인")
        found = await category_repo.get_by_id(9999, cat.id)
        assert found is None

    @pytest.mark.asyncio
    async def test_get_by_name(self, store, category_repo):
        await category_repo.create(store.id, "메인")
        found = await category_repo.get_by_name(store.id, "메인")
        assert found is not None

    @pytest.mark.asyncio
    async def test_delete_category(self, store, category_repo):
        cat = await category_repo.create(store.id, "삭제대상")
        await category_repo.delete(cat)
        found = await category_repo.get_by_id(store.id, cat.id)
        assert found is None

    @pytest.mark.asyncio
    async def test_has_menu_items_false(self, store, category_repo):
        cat = await category_repo.create(store.id, "빈카테고리")
        result = await category_repo.has_menu_items(store.id, cat.id)
        assert result is False

    @pytest.mark.asyncio
    async def test_has_menu_items_true(self, db_session, store, category_repo):
        cat = await category_repo.create(store.id, "메뉴있음")
        item = MenuItem(
            store_id=store.id, category_id=cat.id,
            name="테스트메뉴", price=10000, is_active=True,
        )
        db_session.add(item)
        await db_session.flush()
        result = await category_repo.has_menu_items(store.id, cat.id)
        assert result is True


# --- MenuRepository Tests ---


class TestMenuRepository:
    @pytest.mark.asyncio
    async def test_create_menu_item(self, store, category, menu_repo):
        item = await menu_repo.create(
            store_id=store.id, category_id=category.id,
            name="김치찌개", price=8000, description="맛있는 김치찌개",
        )
        assert item.id is not None
        assert item.name == "김치찌개"
        assert item.price == 8000
        assert item.is_active is True

    @pytest.mark.asyncio
    async def test_get_by_store_active_only(self, store, category, menu_repo):
        await menu_repo.create(store.id, category.id, "활성메뉴", 5000)
        inactive = await menu_repo.create(store.id, category.id, "비활성메뉴", 6000)
        await menu_repo.soft_delete(inactive)

        items = await menu_repo.get_by_store(store.id)
        assert len(items) == 1
        assert items[0].name == "활성메뉴"

    @pytest.mark.asyncio
    async def test_get_by_store_include_inactive(self, store, category, menu_repo):
        await menu_repo.create(store.id, category.id, "활성", 5000)
        inactive = await menu_repo.create(store.id, category.id, "비활성", 6000)
        await menu_repo.soft_delete(inactive)

        items = await menu_repo.get_by_store(store.id, include_inactive=True)
        assert len(items) == 2

    @pytest.mark.asyncio
    async def test_get_by_category(self, store, category, menu_repo):
        await menu_repo.create(store.id, category.id, "메뉴1", 5000)
        await menu_repo.create(store.id, category.id, "메뉴2", 6000)
        items = await menu_repo.get_by_category(store.id, category.id)
        assert len(items) == 2

    @pytest.mark.asyncio
    async def test_get_by_id(self, store, category, menu_repo):
        item = await menu_repo.create(store.id, category.id, "테스트", 5000)
        found = await menu_repo.get_by_id(store.id, item.id)
        assert found is not None
        assert found.name == "테스트"

    @pytest.mark.asyncio
    async def test_soft_delete(self, store, category, menu_repo):
        item = await menu_repo.create(store.id, category.id, "삭제대상", 5000)
        await menu_repo.soft_delete(item)
        assert item.is_active is False

    @pytest.mark.asyncio
    async def test_update_display_orders(self, store, category, menu_repo):
        item1 = await menu_repo.create(store.id, category.id, "메뉴1", 5000, display_order=0)
        item2 = await menu_repo.create(store.id, category.id, "메뉴2", 6000, display_order=1)
        await menu_repo.update_display_orders(store.id, [
            {"menu_item_id": item1.id, "display_order": 1},
            {"menu_item_id": item2.id, "display_order": 0},
        ])
        assert item1.display_order == 1
        assert item2.display_order == 0

    @pytest.mark.asyncio
    async def test_get_max_display_order(self, store, category, menu_repo):
        await menu_repo.create(store.id, category.id, "메뉴1", 5000, display_order=3)
        await menu_repo.create(store.id, category.id, "메뉴2", 6000, display_order=5)
        max_order = await menu_repo.get_max_display_order(store.id, category.id)
        assert max_order == 5
