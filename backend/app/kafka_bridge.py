"""Kafka bridge for QDPI events - transparent integration with event bus"""

import os
import json
import asyncio
import logging
from typing import Optional, Dict, Any
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from aiokafka.errors import KafkaError

from .events import BUS, Event, make_event

logger = logging.getLogger(__name__)

class KafkaBridge:
    """Bridge between in-memory event bus and Kafka for scalable event streaming"""
    
    def __init__(self):
        self.enabled = os.getenv("KAFKA_ENABLED", "false").lower() == "true"
        self.brokers = os.getenv("KAFKA_BROKERS", "localhost:9092").split(",")
        self.topic_prefix = os.getenv("KAFKA_TOPICS_PREFIX", "gibsey")
        
        self.producer: Optional[AIOKafkaProducer] = None
        self.consumer: Optional[AIOKafkaConsumer] = None
        self.running = False
        
        # Topic names
        self.topics = {
            "ui_symbol": f"{self.topic_prefix}.ui.symbol",
            "page_request": f"{self.topic_prefix}.generate.page.request", 
            "page_done": f"{self.topic_prefix}.generate.page.done"
        }
        
        logger.info(f"Kafka bridge initialized: enabled={self.enabled}, topics={self.topics}")
    
    async def start(self):
        """Start Kafka producer and consumer if enabled"""
        if not self.enabled:
            logger.info("Kafka bridge disabled - events will only use in-memory bus")
            return
            
        try:
            # Start producer
            self.producer = AIOKafkaProducer(
                bootstrap_servers=self.brokers,
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                compression_type="gzip"
            )
            await self.producer.start()
            logger.info(f"Kafka producer started: {self.brokers}")
            
            # Start consumer for page.done events
            self.consumer = AIOKafkaConsumer(
                self.topics["page_done"],
                bootstrap_servers=self.brokers,
                group_id="qdpi-event-bridge",
                value_deserializer=lambda v: json.loads(v.decode('utf-8')),
                auto_offset_reset="latest"
            )
            await self.consumer.start()
            logger.info(f"Kafka consumer started for topic: {self.topics['page_done']}")
            
            # Start consumer task
            self.running = True
            asyncio.create_task(self._consume_loop())
            
        except Exception as e:
            logger.error(f"Failed to start Kafka bridge: {e}")
            self.enabled = False
            await self.stop()
    
    async def stop(self):
        """Stop Kafka producer and consumer"""
        self.running = False
        
        if self.producer:
            try:
                await self.producer.stop()
                logger.info("Kafka producer stopped")
            except Exception as e:
                logger.error(f"Error stopping producer: {e}")
                
        if self.consumer:
            try:
                await self.consumer.stop() 
                logger.info("Kafka consumer stopped")
            except Exception as e:
                logger.error(f"Error stopping consumer: {e}")
    
    async def publish_to_kafka(self, topic: str, event: Event):
        """Publish event to Kafka topic"""
        if not self.enabled or not self.producer:
            return
            
        try:
            await self.producer.send(topic, event.to_dict())
            logger.debug(f"Published event {event.event_id} to Kafka topic {topic}")
        except Exception as e:
            logger.error(f"Failed to publish to Kafka: {e}")
    
    async def _consume_loop(self):
        """Consumer loop to forward Kafka events to event bus"""
        if not self.consumer:
            return
            
        logger.info("Starting Kafka consumer loop")
        
        try:
            async for msg in self.consumer:
                if not self.running:
                    break
                    
                try:
                    event_data = msg.value
                    event = Event(**event_data)
                    
                    # Forward to event bus for WebSocket/SSE distribution
                    await BUS.publish(event)
                    
                    logger.debug(f"Forwarded Kafka event {event.event_id} to event bus")
                    
                except Exception as e:
                    logger.error(f"Error processing Kafka message: {e}")
                    
        except Exception as e:
            logger.error(f"Kafka consumer loop error: {e}")
        finally:
            logger.info("Kafka consumer loop ended")
    
    async def handle_page_generated(self, event: Event):
        """Handle page generated events - publish to Kafka and local bus"""
        # Always publish to local bus for WebSocket/SSE
        await BUS.publish(event)
        
        # Also publish to Kafka if enabled
        if self.enabled:
            await self.publish_to_kafka(self.topics["page_done"], event)
    
    async def handle_symbol_interaction(self, event: Event):
        """Handle symbol interaction events"""
        # Publish to local bus
        await BUS.publish(event)
        
        # Also publish to Kafka if enabled  
        if self.enabled:
            await self.publish_to_kafka(self.topics["ui_symbol"], event)
    
    async def request_page_generation(self, session_id: str, symbol_code: int, user_intent: str = ""):
        """Request page generation via Kafka (for worker architecture)"""
        if not self.enabled:
            logger.debug("Kafka disabled - page generation requests handled locally")
            return
            
        request_event = make_event(
            "gibsey.generate.page.request",
            session_id,
            {
                "symbol_code": symbol_code,
                "user_intent": user_intent,
                "request_id": f"req-{symbol_code:02x}-{session_id}"
            }
        )
        
        await self.publish_to_kafka(self.topics["page_request"], request_event)
        logger.info(f"Requested page generation via Kafka: session={session_id}, symbol={symbol_code}")

# Global bridge instance
BRIDGE = KafkaBridge()

# Enhanced event publishing functions that use the bridge
async def publish_page_generated_with_kafka(session_id: str, page_data: Dict[str, Any]):
    """Publish page generated event via bridge (Kafka + local bus)"""
    event = make_event("gibsey.generate.page.done", session_id, page_data)
    await BRIDGE.handle_page_generated(event)

async def publish_symbol_interaction_with_kafka(session_id: str, symbol_code: int, action: str):
    """Publish symbol interaction event via bridge"""
    payload = {
        "symbol_code": symbol_code,
        "action": action,
        "char_hex": (symbol_code >> 4) & 0xF,
        "behavior": symbol_code & 0xF
    }
    event = make_event("gibsey.ui.symbol", session_id, payload)
    await BRIDGE.handle_symbol_interaction(event)