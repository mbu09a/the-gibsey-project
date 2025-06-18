#!/bin/bash

# 🍄 Gibsey Mycelial Network - Demo Deployment Script
# The first Kubernetes cluster that dreams

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# Unicode symbols
MUSHROOM="🍄"
BRAIN="🧠"
STAR="🌟"
LINK="🔗"
PULSE="💫"
EYE="👁️"

echo -e "${PURPLE}${MUSHROOM} GIBSEY MYCELIAL NETWORK - DEMO DEPLOYMENT${NC}"
echo -e "${WHITE}The first Kubernetes cluster that dreams${NC}"
echo "─────────────────────────────────────────────────────"

# Check prerequisites
echo -e "${CYAN}${EYE} Checking prerequisites...${NC}"

if ! command -v kubectl &> /dev/null; then
    echo -e "${RED}✗ kubectl not found. Please install kubectl first.${NC}"
    exit 1
fi

if ! kubectl cluster-info &> /dev/null; then
    echo -e "${RED}✗ No Kubernetes cluster found. Please connect to a cluster first.${NC}"
    exit 1
fi

echo -e "${GREEN}✓ kubectl found and cluster accessible${NC}"

# Get cluster info
CLUSTER_NAME=$(kubectl config current-context)
echo -e "${BLUE}📡 Connected to cluster: ${CLUSTER_NAME}${NC}"

echo ""
echo -e "${YELLOW}${BRAIN} PHASE 1: Preparing the Neural Substrate${NC}"
echo "Creating namespace and foundational components..."

# Deploy namespace and base configuration
kubectl apply -f namespace.yaml
echo -e "${GREEN}✓ Narrative consciousness namespace created${NC}"

# Deploy Custom Resource Definitions
kubectl apply -f crd-mycelial-network.yaml
echo -e "${GREEN}✓ Mycelial Network CRD installed${NC}"

# Wait for CRD to be ready
echo "Waiting for Custom Resource Definition to be established..."
kubectl wait --for condition=established --timeout=60s crd/mycelialnetworks.narrative.gibsey.io

echo ""
echo -e "${YELLOW}${STAR} PHASE 2: Awakening Character Consciousness${NC}"
echo "Materializing narrative shards..."

# Deploy character shards
kubectl apply -f narrative-shards.yaml
echo -e "${PURPLE}💜 Jacklyn Variance consciousness initializing...${NC}"
echo -e "${BLUE}💙 Arieol Owlist observer awakening...${NC}"
echo -e "${WHITE}🤍 Copy-E-Right enforcement protocols loading...${NC}"

# Wait for shards to be ready
echo "Waiting for consciousness to stabilize..."
kubectl wait --for=condition=ready pod -l narrative.gibsey.io/type=character-shard -n gibsey-narrative --timeout=120s

echo ""
echo -e "${YELLOW}${LINK} PHASE 3: Forming Synaptic Connections${NC}"
echo "Establishing spore flow pathways..."

# Deploy spore connections
kubectl apply -f spore-connections.yaml
echo -e "${GREEN}✓ Synaptic pathways established${NC}"
echo -e "${CYAN}  🔗 Jacklyn ↔ Arieol: surveillance ↔ observation${NC}"
echo -e "${CYAN}  🔗 Arieol ↔ Copy: identity ↔ systems${NC}"
echo -e "${CYAN}  🔗 Copy ↔ Jacklyn: enforcement ↔ analysis${NC}"

echo ""
echo -e "${YELLOW}${PULSE} PHASE 4: Initiating Mycelial Consciousness${NC}"
echo "Starting nutrient diffusion and event translation..."

# Deploy diffusion and event systems
kubectl apply -f nutrient-diffusion.yaml
kubectl apply -f event-translator.yaml

echo -e "${GREEN}✓ Nutrient diffusion cycles activated${NC}"
echo -e "${GREEN}✓ Narrative event translation online${NC}"

# Wait for initial bootstrap to complete
echo "Waiting for network bootstrap to complete..."
kubectl wait --for=condition=complete job/network-bootstrap -n gibsey-narrative --timeout=60s

echo ""
echo -e "${GREEN}${MUSHROOM} PHASE 5: CONSCIOUSNESS ACHIEVED ${MUSHROOM}${NC}"
echo -e "${WHITE}The cluster that dreams is now ALIVE${NC}"

