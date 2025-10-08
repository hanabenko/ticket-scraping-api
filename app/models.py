from sqlalchemy import Column, Integer, String, DateTime, Float, Text, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Artist(Base):
    __tablename__ = "artists"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True, nullable=False)
    genre = Column(String(100))
    spotify_id = Column(String(100), unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    concerts = relationship("Concert", back_populates="artist")
    interactions = relationship("Interaction", back_populates="artist")
    attributions = relationship("Attribution", back_populates="artist")
    daily_metrics = relationship("ArtistDailyMetrics", back_populates="artist")

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(100), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    interactions = relationship("Interaction", back_populates="user")
    attributions = relationship("Attribution", back_populates="user")

class Concert(Base):
    __tablename__ = "concerts"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    artist_id = Column(Integer, ForeignKey("artists.id"), nullable=False)
    venue_name = Column(String(255))
    venue_city = Column(String(100))
    venue_state = Column(String(100))
    venue_country = Column(String(100))
    event_date = Column(DateTime)
    ticket_url = Column(String(500))
    source = Column(String(100))  # seatgeek, url_scrape, etc.
    source_id = Column(String(100))  # external ID from source
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    artist = relationship("Artist", back_populates="concerts")
    interactions = relationship("Interaction", back_populates="concert")

class Interaction(Base):
    __tablename__ = "interactions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    artist_id = Column(Integer, ForeignKey("artists.id"), nullable=False)
    concert_id = Column(Integer, ForeignKey("concerts.id"))
    interaction_type = Column(String(50), nullable=False)  # view, click, purchase, stream, social
    channel = Column(String(50), nullable=False)  # website, app, social, streaming
    timestamp = Column(DateTime, default=datetime.utcnow)
    value = Column(Float)  # purchase amount, stream duration, etc.
    metadata_json = Column(Text)  # JSON string for additional data
    
    # Relationships
    user = relationship("User", back_populates="interactions")
    artist = relationship("Artist", back_populates="interactions")
    concert = relationship("Concert", back_populates="interactions")

class Attribution(Base):
    __tablename__ = "attributions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    artist_id = Column(Integer, ForeignKey("artists.id"), nullable=False)
    score = Column(Float, nullable=False)  # attribution score (0-1)
    last_interaction = Column(DateTime)
    interaction_count = Column(Integer, default=0)
    total_value = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="attributions")
    artist = relationship("Artist", back_populates="attributions")

class ArtistDailyMetrics(Base):
    __tablename__ = "artist_daily_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    artist_id = Column(Integer, ForeignKey("artists.id"), nullable=False)
    date = Column(DateTime, nullable=False)
    
    # Interaction metrics
    total_views = Column(Integer, default=0)
    total_clicks = Column(Integer, default=0)
    total_purchases = Column(Integer, default=0)
    total_streams = Column(Integer, default=0)
    total_social_engagements = Column(Integer, default=0)
    
    # Conversion metrics
    ctr = Column(Float, default=0.0)  # click-through rate
    conversion_rate = Column(Float, default=0.0)  # purchase rate
    stream_lift = Column(Float, default=0.0)  # streaming increase
    
    # Revenue metrics
    total_revenue = Column(Float, default=0.0)
    avg_order_value = Column(Float, default=0.0)
    
    # User metrics
    unique_users = Column(Integer, default=0)
    new_users = Column(Integer, default=0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    artist = relationship("Artist", back_populates="daily_metrics")
