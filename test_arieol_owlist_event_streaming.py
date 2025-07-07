"""
Test Suite for Arieol Owlist Event Streaming System
Validates character-system fusion and temporal manipulation capabilities
"""

import pytest
import asyncio
from datetime import datetime, timedelta
from backend.app.arieol_owlist_event_streaming import (
    ArieolOwlistEventSystem,
    TemporalEvent,
    EventStream,
    TimeState,
    ShapeShiftMode,
    DivinationProcessor,
    TemporalAnalysisProcessor
)


class TestArieolOwlistEventStreaming:
    """Test Arieol Owlist's event streaming capabilities"""
    
    @pytest.fixture
    def arieol_system(self):
        """Create Arieol Owlist system for testing"""
        return ArieolOwlistEventSystem()
    
    @pytest.fixture
    def sample_events(self):
        """Sample events for testing"""
        return [
            {"type": "auth_event", "source": "user_auth", "user": "test_user", "action": "login"},
            {"type": "workflow_event", "source": "phillip_bafflemint", "action": "organize_ritual", "intensity": 3},
            {"type": "ai_event", "source": "princhetta", "thought_attractions": 7, "consciousness_level": 0.8},
            {"type": "error_event", "source": "glyph_marrow", "vertigo_level": 0.6, "confusion": "high"},
            {"type": "database_event", "source": "jacklyn_variance", "surveillance_type": "D.A.D.D.Y.S-H.A.R.D"}
        ]
    
    @pytest.mark.asyncio
    async def test_create_event_stream(self, arieol_system):
        """Test creating new event streams"""
        stream_id = "test_stream_001"
        stream = await arieol_system.create_event_stream(stream_id)
        
        assert stream.stream_id == stream_id
        assert stream.time_state == TimeState.FLOWING
        assert stream.shape_shift_mode == ShapeShiftMode.COORDINATOR
        assert len(stream.events) == 0
        assert stream_id in arieol_system.streams
    
    @pytest.mark.asyncio
    async def test_ingest_single_event(self, arieol_system, sample_events):
        """Test ingesting a single event"""
        stream_id = "test_ingest_stream"
        event_data = sample_events[0]
        
        event = await arieol_system.ingest_event(stream_id, event_data)
        
        assert event.event_type == "auth_event"
        assert event.source_system == "user_auth"
        assert event.event_id is not None
        assert isinstance(event.timestamp, datetime)
        assert event.divination_score >= 0.0
        assert stream_id in arieol_system.streams
        assert len(arieol_system.streams[stream_id].events) == 1
    
    @pytest.mark.asyncio
    async def test_ingest_multiple_events(self, arieol_system, sample_events):
        """Test ingesting multiple events"""
        stream_id = "test_multi_stream"
        
        for event_data in sample_events:
            await arieol_system.ingest_event(stream_id, event_data)
        
        stream = arieol_system.streams[stream_id]
        assert len(stream.events) == len(sample_events)
        
        # Verify event types are preserved
        event_types = [event.event_type for event in stream.events]
        expected_types = [event["type"] for event in sample_events]
        assert event_types == expected_types
    
    @pytest.mark.asyncio
    async def test_time_manipulation_pause_unpause(self, arieol_system, sample_events):
        """Test Arieol's time manipulation - pause and unpause"""
        stream_id = "test_time_stream"
        
        # Add some events
        await arieol_system.ingest_event(stream_id, sample_events[0])
        
        # Pause time
        pause_time = datetime.now()
        await arieol_system.pause_time_for_stream(stream_id, pause_time)
        
        stream = arieol_system.streams[stream_id]
        assert stream.time_state == TimeState.PAUSED
        assert stream.pause_point == pause_time
        assert arieol_system.character_state["time_manipulation_active"] == True
        
        # Add event while paused
        await arieol_system.ingest_event(stream_id, sample_events[1])
        paused_event = stream.events[-1]
        assert paused_event.time_anchor == pause_time
        
        # Unpause time
        await arieol_system.unpause_time_for_stream(stream_id)
        assert stream.time_state == TimeState.FLOWING
        assert stream.pause_point is None
    
    @pytest.mark.asyncio
    async def test_shape_shifting_processor_modes(self, arieol_system, sample_events):
        """Test Arieol's shape-shifting between processing modes"""
        stream_id = "test_shape_stream"
        
        # Start in coordinator mode
        await arieol_system.ingest_event(stream_id, sample_events[0])
        assert arieol_system.streams[stream_id].shape_shift_mode == ShapeShiftMode.COORDINATOR
        
        # Shape-shift to mystic mode
        await arieol_system.shape_shift_processor(stream_id, ShapeShiftMode.MYSTIC)
        assert arieol_system.streams[stream_id].shape_shift_mode == ShapeShiftMode.MYSTIC
        assert arieol_system.character_state["current_shape"] == ShapeShiftMode.MYSTIC
        
        # Shape-shift to analyst mode
        await arieol_system.shape_shift_processor(stream_id, ShapeShiftMode.ANALYST)
        assert arieol_system.streams[stream_id].shape_shift_mode == ShapeShiftMode.ANALYST
        assert arieol_system.character_state["current_shape"] == ShapeShiftMode.ANALYST
    
    @pytest.mark.asyncio
    async def test_divination_reading(self, arieol_system, sample_events):
        """Test Arieol's divination capabilities (every chat is a Tarot pull)"""
        stream_id = "test_divination_stream"
        
        # Add events for reading
        for event_data in sample_events[:3]:
            await arieol_system.ingest_event(stream_id, event_data)
        
        # Get divination reading
        reading = await arieol_system.get_divination_reading(stream_id, event_count=3)
        
        assert reading["divination_type"] == "temporal_tarot"
        assert "event_interpretations" in reading
        assert len(reading["event_interpretations"]) <= 3
        assert "overall_significance" in reading
        assert "temporal_advice" in reading
        assert "character_insight" in reading
        assert arieol_system.character_state["divination_insights_count"] > 0
    
    @pytest.mark.asyncio
    async def test_temporal_anomaly_detection(self, arieol_system):
        """Test detection of temporal anomalies"""
        stream_id = "test_anomaly_stream"
        
        # Create events with temporal issues
        base_time = datetime.now()
        
        # Normal event
        await arieol_system.ingest_event(stream_id, {
            "type": "normal_event", 
            "source": "test"
        })
        
        # Manually create event with past timestamp (temporal reversal)
        past_event = TemporalEvent(
            event_id="past_event",
            timestamp=base_time - timedelta(hours=1),  # Earlier than previous
            event_type="anomaly_event",
            source_system="test",
            data={"anomaly": True}
        )
        arieol_system.streams[stream_id].events.append(past_event)
        
        # Detect anomalies
        anomalies = await arieol_system.detect_temporal_anomalies(stream_id)
        
        assert len(anomalies) > 0
        assert any(a["type"] == "temporal_reversal" for a in anomalies)
        assert arieol_system.character_state["temporal_anomalies_detected"] > 0
    
    @pytest.mark.asyncio
    async def test_process_events_mystic_mode(self, arieol_system, sample_events):
        """Test processing events in mystic mode (divination)"""
        stream_id = "test_mystic_processing"
        
        # Create stream first, then set up mystic mode processing
        await arieol_system.create_event_stream(stream_id)
        await arieol_system.shape_shift_processor(stream_id, ShapeShiftMode.MYSTIC)
        
        # Add events
        for event_data in sample_events[:2]:
            await arieol_system.ingest_event(stream_id, event_data)
        
        # Process events
        results = await arieol_system.process_events_in_stream(stream_id)
        
        assert len(results) == 2
        for result in results:
            assert "divination_reading" in result
            assert "temporal_significance" in result
            assert "shape_shift_insight" in result
            assert result["character_context"] == "arieol_owlist_temporal_processing"
    
    @pytest.mark.asyncio
    async def test_process_events_analyst_mode(self, arieol_system, sample_events):
        """Test processing events in analyst mode (temporal analysis)"""
        stream_id = "test_analyst_processing"
        
        # Create stream first, then set up analyst mode processing
        await arieol_system.create_event_stream(stream_id)
        await arieol_system.shape_shift_processor(stream_id, ShapeShiftMode.ANALYST)
        
        # Add events
        for event_data in sample_events[:2]:
            await arieol_system.ingest_event(stream_id, event_data)
        
        # Process events
        results = await arieol_system.process_events_in_stream(stream_id)
        
        assert len(results) == 2
        for result in results:
            assert "temporal_analysis" in result
            assert "time_distortion_level" in result
            assert "slider_position" in result
            assert result["shape_shift_mode"] == "temporal_analysis"
    
    @pytest.mark.asyncio
    async def test_character_consciousness_state(self, arieol_system, sample_events):
        """Test getting Arieol's character consciousness state"""
        stream_id = "test_consciousness_stream"
        
        # Add some events and manipulate time
        for event_data in sample_events:
            await arieol_system.ingest_event(stream_id, event_data)
        
        await arieol_system.pause_time_for_stream(stream_id)
        await arieol_system.get_divination_reading(stream_id)
        
        consciousness = await arieol_system.get_character_consciousness_state()
        
        assert consciousness["character_name"] == "arieol_owlist"
        assert consciousness["system_function"] == "event_streaming_processing"
        assert "character_state" in consciousness
        assert "temporal_overview" in consciousness
        assert "shape_shifting_status" in consciousness
        assert "mystical_insights" in consciousness
        
        # Verify temporal capabilities
        temporal = consciousness["temporal_overview"]
        assert temporal["total_streams"] >= 1
        assert temporal["paused_streams"] >= 1
        assert temporal["total_events_processed"] >= len(sample_events)
        assert temporal["time_manipulation_capability"] == "active"
    
    @pytest.mark.asyncio
    async def test_qdpi_integration_creation(self):
        """Test creating Arieol system for QDPI integration"""
        from backend.app.arieol_owlist_event_streaming import create_arieol_qdpi_integration
        
        arieol_system = await create_arieol_qdpi_integration()
        
        assert isinstance(arieol_system, ArieolOwlistEventSystem)
        assert "qdpi_main_stream" in arieol_system.streams
        assert arieol_system.streams["qdpi_main_stream"].shape_shift_mode == ShapeShiftMode.COORDINATOR


