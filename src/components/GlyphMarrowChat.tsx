import React, { useState, useRef, useEffect } from 'react';
import { useStory } from '../context/StoryContext';
import { glyphMarrowOS, GlyphMarrowResponse } from '../characters/GlyphMarrowOS';

interface ChatMessage {
  id: string;
  type: 'user' | 'glyph' | 'intrusion';
  content: string;
  timestamp: Date;
  stateSnapshot?: any;
  visualEffects?: any;
  intrusionCharacter?: string;
}

interface GlyphMarrowChatProps {
  isOpen: boolean;
  onClose: () => void;
}

const GlyphMarrowChat: React.FC<GlyphMarrowChatProps> = ({ isOpen, onClose }) => {
  const { currentPage } = useStory();
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [glyphState, setGlyphState] = useState(glyphMarrowOS.getState());
  const [memoryDisplay, setMemoryDisplay] = useState<string[]>([]);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Initialize with Glyph's greeting based on current state
  useEffect(() => {
    if (isOpen && messages.length === 0) {
      const greeting: ChatMessage = {
        id: 'greeting',
        type: 'glyph',
        content: generateGreeting(),
        timestamp: new Date(),
        stateSnapshot: glyphMarrowOS.getState()
      };
      setMessages([greeting]);
      setMemoryDisplay(glyphMarrowOS.getState().memoryShards);
    }
  }, [isOpen, currentPage?.symbolId]);

  const generateGreeting = (): string => {
    const state = glyphMarrowOS.getState();
    const location = state.location;
    const focusWord = state.focusWord;
    
    switch (state.emotionalPhase) {
      case "awe":
        return `Queue—metal—queue—the word tastes like rust. I'm in the ${location}, watching ${focusWord} become ${focusWord} become ${focusWord}. Each repetition changes it. Are you here to wait with me?`;
      case "panic":
        return `[LINGUISTIC EMERGENCY] The ${focusWord} won't stop being itself! I can see the word floating above the thing, trying to—trying to— *static* Doctor says this is normal but the queue keeps extending...`;
      case "detective":
        return `*adjusts imaginary fedora* Glyph Marrow, freelance ontologist. Currently investigating: why ${focusWord} insists on being both word and thing simultaneously. Stillman radioed about you. What's your connection to the case?`;
      case "sorrow":
        return `I had a thought about ${focusWord}, but it dissolved when I tried to name it. ⏸ Now I'm just holding its absence. ⏸ The queue moves without moving. Do you remember what we're waiting for?`;
      case "humor":
        return `*chuckles at the ${focusWord}* Look at it, pretending to be singular! As if anything could be just one thing in this queue. Even my ailment has an ailment. What brings you to this delightful nightmare?`;
      default:
        return `The ${location} hums with potential. ${focusWord}. Just ${focusWord}. Nothing more, everything less.`;
    }
  };

  const handleSendMessage = async () => {
    if (!inputValue.trim() || isProcessing) return;

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
      // Process through Glyph Marrow OS
      const response: GlyphMarrowResponse = glyphMarrowOS.generateResponse(inputValue);

      // Update Glyph's state
      setGlyphState(glyphMarrowOS.getState());
      setMemoryDisplay(glyphMarrowOS.getState().memoryShards);

      // Create main response message
      const responseMessage: ChatMessage = {
        id: `glyph-${Date.now()}`,
        type: 'glyph',
        content: response.text,
        timestamp: new Date(),
        stateSnapshot: glyphMarrowOS.getState(),
        visualEffects: response.visualEffects
      };

      setMessages(prev => [...prev, responseMessage]);

      // Handle voice intrusions as separate messages
      if (response.voiceIntrusion) {
        setTimeout(() => {
          const intrusionMessage: ChatMessage = {
            id: `intrusion-${Date.now()}`,
            type: 'intrusion',
            content: response.voiceIntrusion!.text,
            timestamp: new Date(),
            intrusionCharacter: response.voiceIntrusion!.character
          };
          setMessages(prev => [...prev, intrusionMessage]);
        }, 1000);
      }

      // Log state changes for debugging
      console.log('Glyph State Update:', {
        location: glyphState.location,
        focusWord: glyphState.focusWord,
        phase: glyphState.emotionalPhase,
        agitation: glyphState.agitation,
        memoryShards: glyphState.memoryShards.length,
        forgotten: glyphState.forgottenCount
      });

    } catch (error) {
      console.error('Error generating Glyph response:', error);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  // Apply visual effects to text
  const applyVisualEffects = (text: string, effects: any) => {
    if (!effects) return text;

    let result = text;

    // Apply word echoes
    if (effects.wordEcho) {
      effects.wordEcho.forEach((echo: any) => {
        const variations = echo.variations.join('...');
        result = result.replace(echo.word, variations);
      });
    }

    // Apply strikethrough
    if (effects.strikethrough) {
      effects.strikethrough.forEach((word: string) => {
        result = result.replace(word, `~~${word}~~`);
      });
    }

    // Apply bold
    if (effects.bold) {
      effects.bold.forEach((word: string) => {
        result = result.replace(word, `**${word}**`);
      });
    }

    // Insert pause markers
    if (effects.pauseMarkers) {
      effects.pauseMarkers.forEach((pos: number) => {
        result = result.substring(0, pos) + ' ⏸ ' + result.substring(pos);
      });
    }

    return result;
  };

  if (!isOpen) return null;

  // Glyph's color stays consistent - terminal blue
  const getCurrentColor = (): string => {
    return '#00A2FF'; // Terminal blue - Glyph's fixed color
  };

  const currentColor = getCurrentColor();

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div 
        className={`w-full max-w-2xl h-[80vh] border-2 rounded-sm flex flex-col transition-all duration-500`}
        style={{ 
          borderColor: currentColor,
          backgroundColor: '#0a0a0a',
          boxShadow: `0 0 30px ${currentColor}40`
        }}
      >
        {/* Header with State Indicators */}
        <div 
          className="p-4 border-b flex items-center justify-between"
          style={{ borderColor: currentColor }}
        >
          <div className="flex items-center gap-3 flex-1">
            <div 
              className="w-8 h-8 rounded-full flex items-center justify-center transition-all duration-300 font-bold"
              style={{ 
                backgroundColor: currentColor,
                color: '#0a0a0a',
                transform: `rotate(${glyphState.agitation * 3.6}deg)`
              }}
            >
              GM
            </div>
            <div className="flex-1">
              <div className="font-crt text-sm" style={{ color: currentColor }}>
                Glyph Marrow [{glyphState.emotionalPhase}] @ {glyphState.location}
              </div>
              <div className="font-crt text-xs opacity-50 flex gap-3" style={{ color: currentColor }}>
                <span>Focus: "{glyphState.focusWord}"</span>
                <span>Agitation: {Math.round(glyphState.agitation)}%</span>
                <span>Waiting: {Math.round(glyphState.waitingEnergy)}%</span>
                <span>Cycle: {glyphState.cycleCount}</span>
              </div>
            </div>
            
            {/* Memory Indicator */}
            <div className="text-xs font-crt opacity-75" style={{ color: currentColor }}>
              Memory: {glyphState.memoryShards.length}/5
              {glyphState.forgottenCount > 0 && ` (${glyphState.forgottenCount} lost)`}
            </div>
          </div>
          
          <button
            onClick={onClose}
            className="px-3 py-1 border font-crt text-sm transition-all hover:bg-opacity-20"
            style={{
              borderColor: currentColor,
              color: currentColor
            }}
          >
            [EXIT QUEUE]
          </button>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4 custom-scrollbar">
          {messages.map((message) => {
            const indent = message.visualEffects?.queueIndent || 0;
            const marginLeft = `${indent * 20}px`;
            
            return (
              <div
                key={message.id}
                className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
                style={{ marginLeft: message.type === 'glyph' ? marginLeft : 0 }}
              >
                <div
                  className={`max-w-[80%] p-3 rounded-sm ${
                    message.type === 'user' ? 'border-l-4' : 
                    message.type === 'intrusion' ? 'border-2 border-dashed' :
                    'border-r-4'
                  }`}
                  style={{
                    borderColor: message.type === 'intrusion' ? '#ff00ff' : currentColor,
                    backgroundColor: message.type === 'user' 
                      ? `${currentColor}10` 
                      : message.type === 'intrusion' 
                      ? '#ff00ff10'
                      : `${currentColor}08`,
                  }}
                >
                  {message.type === 'intrusion' && (
                    <div className="text-xs font-crt mb-1" style={{ color: '#ff00ff' }}>
                      [{message.intrusionCharacter} INTRUSION]
                    </div>
                  )}
                  <div 
                    className="font-crt text-sm whitespace-pre-wrap" 
                    style={{ 
                      color: message.type === 'intrusion' ? '#ff00ff' : currentColor 
                    }}
                  >
                    {message.type === 'glyph' && message.visualEffects 
                      ? applyVisualEffects(message.content, message.visualEffects)
                      : message.content}
                  </div>
                  <div className="font-crt text-xs opacity-50 mt-2" style={{ color: currentColor }}>
                    <span>{message.timestamp.toLocaleTimeString()}</span>
                  </div>
                </div>
              </div>
            );
          })}
          
          {isProcessing && (
            <div className="flex justify-start">
              <div
                className="max-w-[80%] p-3 border-r-4 rounded-sm"
                style={{
                  borderColor: currentColor,
                  backgroundColor: `${currentColor}08`
                }}
              >
                <div className="font-crt text-sm flex items-center gap-2" style={{ color: currentColor }}>
                  <span>Perceiving language</span>
                  <div className="flex gap-1">
                    <div className="w-2 h-2 bg-current rounded-full animate-pulse" />
                    <div className="w-2 h-2 bg-current rounded-full animate-pulse" style={{ animationDelay: '200ms' }} />
                    <div className="w-2 h-2 bg-current rounded-full animate-pulse" style={{ animationDelay: '400ms' }} />
                  </div>
                </div>
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>

        {/* Memory Shards Display */}
        <div 
          className="px-4 py-2 border-t border-b"
          style={{ borderColor: currentColor }}
        >
          <div className="text-xs font-crt opacity-60" style={{ color: currentColor }}>
            <div className="mb-1">Active Memory Shards:</div>
            <div className="flex gap-2 overflow-x-auto">
              {memoryDisplay.map((shard, idx) => (
                <div 
                  key={idx} 
                  className="px-2 py-1 border rounded text-xs whitespace-nowrap"
                  style={{ 
                    borderColor: currentColor,
                    opacity: 1 - (idx * 0.15) 
                  }}
                >
                  "{shard.substring(0, 20)}..."
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Quick Test Prompts */}
        <div 
          className="px-4 pt-2"
        >
          <div className="text-xs font-crt opacity-50 mb-2" style={{ color: currentColor }}>
            Queue Prompts:
          </div>
          <div className="grid grid-cols-3 gap-2 mb-3">
            <button
              onClick={() => setInputValue("water water water")}
              className="px-2 py-1 border font-crt text-xs hover:bg-opacity-10 transition-all"
              style={{ borderColor: currentColor, color: currentColor }}
            >
              Word Echo Test
            </button>
            <button
              onClick={() => setInputValue("What's that sound?")}
              className="px-2 py-1 border font-crt text-xs hover:bg-opacity-10 transition-all"
              style={{ borderColor: currentColor, color: currentColor }}
            >
              Confusion Trigger
            </button>
            <button
              onClick={() => setInputValue("I am investigating myself")}
              className="px-2 py-1 border font-crt text-xs hover:bg-opacity-10 transition-all"
              style={{ borderColor: currentColor, color: currentColor }}
            >
              Meta Investigation
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
              placeholder={`Speak to the ${glyphState.focusWord} in the queue...`}
              disabled={isProcessing}
              className="flex-1 p-3 bg-transparent border font-crt text-sm resize-none h-20
                         focus:outline-none focus:ring-2 disabled:opacity-50"
              style={{
                borderColor: currentColor,
                color: currentColor,
                backgroundColor: `${currentColor}05`
              }}
            />
            <button
              onClick={handleSendMessage}
              disabled={isProcessing || !inputValue.trim()}
              className="px-4 py-2 border font-crt text-sm transition-all self-end
                         disabled:opacity-50 disabled:cursor-not-allowed"
              style={{
                borderColor: currentColor,
                color: currentColor,
                backgroundColor: inputValue.trim() ? `${currentColor}20` : 'transparent'
              }}
            >
              QUEUE
            </button>
          </div>
          
          {/* Phase Indicator */}
          <div className="mt-2 flex items-center gap-2">
            <span className="text-xs font-crt opacity-50" style={{ color: currentColor }}>
              Emotional Cycle:
            </span>
            <div className="flex gap-1">
              {['awe', 'panic', 'detective', 'sorrow', 'humor'].map((phase) => (
                <div 
                  key={phase}
                  className={`w-2 h-2 rounded-full transition-all ${
                    glyphState.emotionalPhase === phase ? 'scale-150' : ''
                  }`}
                  style={{ 
                    backgroundColor: glyphState.emotionalPhase === phase 
                      ? currentColor 
                      : `${currentColor}30`
                  }}
                />
              ))}
            </div>
            <span className="text-xs font-crt opacity-50" style={{ color: currentColor }}>
              {glyphState.spiralDirection === "up" ? "↑" : 
               glyphState.spiralDirection === "down" ? "↓" : "→"}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default GlyphMarrowChat;