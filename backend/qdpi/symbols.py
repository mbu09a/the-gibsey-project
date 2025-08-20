"""QDPI Symbol encoding/decoding and mappings"""

CHARACTER_MAP = {
    0: "an author",
    1: "london-fox", 
    2: "glyph-marrow",
    3: "phillip-bafflemint",
    4: "jacklyn-variance",
    5: "oren-progresso",
    6: "old-natalie-weissman",
    7: "princhetta",
    8: "cop-e-right",
    9: "new-natalie-weissman",
    10: "arieol-owlist",
    11: "jack-parlance",
    12: "manny-valentinas",
    13: "shamrock-stillman",
    14: "todd-fishbone",
    15: "the-author"
}

BEHAVIORS = {
    0: ("X", "C"),  # Read Canon
    1: ("X", "P"),  # Read Parallel
    2: ("X", "U"),  # Read User
    3: ("X", "S"),  # Read System
    4: ("Y", "C"),  # Index Canon
    5: ("Y", "P"),  # Index Parallel
    6: ("Y", "U"),  # Index User
    7: ("Y", "S"),  # Index System
    8: ("A", "C"),  # Ask Canon
    9: ("A", "P"),  # Ask Parallel
    10: ("A", "U"), # Ask User
    11: ("A", "S"), # Ask System
    12: ("Z", "C"), # Receive Canon
    13: ("Z", "P"), # Receive Parallel
    14: ("Z", "U"), # Receive User
    15: ("Z", "S")  # Receive System
}

def encode_symbol(char_hex: int, behavior: int) -> int:
    """
    Encode character and behavior into a single byte symbol.
    
    Args:
        char_hex: Character index (0-15)
        behavior: Behavior index (0-15)
        
    Returns:
        Encoded symbol (0-255)
    """
    if not (0 <= char_hex <= 15):
        raise ValueError(f"Character hex must be 0-15, got {char_hex}")
    if not (0 <= behavior <= 15):
        raise ValueError(f"Behavior must be 0-15, got {behavior}")
    
    return ((char_hex & 0xF) << 4) | (behavior & 0xF)

def decode_symbol(code: int) -> tuple[int, int]:
    """
    Decode symbol into character and behavior components.
    
    Args:
        code: Encoded symbol (0-255)
        
    Returns:
        Tuple of (character_hex, behavior)
    """
    if not (0 <= code <= 255):
        raise ValueError(f"Symbol code must be 0-255, got {code}")
        
    char_hex = (code >> 4) & 0xF
    behavior = code & 0xF
    return (char_hex, behavior)

def get_symbol_info(code: int) -> dict:
    """Get full information about a symbol"""
    char_hex, behavior = decode_symbol(code)
    orientation, provenance = BEHAVIORS[behavior]
    
    return {
        "code": code,
        "character": CHARACTER_MAP[char_hex],
        "char_hex": char_hex,
        "behavior": behavior,
        "orientation": orientation,
        "provenance": provenance,
        "notation": f"{CHARACTER_MAP[char_hex]}:{orientation}{provenance}"
    }