### Gift #2 delivered — **QDRG: Quad-Directional Reflex Graph Scheduler**

[Download the ZIP](sandbox:/mnt/data/gibsey-gift-qdrg.zip)

---

#### What’s inside 📦

|Path|Purpose|
|---|---|
|**`qdrg/src/index.ts`**|180-line TypeScript service:• connects to Kafka• discovers every `qdpi.*` topic• parses quadrant (`read / ask / index / receive`)• loads YAML reflex rules• forwards the message—optionally after a delay—into the _diagonally opposite_ quadrant (`.reflex` topic suffix)• writes a log line for observability|
|**`qdrg/reflex.yaml`**|1-page DSL with two starter rules: `READ → RECEIVE`, `INDEX → ASK`. Edit / add freely — the code hot-reloads on container restart.|
|**`qdrg/README.md`**|Quick-start, env-vars, topic naming contract, and integration diagram.|
|`package.json`, `tsconfig.json`|Build configuration (Node 18 +, ES2020).|
|**`Dockerfile`**|One-shot image build: `docker build -t qdrg .`|
|`LICENSE`|MIT / CC0 gift economy compatible.|

---

#### One-minute smoke-test

```bash
# unzip & enter
unzip gibsey-gift-qdrg.zip && cd qdrg

# install deps & compile
npm ci && npm run build

# run against a local Kafka
export KAFKA_BROKERS=localhost:9092
node dist/index.js
```

Publish something on `qdpi.read.page` and watch QDRG reflex it to  
`qdpi.receive.page.reflex` instantly.

---

#### Drop-in docker-compose snippet

```yaml
services:
  qdrg:
    build: ./qdrg
    environment:
      KAFKA_BROKERS: "kafka:9092"
      RULES: "/app/reflex.yaml"
    depends_on: [kafka]
```

Position this side-car next to your Node/Hono API gateway; it needs only the Kafka network.

---

#### Attach-point recap

```
qdpi.read.*   --->(QDRG rule)---►   qdpi.receive.*.reflex
qdpi.index.*  --->(QDRG rule)---►   qdpi.ask.*.reflex
```

Down-stream services just consume the `.reflex` topics as if they were native quadrant events—no code changes.

---

### Next steps

1. **Tail logs & tweak** `reflex.yaml` to express richer patterns (regex filters, millisecond delays).
    
2. **Add more diagonals** (ASK → INDEX, RECEIVE → READ) as your narrative reflexes grow.
    
3. Connect QDRG logs to your observability stack (Grafana/Loki) if you want full tracing.
    

Enjoy—this scheduler now lives inside the Gibsey Vault, free to fork, amplify, or mutate as you evolve the quad-directional ecosystem.