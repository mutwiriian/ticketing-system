from sqlalchemy import (
    Table, MetaData, Column, 
    Integer, Float, String,
    Boolean, ForeignKey, UniqueConstraint
)

metadata = MetaData()

tickets_table = Table(
    "tickets",
    metadata,
    Column("id", Integer,primary_key=True),
    Column("price",Float,nullable=False),
    Column("show",String,nullable=True),
    Column("user_id",ForeignKey("user_profile.id",ondelete="cascade")),
    Column("sold",Boolean,default=False),
    Column("event_id",ForeignKey("events.id",ondelete="cascade"))
)

ticket_details_table = Table(
    "ticket_details",
    metadata,
    Column("id",Integer,primary_key=True),
    Column("ticket_id",ForeignKey("tickets.id",ondelete="cascade")),
    Column("seat",Integer,nullable=True),
    Column("ticket_type",String,nullable=True)
)

events_table = Table(
    "events",
    metadata,
    Column("id",Integer,primary_key=True),
    Column("name",String,unique=True),
)

sponsors_table = Table(
    "sponsors",
    metadata,
    Column("id",Integer,primary_key=True),
    Column("name",String, unique=True)
)

sponsorships_table = Table(
    "sponsorships",
    metadata,
    Column("id",Integer,primary_key=True),
    Column("event_id",ForeignKey("events.id")),
    Column("sponsor_id",ForeignKey("sponsors.id")),
    Column("amount",Float,nullable=False,default=10),
    UniqueConstraint("event_id","sponsor_id")
)

users_table = Table(
    "user_profile",
    metadata,
    Column("id",Integer,primary_key=True),
    Column("user_name",String,unique=True),
    Column("first_name",String),
    Column("last_name",String),
    Column("email",String),
    Column("password",String)
)
