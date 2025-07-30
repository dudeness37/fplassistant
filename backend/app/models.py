"""
SQLAlchemy models for FPL Assistant database
"""
from sqlalchemy import Column, Integer, String, Numeric, Boolean, DateTime, Date, Text, ForeignKey, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()

class Team(Base):
    __tablename__ = "teams"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    fpl_id = Column(Integer, unique=True)
    sportmonks_id = Column(Integer, unique=True)
    name = Column(String, nullable=False)
    short_name = Column(String, nullable=False)
    league = Column(String, nullable=False, default="Premier League")
    founded_year = Column(Integer)
    venue = Column(String)
    venue_capacity = Column(Integer)
    current_manager = Column(String)
    manager_appointed_date = Column(Date)
    primary_color = Column(String)
    secondary_color = Column(String)
    logo_url = Column(String)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    players = relationship("Player", back_populates="team")
    home_fixtures = relationship("Fixture", foreign_keys="Fixture.home_team_id", back_populates="home_team")
    away_fixtures = relationship("Fixture", foreign_keys="Fixture.away_team_id", back_populates="away_team")

class Player(Base):
    __tablename__ = "players"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    fpl_id = Column(Integer, unique=True)
    sportmonks_id = Column(Integer, unique=True)
    understat_id = Column(Integer)
    
    # Basic info
    first_name = Column(String, nullable=False)
    second_name = Column(String, nullable=False)
    web_name = Column(String)
    
    # FPL specific
    team_id = Column(Integer, ForeignKey("teams.id"))
    position = Column(String, nullable=False)
    price = Column(Numeric(4, 1))
    selected_by_percent = Column(Numeric(5, 2))
    status = Column(String, default="a")
    
    # Physical attributes
    date_of_birth = Column(Date)
    nationality = Column(String)
    height_cm = Column(Integer)
    weight_kg = Column(Integer)
    
    # Career info
    market_value_eur = Column(Integer)
    contract_expires = Column(Date)
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    team = relationship("Team", back_populates="players")
    gameweek_stats = relationship("PlayerGameweekStats", back_populates="player")
    feature_ratings = relationship("PlayerFeatureRating", back_populates="player")

class Fixture(Base):
    __tablename__ = "fixtures"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    fpl_id = Column(Integer, unique=True)
    sportmonks_id = Column(Integer, unique=True)
    
    # Basic match info
    season = Column(String, nullable=False, default="2024-25")
    gameweek = Column(Integer, nullable=False)
    home_team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    away_team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    
    # Scheduling
    kickoff_time = Column(DateTime, nullable=False)
    timezone = Column(String, default="Europe/London")
    venue = Column(String)
    referee = Column(String)
    
    # State tracking
    status = Column(String, default="scheduled")
    minute_live = Column(Integer)
    
    # Results
    home_score = Column(Integer)
    away_score = Column(Integer)
    home_score_ht = Column(Integer)
    away_score_ht = Column(Integer)
    
    # Match conditions
    weather_description = Column(String)
    temperature_celsius = Column(Integer)
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    home_team = relationship("Team", foreign_keys=[home_team_id])
    away_team = relationship("Team", foreign_keys=[away_team_id])
    match_statistics = relationship("MatchStatistics", back_populates="fixture")
    match_odds = relationship("MatchOdds", back_populates="fixture")
    
    __table_args__ = (
        UniqueConstraint("season", "gameweek", "home_team_id", "away_team_id", name="unique_team_gw"),
    )

