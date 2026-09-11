import os

class Settings:
    
    DB_URI = f"postgresql://{os.getenv('DB_USER', 'mediscope_user')}:{os.getenv('DB_PASSWORD', 'mediscope_password')}@{os.getenv('DB_HOST', 'postgres')}:{os.getenv('DB_PORT', '5432')}/{os.getenv('DB_NAME', 'mediscope')}"
    

    KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")
    PRESCRIPTION_TOPIC = "prescriptions_stream"
    RISK_ALERTS_TOPIC = "risk_alerts_stream"
    ALERTS_TOPIC: str = "alerts_stream"

settings = Settings()