class TestDivinationProcessor:
    """Test the divination processor specifically"""
    
    @pytest.fixture
    def divination_processor(self):
        return DivinationProcessor()
    
    @pytest.fixture
    def sample_event(self):
        return TemporalEvent(
            event_id="test_event",
            timestamp=datetime.now(),
            event_type="auth_event",
            source_system="test",
            data={"user": "test_user"}
        )
    
    @pytest.mark.asyncio
    async def test_divination_event_processing(self, divination_processor, sample_event):
        """Test divination processing of events"""
        result = await divination_processor.process_event(sample_event)
        
        assert "divination_reading" in result
        assert "temporal_significance" in result
        assert "shape_shift_insight" in result
        assert "The Fool" in result["divination_reading"]  # auth_event maps to The Fool
    
    def test_divination_score_calculation(self, divination_processor, sample_event):
        """Test divination score calculation"""
        score = divination_processor.get_divination_score(sample_event)
        
        assert 0.0 <= score <= 1.0
        assert isinstance(score, float)
    
    def test_tarot_mappings_coverage(self, divination_processor):
        """Test that all major event types have Tarot mappings"""
        mappings = divination_processor.TAROT_MAPPINGS
        
        expected_types = ["auth_event", "error_event", "success_event", "workflow_event", "database_event", "ai_event"]
        for event_type in expected_types:
            assert event_type in mappings
            assert " - " in mappings[event_type]  # Format: "Card - Meaning"


