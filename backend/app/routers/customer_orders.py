"""
개발자 3 담당: 고객 주문 API
TODO: OrderService 구현 후 연동
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.middleware.auth import require_role, get_store_id
from app.schemas.order import OrderCreateRequest, OrderResponse

router = APIRouter(prefix="/api/customer/orders", tags=["Customer - Orders"])


@router.post("/", response_model=OrderResponse)
async def create_order(
    request: OrderCreateRequest,
    store_id: int = Depends(get_store_id),
    db: AsyncSession = Depends(get_db),
):
    # TODO: 구현 (세션 연동, 주문번호 생성, SSE 발행)
    pass


@router.get("/session/{session_id}", response_model=list[OrderResponse])
async def get_session_orders(
    session_id: int,
    store_id: int = Depends(get_store_id),
    db: AsyncSession = Depends(get_db),
):
    # TODO: 구현
    return []
