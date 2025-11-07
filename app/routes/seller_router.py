from fastapi import APIRouter, HTTPException
from app.services.seller_service import SellerService

router = APIRouter(prefix="/sellers", tags=["Sellers"])

@router.post("/register")
def register_seller(customerid: int, rating: float = 0.0):
    service = SellerService()
    result = service.register_seller(customerid, rating)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.put("/{sellerid}/rating")
def update_rating(sellerid: int, new_rating: float):
    service = SellerService()
    result = service.update_seller_rating(sellerid, new_rating)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@router.get("/{sellerid}")
def get_seller(sellerid: int):
    service = SellerService()
    result = service.get_seller_profile(sellerid)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@router.get("/customer/{customerid}")
def get_seller_by_customer(customerid: int):
    service = SellerService()
    result = service.get_seller_by_customer(customerid)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@router.put("/{sellerid}/product/{productid}/stock")
def update_product_stock(sellerid: int, productid: int, new_stock: int):
    service = SellerService()
    result = service.update_stock(sellerid, productid, new_stock)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.post("/{sellerid}/product/add")
def add_product(sellerid: int, description: str, subcategoryid: int, stock: int, rating: float = 0.0):
    service = SellerService()
    result = service.add_product(sellerid, description, subcategoryid, stock, rating)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.put("/{sellerid}/product/{productid}")
def update_product(sellerid: int, productid: int, description: str = None, subcategoryid: int = None, rating: float = None):
    service = SellerService()
    result = service.update_product(sellerid, productid, description, subcategoryid, rating)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@router.delete("/{sellerid}/product/{productid}")
def delete_product(sellerid: int, productid: int):
    service = SellerService()
    result = service.delete_product(sellerid, productid)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@router.put("/{sellerid}/order/{orderid}/status")
def update_order_status(sellerid: int, orderid: int, new_status: str):
    service = SellerService()
    result = service.update_order_status(sellerid, orderid, new_status)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.get("/{sellerid}/orders")
def view_orders(sellerid: int):
    service = SellerService()
    result = service.get_seller_orders(sellerid)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result
