import json
import pytest

from kafka import KafkaProducer
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import NoBrokersAvailable, TopicAlreadyExistsError, KafkaError
from src.core.config import settings
from src.utils.logger import logger


KAFKA_BROKER = settings.KAFKA_BROKER
TEST_TOPIC = "test_health_check"

def test_kafka_admin_and_topic_creation():
    """Kafka'ya bağlanır, topic var mı kontrol eder, yoksa oluşturur."""
    try:
       
        admin_client = KafkaAdminClient(
            bootstrap_servers=KAFKA_BROKER,
            client_id='mediguard_admin_test',
            request_timeout_ms=5000
        )
        
        # 2. Mevcut Topic'leri Listele
        existing_topics = admin_client.list_topics()
        
        
        if TEST_TOPIC not in existing_topics:
            logger.info(f"\n[INFO] '{TEST_TOPIC}' bulunamadı, oluşturuluyor...")
            new_topic = NewTopic(name=TEST_TOPIC, num_partitions=1, replication_factor=1)
            try:
                admin_client.create_topics(new_topics=[new_topic], validate_only=False)
                logger.info(f"[SUCCESS] '{TEST_TOPIC}' başarıyla oluşturuldu.")
            except TopicAlreadyExistsError:
                pass 
        else:
            logger.info(f"\n[SUCCESS] '{TEST_TOPIC}' zaten mevcut.")
            
        admin_client.close()
        
    except NoBrokersAvailable:
        pytest.fail(f"Kafka broker'ına ulaşılamadı! Admin bağlantısı başarısız. Hedef: {KAFKA_BROKER}")
    except Exception as e:
        pytest.fail(f"Topic kontrolü/oluşturulması sırasında hata: {e}")

def test_kafka_producer_message():
    """Oluşturulan veya var olan topic'e mesaj gönderimini test eder."""
    try:
        producer = KafkaProducer(
            bootstrap_servers=KAFKA_BROKER,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            api_version_auto_timeout_ms=5000,
            request_timeout_ms=5000
        )
        
        test_event = {"event": "ping", "status": "ok", "service": "mediguard_pytest"}
        
        
        future = producer.send(TEST_TOPIC, test_event)
        
        
        record_metadata = future.get(timeout=5)
        
        assert record_metadata.topic == TEST_TOPIC
        assert record_metadata.partition is not None
        
        producer.close()
        
    except Exception as e:
        pytest.fail(f"Mesaj gönderim testi başarısız: {e}")