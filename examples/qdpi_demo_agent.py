#!/usr/bin/env python3
"""
QDPI Demo Agent
Demonstrates complete QDPI-256 integration workflow
"""

import requests
import json
import time
import uuid
from typing import Dict, List, Any

class QDPIAgent:
    """Simple QDPI agent for demonstration"""
    
    def __init__(self, base_url: str = "http://localhost:8000/api/v1/qdpi"):
        self.base_url = base_url
        self.session_id = f"demo-agent-{uuid.uuid4().hex[:8]}"
        print(f"🤖 QDPI Agent initialized with session: {self.session_id}")
    
    def get_state(self) -> Dict[str, Any]:
        """Get current QDPI state"""
        response = requests.get(f"{self.base_url}/mode/{self.session_id}")
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Failed to get state: {response.status_code}")
            return {}
    
    def set_mode(self, mode: str, orientation: str = None, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Set QDPI mode and orientation"""
        data = {"mode": mode}
        if orientation:
            data["orientation"] = orientation
        if context:
            data["context"] = context
        
        response = requests.post(f"{self.base_url}/mode/{self.session_id}", json=data)
        if response.status_code == 200:
            result = response.json()
            print(f"🔄 Mode set to: {result['mode']} (orientation: {result['orientation']})")
            return result
        else:
            print(f"❌ Failed to set mode: {response.status_code}")
            return {}
    
    def encode_data(self, data: str, execute_flows: bool = False) -> Dict[str, Any]:
        """Encode data into QDPI symbols"""
        payload = {"data": data, "execute_flows": execute_flows}
        response = requests.post(f"{self.base_url}/encode/{self.session_id}", json=payload)
        
        if response.status_code == 200:
            result = response.json()
            symbols_count = len(result.get('encoded_symbols', []))
            print(f"📝 Encoded '{data}' into {symbols_count} symbols")
            
            # Show which symbols have functions
            for symbol in result.get('encoded_symbols', []):
                if any(exec_result.get('function') for exec_result in result.get('execution_results', []) 
                       if exec_result.get('symbol') == symbol['name']):
                    print(f"  ⚡ {symbol['name']} -> has function")
                else:
                    print(f"  • {symbol['name']} (glyph_id: {symbol['glyph_id']})")
            
            return result
        else:
            print(f"❌ Failed to encode data: {response.status_code}")
            return {}
    
    def search_symbols(self, query: str, limit: int = 5) -> Dict[str, Any]:
        """Search for symbols semantically"""
        payload = {"query": query, "limit": limit}
        response = requests.post(f"{self.base_url}/search/{self.session_id}", json=payload)
        
        if response.status_code == 200:
            result = response.json()
            matches_count = len(result.get('matches', []))
            print(f"🔍 Found {matches_count} matches for '{query}':")
            
            for match in result.get('matches', []):
                symbol = match['symbol']
                similarity = match['similarity'] * 100
                function = match.get('function', 'No function')
                print(f"  • {symbol['name']} ({similarity:.1f}% match) - {function}")
            
            return result
        else:
            print(f"❌ Failed to search symbols: {response.status_code}")
            return {}
    
    def execute_symbol(self, symbol_name: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute flows for a specific symbol"""
        payload = {"symbol_name": symbol_name, "context": context or {}}
        response = requests.post(f"{self.base_url}/execute/{self.session_id}", json=payload)
        
        if response.status_code == 200:
            result = response.json()
            flows = result.get('execution_result', {}).get('flows', [])
            print(f"⚡ Executed {len(flows)} flows for '{symbol_name}':")
            
            for flow in flows:
                status = flow.get('status', 'unknown')
                flow_name = flow.get('flow', 'unnamed')
                action = flow.get('action', 'no action')
                print(f"  • {flow_name}: {status} ({action})")
            
            return result
        else:
            print(f"❌ Failed to execute symbol: {response.status_code}")
            return {}
    
    def get_history(self, history_type: str = "all", limit: int = 10) -> Dict[str, Any]:
        """Get session history"""
        params = {"history_type": history_type, "limit": limit}
        response = requests.get(f"{self.base_url}/history/{self.session_id}", params=params)
        
        if response.status_code == 200:
            result = response.json()
            
            if 'symbol_history' in result:
                print(f"📚 Symbol history ({len(result['symbol_history'])} items):")
                for item in result['symbol_history'][-5:]:  # Show last 5
                    timestamp = item['timestamp'].split('T')[1].split('.')[0]
                    print(f"  {timestamp}: {item['action']} {item['symbol']}")
            
            if 'flow_history' in result:
                print(f"⚡ Flow history ({len(result['flow_history'])} items):")
                for item in result['flow_history'][-3:]:  # Show last 3
                    timestamp = item['timestamp'].split('T')[1].split('.')[0]
                    symbols = ', '.join(item.get('symbols', []))
                    print(f"  {timestamp}: {symbols} -> {len(item.get('flows', []))} flows")
            
            return result
        else:
            print(f"❌ Failed to get history: {response.status_code}")
            return {}

def demo_workflow():
    """Complete QDPI workflow demonstration"""
    print("🚀 Starting QDPI-256 Demo Workflow")
    print("=" * 50)
    
    agent = QDPIAgent()
    time.sleep(1)
    
    # 1. Check initial state
    print("\n1️⃣ Getting initial state...")
    state = agent.get_state()
    print(f"   Initial mode: {state.get('mode', 'unknown')}")
    time.sleep(1)
    
    # 2. Switch to ASK mode for querying
    print("\n2️⃣ Switching to ASK mode...")
    agent.set_mode("ask", context={"purpose": "seeking wisdom"})
    time.sleep(1)
    
    # 3. Search for wisdom-related symbols
    print("\n3️⃣ Searching for wisdom symbols...")
    search_results = agent.search_symbols("wisdom and knowledge", limit=5)
    time.sleep(1)
    
    # 4. Execute a search symbol if found
    if search_results.get('matches'):
        print("\n4️⃣ Executing first search result...")
        first_match = search_results['matches'][0]
        symbol_name = first_match['symbol']['name']
        agent.execute_symbol(symbol_name, {"query": "what is wisdom?"})
    else:
        print("\n4️⃣ No search results, executing london_fox symbol...")
        agent.execute_symbol("london_fox", {"query": "search for patterns"})
    time.sleep(1)
    
    # 5. Switch to INDEX mode for creation
    print("\n5️⃣ Switching to INDEX mode...")
    agent.set_mode("index", context={"purpose": "creating content"})
    time.sleep(1)
    
    # 6. Encode some creative content
    print("\n6️⃣ Encoding creative content...")
    encoded = agent.encode_data("Once upon a time in the Gibsey universe, symbols came alive...", execute_flows=True)
    time.sleep(1)
    
    # 7. Execute author symbol for narrative creation
    print("\n7️⃣ Executing narrative creation...")
    agent.execute_symbol("an_author", {
        "story_type": "symbolic", 
        "theme": "consciousness",
        "setting": "digital realm"
    })
    time.sleep(1)
    
    # 8. Switch to READ mode for analysis
    print("\n8️⃣ Switching to READ mode...")
    agent.set_mode("read", context={"purpose": "analysis"})
    time.sleep(1)
    
    # 9. Execute variance analysis
    print("\n9️⃣ Performing variance analysis...")
    agent.execute_symbol("jacklyn_variance", {
        "data_source": "narrative_patterns",
        "analysis_depth": "deep"
    })
    time.sleep(1)
    
    # 10. Flip orientation and test
    print("\n🔟 Flipping orientation...")
    agent.set_mode("read", orientation="u", context={"perspective": "inverted"})
    time.sleep(1)
    
    # 11. Get session history
    print("\n1️⃣1️⃣ Reviewing session history...")
    agent.get_history()
    time.sleep(1)
    
    print("\n" + "=" * 50)
    print("✅ QDPI-256 Demo Workflow Complete!")
    print(f"   Session ID: {agent.session_id}")
    print("   All systems operational. QDPI symbolic machine language is live!")

def simple_demo():
    """Simple demonstration for quick testing"""
    print("🧪 Simple QDPI Demo")
    print("-" * 30)
    
    agent = QDPIAgent()
    
    # Quick mode test
    agent.set_mode("ask")
    
    # Quick encoding test
    agent.encode_data("Hello QDPI!", execute_flows=False)
    
    # Quick symbol execution
    agent.execute_symbol("london_fox", {"test": "simple demo"})
    
    print("✅ Simple demo complete!")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "simple":
        simple_demo()
    else:
        demo_workflow()