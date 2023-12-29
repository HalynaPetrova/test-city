from sqlalchemy.orm import Session

from city import models
from city.schemas import City, CityCreate, CityUpdate


def get_city_list(
        db: Session,
        skip: int = 0,
        limit: int = 5,
) -> list[City]:

    return db.query(models.City).limit(limit).offset(skip).all()


def create_city(db: Session, city: CityCreate) -> models.City:
    db_city = models.City(
        name=city.name,
        additional_info=city.additional_info,
    )
    db.add(db_city)
    db.commit()
    db.refresh(db_city)

    return db_city


def update_city(
        db: Session,
        city: CityUpdate,
        db_city: models.City,
) -> models.City:

    for field, value in city.model_dump().items():
        setattr(db_city, field, value)
    db.commit()
    db.refresh(db_city)
    return db_city


def delete_city(db: Session, db_city: models.City) -> None:
    db.delete(db_city)
    db.commit()


def get_city_by_id(db: Session, city_id: int) -> models.City | None:
    return (
        db.query(models.City).filter(models.City.id == city_id).first()
    )


def get_city_by_name(db: Session, name: str) -> models.City | None:
    return (
        db.query(models.City).filter(models.City.name == name).first()
    )
