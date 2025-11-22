from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional, List

from app.db import get_db
from app.models.car import Car
from app.web.cars.schemas import CarRead


router = APIRouter(prefix="/cars", tags=["Cars"])


@router.get("/", response_model=dict)
def list_cars(
    make: Optional[str] = Query(None),
    model: Optional[str] = Query(None),
    year: Optional[int] = Query(None),
    page: int = 1,
    per_page: int = 20,
    db: Session = Depends(get_db),
):
    """
    List cars with filters + pagination
    """

    query = db.query(Car)

    # Filters
    if make:
        query = query.filter(Car.make.ilike(f"%{make}%"))
    if model:
        query = query.filter(Car.model.ilike(f"%{model}%"))
    if year:
        query = query.filter(Car.year == year)

    total = query.count()   # total items BEFORE pagination

    # Pagination manually
    items = (
        query.order_by(Car.year.desc())
        .offset((page - 1) * per_page)
        .limit(per_page)
        .all()
    )

    return {
        "total": total,
        "page": page,
        "per_page": per_page,
        "pages": (total + per_page - 1) // per_page,
        "items": [CarRead.from_orm(i) for i in items],
    }