class PlayerGameweekStats(Base):
    __tablename__ = "player_gameweek_stats"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    fixture_id = Column(Integer, ForeignKey("fixtures.id"))
    season = Column(String, nullable=False, default="2024-25")
    gameweek = Column(Integer, nullable=False)
    
    # FPL scoring
    total_points = Column(Integer, default=0)
    minutes = Column(Integer, default=0)
    goals_scored = Column(Integer, default=0)
    assists = Column(Integer, default=0)
    clean_sheets = Column(Integer, default=0)
    goals_conceded = Column(Integer, default=0)
    own_goals = Column(Integer, default=0)
    penalties_saved = Column(Integer, default=0)
    penalties_missed = Column(Integer, default=0)
    yellow_cards = Column(Integer, default=0)
    red_cards = Column(Integer, default=0)
    saves = Column(Integer, default=0)
    bonus = Column(Integer, default=0)
    bps = Column(Integer, default=0)
    
    # Advanced metrics
    shots = Column(Integer, default=0)
    shots_on_target = Column(Integer, default=0)
    key_passes = Column(Integer, default=0)
    big_chances_created = Column(Integer, default=0)
    big_chances_missed = Column(Integer, default=0)
    xg = Column(Numeric(6, 3), default=0)
    xa = Column(Numeric(6, 3), default=0)
    npxg = Column(Numeric(6, 3))
    
    # Market data
    price_at_start = Column(Numeric(4, 1))
    ownership_at_start = Column(Numeric(5, 2))
    transfers_in = Column(Integer, default=0)
    transfers_out = Column(Integer, default=0)
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    player = relationship("Player", back_populates="gameweek_stats")
    fixture = relationship("Fixture")
    
    __table_args__ = (
        UniqueConstraint("player_id", "season", "gameweek", name="unique_player_gw"),
    )

class MatchStatistics(Base):
    __tablename__ = "match_statistics"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    # FIXED: Support both FPL and Sportmonks fixture references
    fixture_id = Column(Integer, ForeignKey("fixtures.id"))  # FPL fixture (optional)
    fixture_sportmonks_id = Column(Integer)  # Sportmonks fixture ID (for external data)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    is_home = Column(Boolean, nullable=False)
    
    # Shooting
    shots_total = Column(Integer, default=0)
    shots_on_target = Column(Integer, default=0)
    shots_off_target = Column(Integer, default=0)
    shots_inside_box = Column(Integer, default=0)
    shots_outside_box = Column(Integer, default=0)
    big_chances_created = Column(Integer, default=0)
    big_chances_missed = Column(Integer, default=0)
    
    # Expected goals
    xg = Column(Numeric(6, 3), default=0)
    xga = Column(Numeric(6, 3), default=0)
    
    # Possession & passing
    possession_percentage = Column(Numeric(5, 2))
    passes_total = Column(Integer, default=0)
    passes_accurate = Column(Integer, default=0)
    pass_accuracy_percentage = Column(Numeric(5, 2))
    key_passes = Column(Integer, default=0)
    
    # Defensive
    tackles = Column(Integer, default=0)
    blocks = Column(Integer, default=0)
    interceptions = Column(Integer, default=0)
    clearances = Column(Integer, default=0)
    
    # Set pieces
    corners = Column(Integer, default=0)
    offsides = Column(Integer, default=0)
    fouls = Column(Integer, default=0)
    
    # Cards
    yellow_cards = Column(Integer, default=0)
    red_cards = Column(Integer, default=0)
    
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    fixture = relationship("Fixture", back_populates="match_statistics")
    team = relationship("Team")
    
    __table_args__ = (
        # Updated constraint to handle both fixture types
        UniqueConstraint("fixture_sportmonks_id", "team_id", name="unique_sportmonks_fixture_team"),
    )

