from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.services.category_service import CategoryService

router = APIRouter(prefix="/categories", tags=["Categories"])
ADMIN_ID = 100002

# ---------- CATEGORY ROUTES ----------

@router.post("/add")
def add_category(name: str, request: Request):
    customer_id = int(request.query_params.get("customerid", 0))
    if customer_id != ADMIN_ID:
        raise HTTPException(status_code=403, detail="Admins only.")

    service = CategoryService()
    result = service.add_category(name)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.get("/")
def get_all_categories():
    service = CategoryService()
    return service.get_all_categories()


@router.put("/update/{category_id}")
def update_category(category_id: int, new_name: str):
    service = CategoryService()
    result = service.update_category(category_id, new_name)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@router.delete("/delete/{category_id}")
def delete_category(category_id: int):
    service = CategoryService()
    result = service.delete_category(category_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


# ---------- SUBCATEGORY ROUTES ----------

@router.post("/{category_id}/subcategories/add")
def add_subcategory(category_id: int, name: str):
    service = CategoryService()
    result = service.add_subcategory(category_id, name)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.get("/{category_id}/subcategories")
def get_subcategories(category_id: int):
    service = CategoryService()
    return service.get_subcategories_by_category(category_id)
