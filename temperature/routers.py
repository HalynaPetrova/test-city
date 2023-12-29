from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from dependencies import get_db
from . import schemas, crud


router = APIRouter()


@router.get("/temperatures/", response_model=list[schemas.Temperature])
def read_temperatures(
        db: Session = Depends(get_db),
        limit: int = Query(5, ge=0),
        skip: int = Query(0, ge=0)
) -> list[schemas.Temperature]:
    return crud.get_temperature_list(
        db=db,
        limit=limit,
        skip=skip,
    )








# @router.get("/temperatures/", response_model=schemas.Temperature)
# def read_temperature_by_city_id(db: Session = Depends(get_db)):
#     db_temperatures = crud.get_temperature_by_city_id(db=db, city_id=city_id)
#     if db_temperatures is None:
#         raise HTTPException(status_code=404, detail="Temperature not found")
#
#     return db_temperatures
