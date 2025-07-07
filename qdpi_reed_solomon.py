#!/usr/bin/env python3
"""
QDPI Reed-Solomon Error Correction
Implements RS(255,223) encoding to protect QDPI symbol sequences

Based on QDPI documentation:
- Corrects up to 16 byte errors per 256-glyph block
- Code rate 0.874 (223/255)
- Adds 32 parity bytes per block
- Target <4ms decode time
"""

try:
    from reedsolo import RSCodec, ReedSolomonError
except ImportError:
    print("Installing reedsolo library...")
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "reedsolo"])
    from reedsolo import RSCodec, ReedSolomonError

import time
import random
from typing import List, Tuple, Optional, Dict, Any
from dataclasses import dataclass

@dataclass
class QDPIBlock:
    """QDPI symbol block with error correction"""
    data: bytes           # Original 223 bytes of QDPI symbols
    encoded: bytes        # 255 bytes with 32 parity bytes
    block_id: int         # Block sequence number
    timestamp: float      # Encoding timestamp

class QDPIReedSolomon:
    """Reed-Solomon error correction for QDPI symbol sequences"""
    
    def __init__(self):
        # RS(255,223) - corrects up to 16 byte errors
        self.rs = RSCodec(32)  # 32 parity bytes = 16 error correction capacity
        self.data_size = 223   # Actual data bytes per block
        self.block_size = 255  # Total bytes with parity
        self.parity_size = 32  # Parity bytes
        
        # Performance tracking
        self.encode_times = []
        self.decode_times = []
        
    def encode_sequence(self, symbol_sequence: bytes, block_id: int = 0) -> QDPIBlock:
        """Encode a QDPI symbol sequence with Reed-Solomon protection"""
        
        start_time = time.time()
        
        # Pad sequence to data_size if needed
        if len(symbol_sequence) > self.data_size:
            raise ValueError(f"Sequence too long: {len(symbol_sequence)} > {self.data_size}")
        
        # Pad with zeros if sequence is shorter than block size
        padded_data = symbol_sequence + b'\x00' * (self.data_size - len(symbol_sequence))
        
        # Apply Reed-Solomon encoding
        encoded_data = self.rs.encode(padded_data)
        
        encode_time = time.time() - start_time
        self.encode_times.append(encode_time)
        
        return QDPIBlock(
            data=symbol_sequence,  # Store original unpadded data
            encoded=bytes(encoded_data),
            block_id=block_id,
            timestamp=time.time()
        )
    
    def decode_block(self, corrupted_block: bytes, original_length: int) -> Tuple[bytes, Dict[str, Any]]:
        """Decode and error-correct a QDPI block"""
        
        start_time = time.time()
        stats = {
            'errors_detected': 0,
            'errors_corrected': 0,
            'correction_successful': False,
            'correction_info': None
        }
        
        try:
            # Attempt Reed-Solomon decoding (returns tuple: corrected_data, corrected_ecc, errata)
            decode_result = self.rs.decode(corrupted_block)
            
            # Extract the corrected data (first element of tuple)
            if isinstance(decode_result, tuple):
                corrected_data = decode_result[0]  # Get the corrected data part
            else:
                corrected_data = decode_result
            
            # Extract original data (remove padding) 
            recovered_sequence = bytes(corrected_data)[:original_length]
            
            # Count differences to estimate errors corrected
            errors_corrected = sum(1 for a, b in zip(corrupted_block, self.rs.encode(corrected_data)) if a != b)
            
            # Update statistics
            stats['errors_detected'] = errors_corrected
            stats['errors_corrected'] = errors_corrected
            stats['correction_successful'] = True
            stats['correction_info'] = {
                'errors_estimated': errors_corrected
            }
            
        except ReedSolomonError as e:
            # Error correction failed
            stats['correction_successful'] = False
            stats['correction_info'] = str(e)
            recovered_sequence = corrupted_block[:original_length]  # Return uncorrected data
        
        decode_time = time.time() - start_time
        self.decode_times.append(decode_time)
        stats['decode_time_ms'] = decode_time * 1000
        
        return recovered_sequence, stats
    
    def simulate_transmission_errors(self, block: QDPIBlock, error_rate: float = 0.01) -> bytes:
        """Simulate transmission errors for testing"""
        
        corrupted = bytearray(block.encoded)
        
        # Calculate number of errors to introduce
        total_bits = len(corrupted) * 8
        num_errors = int(total_bits * error_rate)
        
        # Introduce random bit errors
        for _ in range(num_errors):
            byte_pos = random.randint(0, len(corrupted) - 1)
            bit_pos = random.randint(0, 7)
            corrupted[byte_pos] ^= (1 << bit_pos)
        
        return bytes(corrupted)
    
    def get_performance_stats(self) -> Dict[str, float]:
        """Get performance statistics"""
        
        if not self.encode_times or not self.decode_times:
            return {'encode_avg_ms': 0, 'decode_avg_ms': 0, 'total_blocks': 0}
        
        return {
            'encode_avg_ms': (sum(self.encode_times) / len(self.encode_times)) * 1000,
            'decode_avg_ms': (sum(self.decode_times) / len(self.decode_times)) * 1000,
            'encode_max_ms': max(self.encode_times) * 1000,
            'decode_max_ms': max(self.decode_times) * 1000,
            'total_blocks_encoded': len(self.encode_times),
            'total_blocks_decoded': len(self.decode_times)
        }

