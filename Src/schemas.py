from datetime import datetime
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.dialects.postgresql import ARRAY, JSONB

#TODO see if relationship is worth using for this schema

class Base(DeclarativeBase):
    pass

class Events(Base):
    __tablename__ = 'Events_Dim'

    id: Mapped[int] = mapped_column(primary_key = True)
    name : Mapped[str] = mapped_column()
    date: Mapped[datetime] = mapped_column()
    players = Mapped[int] = mapped_column()

class Decks(Base):
    __tablename__ = 'Decks_Dim'

    id: Mapped[int] = mapped_column(primary_key = True)
    archetype: Mapped[str] = mapped_column()
    player : Mapped[str] = mapped_column()

class Cards(Base):
    __tablename__ = 'Cards_Dim'

    #Top level data found in every card
    name: Mapped[str] = mapped_column(primary_key = True)
    released_at: Mapped[datetime] = mapped_column()
    layout: Mapped[str] = mapped_column()
    cmc: Mapped[float] = mapped_column()
    set: Mapped[str] = mapped_column()
    set_name: Mapped[str] = mapped_column()
    artist: Mapped[str] = mapped_column()
    price: Mapped[float | None] = mapped_column()

    #Front face info
    front_name: Mapped[String] = mapped_column()
    front_image_uris: Mapped[dict[str, str]] = mapped_column(MutableDict.as_mutable(JSONB), default = dict)
    front_mana_cost: Mapped[str] = mapped_column()
    front_type_line: Mapped[str] = mapped_column()
    front_oracle_text: Mapped[str] = mapped_column()
    front_power: Mapped[str | None] = mapped_column()
    front_toughness: Mapped[str | None] = mapped_column()
    front_colors: Mapped[list[str]] = mapped_column(ARRAY(String))
    front_keywords: Mapped[list[str]] = mapped_column(ARRAY(String))

    #Back/alternate face info for dual faced cards, rooms, split cards, prepare cards, etc.
    alt_name: Mapped[String | None] = mapped_column()
    alt_image_uris: Mapped[dict[str, str] | None] = mapped_column(MutableDict.as_mutable(JSONB), default = dict)
    alt_mana_cost: Mapped[str | None] = mapped_column()
    alt_type_line: Mapped[str | None] = mapped_column()
    alt_oracle_text: Mapped[str | None] = mapped_column()
    alt_power: Mapped[str | None] = mapped_column()
    alt_toughness: Mapped[str | None] = mapped_column()
    alt_colors = Mapped[list[str] | None] = mapped_column(ARRAY(String))
    alt_keywords: Mapped[list[str] | None] = mapped_column(ARRAY(String))

class DeckCards(Base):
    __tablename__ = 'Deck_Cards_Fact'

    id: Mapped[int] = mapped_column(primary_key = True)
    deck: Mapped[int] = mapped_column(ForeignKey('Decks_Dim.id'))
    card: Mapped[int] = mapped_column(ForeignKey('Cards_Dim.name'))
    event: Mapped[int] = mapped_column(ForeignKey('Events_Dim.id'))
    zone: Mapped[str] = mapped_column()
    quantity: Mapped[int] = mapped_column()