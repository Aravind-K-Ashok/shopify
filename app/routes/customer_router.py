from fastapi import APIRouter, HTTPException
from app.services.customer_service import CustomerService

router = APIRouter(prefix="/customers", tags=["Customers"])


@router.post("/register")
def register_customer(
    fname: str,
    lname: str,
    phoneno: str,
    password: str,
    address: str,
    pincode: str,
    district: str,
    state: str,
    housename: str
):
    service = CustomerService()
    result = service.register_customer(fname, lname, phoneno, password, address, pincode, district, state, housename)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.post("/login")
def login_customer(customerID: int, password: str):
    service = CustomerService()
    result = service.authenticate_customer(customerID, password)
    if "error" in result:
        raise HTTPException(status_code=401, detail=result["error"])
    return result


@router.get("/{customerID}")
def get_customer(customerID: int):
    service = CustomerService()
    result = service.get_customer_details(customerID)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@router.put("/{customerID}/phone")
def update_phone(customerID: int, newphoneno: str):
    service = CustomerService()
    result = service.update_customer_phone(customerID, newphoneno)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@router.put("/{customerID}/address")
def update_address(
    customerID: int,
    newaddress: str,
    newpincode: str,
    newdistrict: str,
    newstate: str,
    newhousename: str
):
    service = CustomerService()
    result = service.update_customer_address(customerID, newaddress, newpincode, newdistrict, newstate, newhousename)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@router.put("/{customerID}/password")
def change_password(customerID: int, oldpassword: str, newpassword: str):
    service = CustomerService()
    result = service.change_customer_password(customerID, oldpassword, newpassword)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.put("/{customerID}/reset-password")
def reset_password(customerID: int, phoneno: str, newpassword: str):
    service = CustomerService()
    result = service.change_phone_password(customerID, phoneno, newpassword)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.put("/{customerID}/name")
def change_name(customerID: int, newfname: str, newlname: str):
    service = CustomerService()
    result = service.change_name(customerID, newfname, newlname)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@router.delete("/{customerID}")
def delete_customer(customerID: int):
    service = CustomerService()
    result = service.delete_customer(customerID)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result
