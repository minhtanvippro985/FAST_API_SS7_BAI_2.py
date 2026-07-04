from fastapi import FastAPI,HTTPException
from pydantic import BaseModel

app = FastAPI()

orders_db = [
    {"id": 1, "customer_name": "Nguyen Van A", "status": "PENDING"},
    {"id": 2, "customer_name": "Tran Thi B", "status": "SHIPPING"}
]

class StatusUpdate(BaseModel):
    status: str

@app.get("/orders/{order_id}")
def get_order(order_id: int):
    return next((o for o in orders_db if o["id"] == order_id), None)

@app.put("/orders/{order_id}/status")
def update_order_status(order_id: int, data: StatusUpdate):
    order = None
    for check_order in orders_db:
        if check_order["id"] == order_id:
            order = check_order
            break
    
    if not order:
        raise HTTPException(status_code=404 , detail="Khong tim thay san pham")
        
    if data.status not in ["PENDING", "SHIPPING", "DELIVERED"]:
        return {"error": "Trạng thái không hợp lệ"} 
        
    if order:
        order["status"] = data.status

    return {"statusCode": 200, "message": "Cập nhật thành công", "data": order}