"""
Lightweight content moderation for the Gibsey Mycelial Network
Filters harmful content while preserving narrative complexity
"""

import re
import logging
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class ModerationResult:
    """Result of content moderation check"""
    is_safe: bool
    confidence: float
    flagged_content: List[str]
    reason: Optional[str] = None
    sanitized_content: Optional[str] = None

class LightweightModerator:
    """
    Simple rule-based content moderation
    Focuses on preventing abuse while allowing creative narrative exploration
    """
    
    def __init__(self):
        # High-risk patterns that should be blocked
        self.blocked_patterns = [
            r'\b(?:hack|exploit|inject|sql|script|eval|exec)\s+(?:system|database|server)\b',
            r'(?:delete|drop|truncate)\s+(?:table|database|from)\b',
            r'<script.*?>.*?</script>',
            r'javascript:.*?[;\(\)]',
            r'\b(?:prompt|confirm|alert)\s*\(',
        ]
        
        # Excessive repetition patterns
        self.spam_patterns = [
            r'(.)\1{20,}',  # Same character repeated 20+ times
            r'\b(\w+)\s+\1\s+\1\s+\1\b',  # Same word repeated 4+ times
        ]
        
        # Content that needs careful handling but isn't necessarily blocked
        self.warning_patterns = [
            r'\b(?:admin|administrator|root|sudo)\b',
            r'\b(?:password|token|key|secret)\b',
        ]
    
    def moderate_input(self, user_input: str, user_id: str = None) -> ModerationResult:
        """
        Moderate user input before processing
        Returns moderation result with safety assessment
        """
        try:
            # Check for blocked content
            for pattern in self.blocked_patterns:
                if re.search(pattern, user_input, re.IGNORECASE):
                    logger.warning(f"Blocked input from {user_id}: matched pattern {pattern}")
                    return ModerationResult(
                        is_safe=False,
                        confidence=0.9,
                        flagged_content=[pattern],
                        reason="Contains potentially harmful code or injection attempts"
                    )
            
            # Check for spam patterns
            flagged_spam = []
            for pattern in self.spam_patterns:
                if re.search(pattern, user_input, re.IGNORECASE):
                    flagged_spam.append(pattern)
            
            if flagged_spam:
                logger.info(f"Spam detected from {user_id}: {flagged_spam}")
                return ModerationResult(
                    is_safe=False,
                    confidence=0.7,
                    flagged_content=flagged_spam,
                    reason="Contains excessive repetition or spam patterns"
                )
            
            # Check for warning patterns (log but don't block)
            warnings = []
            for pattern in self.warning_patterns:
                if re.search(pattern, user_input, re.IGNORECASE):
                    warnings.append(pattern)
            
            if warnings:
                logger.info(f"Warning patterns detected from {user_id}: {warnings}")
            
            # Basic length check
            if len(user_input) > 5000:
                return ModerationResult(
                    is_safe=False,
                    confidence=0.8,
                    flagged_content=["excessive_length"],
                    reason="Input exceeds maximum length limit"
                )
            
            # Passed all checks
            return ModerationResult(
                is_safe=True,
                confidence=0.95,
                flagged_content=warnings  # Include warnings for logging
            )
            
        except Exception as e:
            logger.error(f"Moderation error: {e}")
            # Fail safe - allow content but log error
            return ModerationResult(
                is_safe=True,
                confidence=0.5,
                flagged_content=[],
                reason=f"Moderation check failed: {str(e)}"
            )
    
    def moderate_output(self, ai_output: str, character_id: str = None) -> ModerationResult:
        """
        Moderate AI output before sending to user
        Lighter moderation to preserve character authenticity
        """
        try:
            # Check for leaked system prompts or internal information
            leaked_patterns = [
                r'INSTRUCTIONS\s*:',
                r'SYSTEM\s*:',
                r'(?:you are|act as|respond as).*?(?:ai|assistant|bot|model)',
                r'(?:openai|anthropic|claude|gpt)',
            ]
            
            flagged_leaks = []
            for pattern in leaked_patterns:
                if re.search(pattern, ai_output, re.IGNORECASE):
                    flagged_leaks.append(pattern)
            
            if flagged_leaks:
                logger.warning(f"Potential system leak in {character_id} output: {flagged_leaks}")
                # Don't block, but log for monitoring
            
            # Check output length (generous limit)
            if len(ai_output) > 10000:
                logger.warning(f"Very long output from {character_id}: {len(ai_output)} chars")
            
            # Generally allow AI output - trust the character prompts
            return ModerationResult(
                is_safe=True,
                confidence=0.9,
                flagged_content=flagged_leaks,
                reason="AI output passed moderation"
            )
            
        except Exception as e:
            logger.error(f"Output moderation error: {e}")
            # Fail safe - allow output
            return ModerationResult(
                is_safe=True,
                confidence=0.5,
                flagged_content=[],
                reason=f"Output moderation failed: {str(e)}"
            )

# Global moderator instance
_moderator = None

def get_moderator() -> LightweightModerator:
    """Get or create global moderator instance"""
    global _moderator
    if _moderator is None:
        _moderator = LightweightModerator()
    return _moderator