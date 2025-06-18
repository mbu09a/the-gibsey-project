/**
 * WebSocket service for real-time LLM streaming from the Gibsey backend
 */

export interface StreamingMessage {
  type: 'ai_response_stream' | 'connection_established' | 'error' | 'vault_update' | 'page_update';
  data: {
    response_id?: string;
    token?: string;
    is_complete?: boolean;
    timestamp?: string;
    session_id?: string;
    message?: string;
    code?: string;
    [key: string]: any;
  };
}

export interface ChatRequest {
  type: 'ai_chat_request';
  data: {
    prompt: string;
    character_id: string;
    current_page_id?: string;
  };
}

type MessageHandler = (message: StreamingMessage) => void;
type ErrorHandler = (error: Event) => void;
type ConnectionHandler = () => void;

export class WebSocketService {
  private ws: WebSocket | null = null;
  private sessionId: string;
  private messageHandlers: Set<MessageHandler> = new Set();
  private errorHandlers: Set<ErrorHandler> = new Set();
  private connectionHandlers: Set<ConnectionHandler> = new Set();
  private disconnectionHandlers: Set<ConnectionHandler> = new Set();
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectTimeout: NodeJS.Timeout | null = null;

  constructor(sessionId?: string) {
    this.sessionId = sessionId || `session-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  }

  /**
   * Connect to the WebSocket server
   */
  connect(): Promise<void> {
    return new Promise((resolve, reject) => {
      try {
        const wsUrl = `ws://localhost:8000/ws/${this.sessionId}`;
        this.ws = new WebSocket(wsUrl);

        this.ws.onopen = () => {
          console.log(`[WebSocket] Connected with session: ${this.sessionId}`);
          this.reconnectAttempts = 0;
          this.connectionHandlers.forEach(handler => handler());
          resolve();
        };

        this.ws.onmessage = (event) => {
          try {
            const message: StreamingMessage = JSON.parse(event.data);
            this.messageHandlers.forEach(handler => handler(message));
          } catch (error) {
            console.error('[WebSocket] Failed to parse message:', error);
          }
        };

        this.ws.onclose = (event) => {
          console.log('[WebSocket] Connection closed:', event.code, event.reason);
          this.disconnectionHandlers.forEach(handler => handler());
          this.attemptReconnect();
        };

        this.ws.onerror = (error) => {
          console.error('[WebSocket] Error:', error);
          this.errorHandlers.forEach(handler => handler(error));
          reject(error);
        };

      } catch (error) {
        reject(error);
      }
    });
  }

  /**
   * Disconnect from the WebSocket server
   */
  disconnect(): void {
    if (this.reconnectTimeout) {
      clearTimeout(this.reconnectTimeout);
      this.reconnectTimeout = null;
    }
    
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }

  /**
   * Send a chat request to the backend
   */
  sendChatRequest(prompt: string, characterId: string, currentPageId?: string): void {
    if (!this.ws || this.ws.readyState !== WebSocket.OPEN) {
      throw new Error('WebSocket is not connected');
    }

    const request: ChatRequest = {
      type: 'ai_chat_request',
      data: {
        prompt,
        character_id: characterId,
        current_page_id: currentPageId
      }
    };

    this.ws.send(JSON.stringify(request));
  }

  /**
   * Send a ping to keep the connection alive
   */
  ping(): void {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify({
        type: 'ping',
        data: { timestamp: new Date().toISOString() }
      }));
    }
  }

  /**
   * Attempt to reconnect to the WebSocket server
   */
  private attemptReconnect(): void {
    if (this.reconnectAttempts >= this.maxReconnectAttempts) {
      console.error('[WebSocket] Max reconnection attempts reached');
      return;
    }

    this.reconnectAttempts++;
    const delay = Math.min(1000 * Math.pow(2, this.reconnectAttempts), 10000); // Exponential backoff

    console.log(`[WebSocket] Attempting to reconnect in ${delay}ms (attempt ${this.reconnectAttempts})`);
    
    this.reconnectTimeout = setTimeout(() => {
      this.connect().catch(error => {
        console.error('[WebSocket] Reconnection failed:', error);
      });
    }, delay);
  }

  /**
   * Check if the WebSocket is connected
   */
  isConnected(): boolean {
    return this.ws !== null && this.ws.readyState === WebSocket.OPEN;
  }

  /**
   * Get the current session ID
   */
  getSessionId(): string {
    return this.sessionId;
  }

  // Event handlers
  onMessage(handler: MessageHandler): () => void {
    this.messageHandlers.add(handler);
    return () => this.messageHandlers.delete(handler);
  }

  onError(handler: ErrorHandler): () => void {
    this.errorHandlers.add(handler);
    return () => this.errorHandlers.delete(handler);
  }

  onConnection(handler: ConnectionHandler): () => void {
    this.connectionHandlers.add(handler);
    return () => this.connectionHandlers.delete(handler);
  }

  onDisconnection(handler: ConnectionHandler): () => void {
    this.disconnectionHandlers.add(handler);
    return () => this.disconnectionHandlers.delete(handler);
  }
}

// Global WebSocket service instance
let globalWebSocketService: WebSocketService | null = null;

export const getWebSocketService = (sessionId?: string): WebSocketService => {
  if (!globalWebSocketService) {
    globalWebSocketService = new WebSocketService(sessionId);
  }
  return globalWebSocketService;
};

export const disconnectWebSocketService = (): void => {
  if (globalWebSocketService) {
    globalWebSocketService.disconnect();
    globalWebSocketService = null;
  }
};