from fastapi import APIRouter, HTTPException
from app.services.order_service import OrderService

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/place")
def place_order(customerid: int, productid: int, qty: int):
    service = OrderService()
    result = service.place_order(customerid, productid, qty)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.get("/{orderid}")
def get_order_details(orderid: int):
    service = OrderService()
    result = service.get_order_details(orderid)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@router.get("/customer/{customerid}")
def get_orders_by_customer(customerid: int):
    service = OrderService()
    result = service.get_orders_by_customer(customerid)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@router.get("/seller/{sellerid}")
def get_orders_by_seller(sellerid: int):
    service = OrderService()
    result = service.get_orders_by_seller(sellerid)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@router.put("/{orderid}/status")
def update_order_status(orderid: int, new_status: str):
    service = OrderService()
    result = service.update_order_status(orderid, new_status)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.put("/{orderid}/cancel")
def cancel_order(orderid: int):
    service = OrderService()
    result = service.cancel_order(orderid)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.get("/{orderid}/transaction")
def get_order_transaction(orderid: int):
    service = OrderService()
    result = service.get_transaction_for_order(orderid)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@router.post("/{orderid}/transaction")
def create_transaction(orderid: int, amount: float, status: str = "Completed"):
    service = OrderService()
    result = service.create_or_update_transaction(orderid, amount, status)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.get("/transactions/{customerid}")
def get_customer_transactions(customerid: int):
    service = OrderService()
    result = service.get_transactions_by_customer(customerid)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result
