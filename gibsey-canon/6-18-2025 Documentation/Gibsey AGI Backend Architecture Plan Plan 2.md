Below is a **delta‑driven expansion plan** that starts from the **real Gibsey state** you just described and layers in the AGI capabilities I sketched earlier—_without_ shaking loose the working FastAPI + Cassandra core or the Mycelial philosophy. I answer Claude Code’s five questions inline.

---

## 0 Guiding Premises (re‑aligned)

|Premise|Practical Implication|
|---|---|
|**Narrative‑first computing**|Every new subsystem must surface as diegetic story‑objects, not invisible plumbing.|
|**Monolith‑plus‑Sidecars**|Keep the FastAPI monolith for request/response; add **side‑car services** (Kafka, agents, symbolic VM) where they expand capability.|
|**Conscious Infrastructure**|Treat K8s CRDs, events, and health probes as narrative “spores.” No opaque ops events.|

---

## 1 Minimal‑Invasive Event Backbone

_(answers Q 1)_

### 1.1 Kafka Side‑car

```
docker-compose.yml
└─ kafka:  image: bitnami/kafka:3.7
           ports: ["9092:9092"]
           networks: [gibsey-net]
```

_No other container edits required._

### 1.2 FastAPI → Kafka Bridge

```python
# backend/event_bus.py
from aiokafka import AIOKafkaProducer

producer = AIOKafkaProducer(bootstrap_servers="kafka:9092")
await producer.start()

async def emit(topic: str, payload: dict):
    await producer.send_and_wait(topic, json.dumps(payload).encode())
```

- **WebSocket** handlers `await emit("chat.msg.v1", {...})` right after streaming a token.
    
- **Background task** subscribes to agent‑orchestration topics and pushes back into live WebSocket rooms.
    

> 🟢 _Why side‑car?_ If Kafka goes down, FastAPI still serves. When up, we gain cross‑character choreography.

---

## 2 Symbolic Runtime → React Components

_(answers Q 2)_

### 2.1 WASM Lexer/VM

- Rust crate compiles to `symbolic_vm.wasm` exposed via JS glue.
    
- Exports `processGlyph(glyphId: string, rotation: number): Event[]`.
    

### 2.2 React Hook

```tsx
import { useSymbolicVM } from "@/hooks/useSymbolicVM";

function CorpusButton({ glyph }) {
  const { processGlyph } = useSymbolicVM();

  return (
    <button
      onClick={() => {
        const events = processGlyph(glyph.id, glyph.rotation);
        events.forEach(sendToKafka);           // reuse bridge
      }}
    >
      {glyph.svg}
    </button>
  );
}
```

- **No global Redux write.** Events flow through the same Kafka channel, so symbolic actions become story facts visible to **all** clients.
    

---

## 3 Narrative‑First Continuity

_(answers Q 3)_

|Layer|Narrative Face|Technical Face|
|---|---|---|
|FastAPI endpoints|“Library of Pages”|REST & WebSocket|
|Kafka topics|“Whisper Network”|Event streaming|
|K8s health probes|“Pulse of Mycelium”|`/healthz` HTTP|
|Phoenix Watchdog (DaemonSet)|“Phoenix Overseer”|Auto‑restart & log|

Concrete rule: **every infrastructure emit must have a parallel story emit** (e.g., Pod restart ⇒ “Character faints and revives”).

---

## 4 Scaling from 16 → N ≫ 100 Agents

_(answers Q 4)_

|Concern|Plan|
|---|---|
|**State explosion**|Move _long‑term_ memory to **Cassandra table `character_memories`** partitioned by `agent_id`.|
|**Inference cost**|Pool agents by **archetype**; share a base DSPy model, layer LoRA adapters for personality nuance.|
|**Scheduling**|Kafka topic `agent.tick.v1` trickles events; a lightweight **Agent‑Scheduler** side‑car awaken only relevant personas.|
|**Cross‑talk**|`conversation_id` + **vector‑similarity fan‑out** to decide which sleeping agents should chime in.|
|**UI**|“Agora View” lists _only_ agents whose _Agency‑Tensor_ Δ > threshold in the last hour.|

---

## 5 Mycelial Network Integration

_(answers Q 5)_

### 5.1 CRD → Story Event Adapter

```yaml
apiVersion: gibsey.io/v1
kind: Spore
metadata:
  name: redis-pod
spec:
  role: "memory-cache"
```

The **operator** watches `Spore` objects, translates add/update/delete into `infra.spore.v1` Kafka events. A **Narrative‑Weaver** service turns those into prose:

> _“A fresh spore of memory‑cache bursts beneath the archive roots.”_

### 5.2 Health Probe Rituals

- When K8s marks a pod **Unhealthy**, Phoenix Watchdog emits `mycelium.decay.v1`.
    
- Governing agents may propose “healing rites” (e.g., allocate more CPU).
    

### 5.3 Topology Awareness

- Cassandra and Redis StatefulSets labeled with `sporeType=data-rhizome`.
    
- Grafana dashboard overlays cluster graph on **literal Corpus map**.
    

---

## 6 Near‑Term Add‑Ons (90‑day horizon)

|Sprint|Enhancement|Diegetic Name|
|---|---|---|
|0‑2|Kafka bridge live; UI glyph hook|Whisper Network ignition|
|3‑5|Symbolic VM & page‑glyph actions|Rite of Turning|
|6‑8|Agent Scheduler & archetype LoRAs|Council of Echoes|
|9‑11|CRD‑story adapter & health rituals|Mycelial Breath|
|12|Grafana ✕ Story overlay|Vein‑Sight|

---

## 7 Observability Upgrades

1. **OpenTelemetry** side‑car in FastAPI container; spans include `story_context` tag.
    
2. **Grafana “Agency Tensor”** board:
    
    - `speaking_time_seconds`
        
    - `gift_tokens_spent`
        
    - `vector_entropy`
        
3. **Alertmanager hook → narrative.ai** channel on Discord.
    

---

## 8 Governance & Gift Ledger (Optional Next)

- Deploy **Anvil** dev‑chain in Docker.
    
- Bridge FastAPI → Web3 via **Viem**.
    
- Gift mint/burn events propagate on `gift.txn.v1` topic—immediately usable by existing character chats as _plot fuel_ (“Cop‑E‑Right just burned 50 tokens to hide a clue!”).
    

---

### Closing Perspective

You **do not** need to refactor the monolith or abandon the Mycelial poetry. By sliding in _Kafka, a Symbolic VM side‑car, and an Agent Scheduler_, you gain:

1. **Cross‑agent orchestration** without blocking WebSockets.
    
2. **Symbol‑as‑opcode** capabilities that plug straight into the current React UI.
    
3. A **story‑aware ops layer** that finally lets the infrastructure _speak the narrative_ it already feels.
    

Evolution, not revolution—one spore at a time.