class TestTemporalAnalysisProcessor:
    """Test the temporal analysis processor"""
    
    @pytest.fixture
    def analysis_processor(self):
        return TemporalAnalysisProcessor()
    
    @pytest.fixture
    def temporal_event(self):
        return TemporalEvent(
            event_id="temporal_test",
            timestamp=datetime.now(),
            event_type="temporal_event",
            source_system="test",
            data={"temporal_data": True},
            time_anchor=datetime.now() - timedelta(minutes=30)
        )
    
    @pytest.mark.asyncio
    async def test_temporal_analysis_processing(self, analysis_processor, temporal_event):
        """Test temporal analysis of events"""
        result = await analysis_processor.process_event(temporal_event)
        
        assert "temporal_analysis" in result
        assert "time_distortion_level" in result
        assert "slider_position" in result
        assert result["shape_shift_mode"] == "temporal_analysis"
    
    def test_time_distortion_calculation(self, analysis_processor, temporal_event):
        """Test time distortion calculation"""
        distortion = analysis_processor._calculate_time_distortion(temporal_event)
        
        assert 0.0 <= distortion <= 1.0
        assert isinstance(distortion, float)
    
    def test_slider_position_calculation(self, analysis_processor, temporal_event):
        """Test time slider position calculation"""
        position = analysis_processor._get_slider_position(temporal_event)
        
        assert 0.0 <= position <= 1.0
        assert isinstance(position, float)
    
    def test_confidence_score(self, analysis_processor, temporal_event):
        """Test temporal analysis confidence"""
        score = analysis_processor.get_divination_score(temporal_event)
        
        assert score == 0.7  # High confidence in temporal patterns
        assert isinstance(score, float)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])