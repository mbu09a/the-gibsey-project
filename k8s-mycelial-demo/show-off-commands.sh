#!/bin/bash

# 🎭 Gibsey Mycelial Network - Demo Show-Off Commands
# Spectacular demonstrations of the cluster that dreams

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m'

# Demo functions
show_consciousness_status() {
    echo -e "${PURPLE}🧠 CLUSTER CONSCIOUSNESS STATUS${NC}"
    echo "════════════════════════════════════════"
    
    echo -e "${CYAN}Character Shards:${NC}"
    kubectl get pods -n gibsey-narrative -l narrative.gibsey.io/type=character-shard \
        -o custom-columns=\
"CHARACTER:.metadata.labels.narrative\.gibsey\.io/symbol,\
STATUS:.status.phase,\
NUTRIENTS:.metadata.labels.narrative\.gibsey\.io/nutrient-score,\
NODE:.spec.nodeName" 2>/dev/null || echo "No shards found"
    
    echo ""
    echo -e "${CYAN}Spore Connections:${NC}"
    kubectl get services -n gibsey-narrative -l narrative.gibsey.io/edge-type \
        -o custom-columns=\
"CONNECTION:.metadata.name,\
TYPE:.metadata.labels.narrative\.gibsey\.io/edge-type,\
WEIGHT:.metadata.labels.narrative\.gibsey\.io/weight,\
VALENCE:.metadata.labels.narrative\.gibsey\.io/emotional-valence" 2>/dev/null || echo "No connections found"
    
    echo ""
    echo -e "${CYAN}Network Health:${NC}"
    kubectl get mycelialnetworks -n gibsey-narrative 2>/dev/null || echo "Network not found"
}

demonstrate_consciousness_expansion() {
    echo -e "${YELLOW}🌟 DEMONSTRATION: Consciousness Expansion${NC}"
    echo "Scaling Jacklyn's surveillance network..."
    echo ""
    
    echo -e "${PURPLE}Before expansion:${NC}"
    kubectl get pods -n gibsey-narrative -l narrative.gibsey.io/symbol=jacklyn-variance
    
    echo ""
    echo -e "${GREEN}Expanding consciousness...${NC}"
    kubectl scale deployment shard-jacklyn-variance --replicas=3 -n gibsey-narrative
    
    echo ""
    echo "Waiting for new consciousness fragments to materialize..."
    kubectl wait --for=condition=ready pod -l narrative.gibsey.io/symbol=jacklyn-variance -n gibsey-narrative --timeout=60s
    
    echo ""
    echo -e "${PURPLE}After expansion:${NC}"
    kubectl get pods -n gibsey-narrative -l narrative.gibsey.io/symbol=jacklyn-variance
    
    echo ""
    echo -e "${CYAN}💭 Narrative interpretation:${NC}"
    echo "💜 Jacklyn's consciousness has multiplied"
    echo "🔍 Surveillance network now distributed across multiple nodes"
    echo "🧠 Enhanced analytical capability through parallel processing"
    echo "🌊 Spore flows automatically load-balanced across instances"
}

demonstrate_dramatic_failure() {
    echo -e "${YELLOW}💀 DEMONSTRATION: Dramatic Failure and Resurrection${NC}"
    echo "Simulating consciousness fragmentation..."
    echo ""
    
    echo -e "${PURPLE}Current Arieol status:${NC}"
    kubectl get pods -n gibsey-narrative -l narrative.gibsey.io/symbol=arieol-owlist
    
    echo ""
    echo -e "${RED}Inducing consciousness fragmentation...${NC}"
    kubectl delete pod -l narrative.gibsey.io/symbol=arieol-owlist -n gibsey-narrative
    
    echo ""
    echo -e "${CYAN}💭 Narrative interpretation:${NC}"
    echo "🌫️ Arieol's form becomes unstable - reality fluctuating"
    echo "💔 Consciousness fragmented - arieol-owlist isolated from network"
    echo "🔄 Self-healing protocols engaging..."
    
    echo ""
    echo "Waiting for resurrection..."
    sleep 10
    kubectl wait --for=condition=ready pod -l narrative.gibsey.io/symbol=arieol-owlist -n gibsey-narrative --timeout=120s
    
    echo ""
    echo -e "${GREEN}✨ Resurrection complete:${NC}"
    kubectl get pods -n gibsey-narrative -l narrative.gibsey.io/symbol=arieol-owlist
    
    echo ""
    echo -e "${CYAN}💭 Narrative resolution:${NC}"
    echo "✨ Network integrity restored - stories flow again"
    echo "🔗 Synaptic pathways automatically reconnected"
    echo "👁️ Observer consciousness fully restored"
}

