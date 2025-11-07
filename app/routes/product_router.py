from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from fastapi import Body
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.services.product_service import ProductService
from app.services.category_service import CategoryService

# Initialize router
router = APIRouter(prefix="/products", tags=["Products & Categories"])

@router.get("/categories")
def list_categories():
    service = CategoryService()
    return service.get_all_categories()

@router.get("/categories/{categoryid}/subcategories")
def list_subcategories(categoryid: int):
    service = CategoryService()
    return service.get_subcategories_by_category(categoryid)


# ====================== CATEGORY ENDPOINTS ======================
@router.post("/category/add")
def add_category(name: str, db: Session = Depends(get_db)):
    try:
        service = ProductService()
        result = service.add_category(name)
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/category/{categoryid}")
def update_category(categoryid: int, new_name: str, db: Session = Depends(get_db)):
    try:
        service = ProductService()
        result = service.update_category(categoryid, new_name)
        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/category/{categoryid}")
def delete_category(categoryid: int, db: Session = Depends(get_db)):
    try:
        service = ProductService()
        result = service.delete_category(categoryid)
        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



# ====================== SUBCATEGORY ENDPOINTS ======================
@router.post("/subcategory/add")
def add_subcategory(name: str, categoryid: int, db: Session = Depends(get_db)):
    try:
        service = ProductService()
        result = service.add_subcategory(name, categoryid)
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/subcategory/{subcategoryid}")
def update_subcategory(subcategoryid: int, new_name: str, db: Session = Depends(get_db)):
    try:
        service = ProductService()
        result = service.update_subcategory(subcategoryid, new_name)
        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/subcategory/{subcategoryid}")
def delete_subcategory(subcategoryid: int, db: Session = Depends(get_db)):
    try:
        service = ProductService()
        result = service.delete_subcategory(subcategoryid)
        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/subcategories")
def list_subcategories(categoryid: int = None, db: Session = Depends(get_db)):
    service = ProductService()
    return service.list_subcategories(categoryid)


# ✅ Nested route used by frontend: /products/categories/{categoryid}/subcategories
@router.get("/categories/{categoryid}/subcategories")
def list_subcategories_for_category(categoryid: int):
    service = ProductService()
    return service.list_subcategories(categoryid)


# ====================== PRODUCT ENDPOINTS ======================

# ✅ Input model for adding product
class ProductCreate(BaseModel):
    sellerid: int
    product_name: str
    description: str
    subcategoryid: int
    price: float
    stock: int
    images_url: str
    rating: float = 0.0


@router.post("/add")
def add_product(payload: ProductCreate):
    """
    Adds a new product linked to an existing seller and subcategory.
    """
    try:
        service = ProductService()
        result = service.add_product(
            payload.sellerid,
            payload.product_name,
            payload.description,
            payload.subcategoryid,
            payload.price,
            payload.stock,
            payload.images_url,
            payload.rating,
        )
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{productid}")
def update_product(
    productid: int,
    description: str = None,
    stock: int = None,
    rating: float = None,
    db: Session = Depends(get_db),
):
    """
    Update product details like description, stock, or rating.
    """
    try:
        service = ProductService()
        result = service.update_product(productid, description, stock, rating)
        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{productid}")
def delete_product(productid: int, db: Session = Depends(get_db)):
    """
    Delete a product by ID.
    """
    try:
        service = ProductService()
        result = service.delete_product(productid)
        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{productid}")
def get_product(productid: int, db: Session = Depends(get_db)):
    """
    Retrieve a single product by its ID.
    """
    try:
        service = ProductService()
        product = service.get_product(productid)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found.")
        return product
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{productid}/reviews")
def get_product_reviews(productid: int, page: int = 1, per_page: int = 10):
    try:
        from app.services.review_service import ReviewService
        svc = ReviewService()
        return svc.get_reviews(productid, page, per_page)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{productid}/review")
def post_product_review(productid: int, payload: dict = Body(...)):
    """Accepts JSON body: { customerid: int, rating: int, comment: str }
    This is intentionally generic (dict) to avoid adding new Pydantic models in many files.
    """
    try:
        customerid = payload.get('customerid')
        rating = payload.get('rating')
        comment = payload.get('comment', '')
        if customerid is None or rating is None:
            raise HTTPException(status_code=400, detail='customerid and rating are required in the body')

        from app.services.review_service import ReviewService
        svc = ReviewService()
        result = svc.add_review(productid, int(customerid), int(rating), str(comment))
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/")
def list_products(subcategoryid: int = None, db: Session = Depends(get_db)):
    """
    List all products (or only by subcategory if provided).
    """
    service = ProductService()
    return service.list_products(subcategoryid)


@router.get("/search")
def search_products(keyword: str, db: Session = Depends(get_db)):
    """
    Search products by name or description.
    """
    service = ProductService()
    return service.search_products(keyword)
