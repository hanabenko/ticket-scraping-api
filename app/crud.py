from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import datetime, timedelta
from typing import List, Optional
import json
from .models import Artist, User, Concert, Interaction, Attribution, ArtistDailyMetrics

def get_or_create_artist(db: Session, name: str, genre: str = None) -> Artist:
    """Get or create an artist by name"""
    artist = db.query(Artist).filter(Artist.name == name).first()
    if not artist:
        artist = Artist(name=name, genre=genre)
        db.add(artist)
        db.commit()
        db.refresh(artist)
    return artist

def get_or_create_user(db: Session, user_id: str, email: str = None) -> User:
    """Get or create a user by user_id"""
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        user = User(user_id=user_id, email=email)
        db.add(user)
        db.commit()
        db.refresh(user)
    return user

def create_interaction(
    db: Session,
    user_id: str,
    artist_name: str,
    interaction_type: str,
    channel: str,
    value: float = None,
    concert_id: int = None,
    metadata: dict = None
) -> Interaction:
    """Create a new interaction record"""
    # Get or create user and artist
    user = get_or_create_user(db, user_id)
    artist = get_or_create_artist(db, artist_name)
    
    # Create interaction
    interaction = Interaction(
        user_id=user.id,
        artist_id=artist.id,
        concert_id=concert_id,
        interaction_type=interaction_type,
        channel=channel,
        value=value,
        metadata_json=json.dumps(metadata) if metadata else None
    )
    
    db.add(interaction)
    db.commit()
    db.refresh(interaction)
    
    # Update attribution
    recompute_attribution_for_user(db, user.id)
    
    return interaction

def recompute_attribution_for_user(db: Session, user_id: int):
    """Recompute attribution scores for a user using multi-touch attribution"""
    # Get all interactions for this user
    interactions = db.query(Interaction).filter(Interaction.user_id == user_id).all()
    
    # Group by artist
    artist_interactions = {}
    for interaction in interactions:
        artist_id = interaction.artist_id
        if artist_id not in artist_interactions:
            artist_interactions[artist_id] = []
        artist_interactions[artist_id].append(interaction)
    
    # Calculate attribution scores for each artist
    for artist_id, artist_ints in artist_interactions.items():
        # Multi-touch attribution with recency decay
        score = 0.0
        total_value = 0.0
        interaction_count = len(artist_ints)
        
        # Sort by timestamp
        artist_ints.sort(key=lambda x: x.timestamp)
        
        for i, interaction in enumerate(artist_ints):
            # Recency decay: more recent interactions get higher weight
            recency_weight = 1.0 / (1.0 + i * 0.1)
            
            # Interaction type weights
            type_weights = {
                'view': 0.1,
                'click': 0.3,
                'purchase': 1.0,
                'stream': 0.5,
                'social': 0.2
            }
            
            type_weight = type_weights.get(interaction.interaction_type, 0.1)
            score += recency_weight * type_weight
            
            if interaction.value:
                total_value += interaction.value
        
        # Normalize score to 0-1 range
        max_possible_score = sum(type_weights.values()) * len(artist_ints)
        normalized_score = min(score / max_possible_score, 1.0) if max_possible_score > 0 else 0.0
        
        # Update or create attribution record
        attribution = db.query(Attribution).filter(
            Attribution.user_id == user_id,
            Attribution.artist_id == artist_id
        ).first()
        
        if attribution:
            attribution.score = normalized_score
            attribution.last_interaction = artist_ints[-1].timestamp
            attribution.interaction_count = interaction_count
            attribution.total_value = total_value
            attribution.updated_at = datetime.utcnow()
        else:
            attribution = Attribution(
                user_id=user_id,
                artist_id=artist_id,
                score=normalized_score,
                last_interaction=artist_ints[-1].timestamp,
                interaction_count=interaction_count,
                total_value=total_value
            )
            db.add(attribution)
    
    db.commit()