def test_qdpi_error_correction():
    """Test Reed-Solomon error correction with real QDPI symbol sequences"""
    
    print("🛡️ QDPI Reed-Solomon Error Correction Test")
    print("=" * 60)
    
    rs_encoder = QDPIReedSolomon()
    
    # Test sequences from our narrative experiments
    test_sequences = [
        {
            'name': 'User Login Flow',
            'sequence': bytes([33, 223, 15, 6]),  # cop_e_right@90° → VALIDATE@270° → phillip_bafflemint@270° → london_fox@180°
            'meaning': 'ASK Security → RECEIVE Validation → RECEIVE Interface → INDEX Graph'
        },
        {
            'name': 'Data Analysis Request', 
            'sequence': bytes([17, 232, 227, 15]),  # jacklyn_variance@90° → OBSERVE@0° → TRANSFORM@270° → phillip_bafflemint@270°
            'meaning': 'ASK Database → READ Observe → RECEIVE Transform → RECEIVE Interface'
        },
        {
            'name': 'AI Collaboration',
            'sequence': bytes([29, 3, 199, 10]),  # princhetta@90° → an_author@270° → MERGE@270° → glyph_marrow@180°
            'meaning': 'ASK AI → RECEIVE Content → RECEIVE Merge → INDEX Protocol'
        },
        {
            'name': 'System Bootstrap',
            'sequence': bytes([61, 251, 11, 22]),  # The_Author@90° → SYNCHRONIZE@270° → glyph_marrow@270° → oren_progresso@180°
            'meaning': 'ASK Meta-System → RECEIVE Sync → RECEIVE Protocol → INDEX Orchestration'
        }
    ]
    
    for i, test in enumerate(test_sequences, 1):
        print(f"\n## Test {i}: {test['name']}")
        print(f"**Original Sequence**: {list(test['sequence'])}")
        print(f"**Meaning**: {test['meaning']}")
        
        # Encode with Reed-Solomon
        block = rs_encoder.encode_sequence(test['sequence'], block_id=i)
        print(f"**Encoded Length**: {len(block.data)} → {len(block.encoded)} bytes (+{rs_encoder.parity_size} parity)")
        
        # Test different error rates
        error_rates = [0.0, 0.005, 0.01, 0.02]  # 0%, 0.5%, 1%, 2% bit error rates
        
        for error_rate in error_rates:
            # Simulate transmission errors
            if error_rate > 0:
                corrupted = rs_encoder.simulate_transmission_errors(block, error_rate)
                
                # Count actual byte differences
                byte_errors = sum(1 for a, b in zip(block.encoded, corrupted) if a != b)
                
                # Attempt correction
                recovered, stats = rs_encoder.decode_block(corrupted, len(test['sequence']))
                
                # Check if recovery was successful
                success = recovered == test['sequence']
                status = "✅ SUCCESS" if success else "❌ FAILED"
                
                print(f"   **{error_rate*100:0.1f}% Error Rate**: {byte_errors} byte errors → {status}")
                print(f"     Corrected: {stats['errors_corrected']}/{stats['errors_detected']} errors")
                print(f"     Decode Time: {stats['decode_time_ms']:.2f}ms")
                
                if not success:
                    print(f"     Expected: {list(test['sequence'])}")
                    print(f"     Got:      {list(recovered)}")
            else:
                # No errors - direct decode test
                recovered, stats = rs_encoder.decode_block(block.encoded, len(test['sequence']))
                success = recovered == test['sequence']
                status = "✅ SUCCESS" if success else "❌ FAILED"
                print(f"   **0.0% Error Rate**: No errors → {status}")
                print(f"     Decode Time: {stats['decode_time_ms']:.2f}ms")
    
    # Performance summary
    print(f"\n{'='*60}")
    print("📊 Performance Summary")
    print(f"{'='*60}")
    
    perf_stats = rs_encoder.get_performance_stats()
    print(f"**Average Encode Time**: {perf_stats['encode_avg_ms']:.2f}ms")
    print(f"**Average Decode Time**: {perf_stats['decode_avg_ms']:.2f}ms")
    print(f"**Max Decode Time**: {perf_stats['decode_max_ms']:.2f}ms")
    print(f"**Blocks Processed**: {perf_stats['total_blocks_encoded']} encoded, {perf_stats['total_blocks_decoded']} decoded")
    
    # Check if we meet the <4ms target
    target_met = perf_stats['decode_max_ms'] < 4.0
    target_status = "✅ TARGET MET" if target_met else "⚠️ TARGET MISSED"
    print(f"**<4ms Target**: {target_status}")

