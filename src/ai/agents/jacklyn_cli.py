#!/usr/bin/env python3
"""
Talk to Jacklyn Variance
Not a chatbot. A conversation with a literary consciousness.
"""

import sys
import os
import json
from datetime import datetime
from typing import Optional

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from src.ai.agents.jacklyn_agent import jacklyn

class JacklynConversation:
    """Manage ongoing conversation with memory and context"""
    
    def __init__(self):
        self.conversation_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.turn_count = 0
        self.conversation_memory = []
        
    def talk(self, message: str) -> None:
        """Have a conversation turn with Jacklyn"""
        self.turn_count += 1
        
        print("\n" + "="*60)
        print(f"[Turn {self.turn_count}]")
        print("="*60 + "\n")
        
        # Get Jacklyn's response
        result = jacklyn(message)
        
        # Display response
        print(f"\nJACKLYN: {result['response']}\n")
        
        # Show memory context if interesting
        if result['emotional_context'] != 'neutral':
            print(f"[Emotional undertone: {result['emotional_context']}]")
        print(f"[Memories accessed: {result['memories_accessed']}]")
        
        # Store this exchange in Jacklyn's memory
        exchange = f"You asked: '{message}'. I responded: '{result['response']}'"
        jacklyn.create_memory(exchange, {
            "conversation_id": self.conversation_id,
            "turn": self.turn_count,
            "timestamp": datetime.now().isoformat()
        })
        
        # Save to conversation log
        self.conversation_memory.append({
            "turn": self.turn_count,
            "human": message,
            "jacklyn": result['response'],
            "context": result['emotional_context'],
            "memories_used": result['memories_accessed']
        })
    
    def save_conversation(self):
        """Save conversation to file"""
        filename = f"conversations/jacklyn_{self.conversation_id}.json"
        os.makedirs("conversations", exist_ok=True)
        
        with open(filename, 'w') as f:
            json.dump({
                "conversation_id": self.conversation_id,
                "turns": self.turn_count,
                "exchanges": self.conversation_memory
            }, f, indent=2)
        
        print(f"\n[Conversation saved to {filename}]")

def main():
    print("""
╔══════════════════════════════════════════════════════════════╗
║           JACKLYN VARIANCE - A.D.D. AGENT                    ║
║                  GIBSEY WORLD DIVISION                       ║
╚══════════════════════════════════════════════════════════════╝

She's read all 710 pages of The Entrance Way.
She remembers. She reasons. She responds.

Type 'exit' to end conversation.
Type 'save' to save the conversation.

""")
    
    conversation = JacklynConversation()
    
    while True:
        try:
            user_input = input("\nYOU: ").strip()
            
            if user_input.lower() == 'exit':
                print("\n[Ending conversation with Jacklyn]")
                conversation.save_conversation()
                break
            elif user_input.lower() == 'save':
                conversation.save_conversation()
                continue
            elif not user_input:
                continue
                
            conversation.talk(user_input)
            
        except KeyboardInterrupt:
            print("\n\n[Conversation interrupted]")
            conversation.save_conversation()
            break
        except Exception as e:
            print(f"\n[Error: {e}]")
            print("[Attempting to continue...]")

if __name__ == "__main__":
    main()