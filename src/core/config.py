import os

class Config:
    # Database Settings
    DB_USER = os.getenv("DB_USER", "mediscope_user")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "mediscope_password")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "mediscope")
    
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
    # Kafka Settings
    KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    PRESCRIPTION_TOPIC = "prescription.created"
    RISK_TOPIC = "risk.calculated"