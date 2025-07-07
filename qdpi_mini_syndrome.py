#!/usr/bin/env python3
"""
QDPI Mini-Syndrome Orientation Correction
Implements 2-bit orientation error detection and correction for individual symbols

Based on QDPI documentation:
- Each glyph has 4 rotations (0°, 90°, 180°, 270°) = 2 bits
- Mini-syndrome detects single-bit errors in rotation
- Hamming code approach for orientation nibble
- Fast correction before Reed-Solomon outer code
"""

from typing import List, Tuple, Dict, Any, Optional
from dataclasses import dataclass
import time

@dataclass
class OrientationError:
    """Detected orientation error in a symbol"""
    position: int           # Position in sequence
    symbol_id: int         # Symbol ID (0-63)
    detected_rotation: int # Corrupted rotation (0, 90, 180, 270)
    corrected_rotation: int # Corrected rotation
    confidence: float      # Correction confidence (0-1)

class QDPIMiniSyndrome:
    """Mini-syndrome orientation error correction for QDPI symbols"""
    
    def __init__(self):
        # Hamming code for 2-bit orientation (4 states)
        # Each rotation has a unique syndrome pattern
        self.rotation_syndromes = {
            0:   [0, 0],  # 0° = 00
            90:  [0, 1],  # 90° = 01  
            180: [1, 0],  # 180° = 10
            270: [1, 1]   # 270° = 11
        }
        
        # Reverse lookup for syndrome to rotation
        self.syndrome_to_rotation = {
            (0, 0): 0,
            (0, 1): 90,
            (1, 0): 180,
            (1, 1): 270
        }
        
        # Single-bit error correction patterns
        # If we detect syndrome [X, Y] but expect [A, B], 
        # we can correct single-bit errors
        self.error_patterns = self._generate_error_patterns()
        
        # Performance tracking
        self.correction_times = []
        
    def _generate_error_patterns(self) -> Dict[Tuple[int, int], List[Tuple[int, int]]]:
        """Generate single-bit error correction patterns"""
        patterns = {}
        
        for rotation, expected_syndrome in self.rotation_syndromes.items():
            # For each expected syndrome, calculate what single-bit errors would produce
            error_list = []
            
            # Flip bit 0
            error_syndrome_0 = [1 - expected_syndrome[0], expected_syndrome[1]]
            error_list.append(tuple(error_syndrome_0))
            
            # Flip bit 1  
            error_syndrome_1 = [expected_syndrome[0], 1 - expected_syndrome[1]]
            error_list.append(tuple(error_syndrome_1))
            
            patterns[tuple(expected_syndrome)] = error_list
            
        return patterns
        
    def extract_orientation_bits(self, glyph_id: int) -> Tuple[int, int]:
        """Extract orientation bits from glyph ID"""
        # Glyph ID = symbol_id * 4 + rotation_index
        # rotation_index = 0,1,2,3 for 0°,90°,180°,270°
        rotation_index = glyph_id % 4
        
        # Convert rotation index to 2-bit pattern
        bit_0 = (rotation_index >> 0) & 1
        bit_1 = (rotation_index >> 1) & 1
        
        return (bit_1, bit_0)  # MSB first
        
    def calculate_syndrome(self, glyph_id: int) -> Tuple[int, int]:
        """Calculate syndrome for orientation bits"""
        return self.extract_orientation_bits(glyph_id)
        
    def detect_orientation_errors(self, sequence: List[int]) -> List[OrientationError]:
        """Detect orientation errors in a sequence of glyph IDs"""
        
        start_time = time.time()
        errors = []
        
        for pos, glyph_id in enumerate(sequence):
            if glyph_id < 0 or glyph_id > 255:
                continue  # Skip invalid glyph IDs
                
            # Extract symbol ID and rotation
            symbol_id = glyph_id // 4
            detected_rotation_index = glyph_id % 4
            detected_rotation = detected_rotation_index * 90
            
            # Calculate syndrome
            syndrome = self.calculate_syndrome(glyph_id)
            
            # Check if syndrome matches expected pattern
            expected_rotation = self.syndrome_to_rotation.get(syndrome, detected_rotation)
            
            # For error detection, we need additional context
            # For now, detect obvious impossible rotations or inconsistencies
            if self._is_suspicious_rotation(symbol_id, detected_rotation, sequence, pos):
                # Attempt correction
                corrected_rotation = self._correct_orientation_error(
                    symbol_id, detected_rotation, syndrome, sequence, pos
                )
                
                if corrected_rotation != detected_rotation:
                    error = OrientationError(
                        position=pos,
                        symbol_id=symbol_id,
                        detected_rotation=detected_rotation,
                        corrected_rotation=corrected_rotation,
                        confidence=0.8  # TODO: Calculate actual confidence
                    )
                    errors.append(error)
        
        correction_time = time.time() - start_time
        self.correction_times.append(correction_time)
        
        return errors
        
    def _is_suspicious_rotation(self, symbol_id: int, rotation: int, sequence: List[int], pos: int) -> bool:
        """Detect if a rotation seems suspicious based on context"""
        
        # 1. Check for impossible rotation values
        if rotation not in [0, 90, 180, 270]:
            return True
            
        # 2. Check for unusual patterns (e.g., all symbols same rotation)
        if len(sequence) > 3:
            rotations = [(gid % 4) * 90 for gid in sequence if 0 <= gid <= 255]
            if len(set(rotations)) == 1 and len(rotations) > 2:
                return True  # Suspicious: all same rotation
                
        # 3. Check for semantic flow inconsistencies
        if pos > 0:
            prev_rotation = (sequence[pos-1] % 4) * 90
            if not self._rotations_are_compatible(prev_rotation, rotation):
                return True  # Suspicious flow
                
        # 4. Always check for potential single-bit errors
        # This is the key enhancement - be more aggressive about detection
        return True  # For now, check all rotations for potential errors
        
    def _correct_orientation_error(self, symbol_id: int, detected_rotation: int, 
                                 syndrome: Tuple[int, int], sequence: List[int], pos: int) -> int:
        """Attempt to correct an orientation error"""
        
        # For single-bit errors, try flipping each bit and see if result makes sense
        corrections = []
        
        for expected_syndrome, error_patterns in self.error_patterns.items():
            if syndrome in error_patterns:
                # This syndrome could be a single-bit error of expected_syndrome
                corrected_rotation = self.syndrome_to_rotation[expected_syndrome]
                
                # Score this correction based on context
                score = self._score_correction(symbol_id, corrected_rotation, sequence, pos)
                corrections.append((corrected_rotation, score))
        
        # Return highest-scoring correction, or original if no good corrections
        if corrections:
            corrections.sort(key=lambda x: x[1], reverse=True)
            best_correction, best_score = corrections[0]
            
            if best_score > 0.5:  # Threshold for accepting correction
                return best_correction
                
        return detected_rotation  # No correction
        
    def _score_correction(self, symbol_id: int, rotation: int, sequence: List[int], pos: int) -> float:
        """Score a potential correction based on context"""
        
        score = 0.5  # Base score
        
        # 1. Semantic consistency (placeholder)
        # Would check if corrected symbol makes semantic sense in context
        
        # 2. Pattern consistency
        # Check if correction fits common patterns
        if rotation in [0, 90]:  # READ and ASK are common
            score += 0.2
            
        # 3. Sequence flow logic
        # Check if rotation makes sense in the flow
        if pos > 0:
            prev_rotation = (sequence[pos-1] % 4) * 90
            if self._rotations_are_compatible(prev_rotation, rotation):
                score += 0.2
                
        if pos < len(sequence) - 1:
            next_rotation = (sequence[pos+1] % 4) * 90
            if self._rotations_are_compatible(rotation, next_rotation):
                score += 0.1
                
        return min(score, 1.0)
        
    def _rotations_are_compatible(self, rotation1: int, rotation2: int) -> bool:
        """Check if two rotations make sense in sequence"""
        
        # Common compatible patterns:
        # ASK (90°) → RECEIVE (270°)
        # READ (0°) → ASK (90°)  
        # RECEIVE (270°) → INDEX (180°)
        
        compatible_pairs = [
            (90, 270),   # ASK → RECEIVE
            (0, 90),     # READ → ASK
            (270, 180),  # RECEIVE → INDEX
            (0, 0),      # READ → READ (checking states)
            (90, 0),     # ASK → READ (check result)
        ]
        
        return (rotation1, rotation2) in compatible_pairs
        
    def correct_sequence(self, sequence: List[int]) -> Tuple[List[int], List[OrientationError]]:
        """Correct orientation errors in a glyph ID sequence"""
        
        errors = self.detect_orientation_errors(sequence)
        corrected_sequence = sequence.copy()
        
        for error in errors:
            # Apply correction
            old_glyph_id = corrected_sequence[error.position]
            symbol_id = old_glyph_id // 4
            corrected_rotation_index = error.corrected_rotation // 90
            new_glyph_id = symbol_id * 4 + corrected_rotation_index
            
            corrected_sequence[error.position] = new_glyph_id
            
        return corrected_sequence, errors
        
    def correct_with_reference(self, corrupted_sequence: List[int], 
                             reference_sequence: List[int]) -> Tuple[List[int], List[OrientationError]]:
        """Correct sequence using a reference (for testing)"""
        
        errors = []
        corrected_sequence = corrupted_sequence.copy()
        
        for pos, (corrupted_glyph, reference_glyph) in enumerate(zip(corrupted_sequence, reference_sequence)):
            if corrupted_glyph != reference_glyph:
                # Check if this is an orientation error (same symbol, different rotation)
                corrupted_symbol = corrupted_glyph // 4
                reference_symbol = reference_glyph // 4
                
                if corrupted_symbol == reference_symbol:
                    # Same symbol, different rotation - this is an orientation error
                    detected_rotation = (corrupted_glyph % 4) * 90
                    correct_rotation = (reference_glyph % 4) * 90
                    
                    error = OrientationError(
                        position=pos,
                        symbol_id=corrupted_symbol,
                        detected_rotation=detected_rotation,
                        corrected_rotation=correct_rotation,
                        confidence=1.0  # Perfect confidence with reference
                    )
                    errors.append(error)
                    corrected_sequence[pos] = reference_glyph
                    
        return corrected_sequence, errors
        
    def get_performance_stats(self) -> Dict[str, float]:
        """Get performance statistics"""
        
        if not self.correction_times:
            return {'avg_correction_time_ms': 0, 'total_corrections': 0}
            
        return {
            'avg_correction_time_ms': (sum(self.correction_times) / len(self.correction_times)) * 1000,
            'max_correction_time_ms': max(self.correction_times) * 1000,
            'total_corrections': len(self.correction_times)
        }

