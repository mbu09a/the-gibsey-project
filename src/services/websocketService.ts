export interface WebSocketMessage {
  type: string;
  data: any;
}

export interface StreamingMessage {
  token: string;
  isComplete: boolean;
  characterId?: string;
}

export class WebSocketService {
  private ws: WebSocket | null = null;
  
  connect(url?: string): Promise<void> {
    const sessionId = `session-${Math.random().toString(36).substr(2, 9)}`;
    const wsUrl = url || `ws://localhost:8000/ws/${sessionId}`;
    
    return new Promise((resolve, reject) => {
      try {
        console.log('[WebSocket] Connecting to:', wsUrl);
        this.ws = new WebSocket(wsUrl);
        
        this.ws.onopen = () => {
          console.log('[WebSocket] Connected successfully');
          resolve();
        };
        
        this.ws.onerror = (error) => {
          console.error('[WebSocket] Connection error:', error);
          // Fall back to simulation if real backend fails
          console.log('[WebSocket] Falling back to simulation mode');
          this.ws = null;
          resolve();
        };
        
        this.ws.onclose = () => {
          console.log('[WebSocket] Connection closed');
          this.ws = null;
        };
      } catch (error) {
        console.error('[WebSocket] Failed to create connection:', error);
        // Fall back to simulation
        resolve();
      }
    });
  }
  
  send(message: WebSocketMessage): void {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      console.log('[WebSocket] Sending message:', message);
      this.ws.send(JSON.stringify(message));
    } else {
      console.log('[WebSocket] Not connected, simulating send:', message);
    }
  }

  sendChatRequest(prompt: string, characterId: string, pageId?: string): void {
    this.send({
      type: 'ai_chat_request',
      data: {
        prompt,
        character_id: characterId,
        page_id: pageId
      }
    });
  }
  
  onMessage(callback: (message: WebSocketMessage) => void): () => void {
    if (this.ws) {
      this.ws.onmessage = (event) => {
        try {
          const message = JSON.parse(event.data);
          console.log('[WebSocket] Received message:', message);
          callback(message);
        } catch (error) {
          console.error('[WebSocket] Failed to parse message:', error);
        }
      };
    }
    
    // Return unsubscribe function
    return () => {
      if (this.ws) {
        this.ws.onmessage = null;
      }
      console.log('[WebSocket] Message handler unsubscribed');
    };
  }
  
  disconnect(): void {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }
}

export const websocketService = new WebSocketService();

export function getWebSocketService(): WebSocketService {
  return websocketService;
}