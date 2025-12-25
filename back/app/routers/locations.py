from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

# Данные о городах и районах Казахстана
CITIES_DATA = {
    "Алматы": {
        "name": "Алматы",
        "name_alt": ["Алмата"],
        "districts": [
            "Алмалинский район",
            "Ауэзовский район",
            "Бостандыкский район",
            "Жетысуский район",
            "Медеуский район",
            "Наурызбайский район",
            "Турксибский район"
        ],
        "coordinates": [43.2220, 76.8512]
    },
    "Астана": {
        "name": "Астана",
        "name_alt": ["Нур-Султан"],
        "districts": [
            "Алматинский район",
            "Есильский район",
            "Сарыаркинский район",
            "Байконурский район"
        ],
        "coordinates": [51.1694, 71.4491]
    },
    "Шымкент": {
        "name": "Шымкент",
        "name_alt": [],
        "districts": [
            "Абайский район",
            "Енбекшинский район",
            "Каратауский район",
            "Туранский район"
        ],
        "coordinates": [42.3419, 69.5901]
    },
    "Караганда": {
        "name": "Караганда",
        "name_alt": [],
        "districts": [
            "Казыбек би район",
            "Октябрьский район"
        ],
        "coordinates": [49.8014, 73.1044]
    }
}

class CityInfo(BaseModel):
    name: str
    name_alt: List[str]
    districts: List[str]
    coordinates: List[float]

class LocationSearchResponse(BaseModel):
    cities: List[CityInfo]
    total: int

class DistrictResponse(BaseModel):
    city: str
    districts: List[str]

@router.get("/cities", response_model=LocationSearchResponse)
async def get_cities(
    search: Optional[str] = Query(None, description="Поиск по названию города")
):
    """Получить список городов с возможностью поиска"""
    cities_list = []
    
    for city_data in CITIES_DATA.values():
        if search:
            search_lower = search.lower()
            if (search_lower in city_data["name"].lower() or
                any(search_lower in alt.lower() for alt in city_data["name_alt"])):
                cities_list.append(CityInfo(**city_data))
        else:
            cities_list.append(CityInfo(**city_data))
    
    return LocationSearchResponse(cities=cities_list, total=len(cities_list))

@router.get("/districts", response_model=DistrictResponse)
async def get_districts(
    city: str = Query(..., description="Название города")
):
    """Получить список районов для города"""
    city_lower = city.lower()
    
    for city_name, city_data in CITIES_DATA.items():
        if (city_lower == city_name.lower() or
            city_lower in [alt.lower() for alt in city_data["name_alt"]]):
            return DistrictResponse(
                city=city_data["name"],
                districts=city_data["districts"]
            )
    
    raise HTTPException(status_code=404, detail=f"Город '{city}' не найден")

@router.get("/search")
async def search_location(
    query: str = Query(..., description="Поисковый запрос (город или район)")
):
    """Универсальный поиск по городам и районам"""
    query_lower = query.lower()
    results = {
        "cities": [],
        "districts": []
    }
    
    for city_name, city_data in CITIES_DATA.items():
        # Поиск по городу
        if (query_lower in city_name.lower() or
            any(query_lower in alt.lower() for alt in city_data["name_alt"])):
            results["cities"].append({
                "name": city_data["name"],
                "coordinates": city_data["coordinates"]
            })
        
        # Поиск по районам
        for district in city_data["districts"]:
            if query_lower in district.lower():
                results["districts"].append({
                    "city": city_data["name"],
                    "name": district,
                    "coordinates": city_data["coordinates"]  # Примерные координаты
                })
    
    return results

