"""Kafka producers and consumers for QDPI event processing"""

import os
import json
import asyncio
import logging
from typing import Optional, Dict, Any
from datetime import datetime
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from aiokafka.errors import KafkaError

# Configure logging
logger = logging.getLogger(__name__)

# Kafka configuration
KAFKA_ENABLED = os.getenv("KAFKA_ENABLED", "false").lower() == "true"
KAFKA_BROKERS = os.getenv("KAFKA_BROKERS", "localhost:9092").split(",")

# Topic names
TOPIC_PAGE_REQUEST = "gibsey.generate.page.request"
TOPIC_PAGE_DONE = "gibsey.generate.page.done"
TOPIC_SYMBOL_EVENT = "gibsey.ui.symbol"

class KafkaEventProducer:
    """Async Kafka producer for QDPI events"""
    
    def __init__(self):
        self.producer: Optional[AIOKafkaProducer] = None
        self.enabled = KAFKA_ENABLED
        
    async def start(self):
        """Start the Kafka producer"""
        if not self.enabled:
            logger.info("Kafka disabled - using mock producer")
            return
            
        try:
            self.producer = AIOKafkaProducer(
                bootstrap_servers=KAFKA_BROKERS,
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
            await self.producer.start()
            logger.info(f"Kafka producer started: {KAFKA_BROKERS}")
        except Exception as e:
            logger.error(f"Failed to start Kafka producer: {e}")
            self.enabled = False
    
    async def stop(self):
        """Stop the Kafka producer"""
        if self.producer:
            await self.producer.stop()
            logger.info("Kafka producer stopped")
    
    async def emit_page_request(self, session_id: str, symbol_code: int, user_intent: str = ""):
        """Emit a page generation request event"""
        event = {
            "event_type": "page_request",
            "session_id": session_id,
            "symbol_code": symbol_code,
            "user_intent": user_intent,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        if self.enabled and self.producer:
            try:
                await self.producer.send(TOPIC_PAGE_REQUEST, event)
                logger.info(f"Emitted page request: {session_id} / symbol {symbol_code}")
            except Exception as e:
                logger.error(f"Failed to emit page request: {e}")
        else:
            logger.debug(f"[MOCK] Page request: {event}")
    
    async def emit_page_done(self, session_id: str, page_id: str, result: Dict[str, Any]):
        """Emit a page generation completion event"""
        event = {
            "event_type": "page_done",
            "session_id": session_id,
            "page_id": page_id,
            "symbol": result.get("symbol"),
            "trajectory": result.get("trajectory"),
            "timestamp": datetime.utcnow().isoformat()
        }
        
        if self.enabled and self.producer:
            try:
                await self.producer.send(TOPIC_PAGE_DONE, event)
                logger.info(f"Emitted page done: {session_id} / {page_id}")
            except Exception as e:
                logger.error(f"Failed to emit page done: {e}")
        else:
            logger.debug(f"[MOCK] Page done: {event}")
    
    async def emit_symbol_event(self, user_id: str, symbol_code: int, action: str):
        """Emit a UI symbol interaction event"""
        event = {
            "event_type": "symbol_interaction",
            "user_id": user_id,
            "symbol_code": symbol_code,
            "action": action,  # click, hover, etc.
            "timestamp": datetime.utcnow().isoformat()
        }
        
        if self.enabled and self.producer:
            try:
                await self.producer.send(TOPIC_SYMBOL_EVENT, event)
            except Exception as e:
                logger.error(f"Failed to emit symbol event: {e}")
        else:
            logger.debug(f"[MOCK] Symbol event: {event}")

class KafkaPageWorker:
    """Consumer worker for processing page generation requests"""
    
    def __init__(self, qdpi_program):
        self.consumer: Optional[AIOKafkaConsumer] = None
        self.producer = KafkaEventProducer()
        self.qdpi_program = qdpi_program
        self.enabled = KAFKA_ENABLED
        self.running = False
        
    async def start(self):
        """Start the consumer worker"""
        if not self.enabled:
            logger.info("Kafka disabled - page worker not starting")
            return
            
        try:
            # Start producer for emitting completion events
            await self.producer.start()
            
            # Start consumer
            self.consumer = AIOKafkaConsumer(
                TOPIC_PAGE_REQUEST,
                bootstrap_servers=KAFKA_BROKERS,
                group_id="qdpi-page-workers",
                value_deserializer=lambda v: json.loads(v.decode('utf-8'))
            )
            await self.consumer.start()
            
            self.running = True
            logger.info(f"Kafka page worker started on topic: {TOPIC_PAGE_REQUEST}")
            
            # Start processing loop
            asyncio.create_task(self._process_loop())
            
        except Exception as e:
            logger.error(f"Failed to start page worker: {e}")
            self.enabled = False
    
    async def stop(self):
        """Stop the consumer worker"""
        self.running = False
        
        if self.consumer:
            await self.consumer.stop()
            logger.info("Kafka consumer stopped")
            
        await self.producer.stop()
    
    async def _process_loop(self):
        """Main processing loop"""
        if not self.consumer:
            return
            
        async for msg in self.consumer:
            if not self.running:
                break
                
            try:
                event = msg.value
                logger.info(f"Processing page request: {event}")
                
                # Execute QDPI pipeline
                result = await self._process_page_request(event)
                
                # Emit completion event
                await self.producer.emit_page_done(
                    session_id=event["session_id"],
                    page_id=result.get("page_id", "unknown"),
                    result=result
                )
                
            except Exception as e:
                logger.error(f"Error processing message: {e}")
    
    async def _process_page_request(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Process a single page request"""
        try:
            # Execute QDPI program
            result = self.qdpi_program.forward(
                symbol_code=event["symbol_code"],
                user_intent=event.get("user_intent", "")
            )
            
            # Convert to dict and add page_id
            result_dict = result.to_dict()
            result_dict["page_id"] = f"gen-{event['session_id']}-{event['symbol_code']:03d}"
            
            return result_dict
            
        except Exception as e:
            logger.error(f"QDPI execution failed: {e}")
            return {
                "error": str(e),
                "symbol_code": event["symbol_code"]
            }

# Singleton instances
_producer: Optional[KafkaEventProducer] = None

async def get_kafka_producer() -> KafkaEventProducer:
    """Get or create the singleton Kafka producer"""
    global _producer
    if _producer is None:
        _producer = KafkaEventProducer()
        await _producer.start()
    return _producer