"""태국 음식점 메뉴 시드 데이터 스크립트.

사용법:
    python -m scripts.seed_thai_menu

이 스크립트는 태국 음식점의 카테고리와 메뉴 아이템을 DB에 삽입합니다.
기존 데이터가 있으면 중복 생성하지 않습니다.
"""

import asyncio
import sys
from pathlib import Path

# backend 디렉토리를 path에 추가
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import AsyncSessionLocal, engine
from app.models import Base
from app.models.store import Store
from app.models.category import Category
from app.models.menu_item import MenuItem


# --- 시드 데이터 정의 ---

STORE_DATA = {
    "name": "태국 음식점",
    "code": "thai-restaurant",
    "address": "서울시 강남구",
}

CATEGORIES = [
    {"name": "대표 메뉴", "display_order": 1},
    {"name": "추가 메뉴", "display_order": 2},
    {"name": "음료", "display_order": 3},
    {"name": "세트 메뉴", "display_order": 4},
]

MENU_ITEMS = {
    "대표 메뉴": [
        {
            "name": "팟타이 꿍",
            "price": 13000,
            "description": "태국식 볶음 쌀국수 (새우) | 알레르기: 새우, 땅콩, 달걀",
            "display_order": 1,
        },
        {
            "name": "푸팟퐁커리 (라이스 포함)",
            "price": 28000,
            "description": "부드러운 소프트쉘 크랩 커리 | 알레르기: 게, 달걀, 우유, 대두",
            "display_order": 2,
        },
        {
            "name": "카오팟 사파롯",
            "price": 14000,
            "description": "파인애플 새우 볶음밥 | 알레르기: 새우, 캐슈넛, 달걀",
            "display_order": 3,
        },
        {
            "name": "꾸웨이띠여우 느어",
            "price": 12000,
            "description": "진한 육수의 태국식 소고기 쌀국수 | 알레르기: 쇠고기, 대두",
            "display_order": 4,
        },
        {
            "name": "똠양꿍 (면/밥 선택)",
            "price": 16000,
            "description": "세계 3대 스프로 꼽히는 새콤매콤한 탕 | 알레르기: 새우, 우유, 버섯",
            "display_order": 5,
        },
    ],
    "추가 메뉴": [
        {
            "name": "텃만꿍 (4pcs)",
            "price": 10000,
            "description": "다진 새우 살을 튀겨낸 도넛 모양 고로케 | 알레르기: 새우, 밀, 달걀",
            "display_order": 1,
        },
        {
            "name": "뽀삐아 톳 (4pcs)",
            "price": 8000,
            "description": "채소와 당면을 넣어 튀긴 태국식 춘권 | 알레르기: 밀, 대두",
            "display_order": 2,
        },
        {
            "name": "쏨땀 타이",
            "price": 11000,
            "description": "그린 파파야로 만든 매콤새콤한 샐러드 | 알레르기: 땅콩, 피쉬소스(어류), 마른새우",
            "display_order": 3,
        },
        {
            "name": "공공치킨 (까이텃)",
            "price": 9000,
            "description": "태국식 시즈닝으로 튀긴 닭날개 요리 | 알레르기: 닭고기, 밀",
            "display_order": 4,
        },
    ],
    "음료": [
        {
            "name": "타이 밀크티",
            "price": 5500,
            "description": "연유가 들어간 달콤하고 진한 태국 홍차 | 알레르기: 우유",
            "display_order": 1,
        },
        {
            "name": "땡모반",
            "price": 6500,
            "description": "여름 시즌 한정 시원한 수박 생과일 주스",
            "display_order": 2,
        },
        {
            "name": "창(Chang) / 싱하(Singha)",
            "price": 7000,
            "description": "태국 대표 병맥주 | 알코올 포함",
            "display_order": 3,
        },
        {
            "name": "망고 에이드",
            "price": 5000,
            "description": "달콤한 망고 과육이 씹히는 에이드",
            "display_order": 4,
        },
    ],
    "세트 메뉴": [
        {
            "name": "2인 실속 세트",
            "price": 40000,
            "description": "팟타이 꿍 + 카오팟 사파롯 + 텃만꿍(2pcs) + 에이드 1잔",
            "display_order": 1,
        },
        {
            "name": "시그니처 커리 세트",
            "price": 52000,
            "description": "푸팟퐁커리 + 팟타이 꿍 + 쏨땀 타이 + 공기밥 1개",
            "display_order": 2,
        },
        {
            "name": "혼밥 1인 세트",
            "price": 18000,
            "description": "소고기 쌀국수(S) + 뽀삐아 톳(2pcs) + 타이 밀크티",
            "display_order": 3,
        },
    ],
}


