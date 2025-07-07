# QDPI-256 Canon
*The Definitive Symbol Mapping System*

## Overview

This document establishes the **canonical mapping** for the QDPI-256 system, defining how 64 symbols × 4 rotations = 256 unique glyphs map to real context, characters, systems, and operations.

**Status**: **STABLE FOUNDATION** - Do not modify without significant use case justification.

## Core Principles

1. **Every symbol has meaning** - No arbitrary assignments
2. **Rotations are universal** - 0°=Read, 90°=Ask, 180°=Index, 270°=Receive  
3. **Sequences tell stories** - Symbol chains create readable narratives
4. **Lenses provide perspective** - Same operation, different viewpoints
5. **Meta-verbs operate on flow** - Higher-order operations

## The 64-Symbol Structure

### Character Symbols (0-15): WHO + HOW
**Format**: `{character_name}: {personality} → {system_component}`

- `an_author`: Meta-Narrator → Content Management
- `london_fox`: Connection Weaver → Graph Engine  
- `glyph_marrow`: Symbol Keeper → QDPI Protocol
- `phillip_bafflemint`: UI/UX Designer → Interface Management
- `jacklyn_variance`: Data Analyst → Core Database
- `oren_progresso`: Progress Tracker → Orchestration Engine
- `old_natalie_weissman`: Memory Keeper → Memory Management
- `princhetta`: AI Orchestrator → AI Coordination
- `cop_e_right`: Security Guardian → Security & Permissions
- `new_natalie_weissman`: Innovation Lead → Research & Development
- `arieol_owlist`: Event Coordinator → Event Streaming
- `jack_parlance`: Network Specialist → Network Communications
- `manny_valentinas`: Resource Manager → Resource Allocation
- `shamrock_stillman`: Quality Assurance → Testing & Validation
- `todd_fishbone`: Deployment Specialist → Deployment Pipeline
- `The_Author`: Meta-System → System Bootstrap

### User Lenses (16-31): Audience Perspectives
**Format**: `hidden_symbol_{01-16}: {user_perspective} (mirrors {character})`

- User perspectives on how each character domain appears to users
- One-to-one mapping with character symbols
- Enables user-centric narratives

### System Lenses (32-47): Backend Perspectives  
**Format**: `hidden_symbol_{17-32}: {backend_perspective}`

- How system components see operations internally
- Backend viewpoints on character domains
- Enables system-centric narratives

### Meta-Verbs (48-63): Flow Operations
**Format**: `hidden_symbol_{33-48}: {meta_operation}`

`LINK`, `MERGE`, `SPLIT`, `FORGET`, `REMEMBER`, `GIFT`, `COST`, `VALIDATE`, `TRANSFORM`, `REPLICATE`, `OBSERVE`, `INTERRUPT`, `RESUME`, `BRANCH`, `SYNCHRONIZE`, `TERMINATE`

## The 4-Rotation System

**Universal across all 64 symbols:**

- **0° READ**: Observe/inspect current state
- **90° ASK**: Request information or action  
- **180° INDEX**: Store/catalog for future retrieval
- **270° RECEIVE**: Accept/process incoming data

## Symbol Sequence Grammar

### Basic Pattern
`{symbol}@{rotation}° → {symbol}@{rotation}° → ...`

### Example Translations
- `london_fox@90°` = "Ask Graph Engine to act"
- `hidden_symbol_05@0°` = "Read Data Explorer perspective"  
- `VALIDATE@270°` = "Validation operation completes"

### Flow Patterns
1. **Character Actions**: `character@90°` (ask character to act)
2. **State Inspection**: `character@0°` (check current state)
3. **Data Storage**: `character@180°` (index for later)
4. **Processing**: `character@270°` (receive/process)

## Real-World Example

**System Flow**: User requests data analysis with security validation

**Symbol Sequence**:
```
cop_e_right@90° → hidden_symbol_09@270° → VALIDATE@0° → 
jacklyn_variance@90° → hidden_symbol_05@0° → LINK@180° → 
phillip_bafflemint@270°
```

**Plain English**:
"Ask Security Guardian, Security Participant receives, read validation, ask Data Analyst, read Data Explorer perspective, index the connection, Interface receives result"

**Technical Meaning**: 
User requests data → Security validates → Database queries → Results linked → UI displays

## Implementation Status

- ✅ **256 SVG symbols generated and validated**
- ✅ **QDPI.py encoding/decoding operational**  
- ✅ **SREC semantic embedding system working**
- ✅ **Character-system fusion validated (100% test success)**
- ✅ **Symbol mapping documented and canonized**
- 🔄 **Reed-Solomon error correction** (in progress)

## Usage Guidelines

### DO:
- Use this mapping as the foundation for all QDPI development
- Build symbol sequences that tell coherent stories
- Extend with new lenses/verbs only when clear use case exists
- Preserve the character→system component mappings

### DON'T:
- Modify core 64-symbol assignments without major justification
- Break the 4-rotation pattern
- Create sequences that don't translate to readable English
- Add complexity without clear narrative purpose

## Extension Path

When genuine need arises, new dimensions can be added:
- **Temporal lenses**: Past/Present/Future perspectives
- **Scope verbs**: Local/Global operations  
- **Modal verbs**: Possibility/Necessity operations
- **Emotional verbs**: Joy/Fear/Surprise operations

But **not until we have a proven use case** that this 64-symbol foundation cannot handle.

---

**This canon provides the stable foundation for all QDPI-256 development. Symbol meanings are now fixed and meaningful. Error correction will protect these semantic sequences. The visual programming language is ready for real-world use.**