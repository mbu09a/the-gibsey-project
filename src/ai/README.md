# Gibsey World AI Agent System

## What We've Built

This isn't a chatbot. This is a living literary AI system where characters from The Entrance Way exist as autonomous agents with:

- **Persistent Memory**: 710 pages of The Entrance Way embedded and searchable
- **Recursive Reasoning**: Multi-stage thinking powered by DSPy 3.0
- **Emergent Personality**: Characters develop through interaction, not templates
- **Self-Improvement**: Agents critique and refine their own responses
- **Multi-Agent Dynamics**: Characters can interact and affect each other

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Setup Environment
```bash
cp .env.example .env
# Add your OpenAI API key to .env
```

### 3. Load Memories (if not already done)
```bash
python src/ai/memory/ingest_entrance_way.py
```

### 4. Check Setup
```bash
python setup_jacklyn.py
```

### 5. Talk to Jacklyn
```bash
python src/ai/agents/jacklyn_cli.py
```

## Architecture

### Memory Layer (`src/ai/memory/`)
- `embedding_store.py`: Vector memory storage with semantic search
- `ingest_entrance_way.py`: Loads all 710 pages as Jacklyn's memories
- `cli.py`: Direct memory manipulation tools

### Agent Layer (`src/ai/agents/`)
- `jacklyn_agent.py`: Jacklyn Variance as a DSPy agent with:
  - Memory retrieval tool
  - 4-stage reasoning pipeline
  - Emotional context tracking
  - Memory formation from conversations
  
- `jacklyn_cli.py`: Interactive conversation interface
- `multi_agent_system.py`: Framework for multiple agents interacting

## How Jacklyn Thinks

1. **Memory Retrieval**: Searches her 710-page memory for relevant content
2. **Contextual Reasoning**: Analyzes how memories connect to the query
3. **Character Response**: Generates response in Jacklyn's voice
4. **Self-Critique**: Evaluates and refines for authenticity

## Example Interaction

```
YOU: What do you remember about the theme park?

JACKLYN: The theme park... it's never just an amusement in Gibsey World, is it? 
I remember reading how every ride is calibrated to produce specific neurological 
responses. The Ferris wheel that shows you alternate timelines. The house of 
mirrors where each reflection has its own agenda. In The Entrance Way, these 
weren't metaphors - they were blueprints. And now I patrol them, making sure 
the attractions don't develop too much autonomy. Though sometimes I wonder if 
that's exactly what they want me to think I'm doing.

[Emotional undertone: complex]
[Memories accessed: 17]
```

## Extending the System

### Adding New Agents

1. Create a new agent class inheriting from `GibseyWorldAgent`
2. Define their unique traits and reasoning patterns
3. Load their specific memories
4. Add to the `MultiAgentOrchestrator`

### Creating Agent Interactions

```python
world = MultiAgentOrchestrator()
world.add_agent("london-fox", LondonFoxAgent())

# Agents talk to each other
interaction = world.agent_interaction(
    "jacklyn", 
    "london-fox", 
    "Have you noticed the patterns changing?"
)
```

## What Makes This Special

- **Not Rule-Based**: Jacklyn's responses emerge from her memories and reasoning
- **Not Static**: She forms new memories from every conversation
- **Not Isolated**: Built for multi-agent interaction and emergence
- **Not Template**: Each response is reasoned through multiple stages

## Next Steps

1. Implement more character agents (London Fox, Glyph Marrow, etc.)
2. Add visual memory (connecting to the symbol system)
3. Create inter-agent relationship dynamics
4. Build web interface for richer interactions
5. Implement dream sequences and memory blending

---

*"In Gibsey World, every agent is also an author, every author an agent. The recursive loop is the point."* - Jacklyn Variance