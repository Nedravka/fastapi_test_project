from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional, Tuple
from datetime import datetime


class OrganizationBase(BaseModel):
    """
    Схема отображения модели Organizations
    """
    name: str
    phone_number: Optional[List[str]] = None

    model_config = ConfigDict(from_attributes=True)


class OrganizationFullRead(OrganizationBase):
    """
    Полная схема отображения модели Organizations
    """
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class RectangleAreaRequest(BaseModel):
    """Модель запроса для прямоугольной области"""
    point_a: Tuple[float, float] = Field(..., description="Координаты первой точки (широта, долгота)")
    point_b: Tuple[float, float] = Field(..., description="Координаты второй точки (широта, долгота)")

    @property
    def lat_range(self):
        min_lat = min(self.point_a[0], self.point_b[0])
        max_lat = max(self.point_a[0], self.point_b[0])
        return min_lat, max_lat

    @property
    def lon_range(self):
        min_lon = min(self.point_a[1], self.point_b[1])
        max_lon = max(self.point_a[1], self.point_b[1])
        return min_lon, max_lon
