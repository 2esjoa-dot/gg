from datetime import datetime, date

from sqlalchemy import select, and_, func, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.order import Order, OrderStatus
from app.models.order_item import OrderItem


class OrderRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
        self,
        store_id: int,
        table_id: int,
        session_id: int,
        order_number: str,
        total_amount: int,
    ) -> Order:
        order = Order(
            store_id=store_id,
            table_id=table_id,
            session_id=session_id,
            order_number=order_number,
            status=OrderStatus.PENDING,
            total_amount=total_amount,
        )
        self.db.add(order)
        await self.db.flush()
        return order

    async def create_items(self, items: list[OrderItem]) -> list[OrderItem]:
        self.db.add_all(items)
        await self.db.flush()
        return items

    async def get_by_id(self, order_id: int, store_id: int) -> Order | None:
        result = await self.db.execute(
            select(Order)
            .options(selectinload(Order.items))
            .where(and_(Order.id == order_id, Order.store_id == store_id))
        )
        return result.scalar_one_or_none()

    async def get_by_session(self, session_id: int, store_id: int) -> list[Order]:
        result = await self.db.execute(
            select(Order)
            .options(selectinload(Order.items))
            .where(and_(Order.session_id == session_id, Order.store_id == store_id))
            .order_by(Order.created_at.asc())
        )
        return list(result.scalars().all())

    async def get_by_table(self, table_id: int, store_id: int) -> list[Order]:
        """활성 세션의 주문만 조회 (세션 기반 필터링은 서비스에서 처리)"""
        result = await self.db.execute(
            select(Order)
            .options(selectinload(Order.items))
            .where(and_(Order.table_id == table_id, Order.store_id == store_id))
            .order_by(Order.created_at.desc())
        )
        return list(result.scalars().all())

    async def get_by_table_and_session(
        self, table_id: int, session_id: int, store_id: int
    ) -> list[Order]:
        result = await self.db.execute(
            select(Order)
            .options(selectinload(Order.items))
            .where(
                and_(
                    Order.table_id == table_id,
                    Order.session_id == session_id,
                    Order.store_id == store_id,
                )
            )
            .order_by(Order.created_at.desc())
        )
        return list(result.scalars().all())

    async def update_status(self, order: Order, new_status: OrderStatus) -> Order:
        order.status = new_status
        order.updated_at = datetime.utcnow()
        await self.db.flush()
        return order

    async def delete_order(self, order: Order) -> None:
        await self.db.delete(order)
        await self.db.flush()

    async def get_next_order_number(self, store_id: int, order_date: date) -> str:
        """매장별 + 일별 순번으로 주문 번호 생성"""
        date_str = order_date.strftime("%Y%m%d")
        prefix = f"ORD-{date_str}-"

        result = await self.db.execute(
            select(func.count(Order.id)).where(
                and_(
                    Order.store_id == store_id,
                    Order.order_number.like(f"{prefix}%"),
                )
            )
        )
        count = result.scalar_one()
        seq = count + 1
        return f"{prefix}{seq:04d}"

    async def get_orders_by_sessions(
        self, session_ids: list[int], store_id: int
    ) -> list[Order]:
        if not session_ids:
            return []
        result = await self.db.execute(
            select(Order)
            .options(selectinload(Order.items))
            .where(
                and_(
                    Order.session_id.in_(session_ids),
                    Order.store_id == store_id,
                )
            )
            .order_by(Order.created_at.desc())
        )
        return list(result.scalars().all())
