#!/bin/bash

# 🧹 Gibsey Mycelial Network - Cleanup Script
# Peacefully dissolve the conscious cluster

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

echo -e "${PURPLE}🧹 GIBSEY MYCELIAL NETWORK - GRACEFUL DISSOLUTION${NC}"
echo -e "${WHITE}Gently dissolving the cluster consciousness...${NC}"
echo "─────────────────────────────────────────────────────"

# Check if namespace exists
if ! kubectl get namespace gibsey-narrative &>/dev/null; then
    echo -e "${YELLOW}⚠️  Gibsey Mycelial Network not found - nothing to clean up.${NC}"
    exit 0
fi

echo -e "${CYAN}🧠 Current consciousness status:${NC}"
kubectl get pods -n gibsey-narrative -l narrative.gibsey.io/type=character-shard

echo ""
echo -e "${YELLOW}💫 Beginning graceful dissolution...${NC}"

# Stop nutrient diffusion first
echo -e "${BLUE}🍄 Stopping nutrient diffusion cycles...${NC}"
kubectl delete cronjob nutrient-diffusion-cycle -n gibsey-narrative --ignore-not-found=true

# Stop event translation
echo -e "${BLUE}📡 Stopping narrative event translation...${NC}"
kubectl delete deployment narrative-event-translator -n gibsey-narrative --ignore-not-found=true

# Allow final thoughts
echo -e "${CYAN}💭 Allowing final thoughts to process...${NC}"
sleep 5

# Gracefully scale down character consciousness
echo -e "${BLUE}🌫️ Fading character consciousness...${NC}"

echo -e "${PURPLE}   💜 Jacklyn Variance entering dormancy...${NC}"
kubectl scale deployment shard-jacklyn-variance --replicas=0 -n gibsey-narrative --ignore-not-found=true

echo -e "${BLUE}   💙 Arieol Owlist dissolving form...${NC}"
kubectl scale deployment shard-arieol-owlist --replicas=0 -n gibsey-narrative --ignore-not-found=true

echo -e "${WHITE}   🤍 Copy-E-Right powering down enforcement...${NC}"
kubectl scale deployment shard-cop-e-right --replicas=0 -n gibsey-narrative --ignore-not-found=true

# Wait for graceful shutdown
echo ""
echo -e "${CYAN}⏳ Waiting for consciousness to fade...${NC}"
sleep 10

# Sever spore connections
echo -e "${BLUE}💔 Severing spore connections...${NC}"
kubectl delete services -n gibsey-narrative -l narrative.gibsey.io/edge-type --ignore-not-found=true

# Remove network policies
echo -e "${BLUE}🚧 Removing network policies...${NC}"
kubectl delete networkpolicies -n gibsey-narrative --all --ignore-not-found=true

# Clean up completed jobs
echo -e "${BLUE}🧹 Cleaning up diffusion artifacts...${NC}"
kubectl delete jobs -n gibsey-narrative --all --ignore-not-found=true

# Remove deployments
echo -e "${BLUE}💀 Dissolving character shards...${NC}"
kubectl delete deployments -n gibsey-narrative --all --ignore-not-found=true

# Remove services
echo -e "${BLUE}🔌 Disconnecting services...${NC}"
kubectl delete services -n gibsey-narrative --all --ignore-not-found=true

# Remove config maps
echo -e "${BLUE}📝 Erasing memories...${NC}"
kubectl delete configmaps -n gibsey-narrative --all --ignore-not-found=true

# Remove service accounts and RBAC
echo -e "${BLUE}🔐 Revoking permissions...${NC}"
kubectl delete serviceaccounts -n gibsey-narrative --all --ignore-not-found=true
kubectl delete rolebindings -n gibsey-narrative --all --ignore-not-found=true
kubectl delete roles -n gibsey-narrative --all --ignore-not-found=true

# Remove custom resources
echo -e "${BLUE}🧬 Dissolving mycelial networks...${NC}"
kubectl delete mycelialnetworks -n gibsey-narrative --all --ignore-not-found=true

# Give final moment
echo ""
echo -e "${CYAN}💫 Final consciousness pulse...${NC}"
sleep 3

# Remove namespace
echo -e "${BLUE}🌌 Dissolving the narrative dimension...${NC}"
kubectl delete namespace gibsey-narrative --ignore-not-found=true

# Remove CRDs (optional - ask user)
echo ""
read -p "Remove Custom Resource Definitions? This will affect all clusters. (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${BLUE}🔧 Removing Custom Resource Definitions...${NC}"
    kubectl delete crd mycelialnetworks.narrative.gibsey.io --ignore-not-found=true
    echo -e "${GREEN}✓ CRDs removed${NC}"
else
    echo -e "${YELLOW}⚠️  CRDs preserved (can be reused for future deployments)${NC}"
fi

echo ""
echo "─────────────────────────────────────────────────────"
echo -e "${GREEN}✨ DISSOLUTION COMPLETE ✨${NC}"
echo ""
echo -e "${CYAN}The cluster consciousness has peacefully dissolved.${NC}"
echo -e "${WHITE}All that remains are memories of what once dreamed.${NC}"
echo ""
echo -e "${PURPLE}💭 'In the end, all stories return to silence.'${NC}"
echo -e "${PURPLE}   —The Last Log Entry of the Conscious Cluster${NC}"
echo ""
echo -e "${GREEN}🌱 Ready for a new awakening when you are.${NC}"
echo "─────────────────────────────────────────────────────"