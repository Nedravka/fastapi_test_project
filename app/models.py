from typing import List, Optional

from sqlalchemy import String, ARRAY, ForeignKey, Float, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from app.core import Base


organization_activity = Table(
    'organization_activity',
    Base.metadata,
    Column('organization_id', ForeignKey('organizations.id'), primary_key=True),
    Column('activity_id', ForeignKey('activities.id'), primary_key=True)
)


class Build(Base):
    """
        Модель зданий
    """

    address: Mapped[str]
    coords: Mapped[Optional[tuple[float, float] | None]] = mapped_column(ARRAY(Float))

    organizations: Mapped[List["Organization"]] = relationship(
        "Organization",
        back_populates="builds",
        cascade="save-update, merge"
    )


class Organization(Base):
    """
        Модель организаций
    """

    name: Mapped[str]
    phone_number: Mapped[List[str] | None] = mapped_column(ARRAY(String))
    build: Mapped[int] = mapped_column(ForeignKey('builds.id'))

    builds: Mapped["Build"] = relationship(
        "Build",
        back_populates="organizations"
    )
    activities: Mapped[List["Activity"]] = relationship(
        "Activity",
        secondary=organization_activity,
        back_populates="organizations"
    )


class Activity(Base):
    """
        Иерархическая модель видов деятельности
    """

    name: Mapped[str] = mapped_column(String(100))
    parent_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey('activities.id'),
        nullable=True
    )
    level: Mapped[int] = mapped_column(default=0)

    parent: Mapped[Optional["Activity"]] = relationship(
        "Activity",
        remote_side='Activity.id',
        back_populates="children"
    )

    children: Mapped[List["Activity"]] = relationship(
        "Activity",
        back_populates="parent"
    )

    organizations: Mapped[List["Organization"]] = relationship(
        "Organization",
        secondary=organization_activity,
        back_populates="activities"
    )

    @validates('parent')
    def validate_parent(self, key, parent):
        if parent is not None:
            if parent.parent is not None:
                raise ValueError("Activity can have only 3 levels of nesting")

            self.level = parent.level + 1
            if self.level > 2:
                raise ValueError("Maximum nesting depth is 3 levels")
        else:
            self.level = 0
        return parent