class PlayerMatchStats(Base):
    __tablename__ = "player_match_stats"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    fixture_id = Column(Integer, ForeignKey("fixtures.id"), nullable=False)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    
    # Playing time
    minutes_played = Column(Integer, default=0)
    starting_xi = Column(Boolean, default=False)
    substitute_in_minute = Column(Integer)
    substitute_out_minute = Column(Integer)
    
    # Performance
    rating = Column(Numeric(3, 1))
    goals = Column(Integer, default=0)
    assists = Column(Integer, default=0)
    shots = Column(Integer, default=0)
    shots_on_target = Column(Integer, default=0)
    key_passes = Column(Integer, default=0)
    big_chances_created = Column(Integer, default=0)
    big_chances_missed = Column(Integer, default=0)
    
    # Expected metrics
    xg = Column(Numeric(6, 3), default=0)
    xa = Column(Numeric(6, 3), default=0)
    
    # Defensive stats
    tackles = Column(Integer, default=0)
    interceptions = Column(Integer, default=0)
    clearances = Column(Integer, default=0)
    blocks = Column(Integer, default=0)
    
    # Discipline
    fouls_committed = Column(Integer, default=0)
    fouls_drawn = Column(Integer, default=0)
    yellow_cards = Column(Integer, default=0)
    red_cards = Column(Integer, default=0)
    
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    player = relationship("Player")
    fixture = relationship("Fixture")
    team = relationship("Team")
    
    __table_args__ = (
        UniqueConstraint("player_id", "fixture_id", name="unique_player_match"),
    )

class MatchOdds(Base):
    __tablename__ = "match_odds"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    fixture_id = Column(Integer, ForeignKey("fixtures.id"))
    event_id = Column(String)  # External API event ID
    bookmaker = Column(String, nullable=False)
    market = Column(String, nullable=False)
    
    # Main markets
    home_win = Column(Numeric(6, 2))
    draw = Column(Numeric(6, 2))
    away_win = Column(Numeric(6, 2))
    
    # Totals market
    over_2_5 = Column(Numeric(6, 2))
    under_2_5 = Column(Numeric(6, 2))
    over_1_5 = Column(Numeric(6, 2))
    under_1_5 = Column(Numeric(6, 2))
    
    # Both teams to score
    btts_yes = Column(Numeric(6, 2))
    btts_no = Column(Numeric(6, 2))
    
    # Clean sheet odds
    home_clean_sheet = Column(Numeric(6, 2))
    away_clean_sheet = Column(Numeric(6, 2))
    
    # Calculated probabilities
    prob_home = Column(Numeric(5, 4))
    prob_away = Column(Numeric(5, 4))
    prob_draw = Column(Numeric(5, 4))
    home_lambda = Column(Numeric(5, 3))
    away_lambda = Column(Numeric(5, 3))
    
    # Timing
    snapshot_time = Column(DateTime, default=func.now())
    is_closing_odds = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    fixture = relationship("Fixture", back_populates="match_odds")

class PlayerInjury(Base):
    __tablename__ = "player_injuries"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    injury_type = Column(String, nullable=False)
    severity = Column(String)
    body_part = Column(String)
    
    # Timing
    injury_date = Column(Date)
    expected_return_date = Column(Date)
    actual_return_date = Column(Date)
    
    # Status
    status = Column(String, default="injured")
    
    # Sources
    source = Column(String)
    confidence = Column(Numeric(3, 2), default=1.0)
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    player = relationship("Player")

class TeamFeatureRating(Base):
    __tablename__ = "team_feature_ratings"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    season = Column(String, nullable=False, default="2024-25")
    gameweek = Column(Integer, nullable=False)
    
    # TFP Features (0-100 scale)
    t1_team_form = Column(Numeric(5, 2), default=50)
    t2_attack_strength = Column(Numeric(5, 2), default=50)
    t3_defense_strength = Column(Numeric(5, 2), default=50)
    t4_fixture_difficulty = Column(Numeric(5, 2), default=50)
    t5_manager_edge = Column(Numeric(5, 2), default=50)
    
    # Computed metrics for debugging
    xg_for_last_5 = Column(Numeric(6, 3))
    xg_against_last_5 = Column(Numeric(6, 3))
    points_last_5 = Column(Integer)
    
    # Metadata
    computed_at = Column(DateTime, default=func.now())
    computation_version = Column(String, default="v1.0")
    
    # Relationships
    team = relationship("Team")
    
    __table_args__ = (
        UniqueConstraint("team_id", "season", "gameweek", name="unique_team_gw_features"),
    )

