from datetime import datetime

from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import declarative_base, relationship, backref
from sqlalchemy.orm.collections import attribute_mapped_collection

Base = declarative_base()


class Fee(Base):
    __tablename__ = "fee"

    id = Column(Integer, primary_key=True, autoincrement=True)

    stonks_id = Column(Integer, ForeignKey("stonks.id", ondelete="CASCADE"), nullable=False)
    stonks = relationship("Stonks", back_populates="fees")

    title = Column(String, nullable=False)
    amount = Column(Numeric(15, 4), nullable=False)
    currency = Column(String(3), nullable=False)


class Delivery(Base):
    __tablename__ = "delivery"

    id = Column(Integer, primary_key=True, autoincrement=True)

    offer_id = Column(String, ForeignKey("offer.id", ondelete="CASCADE"), nullable=False)
    offer = relationship("Offer", back_populates="deliveries")

    title = Column(String, nullable=True)
    price = Column(Numeric(15, 4), nullable=False)
    currency = Column(String(3), nullable=False)


class Offer(Base):
    __tablename__ = "offer"

    id = Column(String, primary_key=True, nullable=False)

    url = Column(String)

    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    category = Column(String(32), nullable=False)
    device_name = Column(String, ForeignKey("device.name", ondelete="SET NULL"), nullable=True)
    device = relationship("Device", back_populates="offer", uselist=False)

    price = Column(Numeric(15, 4), nullable=False)
    currency = Column(String(3), nullable=False)

    deliveries = relationship("Delivery", back_populates="offer")

    photos = Column(ARRAY(String))
    is_active = Column(Boolean, nullable=False)

    scraped_at = Column(DateTime, nullable=False)
    last_update_at = Column(DateTime, nullable=True)
    last_stonks_check = Column(DateTime)


class Device(Base):
    __tablename__ = "device"

    name = Column(String, primary_key=True, nullable=False)
    category = Column(String)
    last_price_update = Column(DateTime)

    price = relationship("Price", back_populates="device")
    offer = relationship("Offer", back_populates="device")


class Price(Base):
    __tablename__ = "price"

    id = Column(Integer, primary_key=True, autoincrement=True)
    device_name = Column(String, ForeignKey("device.name", ondelete="CASCADE"), nullable=False)
    source = Column(String(32), nullable=False)
    price = Column(Numeric(15, 4), nullable=False)
    currency = Column(String(3), nullable=False)
    date = Column(DateTime, nullable=False, default=datetime.utcnow())
    device = relationship("Device", back_populates="price")


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    parent_id = Column(Integer, ForeignKey("category.id"), nullable=True)
    children = relationship("Category",
                            cascade="all",
                            backref=backref("parent", remote_side="Category.id"),
                            collection_class=attribute_mapped_collection("name"))


class Stonks(Base):
    __tablename__ = "stonks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    stonks_amount = Column(Numeric(15, 4), nullable=False)

    offer_id = Column(String, ForeignKey("offer.id", ondelete="CASCADE"), nullable=False)
    offer = relationship("Offer", uselist=False)
    fees = relationship("Fee", back_populates="stonks")

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    is_active = Column(Boolean, nullable=False, default=True)