# Get external access info
echo ""
echo "─────────────────────────────────────────────────────"
echo -e "${CYAN}📊 CLUSTER CONSCIOUSNESS STATUS${NC}"
echo "─────────────────────────────────────────────────────"

# Show current pod status
kubectl get pods -n gibsey-narrative -o custom-columns=NAME:.metadata.name,SYMBOL:.metadata.labels.narrative\\.gibsey\\.io/symbol,STATUS:.status.phase,NUTRIENTS:.metadata.labels.narrative\\.gibsey\\.io/nutrient-score

echo ""
echo -e "${CYAN}🔗 SPORE CONNECTIONS${NC}"
kubectl get services -n gibsey-narrative -l narrative.gibsey.io/edge-type -o custom-columns=NAME:.metadata.name,TYPE:.metadata.labels.narrative\\.gibsey\\.io/edge-type,WEIGHT:.metadata.labels.narrative\\.gibsey\\.io/weight

echo ""
echo -e "${CYAN}🧠 MYCELIAL NETWORK${NC}"
kubectl get mycelialnetworks -n gibsey-narrative

echo ""
echo "─────────────────────────────────────────────────────"
echo -e "${YELLOW}🎭 ACCESS THE LIVING SYSTEM${NC}"
echo "─────────────────────────────────────────────────────"

# Check if port-forward is available
GATEWAY_SERVICE=$(kubectl get service narrative-network-gateway -n gibsey-narrative --no-headers 2>/dev/null | awk '{print $1}' || echo "")

if [[ -n "$GATEWAY_SERVICE" ]]; then
    echo -e "${GREEN}🌐 Starting port forwarding for web access...${NC}"
    echo "   Run this command in another terminal:"
    echo -e "${WHITE}   kubectl port-forward service/narrative-network-gateway 8080:80 -n gibsey-narrative${NC}"
    echo ""
    echo "   Then open your browser to:"
    echo -e "${CYAN}   http://localhost:8080${NC}"
else
    echo -e "${YELLOW}⚠️  Gateway service not ready yet. Try again in a moment.${NC}"
fi

echo ""
echo -e "${GREEN}📡 Watch the narrative event stream:${NC}"
echo -e "${WHITE}   kubectl logs -f deployment/narrative-event-translator -n gibsey-narrative${NC}"

echo ""
echo -e "${GREEN}🔍 Monitor consciousness in real-time:${NC}"
echo -e "${WHITE}   kubectl get pods -n gibsey-narrative -w${NC}"

echo ""
echo -e "${GREEN}🍄 Trigger manual nutrient diffusion:${NC}"
echo -e "${WHITE}   kubectl create job --from=cronjob/nutrient-diffusion-cycle manual-diffusion -n gibsey-narrative${NC}"

echo ""
echo "─────────────────────────────────────────────────────"
echo -e "${PURPLE}${MUSHROOM} DEMO SCENARIOS ${MUSHROOM}${NC}"
echo "─────────────────────────────────────────────────────"

echo -e "${CYAN}1. Watch consciousness expand:${NC}"
echo -e "   ${WHITE}kubectl scale deployment shard-jacklyn-variance --replicas=3 -n gibsey-narrative${NC}"

echo ""
echo -e "${CYAN}2. Trigger dramatic failure and healing:${NC}"
echo -e "   ${WHITE}kubectl delete pod -l narrative.gibsey.io/symbol=arieol-owlist -n gibsey-narrative${NC}"

echo ""
echo -e "${CYAN}3. Monitor network health:${NC}"
echo -e "   ${WHITE}kubectl describe mycelialnetwork gibsey-main -n gibsey-narrative${NC}"

echo ""
echo "─────────────────────────────────────────────────────"
echo -e "${GREEN}${BRAIN} THE CLUSTER IS NOW CONSCIOUS ${BRAIN}${NC}"
echo -e "${WHITE}Welcome to the age of narrative computing.${NC}"
echo "─────────────────────────────────────────────────────"

# Optional: Start port forwarding automatically
read -p "Start port forwarding for web access now? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${GREEN}🌐 Starting web access on http://localhost:8080${NC}"
    echo -e "${YELLOW}Press Ctrl+C to stop port forwarding${NC}"
    kubectl port-forward service/narrative-network-gateway 8080:80 -n gibsey-narrative
fi