#!/usr/bin/env python3
"""Test Kafka integration (mock mode)"""

import asyncio
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from workers.kafka_io import KafkaEventProducer, KafkaPageWorker
from qdpi.program import MockQDPIProgram

async def test_kafka_integration():
    """Test Kafka integration in mock mode"""
    
    print("Testing Kafka Integration (Mock Mode)...")
    
    # Initialize components
    producer = KafkaEventProducer()
    qdpi_program = MockQDPIProgram()
    worker = KafkaPageWorker(qdpi_program)
    
    # Start components
    print("Starting Kafka components...")
    await producer.start()
    await worker.start()
    
    # Test producer events
    print("\nTesting event emission...")
    await producer.emit_page_request("session-123", 0x00, "continue reading")
    await producer.emit_symbol_event("user-456", 0x4C, "click")
    
    # Simulate page completion
    mock_result = {
        "symbol": {"code": 0x00, "notation": "an author:XC"},
        "trajectory": "T0",
        "page_text": "Generated content...",
        "edges": {"next": "page-001"}
    }
    await producer.emit_page_done("session-123", "page-000", mock_result)
    
    # Test shutdown
    print("\nShutting down...")
    await worker.stop()
    await producer.stop()
    
    print("✅ Kafka integration test completed!")

if __name__ == "__main__":
    asyncio.run(test_kafka_integration())