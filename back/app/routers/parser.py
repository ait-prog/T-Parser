from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, HttpUrl
from typing import List, Optional
import logging

from app.parsers.krisha_parser import KrishaParser

logger = logging.getLogger(__name__)
router = APIRouter()

class ParseRequest(BaseModel):
    url: HttpUrl
    verify_ssl: Optional[bool] = True

class PropertyItem(BaseModel):
    marketplace: str
    title: str
    price: int
    description: str
    location: str
    district: str
    area: Optional[float] = None
    rooms: Optional[int] = None
    url: str
    scraped_at: str

class ParseResponse(BaseModel):
    success: bool
    count: int
    items: List[PropertyItem]
    message: Optional[str] = None

@router.post("/scrape", response_model=ParseResponse)
async def scrape_krisha(request: ParseRequest):
    """Парсит страницу krisha.kz"""
    try:
        parser = KrishaParser(verify_ssl=request.verify_ssl)
        items = parser.parse_url(str(request.url))
        
        return ParseResponse(
            success=True,
            count=len(items),
            items=[PropertyItem(**item) for item in items],
            message=f"Найдено {len(items)} объявлений"
        )
    except Exception as e:
        logger.error(f"Ошибка парсинга: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/scrape", response_model=ParseResponse)
async def scrape_krisha_get(
    url: str = Query(..., description="URL страницы krisha.kz"),
    verify_ssl: bool = Query(True, description="Проверять SSL")
):
    """Парсит страницу krisha.kz (GET метод)"""
    try:
        parser = KrishaParser(verify_ssl=verify_ssl)
        items = parser.parse_url(url)
        
        return ParseResponse(
            success=True,
            count=len(items),
            items=[PropertyItem(**item) for item in items],
            message=f"Найдено {len(items)} объявлений"
        )
    except Exception as e:
        logger.error(f"Ошибка парсинга: {e}")
        raise HTTPException(status_code=500, detail=str(e))

