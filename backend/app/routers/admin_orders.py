"""
개발자 3 담당: 관리자 주문 관리 API + SSE
TODO: OrderService 구현 후 연동
"""
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.middleware.auth import require_role, get_store_id
from app.schemas.order import OrderResponse, OrderStatusUpdateRequest
from app.services.sse_service import sse_service

router = APIRouter(prefix="/api/admin/orders", tags=["Admin - Orders"])


@router.get("/stream")
async def order_stream(store_id: int = Depends(get_store_id)):
    """SSE 주문 스트림 - 실시간 주문 알림"""
    return StreamingResponse(
        sse_service.subscribe(store_id),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"},
    )


@router.get("/table/{table_id}", response_model=list[OrderResponse])
async def get_table_orders(
    table_id: int,
    store_id: int = Depends(get_store_id),
    db: AsyncSession = Depends(get_db),
):
    # TODO: 구현
    return []


@router.patch("/{order_id}/status", response_model=OrderResponse)
async def update_order_status(
    order_id: int,
    request: OrderStatusUpdateRequest,
    store_id: int = Depends(get_store_id),
    db: AsyncSession = Depends(get_db),
):
    # TODO: 구현 (상태 전이 규칙 적용)
    pass


@router.delete("/{order_id}")
async def delete_order(
    order_id: int,
    store_id: int = Depends(get_store_id),
    db: AsyncSession = Depends(get_db),
):
    # TODO: 구현
    return {"message": "주문이 삭제되었습니다"}