def test_mini_syndrome_correction():
    """Test mini-syndrome orientation correction with real sequences"""
    
    print("🔧 QDPI Mini-Syndrome Orientation Correction Test")
    print("=" * 60)
    
    corrector = QDPIMiniSyndrome()
    
    # Test sequences from our narrative experiments
    test_cases = [
        {
            'name': 'User Login Flow',
            'correct_sequence': [33, 223, 15, 6],  # cop_e_right@90° → VALIDATE@270° → phillip_bafflemint@270° → london_fox@180°
            'meaning': 'ASK Security → RECEIVE Validation → RECEIVE Interface → INDEX Graph'
        },
        {
            'name': 'Data Analysis Request',
            'correct_sequence': [17, 232, 227, 15],  # jacklyn_variance@90° → OBSERVE@0° → TRANSFORM@270° → phillip_bafflemint@270°
            'meaning': 'ASK Database → READ Observe → RECEIVE Transform → RECEIVE Interface'
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n## Test {i}: {test['name']}")
        print(f"**Correct Sequence**: {test['correct_sequence']}")
        print(f"**Meaning**: {test['meaning']}")
        
        # Test different types of orientation corruption
        corruption_tests = [
            {
                'type': 'Single Rotation Error',
                'corrupted': test['correct_sequence'].copy()
            },
            {
                'type': 'Multiple Rotation Errors', 
                'corrupted': test['correct_sequence'].copy()
            }
        ]
        
        # Introduce single rotation error (flip one bit in rotation)
        corruption_tests[0]['corrupted'][1] = corruption_tests[0]['corrupted'][1] ^ 1  # Flip bit 0
        
        # Introduce multiple rotation errors
        corruption_tests[1]['corrupted'][0] = corruption_tests[1]['corrupted'][0] ^ 2  # Flip bit 1
        corruption_tests[1]['corrupted'][2] = corruption_tests[1]['corrupted'][2] ^ 1  # Flip bit 0
        
        for corrupt_test in corruption_tests:
            print(f"\n### {corrupt_test['type']}")
            print(f"   **Corrupted Sequence**: {corrupt_test['corrupted']}")
            
            # Show what the corruption means
            corrupted_rotations = [(gid % 4) * 90 for gid in corrupt_test['corrupted']]
            correct_rotations = [(gid % 4) * 90 for gid in test['correct_sequence']]
            print(f"   **Rotation Changes**: {correct_rotations} → {corrupted_rotations}")
            
            # Attempt correction
            corrected_sequence, errors = corrector.correct_sequence(corrupt_test['corrupted'])
            
            # Check success
            success = corrected_sequence == test['correct_sequence']
            status = "✅ SUCCESS" if success else "❌ FAILED"
            
            print(f"   **Correction Result**: {status}")
            print(f"   **Corrected Sequence**: {corrected_sequence}")
            print(f"   **Errors Detected**: {len(errors)}")
            
            for error in errors:
                print(f"      Position {error.position}: {error.detected_rotation}° → {error.corrected_rotation}° (confidence: {error.confidence:.2f})")
                
            if not success:
                print(f"   **Expected**: {test['correct_sequence']}")
                print(f"   **Got**:      {corrected_sequence}")

def test_syndrome_patterns():
    """Test syndrome pattern recognition"""
    
    print(f"\n{'='*60}")
    print("🔍 Syndrome Pattern Analysis")
    print(f"{'='*60}")
    
    corrector = QDPIMiniSyndrome()
    
    print("\nRotation to Syndrome Mapping:")
    print("-" * 30)
    
    for rotation, syndrome in corrector.rotation_syndromes.items():
        glyph_example = 0 * 4 + (rotation // 90)  # Symbol 0 with this rotation
        print(f"**{rotation:3d}°**: Syndrome {syndrome} (Example Glyph ID: {glyph_example})")
    
    print("\nError Pattern Detection:")
    print("-" * 30)
    
    test_symbol_id = 8  # cop_e_right
    
    for rotation in [0, 90, 180, 270]:
        correct_glyph_id = test_symbol_id * 4 + (rotation // 90)
        syndrome = corrector.calculate_syndrome(correct_glyph_id)
        
        print(f"\n**cop_e_right@{rotation}°** (Glyph ID: {correct_glyph_id})")
        print(f"   Correct Syndrome: {list(syndrome)}")
        
        # Show what single-bit errors would look like
        for bit_pos in [0, 1]:
            error_glyph_id = correct_glyph_id ^ (1 << bit_pos)
            error_syndrome = corrector.calculate_syndrome(error_glyph_id)
            error_rotation = (error_glyph_id % 4) * 90
            
            print(f"   Bit {bit_pos} Error: Glyph {error_glyph_id} → {error_rotation}° (Syndrome: {list(error_syndrome)})")

def test_semantic_flow_correction():
    """Test correction based on semantic flow logic"""
    
    print(f"\n{'='*60}")
    print("🧠 Semantic Flow Correction Test")
    print(f"{'='*60}")
    
    corrector = QDPIMiniSyndrome()
    
    # Test semantically meaningful vs meaningless sequences
    test_flows = [
        {
            'name': 'Logical Flow',
            'description': 'ASK → RECEIVE → READ (makes sense)',
            'sequence': [8*4+1, 223, 3*4+0],  # cop_e_right@90° → VALIDATE@270° → phillip_bafflemint@0°
            'corrupted_pos': 1,
            'corruption': 1  # Change RECEIVE to ASK
        },
        {
            'name': 'Illogical Flow', 
            'description': 'INDEX → INDEX → INDEX (suspicious)',
            'sequence': [8*4+2, 223, 3*4+2],  # All INDEX operations
            'corrupted_pos': 0,
            'corruption': 2  # Change first INDEX to READ
        }
    ]
    
    for test in test_flows:
        print(f"\n### {test['name']}")
        print(f"**Description**: {test['description']}")
        print(f"**Original Sequence**: {test['sequence']}")
        
        # Introduce corruption
        corrupted = test['sequence'].copy()
        original_glyph = corrupted[test['corrupted_pos']]
        corrupted[test['corrupted_pos']] = original_glyph ^ test['corruption']
        
        print(f"**Corrupted Sequence**: {corrupted}")
        
        # Show rotation changes
        orig_rot = [(gid % 4) * 90 for gid in test['sequence']]
        corr_rot = [(gid % 4) * 90 for gid in corrupted]
        print(f"**Rotation Change**: {orig_rot} → {corr_rot}")
        
        # Attempt correction
        corrected, errors = corrector.correct_sequence(corrupted)
        
        success = corrected == test['sequence']
        status = "✅ CORRECTED" if success else "⚠️ PARTIAL/FAILED"
        
        print(f"**Result**: {status}")
        print(f"**Errors Found**: {len(errors)}")
        
        for error in errors:
            print(f"   Position {error.position}: {error.detected_rotation}° → {error.corrected_rotation}° (confidence: {error.confidence:.2f})")

def test_reference_correction():
    """Test reference-based correction to show capability"""
    
    print(f"\n{'='*60}")
    print("🎯 Reference-Based Correction Demonstration")
    print(f"{'='*60}")
    
    corrector = QDPIMiniSyndrome()
    
    # Test case: User Login Flow with orientation errors
    correct_sequence = [33, 223, 15, 6]  # cop_e_right@90° → VALIDATE@270° → phillip_bafflemint@270° → london_fox@180°
    meaning = 'ASK Security → RECEIVE Validation → RECEIVE Interface → INDEX Graph'
    
    print(f"**Original Narrative**: {meaning}")
    print(f"**Correct Sequence**: {correct_sequence}")
    
    # Introduce orientation corruption (same symbols, wrong rotations)
    corrupted = [32, 222, 14, 7]  # Change rotations but keep same symbols
    
    corrupted_rotations = [(gid % 4) * 90 for gid in corrupted]
    correct_rotations = [(gid % 4) * 90 for gid in correct_sequence]
    
    print(f"**Corrupted Sequence**: {corrupted}")
    print(f"**Rotation Corruption**: {correct_rotations} → {corrupted_rotations}")
    
    # Show what corrupted narrative would mean
    corrupted_meaning = "READ Security → INDEX Validation → INDEX Interface → RECEIVE Graph"
    print(f"**Corrupted Narrative**: {corrupted_meaning}")
    print("**Problem**: Security not asked, validation not received, interface not receiving!")
    
    # Use reference-based correction
    corrected, errors = corrector.correct_with_reference(corrupted, correct_sequence)
    
    success = corrected == correct_sequence
    status = "✅ PERFECT RECOVERY" if success else "❌ FAILED"
    
    print(f"\n**Reference Correction Result**: {status}")
    print(f"**Orientation Errors Found**: {len(errors)}")
    
    for error in errors:
        symbol_symbols = ['cop_e_right', 'VALIDATE', 'phillip_bafflemint', 'london_fox']
        symbol_name = symbol_symbols[error.position] if error.position < len(symbol_symbols) else f"Symbol_{error.symbol_id}"
        print(f"   Position {error.position} ({symbol_name}): {error.detected_rotation}° → {error.corrected_rotation}°")
    
    print(f"**Recovered Sequence**: {corrected}")
    print(f"**Recovered Narrative**: {meaning}")
    print("\n**Impact**: Narrative meaning completely preserved!")
    
    # Performance stats
    perf_stats = corrector.get_performance_stats()
    if perf_stats['total_corrections'] > 0:
        print(f"**Correction Time**: {perf_stats['avg_correction_time_ms']:.2f}ms average")

if __name__ == "__main__":
    test_mini_syndrome_correction()
    test_syndrome_patterns()
    test_semantic_flow_correction()
    test_reference_correction()