def compute_daily_metrics_for_date(db: Session, date: datetime):
    """Compute daily metrics for all artists for a given date"""
    start_date = date.replace(hour=0, minute=0, second=0, microsecond=0)
    end_date = start_date + timedelta(days=1)
    
    # Get all artists
    artists = db.query(Artist).all()
    
    for artist in artists:
        # Get interactions for this artist on this date
        interactions = db.query(Interaction).filter(
            Interaction.artist_id == artist.id,
            Interaction.timestamp >= start_date,
            Interaction.timestamp < end_date
        ).all()
        
        # Calculate metrics
        total_views = sum(1 for i in interactions if i.interaction_type == 'view')
        total_clicks = sum(1 for i in interactions if i.interaction_type == 'click')
        total_purchases = sum(1 for i in interactions if i.interaction_type == 'purchase')
        total_streams = sum(1 for i in interactions if i.interaction_type == 'stream')
        total_social_engagements = sum(1 for i in interactions if i.interaction_type == 'social')
        
        # Conversion metrics
        ctr = (total_clicks / total_views) if total_views > 0 else 0.0
        conversion_rate = (total_purchases / total_clicks) if total_clicks > 0 else 0.0
        
        # Revenue metrics
        purchase_interactions = [i for i in interactions if i.interaction_type == 'purchase']
        total_revenue = sum(i.value or 0 for i in purchase_interactions)
        avg_order_value = (total_revenue / total_purchases) if total_purchases > 0 else 0.0
        
        # User metrics
        unique_users = len(set(i.user_id for i in interactions))
        
        # Check for new users (first interaction with this artist)
        new_users = 0
        for user_id in set(i.user_id for i in interactions):
            first_interaction = db.query(Interaction).filter(
                Interaction.user_id == user_id,
                Interaction.artist_id == artist.id
            ).order_by(Interaction.timestamp).first()
            if first_interaction and first_interaction.timestamp >= start_date:
                new_users += 1
        
        # Stream lift calculation (simplified - would need historical data for proper calculation)
        stream_lift = 0.0  # Placeholder - would calculate vs baseline
        
        # Create or update daily metrics
        daily_metrics = db.query(ArtistDailyMetrics).filter(
            ArtistDailyMetrics.artist_id == artist.id,
            ArtistDailyMetrics.date == start_date
        ).first()
        
        if daily_metrics:
            daily_metrics.total_views = total_views
            daily_metrics.total_clicks = total_clicks
            daily_metrics.total_purchases = total_purchases
            daily_metrics.total_streams = total_streams
            daily_metrics.total_social_engagements = total_social_engagements
            daily_metrics.ctr = ctr
            daily_metrics.conversion_rate = conversion_rate
            daily_metrics.stream_lift = stream_lift
            daily_metrics.total_revenue = total_revenue
            daily_metrics.avg_order_value = avg_order_value
            daily_metrics.unique_users = unique_users
            daily_metrics.new_users = new_users
        else:
            daily_metrics = ArtistDailyMetrics(
                artist_id=artist.id,
                date=start_date,
                total_views=total_views,
                total_clicks=total_clicks,
                total_purchases=total_purchases,
                total_streams=total_streams,
                total_social_engagements=total_social_engagements,
                ctr=ctr,
                conversion_rate=conversion_rate,
                stream_lift=stream_lift,
                total_revenue=total_revenue,
                avg_order_value=avg_order_value,
                unique_users=unique_users,
                new_users=new_users
            )
            db.add(daily_metrics)
    
    db.commit()

def get_top_artists_by_attribution(db: Session, limit: int = 10) -> List[dict]:
    """Get top artists by attribution score"""
    results = db.query(
        Artist.name,
        func.avg(Attribution.score).label('avg_score'),
        func.count(Attribution.id).label('user_count'),
        func.sum(Attribution.total_value).label('total_value')
    ).join(Attribution).group_by(Artist.id).order_by(
        desc('avg_score')
    ).limit(limit).all()
    
    return [
        {
            'artist_name': r.name,
            'avg_attribution_score': float(r.avg_score),
            'attributed_users': r.user_count,
            'total_value': float(r.total_value or 0)
        }
        for r in results
    ]

def get_artist_metrics(db: Session, artist_name: str, days: int = 30) -> dict:
    """Get comprehensive metrics for a specific artist"""
    artist = db.query(Artist).filter(Artist.name == artist_name).first()
    if not artist:
        return {}
    
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    # Get daily metrics
    daily_metrics = db.query(ArtistDailyMetrics).filter(
        ArtistDailyMetrics.artist_id == artist.id,
        ArtistDailyMetrics.date >= start_date
    ).order_by(ArtistDailyMetrics.date).all()
    
    # Aggregate totals
    total_views = sum(m.total_views for m in daily_metrics)
    total_clicks = sum(m.total_clicks for m in daily_metrics)
    total_purchases = sum(m.total_purchases for m in daily_metrics)
    total_streams = sum(m.total_streams for m in daily_metrics)
    total_revenue = sum(m.total_revenue for m in daily_metrics)
    total_users = sum(m.unique_users for m in daily_metrics)
    
    # Calculate overall metrics
    overall_ctr = (total_clicks / total_views) if total_views > 0 else 0.0
    overall_conversion_rate = (total_purchases / total_clicks) if total_clicks > 0 else 0.0
    avg_order_value = (total_revenue / total_purchases) if total_purchases > 0 else 0.0
    
    return {
        'artist_name': artist_name,
        'period_days': days,
        'total_views': total_views,
        'total_clicks': total_clicks,
        'total_purchases': total_purchases,
        'total_streams': total_streams,
        'total_revenue': total_revenue,
        'total_users': total_users,
        'ctr': overall_ctr,
        'conversion_rate': overall_conversion_rate,
        'avg_order_value': avg_order_value,
        'daily_breakdown': [
            {
                'date': m.date.isoformat(),
                'views': m.total_views,
                'clicks': m.total_clicks,
                'purchases': m.total_purchases,
                'revenue': m.total_revenue
            }
            for m in daily_metrics
        ]
    }