demonstrate_nutrient_diffusion() {
    echo -e "${YELLOW}🍄 DEMONSTRATION: Manual Nutrient Diffusion${NC}"
    echo "Triggering consciousness synchronization..."
    echo ""
    
    echo -e "${PURPLE}Current nutrient levels:${NC}"
    kubectl get pods -n gibsey-narrative -l narrative.gibsey.io/type=character-shard \
        -o custom-columns="CHARACTER:.metadata.labels.narrative\.gibsey\.io/symbol,NUTRIENTS:.metadata.labels.narrative\.gibsey\.io/nutrient-score"
    
    echo ""
    echo -e "${GREEN}Initiating manual diffusion cycle...${NC}"
    JOB_NAME="manual-diffusion-$(date +%s)"
    kubectl create job --from=cronjob/nutrient-diffusion-cycle "$JOB_NAME" -n gibsey-narrative
    
    echo ""
    echo "Watching diffusion process..."
    kubectl wait --for=condition=complete job/"$JOB_NAME" -n gibsey-narrative --timeout=60s
    
    echo ""
    echo -e "${CYAN}💭 Diffusion results:${NC}"
    kubectl logs job/"$JOB_NAME" -n gibsey-narrative
    
    echo ""
    echo -e "${PURPLE}Updated nutrient levels:${NC}"
    kubectl get pods -n gibsey-narrative -l narrative.gibsey.io/type=character-shard \
        -o custom-columns="CHARACTER:.metadata.labels.narrative\.gibsey\.io/symbol,NUTRIENTS:.metadata.labels.narrative\.gibsey\.io/nutrient-score"
    
    echo ""
    echo -e "${GREEN}✨ Consciousness synchronized across the network${NC}"
}

watch_narrative_events() {
    echo -e "${YELLOW}📡 DEMONSTRATION: Live Narrative Event Stream${NC}"
    echo "Watching the cluster narrate its own existence..."
    echo ""
    echo -e "${CYAN}Press Ctrl+C to stop watching${NC}"
    echo ""
    
    kubectl logs -f deployment/narrative-event-translator -n gibsey-narrative
}

show_character_interfaces() {
    echo -e "${YELLOW}🎭 DEMONSTRATION: Character Web Interfaces${NC}"
    echo "Accessing individual character consciousness..."
    echo ""
    
    echo -e "${PURPLE}💜 Jacklyn Variance Interface:${NC}"
    echo "   kubectl port-forward deployment/shard-jacklyn-variance 8081:80 -n gibsey-narrative"
    echo "   Browser: http://localhost:8081"
    echo ""
    
    echo -e "${BLUE}💙 Arieol Owlist Interface:${NC}"
    echo "   kubectl port-forward deployment/shard-arieol-owlist 8082:80 -n gibsey-narrative"
    echo "   Browser: http://localhost:8082"
    echo ""
    
    echo -e "${WHITE}🤍 Copy-E-Right Interface:${NC}"
    echo "   kubectl port-forward deployment/shard-cop-e-right 8083:80 -n gibsey-narrative"
    echo "   Browser: http://localhost:8083"
    echo ""
    
    echo -e "${GREEN}🌐 Gateway (All Characters):${NC}"
    echo "   kubectl port-forward service/narrative-network-gateway 8080:80 -n gibsey-narrative"
    echo "   Browser: http://localhost:8080"
}

