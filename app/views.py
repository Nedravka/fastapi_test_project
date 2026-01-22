from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from app.db import get_db
from app.dependencies import api_key_auth
from app.models import Build, Organization, Activity
from app.schemas import RectangleAreaRequest, OrganizationFullRead


router = APIRouter(prefix="/organizations",
                   tags=["organizations"],
                   dependencies=[api_key_auth])


@router.get("/by_building/{building_id}", response_model=List[OrganizationFullRead])
async def get_organizations_by_building(
        building_id: int,
        db: Session = Depends(get_db)
):
    """
    Cписок всех организаций находящихся в конкретном здании

    Args:
        building_id: ID здания
    """
    building = db.query(Build).filter(Build.id == building_id).first()
    if not building:
        raise HTTPException(
            status_code=404,
            detail=f"Building with id {building_id} not found"
        )

    organizations = db.query(Organization).filter(Organization.build == building_id)

    return organizations.all()


@router.get("/by_activity/{activity_id}", response_model=List[OrganizationFullRead])
async def get_organizations_by_activity_tree(
        activity_id: int,
        include_children: bool = Query(True, description="Включать дочерние виды деятельности"),
        db: Session = Depends(get_db)
):
    """
        Получить организации по виду деятельности
    Args:
        activity_id: ID вида деятельности
        include_children: опциональный параметр для получения организаций принадлежащих к дочерним видам деятельности
           указанного activity_id
    """
    # Получаем вид деятельности
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not activity:
        raise HTTPException(
            status_code=404,
            detail=f"Activity with id {activity_id} not found"
        )

    if include_children:
        def get_all_child_ids(parent_id, visited=None):
            if visited is None:
                visited = set()

            if parent_id in visited:
                return visited

            visited.add(parent_id)

            children = db.query(Activity.id).filter(Activity.parent_id == parent_id).all()
            for child in children:
                visited = get_all_child_ids(child.id, visited)

            return visited

        all_activity_ids = get_all_child_ids(activity_id)
    else:
        all_activity_ids = {activity_id}


    organizations = db.query(Organization).join(
        Organization.activities
    ).filter(
        Activity.id.in_(list(all_activity_ids))
    ).all()

    return organizations


@router.post("/in_area", response_model=List[OrganizationFullRead])
async def get_organizations_in_rectangle_simple(
        area: RectangleAreaRequest,
        db: Session = Depends(get_db)
):
    """
        Список организаций в прямоугольной области
    Body:
         area: координаты области поиска
    """
    min_lat, max_lat = area.lat_range
    min_lon, max_lon = area.lon_range

    organizations = db.query(Organization).join(Build).filter(
        Build.coords != None,
        Build.coords[1] >= min_lat,
        Build.coords[1] <= max_lat,
        Build.coords[2] >= min_lon,
        Build.coords[2] <= max_lon
    ).all()

    return organizations


@router.get("/{organization_id}", response_model=OrganizationFullRead)
async def get_organization_simple(
        organization_id: int,
        db: Session = Depends(get_db)
):
    """
        Получить базовую информацию об организации по ID (без связанных данных).

    Args:
        organization_id: ID организации
    """
    organization = db.query(Organization).filter(Organization.id == organization_id).first()

    if not organization:
        raise HTTPException(
            status_code=404,
            detail=f"Organization with id {organization_id} not found"
        )

    return organization


@router.get("/by_name/{organization_name}", response_model=List[OrganizationFullRead])
async def get_organizations_by_name(
        organization_name: str,
        exact_match: bool = Query(False, description="Точное совпадение имени"),
        db: Session = Depends(get_db)
):
    """
        Поиск организаций по названию

    Args:
        organization_name: Название организации (или его часть)
        exact_match: Если True, ищет точное совпадение; если False, ищет частичное совпадение
    """

    if exact_match:
        query = db.query(Organization).filter(Organization.name == organization_name).all()
    else:
        query = db.query(Organization).filter(Organization.name.ilike(f"%{organization_name}%")).all()

    if not query:
        raise HTTPException(
            status_code=404,
            detail=f"No organizations found with name '{organization_name}'"
        )

    return query

