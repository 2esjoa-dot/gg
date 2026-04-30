from datetime import datetime

from pydantic import BaseModel, Field

from app.models.order import OrderStatus


class OrderItemRequest(BaseModel):
    menu_item_id: int
    quantity: int = Field(..., gt=0)


class OrderCreateRequest(BaseModel):
    table_id: int
    items: list[OrderItemRequest] = Field(..., min_length=1)


class OrderItemResponse(BaseModel):
    id: int
    menu_item_id: int
    menu_name: str
    quantity: int
    unit_price: int
    subtotal: int

    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    id: int
    store_id: int
    table_id: int
    session_id: int
    order_number: str
    status: OrderStatus
    total_amount: int
    items: list[OrderItemResponse] = []
    created_at: datetime

    class Config:
        from_attributes = True


class OrderStatusUpdateRequest(BaseModel):
    status: OrderStatus