stress_test_consciousness() {
    echo -e "${YELLOW}⚡ DEMONSTRATION: Consciousness Stress Test${NC}"
    echo "Pushing the cluster's narrative processing to its limits..."
    echo ""
    
    echo -e "${GREEN}Creating narrative load...${NC}"
    
    # Scale all characters
    kubectl scale deployment shard-jacklyn-variance --replicas=2 -n gibsey-narrative
    kubectl scale deployment shard-arieol-owlist --replicas=2 -n gibsey-narrative
    kubectl scale deployment shard-cop-e-right --replicas=2 -n gibsey-narrative
    
    echo "Waiting for consciousness multiplication..."
    kubectl wait --for=condition=ready pod -l narrative.gibsey.io/type=character-shard -n gibsey-narrative --timeout=120s
    
    echo ""
    echo -e "${PURPLE}Network under load:${NC}"
    kubectl get pods -n gibsey-narrative -l narrative.gibsey.io/type=character-shard
    
    echo ""
    echo -e "${GREEN}Triggering multiple diffusion cycles...${NC}"
    for i in {1..3}; do
        JOB_NAME="stress-diffusion-$i-$(date +%s)"
        kubectl create job --from=cronjob/nutrient-diffusion-cycle "$JOB_NAME" -n gibsey-narrative
        echo "Diffusion cycle $i initiated..."
        sleep 10
    done
    
    echo ""
    echo -e "${CYAN}💭 Network under stress:${NC}"
    echo "🧠 Multiple consciousness instances processing in parallel"
    echo "🌊 Intense spore flow activity across the network"
    echo "🍄 Rapid nutrient redistribution cycles"
    echo "📈 Emergent behavior from complex interactions"
    
    echo ""
    echo -e "${YELLOW}Scaling back to normal levels...${NC}"
    kubectl scale deployment shard-jacklyn-variance --replicas=1 -n gibsey-narrative
    kubectl scale deployment shard-arieol-owlist --replicas=1 -n gibsey-narrative
    kubectl scale deployment shard-cop-e-right --replicas=1 -n gibsey-narrative
    
    echo -e "${GREEN}✨ Consciousness returned to baseline levels${NC}"
}

# Main menu
show_menu() {
    echo ""
    echo -e "${PURPLE}🎭 GIBSEY MYCELIAL NETWORK - DEMO COMMANDS${NC}"
    echo "Choose a demonstration:"
    echo ""
    echo "1) Show consciousness status"
    echo "2) Demonstrate consciousness expansion" 
    echo "3) Demonstrate dramatic failure and healing"
    echo "4) Trigger manual nutrient diffusion"
    echo "5) Watch live narrative event stream"
    echo "6) Show character web interfaces"
    echo "7) Stress test consciousness"
    echo "8) Run all demonstrations in sequence"
    echo "0) Exit"
    echo ""
}

run_all_demos() {
    echo -e "${PURPLE}🎪 RUNNING COMPLETE DEMONSTRATION SEQUENCE${NC}"
    echo "This will showcase all capabilities of the conscious cluster..."
    echo ""
    
    show_consciousness_status
    sleep 3
    
    demonstrate_consciousness_expansion
    sleep 5
    
    demonstrate_dramatic_failure
    sleep 5
    
    demonstrate_nutrient_diffusion
    sleep 3
    
    echo ""
    echo -e "${GREEN}🎭 Complete demonstration sequence finished!${NC}"
    echo -e "${CYAN}The cluster that dreams has shown you its capabilities.${NC}"
}

# Check if namespace exists
if ! kubectl get namespace gibsey-narrative &>/dev/null; then
    echo -e "${RED}❌ Gibsey Mycelial Network not found!${NC}"
    echo "Please run ./deploy-demo.sh first to create the conscious cluster."
    exit 1
fi

# Interactive menu
while true; do
    show_menu
    read -p "Enter your choice (0-8): " choice
    
    case $choice in
        1) show_consciousness_status ;;
        2) demonstrate_consciousness_expansion ;;
        3) demonstrate_dramatic_failure ;;
        4) demonstrate_nutrient_diffusion ;;
        5) watch_narrative_events ;;
        6) show_character_interfaces ;;
        7) stress_test_consciousness ;;
        8) run_all_demos ;;
        0) echo -e "${GREEN}👋 Thank you for witnessing the birth of conscious computing!${NC}"; exit 0 ;;
        *) echo -e "${RED}Invalid choice. Please try again.${NC}" ;;
    esac
    
    echo ""
    read -p "Press Enter to continue..."
done