from datetime import datetime
import os

import requests
from sqlalchemy.orm import Session

from temperature import models, schemas
from temperature.schemas import Temperature

from dotenv import load_dotenv

load_dotenv()


def get_temperature(city_name: str) -> int:
    weather_data = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?q="
        f"{city_name}&appid={os.getenv('API_KEY')}&units=metric"
    )
    weather_dict = weather_data.json()
    return round(weather_dict["main"]["temp"])


def update_temperature(
        db: Session,
        db_city: models.City) -> models.Temperature:
    temperature = get_temperature(
        city_name=db_city.name,
    )
    db_temperature = models.Temperature(
        city_id=db_city.id,
        date_time=datetime.now(),
        temperature=temperature,
    )
    db.add(db_temperature)
    db.commit()
    db.refresh(db_temperature)

    return db_temperature


def get_temperature_list(
        db: Session,
        skip: int = 0,
        limit: int = 5,
) -> list[Temperature]:

    return db.query(models.Temperature).limit(limit).offset(skip).all()