async def seed_data():
    """시드 데이터를 DB에 삽입합니다."""
    async with AsyncSessionLocal() as session:
        async with session.begin():
            # 1. 매장 생성 (이미 존재하면 스킵)
            store = await _get_or_create_store(session)
            print(f"✅ 매장: {store.name} (id={store.id})")

            # 2. 카테고리 생성
            category_map = {}
            for cat_data in CATEGORIES:
                category = await _get_or_create_category(session, store.id, cat_data)
                category_map[category.name] = category
                print(f"  📂 카테고리: {category.name} (id={category.id})")

            # 3. 메뉴 아이템 생성
            total_items = 0
            for category_name, items in MENU_ITEMS.items():
                category = category_map[category_name]
                for item_data in items:
                    menu_item = await _get_or_create_menu_item(
                        session, store.id, category.id, item_data
                    )
                    total_items += 1
                    print(f"    🍽️  {menu_item.name} - {menu_item.price:,}원")

            print(f"\n🎉 시드 완료: {len(category_map)}개 카테고리, {total_items}개 메뉴 아이템")


async def _get_or_create_store(session: AsyncSession) -> Store:
    """매장을 조회하거나 새로 생성합니다."""
    result = await session.execute(
        select(Store).where(Store.code == STORE_DATA["code"])
    )
    store = result.scalar_one_or_none()
    if store:
        return store

    store = Store(**STORE_DATA)
    session.add(store)
    await session.flush()
    return store


async def _get_or_create_category(
    session: AsyncSession, store_id: int, cat_data: dict
) -> Category:
    """카테고리를 조회하거나 새로 생성합니다."""
    result = await session.execute(
        select(Category).where(
            Category.store_id == store_id,
            Category.name == cat_data["name"],
        )
    )
    category = result.scalar_one_or_none()
    if category:
        category.display_order = cat_data["display_order"]
        return category

    category = Category(
        store_id=store_id,
        name=cat_data["name"],
        display_order=cat_data["display_order"],
    )
    session.add(category)
    await session.flush()
    return category


async def _get_or_create_menu_item(
    session: AsyncSession, store_id: int, category_id: int, item_data: dict
) -> MenuItem:
    """메뉴 아이템을 조회하거나 새로 생성합니다."""
    result = await session.execute(
        select(MenuItem).where(
            MenuItem.store_id == store_id,
            MenuItem.category_id == category_id,
            MenuItem.name == item_data["name"],
        )
    )
    menu_item = result.scalar_one_or_none()
    if menu_item:
        # 기존 아이템 업데이트
        menu_item.price = item_data["price"]
        menu_item.description = item_data.get("description")
        menu_item.display_order = item_data["display_order"]
        menu_item.is_active = True
        return menu_item

    menu_item = MenuItem(
        store_id=store_id,
        category_id=category_id,
        name=item_data["name"],
        price=item_data["price"],
        description=item_data.get("description"),
        display_order=item_data["display_order"],
        is_active=True,
    )
    session.add(menu_item)
    await session.flush()
    return menu_item


async def create_tables():
    """테이블이 없으면 생성합니다."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def main():
    print("🚀 태국 음식점 메뉴 시드 데이터 삽입 시작...\n")
    await create_tables()
    await seed_data()
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