class PlayerFeatureRating(Base):
    __tablename__ = "player_feature_ratings"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    season = Column(String, nullable=False, default="2024-25")
    gameweek = Column(Integer, nullable=False)
    
    # PPP Features (0-100 scale)
    p1_form_involvement = Column(Numeric(5, 2), default=50)
    p2_nailedness = Column(Numeric(5, 2), default=50)
    p3_fixture_rating = Column(Numeric(5, 2), default=50)
    p4_team_context = Column(Numeric(5, 2), default=50)
    p5_explosiveness = Column(Numeric(5, 2), default=50)
    
    # Supporting metrics for debugging
    xgi_per_90_last_6 = Column(Numeric(6, 3))
    minutes_last_10 = Column(Integer)
    start_probability = Column(Numeric(3, 2))
    haul_frequency_l20 = Column(Numeric(3, 2))
    
    # Metadata
    computed_at = Column(DateTime, default=func.now())
    computation_version = Column(String, default="v1.0")
    
    # Relationships
    player = relationship("Player", back_populates="feature_ratings")
    
    __table_args__ = (
        UniqueConstraint("player_id", "season", "gameweek", name="unique_player_gw_features"),
    )

class PlayerRating(Base):
    __tablename__ = "player_ratings"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    season = Column(String, nullable=False, default="2024-25")
    gameweek = Column(Integer, nullable=False)
    
    # Blended ratings (0-100 scale)
    overall_rating = Column(Numeric(5, 2), default=50)
    captaincy_rating = Column(Numeric(5, 2), default=50)
    safe_rating = Column(Numeric(5, 2), default=50)
    differential_rating = Column(Numeric(5, 2), default=50)
    
    # Price and value metrics
    current_price = Column(Numeric(4, 1))
    value_rating = Column(Numeric(5, 2))
    price_change_probability = Column(Numeric(3, 2))
    
    # Market context
    ownership_percentile = Column(Numeric(3, 2))
    transfer_momentum = Column(Numeric(5, 2))
    
    # Metadata
    computed_at = Column(DateTime, default=func.now())
    weights_version = Column(String, default="v1.0")
    
    # Relationships
    player = relationship("Player")
    
    __table_args__ = (
        UniqueConstraint("player_id", "season", "gameweek", name="unique_player_gw_ratings"),
    )

class ExternalProvider(Base):
    __tablename__ = "external_providers"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    base_url = Column(String)
    rate_limit_per_minute = Column(Integer, default=60)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())

class DataJob(Base):
    __tablename__ = "data_jobs"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    job_name = Column(String, nullable=False)
    provider_code = Column(String, ForeignKey("external_providers.code"))
    status = Column(String)
    
    # Execution info
    started_at = Column(DateTime, default=func.now())
    completed_at = Column(DateTime)
    
    # Results
    records_processed = Column(Integer, default=0)
    records_inserted = Column(Integer, default=0)
    records_updated = Column(Integer, default=0)
    records_failed = Column(Integer, default=0)
    
    # Error tracking
    error_message = Column(Text)
    error_details = Column(Text)  # JSON field for detailed errors
    
    # Metadata
    gameweek = Column(Integer)
    season = Column(String, default="2024-25")
    
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    provider = relationship("ExternalProvider")

class FeatureWeight(Base):
    __tablename__ = "feature_weights"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    rating_type = Column(String, nullable=False)
    
    # PPP feature weights (sum to 1.0)
    p1_weight = Column(Numeric(4, 3), default=0.200)
    p2_weight = Column(Numeric(4, 3), default=0.250)
    p3_weight = Column(Numeric(4, 3), default=0.200)
    p4_weight = Column(Numeric(4, 3), default=0.175)
    p5_weight = Column(Numeric(4, 3), default=0.175)
    
    # Metadata
    version = Column(String, nullable=False, default="v1.0")
    active_from = Column(DateTime, default=func.now())
    active_until = Column(DateTime)
    created_by = Column(String, default="system")
    notes = Column(Text)
    created_at = Column(DateTime, default=func.now())
    
    __table_args__ = (
        UniqueConstraint("rating_type", "version", name="unique_rating_type_version"),
    )