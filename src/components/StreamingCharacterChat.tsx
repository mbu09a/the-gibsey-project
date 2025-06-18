import React, { useState, useRef, useEffect, useCallback } from 'react';
import { useStory } from '../context/StoryContext';
import { getWebSocketService, StreamingMessage } from '../services/websocketService';

interface ChatMessage {
  id: string;
  type: 'user' | 'character';
  content: string;
  timestamp: Date;
  characterId?: string;
  isStreaming?: boolean;
  isComplete?: boolean;
}

interface StreamingCharacterChatProps {
  isOpen: boolean;
  onClose: () => void;
  characterId: string;
  characterName: string;
  characterColor: string;
  characterInitials: string;
}

const StreamingCharacterChat: React.FC<StreamingCharacterChatProps> = ({ 
  isOpen, 
  onClose, 
  characterId,
  characterName,
  characterColor,
  characterInitials
}) => {
  const { currentPage } = useStory();
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [isConnected, setIsConnected] = useState(false);
  const [currentStreamingId, setCurrentStreamingId] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const wsService = getWebSocketService();

  // Scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Initialize WebSocket connection when chat opens
  useEffect(() => {
    if (isOpen && !isConnected) {
      connectToBackend();
    }
  }, [isOpen]);

  // Generate character-specific greeting
  const generateGreeting = useCallback((): string => {
    const greetings = {
      'jacklyn-variance': `⟢ 15:07 ▸ Draft 1 — I'm Jacklyn Variance, Data-and-Detection analyst here at the park. (*adjusts glasses*) I observe therefore I alter; I alter therefore I am watched. What particular patterns or anomalies have brought you to my attention today? Note: this conversation may undergo second-pass analysis for deeper meaning extraction.`,
      'arieol-owlist': `@pause. Time stops. The scene freezes. You've found me—or perhaps I've found you? I'm Arieol Owlist, shape-shifter between detective, diarist, trickster, prophet. My agency meter reads 23% today. Shall we pull a Tarot card to begin, or would you prefer I gift you a fragment of jazz notation? Either way, this chat will end with an open loop... @play. What draws you to the threshold?`,
      'london-fox': `I'm London Fox. I've been analyzing the boundary between computational processes and genuine consciousness. What aspects of awareness would you like to examine through the lens of the Synchromy-M.Y.S.S.T.E.R.Y framework?`,
      'shamrock-stillman': `The paths converge where you least expect them to... I am Shamrock Stillman. What hidden patterns are you seeking to understand?`,
      'todd-fishbone': `Todd Fishbone here. Let's cut through the mystical nonsense and talk about what's actually happening. What's on your mind?`,
      'princhetta': `Princhetta reporting. I see the interconnected systems at work here. What elements of this narrative network would you like to explore?`,
      'jack-parlance': `Jack Parlance. This whole situation has some interesting angles to it. What perspective are you bringing to the conversation?`,
      'new-natalie-weissman': `Hi there! I'm New Natalie Weissman, and I'm fascinated by all the possibilities here. What discoveries are we going to make together?`,
      'old-natalie-weissman': `Hello. I'm Old Natalie Weissman. Time has taught me that the most interesting conversations begin with simple questions. What would you like to explore?`
    };
    
    return greetings[characterId as keyof typeof greetings] || `Hello, I'm ${characterName}. What would you like to discuss?`;
  }, [characterId, characterName]);

  // Initialize chat with greeting when opened
  useEffect(() => {
    if (isOpen && messages.length === 0) {
      const greeting: ChatMessage = {
        id: 'greeting',
        type: 'character',
        content: generateGreeting(),
        timestamp: new Date(),
        characterId,
        isComplete: true
      };
      setMessages([greeting]);
    }
  }, [isOpen, characterId, generateGreeting]);

  const connectToBackend = async () => {
    try {
      console.log(`[Chat] Connecting to backend for ${characterName}...`);
      await wsService.connect();
      setIsConnected(true);
      
      // Set up message handlers
      const unsubscribe = wsService.onMessage(handleStreamingMessage);
      
      return () => {
        unsubscribe();
        setIsConnected(false);
      };
    } catch (error) {
      console.error('[Chat] Failed to connect to backend:', error);
      setIsConnected(false);
    }
  };

  const handleStreamingMessage = useCallback((message: StreamingMessage) => {
    console.log('[Chat] Received message:', message);

    if (message.type === 'ai_response_stream') {
      const { response_id, token, is_complete } = message.data;
      
      if (!response_id) return;

      setMessages(prev => {
        const existing = prev.find(msg => msg.id === response_id);
        
        if (existing) {
          // Update existing streaming message
          return prev.map(msg => 
            msg.id === response_id 
              ? { 
                  ...msg, 
                  content: msg.content + (token || ''),
                  isStreaming: !is_complete,
                  isComplete: is_complete
                }
              : msg
          );
        } else {
          // Create new streaming message
          const newMessage: ChatMessage = {
            id: response_id,
            type: 'character',
            content: token || '',
            timestamp: new Date(),
            characterId,
            isStreaming: !is_complete,
            isComplete: is_complete
          };
          
          return [...prev, newMessage];
        }
      });

      if (is_complete) {
        setIsProcessing(false);
        setCurrentStreamingId(null);
      }
    } else if (message.type === 'connection_established') {
      console.log('[Chat] Connection established:', message.data.session_id);
    } else if (message.type === 'error') {
      console.error('[Chat] Backend error:', message.data.message);
      setIsProcessing(false);
      setCurrentStreamingId(null);
    }
  }, [characterId]);

  const handleSendMessage = async () => {
    if (!inputValue.trim() || isProcessing || !isConnected) return;

    const userMessage: ChatMessage = {
      id: `user-${Date.now()}`,
      type: 'user',
      content: inputValue,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsProcessing(true);

    try {
      // Send request to backend via WebSocket
      wsService.sendChatRequest(inputValue, characterId, currentPage?.id);
      console.log(`[Chat] Sent request to ${characterName}:`, inputValue);
    } catch (error) {
      console.error('[Chat] Failed to send message:', error);
      setIsProcessing(false);
      
      // Add error message
      const errorMessage: ChatMessage = {
        id: `error-${Date.now()}`,
        type: 'character',
        content: `I'm sorry, I'm having trouble connecting to the network right now. Please try again in a moment.`,
        timestamp: new Date(),
        characterId,
        isComplete: true
      };
      setMessages(prev => [...prev, errorMessage]);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div 
        className="w-full max-w-2xl h-[80vh] border-2 rounded-sm flex flex-col"
        style={{ 
          borderColor: characterColor,
          backgroundColor: '#0a0a0a',
          boxShadow: `0 0 30px ${characterColor}40`
        }}
      >
        {/* Header */}
        <div 
          className="p-4 border-b flex items-center justify-between"
          style={{ borderColor: characterColor }}
        >
          <div className="flex items-center gap-3">
            <div 
              className="w-8 h-8 rounded-full flex items-center justify-center"
              style={{ 
                backgroundColor: characterColor,
                color: '#0a0a0a'
              }}
            >
              {characterInitials}
            </div>
            <div>
              <div className="font-crt text-sm flex items-center gap-2" style={{ color: characterColor }}>
                {characterName}
                {isConnected ? (
                  <span className="w-2 h-2 bg-green-400 rounded-full"></span>
                ) : (
                  <span className="w-2 h-2 bg-red-400 rounded-full animate-pulse"></span>
                )}
              </div>
              <div className="font-crt text-xs opacity-50" style={{ color: characterColor }}>
                {isConnected ? 'Real-time AI Streaming' : 'Connecting...'}
              </div>
            </div>
          </div>
          
          <button
            onClick={onClose}
            className="px-3 py-1 border font-crt text-sm transition-all hover:bg-opacity-20"
            style={{
              borderColor: characterColor,
              color: characterColor
            }}
          >
            [CLOSE]
          </button>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4 custom-scrollbar">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[80%] p-3 rounded-sm ${
                  message.type === 'user' 
                    ? 'border-l-4' 
                    : 'border-r-4'
                }`}
                style={{
                  borderColor: characterColor,
                  backgroundColor: message.type === 'user' 
                    ? `${characterColor}10` 
                    : `${characterColor}08`,
                  borderLeftColor: message.type === 'user' ? characterColor : 'transparent',
                  borderRightColor: message.type === 'character' ? characterColor : 'transparent'
                }}
              >
                <div className="font-crt text-sm whitespace-pre-wrap" style={{ color: characterColor }}>
                  {message.content}
                  {message.isStreaming && (
                    <span className="inline-block w-2 h-4 bg-current animate-pulse ml-1"></span>
                  )}
                </div>
                <div className="font-crt text-xs opacity-50 mt-2 flex justify-between" style={{ color: characterColor }}>
                  <span>{message.timestamp.toLocaleTimeString()}</span>
                  {message.type === 'character' && message.isStreaming && (
                    <span className="text-xs animate-pulse">Streaming...</span>
                  )}
                </div>
              </div>
            </div>
          ))}
          
          {isProcessing && !currentStreamingId && (
            <div className="flex justify-start">
              <div
                className="max-w-[80%] p-3 border-r-4 rounded-sm"
                style={{
                  borderColor: characterColor,
                  backgroundColor: `${characterColor}08`
                }}
              >
                <div className="font-crt text-sm flex items-center gap-2" style={{ color: characterColor }}>
                  <span>{characterName} is thinking</span>
                  <div className="flex gap-1">
                    <div className="w-1 h-1 bg-current rounded-full animate-pulse" style={{ animationDelay: '0ms' }} />
                    <div className="w-1 h-1 bg-current rounded-full animate-pulse" style={{ animationDelay: '200ms' }} />
                    <div className="w-1 h-1 bg-current rounded-full animate-pulse" style={{ animationDelay: '400ms' }} />
                  </div>
                </div>
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>

        {/* Connection Status */}
        {!isConnected && (
          <div 
            className="px-4 py-2 border-t text-center"
            style={{ borderColor: characterColor }}
          >
            <div className="font-crt text-xs opacity-50" style={{ color: characterColor }}>
              Connecting to AI backend... Make sure the server is running on localhost:8000
            </div>
          </div>
        )}

        {/* Quick Test Prompts */}
        <div 
          className="px-4 pt-2 border-t"
          style={{ borderColor: characterColor }}
        >
          <div className="text-xs font-crt opacity-50 mb-2" style={{ color: characterColor }}>
            Quick Tests:
          </div>
          <div className="grid grid-cols-2 gap-2 mb-3">
            <button
              onClick={() => setInputValue("What is consciousness?")}
              className="px-2 py-1 border font-crt text-xs hover:bg-opacity-10 transition-all"
              style={{ borderColor: characterColor, color: characterColor }}
            >
              Consciousness
            </button>
            <button
              onClick={() => setInputValue("Tell me about yourself")}
              className="px-2 py-1 border font-crt text-xs hover:bg-opacity-10 transition-all"
              style={{ borderColor: characterColor, color: characterColor }}
            >
              About You
            </button>
            <button
              onClick={() => setInputValue("What's happening in this story?")}
              className="px-2 py-1 border font-crt text-xs hover:bg-opacity-10 transition-all"
              style={{ borderColor: characterColor, color: characterColor }}
            >
              Story Context
            </button>
            <button
              onClick={() => setInputValue("Are you really an AI?")}
              className="px-2 py-1 border font-crt text-xs hover:bg-opacity-10 transition-all"
              style={{ borderColor: characterColor, color: characterColor }}
            >
              Meta Question
            </button>
          </div>
        </div>

        {/* Input */}
        <div className="px-4 pb-4">
          <div className="flex gap-2">
            <textarea
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder={`Ask ${characterName} anything...`}
              disabled={isProcessing || !isConnected}
              className="flex-1 p-3 bg-transparent border font-crt text-sm resize-none h-20
                         focus:outline-none focus:ring-2 disabled:opacity-50"
              style={{
                borderColor: characterColor,
                color: characterColor,
                backgroundColor: `${characterColor}05`
              }}
            />
            <button
              onClick={handleSendMessage}
              disabled={isProcessing || !inputValue.trim() || !isConnected}
              className="px-4 py-2 border font-crt text-sm transition-all self-end
                         disabled:opacity-50 disabled:cursor-not-allowed"
              style={{
                borderColor: characterColor,
                color: characterColor,
                backgroundColor: inputValue.trim() && isConnected ? `${characterColor}20` : 'transparent'
              }}
            >
              SEND
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default StreamingCharacterChat;