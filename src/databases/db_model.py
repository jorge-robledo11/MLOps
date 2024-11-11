from sqlalchemy import REAL, INTEGER, VARCHAR
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from config.db_settings import DBSettings


class Base(DeclarativeBase):
    """Base class for SQLAlchemy ORM models."""
    pass


class RentApartments(Base):
    """
    SQLAlchemy model for representing rental apartment data.

    Attributes:
        address (str): Primary key representing the apartment's address.
        area (float): Apartment area in square meters.
        constraction_year (int): Year of construction.
        rooms (int): Total number of rooms in the apartment.
        bedrooms (int): Number of bedrooms.
        bathrooms (int): Number of bathrooms.
        balcony (str): Indicates balcony availability.
        storage (str): Indicates storage space availability.
        parking (str): Indicates parking availability.
        furnished (str): Indicates if the apartment is furnished.
        garage (str): Indicates garage availability.
        garden (str): Indicates garden availability.
        energy (str): Energy rating.
        facilities (str): Additional facilities provided.
        zip (str): ZIP code of the apartment's location.
        neighborhood (str): Neighborhood name.
        rent (int): Monthly rent amount.
    """

    __tablename__ = DBSettings().table_name  # type: ignore

    address: Mapped[str] = mapped_column(VARCHAR(), primary_key=True)
    area: Mapped[float] = mapped_column(REAL())
    constraction_year: Mapped[int] = mapped_column(INTEGER())
    rooms: Mapped[int] = mapped_column(INTEGER())
    bedrooms: Mapped[int] = mapped_column(INTEGER())
    bathrooms: Mapped[int] = mapped_column(INTEGER())
    balcony: Mapped[str] = mapped_column(VARCHAR())
    storage: Mapped[str] = mapped_column(VARCHAR())
    parking: Mapped[str] = mapped_column(VARCHAR())
    furnished: Mapped[str] = mapped_column(VARCHAR())
    garage: Mapped[str] = mapped_column(VARCHAR())
    garden: Mapped[str] = mapped_column(VARCHAR())
    energy: Mapped[str] = mapped_column(VARCHAR())
    facilities: Mapped[str] = mapped_column(VARCHAR())
    zip: Mapped[str] = mapped_column(VARCHAR())
    neighborhood: Mapped[str] = mapped_column(VARCHAR())
    rent: Mapped[int] = mapped_column(INTEGER())
