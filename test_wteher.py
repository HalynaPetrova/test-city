import requests

API_KEY = "fe66378930c0b81f8419216ccb4a22f0"


def get_city_temperature(city_name: str,) -> int:
    weather_data = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?q="f"{city_name}&appid={API_KEY}&units=metric")

    weather_dict = weather_data.json()
    # return round(weather_dict['main']['temp'])
    print(weather_dict)

get_city_temperature("London")




def create_city(db: Session, city: CityCreate) -> models.City:
    db_city = models.City(
        name=city.name,
        additional_info=city.additional_info,
    )
    db.add(db_city)
    db.commit()
    db.refresh(db_city)

    return db_city







async def create_temperature(
        db: AsyncSession,
        db_city: models.DBCity,
        client: httpx.AsyncClient
) -> dict[str, Any]:
    city_temperature = await get_city_temperature(
        city_name=db_city.name,
        client=client
    )
    values_dict = {
        "city_id": db_city.id,
        "date_time": datetime.now(),
        "temperature": city_temperature
    }

    query = insert(models.DBTemperature).values(values_dict)
    result = await db.execute(query)

    resp = {**schemas.TemperatureCreate(**values_dict).model_dump(),
            "id": result.lastrowid}

    return resp
