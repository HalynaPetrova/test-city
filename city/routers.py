from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from dependencies import get_db
from . import schemas, crud


router = APIRouter()


@router.get("/cities/", response_model=list[schemas.City])
def read_cities(
        db: Session = Depends(get_db),
        limit: int = Query(5, ge=0),
        skip: int = Query(0, ge=0)
) -> list[schemas.City]:
    return crud.get_city_list(
        db=db,
        limit=limit,
        skip=skip,
    )


@router.get("/city/{city_id}/", response_model=schemas.City)
def read_single_cheese(city_id: int, db: Session = Depends(get_db)):
    db_city = crud.get_city_by_id(db=db, city_id=city_id)

    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")

    return db_city


@router.post("/cities/", response_model=schemas.City)
def create_city(
    city: schemas.CityCreate,
    db: Session = Depends(get_db),
) -> schemas.City:
    db_city = crud.get_city_by_name(db=db, name=city.name)

    if db_city:
        raise HTTPException(
            status_code=400, detail="Such name for City already exists"
        )

    return crud.create_city(db=db, city=city)


@router.put("/cities/{city_id}/", response_model=schemas.City)
def update_city(
        city_id: int,
        city: schemas.CityUpdate,
        db: Session = Depends(get_db),
) -> schemas.City:
    db_city = crud.get_city_by_id(db=db, city_id=city_id)
    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")
    db_city = crud.update_city(
        db=db,
        db_city=db_city,
        city=city)
    return db_city


@router.delete("/cities/{city_id}/")
def delete_city(
    city_id: int,
    db: Session = Depends(get_db),
) -> dict:
    db_city = crud.get_city_by_id(db=db, city_id=city_id)
    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")
    crud.delete_city(db=db, db_city=db_city)
    return {"message": "City deleted"}