def test_narrative_protection():
    """Test how error correction protects narrative meaning"""
    
    print(f"\n{'='*60}")
    print("📖 Narrative Protection Test")
    print(f"{'='*60}")
    
    rs_encoder = QDPIReedSolomon()
    
    # Original narrative: User Login Flow
    original_sequence = bytes([33, 223, 15, 6])  # cop_e_right@90° → VALIDATE@270° → phillip_bafflemint@270° → london_fox@180°
    original_meaning = "ASK Security → RECEIVE Validation → RECEIVE Interface → INDEX Graph"
    
    print(f"**Original Narrative**: {original_meaning}")
    print(f"**Original Sequence**: {list(original_sequence)}")
    
    # Encode with protection
    block = rs_encoder.encode_sequence(original_sequence)
    
    # Introduce severe corruption (simulate worst-case transmission)
    corrupted = bytearray(block.encoded)
    
    # Corrupt specific positions to break the narrative
    corruption_positions = [0, 50, 100, 150, 200]  # Spread across the block
    print(f"\n**Introducing corruption at positions**: {corruption_positions}")
    
    for pos in corruption_positions:
        if pos < len(corrupted):
            original_byte = corrupted[pos]
            corrupted[pos] = (original_byte + 123) % 256  # Deterministic corruption
            print(f"   Position {pos}: {original_byte} → {corrupted[pos]}")
    
    # Attempt recovery
    recovered, stats = rs_encoder.decode_block(bytes(corrupted), len(original_sequence))
    
    # Check narrative preservation
    narrative_preserved = recovered == original_sequence
    
    print(f"\n**Recovery Results**:")
    print(f"   Errors Detected: {stats['errors_detected']}")
    print(f"   Errors Corrected: {stats['errors_corrected']}")
    print(f"   Recovery Time: {stats['decode_time_ms']:.2f}ms")
    print(f"   Narrative Preserved: {'✅ YES' if narrative_preserved else '❌ NO'}")
    
    if narrative_preserved:
        print(f"   **Recovered Meaning**: {original_meaning}")
        print(f"   **Recovered Sequence**: {list(recovered)}")
    else:
        print(f"   **Corrupted Sequence**: {list(recovered)}")
        print("   **Impact**: Narrative meaning would be lost!")

if __name__ == "__main__":
    test_qdpi_error_correction()
    test_narrative_protection()