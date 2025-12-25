from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
import folium
import os
import tempfile
from pathlib import Path
import logging

from app.routers import locations
from app.utils import ensure_dirs

logger = logging.getLogger(__name__)
router = APIRouter()

# Директория для временных файлов карт
MAPS_DIR = ensure_dirs()

class MapMarker(BaseModel):
    lat: float
    lon: float
    title: str
    price: Optional[int] = None
    url: Optional[str] = None

class MapRequest(BaseModel):
    markers: List[MapMarker]
    center_lat: Optional[float] = None
    center_lon: Optional[float] = None
    zoom: Optional[int] = 12

@router.post("/generate")
async def generate_map(request: MapRequest):
    """Генерирует карту с маркерами"""
    try:
        # Определяем центр карты
        if request.center_lat and request.center_lon:
            center = [request.center_lat, request.center_lon]
        elif request.markers:
            # Центр по среднему значению координат маркеров
            avg_lat = sum(m.lat for m in request.markers) / len(request.markers)
            avg_lon = sum(m.lon for m in request.markers) / len(request.markers)
            center = [avg_lat, avg_lon]
        else:
            # По умолчанию Алматы
            center = [43.2220, 76.8512]
        
        # Создаем карту
        m = folium.Map(
            location=center,
            zoom_start=request.zoom or 12,
            tiles='OpenStreetMap'
        )
        
        # Добавляем маркеры
        for marker in request.markers:
            popup_html = f"<b>{marker.title}</b>"
            if marker.price:
                popup_html += f"<br>Цена: {marker.price:,} ₸".replace(",", " ")
            if marker.url:
                popup_html += f'<br><a href="{marker.url}" target="_blank">Открыть</a>'
            
            folium.Marker(
                [marker.lat, marker.lon],
                popup=folium.Popup(popup_html, max_width=300),
                tooltip=marker.title,
                icon=folium.Icon(color='blue', icon='home')
            ).add_to(m)
        
        # Сохраняем во временный файл
        import uuid
        map_id = str(uuid.uuid4())
        map_path = MAPS_DIR / f"{map_id}.html"
        m.save(str(map_path))
        
        return {
            "success": True,
            "map_id": map_id,
            "map_url": f"/api/maps/view/{map_id}"
        }
    except Exception as e:
        logger.error(f"Ошибка генерации карты: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/view/{map_id}")
async def view_map(map_id: str):
    """Возвращает HTML файл карты"""
    map_path = MAPS_DIR / f"{map_id}.html"
    if not map_path.exists():
        raise HTTPException(status_code=404, detail="Карта не найдена")
    
    return FileResponse(
        str(map_path),
        media_type="text/html",
        filename=f"map_{map_id}.html"
    )

@router.get("/city/{city_name}")
async def get_city_map(
    city_name: str,
    show_districts: bool = Query(False, description="Показать районы")
):
    """Генерирует карту города"""
    city_lower = city_name.lower()
    city_data = None
    
    for name, data in locations.CITIES_DATA.items():
        if (city_lower == name.lower() or
            city_lower in [alt.lower() for alt in data["name_alt"]]):
            city_data = data
            break
    
    if not city_data:
        raise HTTPException(status_code=404, detail=f"Город '{city_name}' не найден")
    
    # Создаем карту города
    m = folium.Map(
        location=city_data["coordinates"],
        zoom_start=11,
        tiles='OpenStreetMap'
    )
    
    # Добавляем маркер центра города
    folium.Marker(
        city_data["coordinates"],
        popup=f"<b>{city_data['name']}</b>",
        tooltip=city_data["name"],
        icon=folium.Icon(color='red', icon='city', prefix='fa')
    ).add_to(m)
    
    # Если нужно показать районы, добавляем примерные маркеры
    if show_districts:
        import random
        for i, district in enumerate(city_data["districts"]):
            # Случайное смещение для визуализации районов
            offset_lat = city_data["coordinates"][0] + random.uniform(-0.1, 0.1)
            offset_lon = city_data["coordinates"][1] + random.uniform(-0.1, 0.1)
            
            folium.Marker(
                [offset_lat, offset_lon],
                popup=f"<b>{district}</b>",
                tooltip=district,
                icon=folium.Icon(color='green', icon='map-marker')
            ).add_to(m)
    
    # Сохраняем карту
    import uuid
    map_id = str(uuid.uuid4())
    map_path = MAPS_DIR / f"{map_id}.html"
    m.save(str(map_path))
    
    return {
        "success": True,
        "city": city_data["name"],
        "map_id": map_id,
        "map_url": f"/api/maps/view/{map_id}"
    }

