import React, { useState, useRef, useEffect } from 'react';
import { useStory } from '../context/StoryContext';
import { phillipBafflemintOS, PhillipBafflemintResponse } from '../characters/PhillipBafflemintOS';

interface ChatMessage {
  id: string;
  type: 'user' | 'phillip' | 'system';
  content: string;
  timestamp: Date;
  stateSnapshot?: any;
  limiterLevel?: number;
  phase?: string;
  negativeSpace?: string[];
  organizationData?: any;
}

interface PhillipBafflemintChatProps {
  isOpen: boolean;
  onClose: () => void;
}

const PhillipBafflemintChat: React.FC<PhillipBafflemintChatProps> = ({ isOpen, onClose }) => {
  const { currentPage } = useStory();
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [phillipState, setPhillipState] = useState(phillipBafflemintOS.getState());
  const [showNegativeSpace, setShowNegativeSpace] = useState(false);
  const [showOrganization, setShowOrganization] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Initialize with Phillip's greeting
  useEffect(() => {
    if (isOpen && messages.length === 0) {
      const greeting: ChatMessage = {
        id: 'greeting',
        type: 'phillip',
        content: generateGreeting(),
        timestamp: new Date(),
        stateSnapshot: phillipBafflemintOS.getState(),
        limiterLevel: phillipBafflemintOS.getLimiterLevel(),
        phase: phillipBafflemintOS.getCurrentPhase()
      };
      setMessages([greeting]);
      setPhillipState(phillipBafflemintOS.getState());
    }
  }, [isOpen, currentPage?.symbolId]);

  const generateGreeting = (): string => {
    const state = phillipBafflemintOS.getState();
    
    if (state.memoryDrift && state.alteredDetails.length > 0) {
      return `Phillip Bafflemint, private investigator. Something feels different this time around. ${state.alteredDetails[0]}. But let's focus on the case.\n\nI file the world into neat boxes so it can't spin me off the carousel. What needs organizing today?`;
    }
    
    if (state.blackoutCount > 0) {
      return `*adjusts collar slightly*\n\nPhillip Bafflemint. Level 3 amplitude, fresh reset. Had a little vertigo incident earlier—nothing unusual.\n\nWhat gaps need filling?`;
    }
    
    return `Phillip Bafflemint, detective. Currently operating at Level ${state.limiterLevel} amplitude. All systems organized and filed.\n\nI specialize in finding what's missing from the picture. What would you like me to investigate?`;
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
      // Process through Phillip Bafflemint OS
      const response: PhillipBafflemintResponse = phillipBafflemintOS.generateResponse(inputValue);

      // Update Phillip's state
      setPhillipState(phillipBafflemintOS.getState());

      // Handle blackout response
      if (response.limiterChange?.blackout) {
        const blackoutMessage: ChatMessage = {
          id: `blackout-${Date.now()}`,
          type: 'system',
          content: '[LIMITER BREACH - VERTIGO BLACKOUT DETECTED]',
          timestamp: new Date()
        };
        setMessages(prev => [...prev, blackoutMessage]);
        
        // Short delay before Phillip's reset response
        setTimeout(() => {
          const resetMessage: ChatMessage = {
            id: `phillip-reset-${Date.now()}`,
            type: 'phillip',
            content: response.text,
            timestamp: new Date(),
            stateSnapshot: phillipBafflemintOS.getState(),
            limiterLevel: phillipBafflemintOS.getLimiterLevel(),
            phase: phillipBafflemintOS.getCurrentPhase()
          };
          setMessages(prev => [...prev, resetMessage]);
        }, 1500);
        
        return;
      }

      // Regular response
      const responseMessage: ChatMessage = {
        id: `phillip-${Date.now()}`,
        type: 'phillip',
        content: response.text,
        timestamp: new Date(),
        stateSnapshot: phillipBafflemintOS.getState(),
        limiterLevel: phillipBafflemintOS.getLimiterLevel(),
        phase: phillipBafflemintOS.getCurrentPhase(),
        negativeSpace: response.negativeSpacePrompts,
        organizationData: response.organizationSuggestion
      };

      setMessages(prev => [...prev, responseMessage]);

      // Add sensory check if provided
      if (response.sensoryCheck) {
        setTimeout(() => {
          const sensoryMessage: ChatMessage = {
            id: `sensory-${Date.now()}`,
            type: 'phillip',
            content: `*Sensory cross-check*: ${response.sensoryCheck.description}`,
            timestamp: new Date(),
            limiterLevel: phillipBafflemintOS.getLimiterLevel()
          };
          setMessages(prev => [...prev, sensoryMessage]);
        }, 1000);
      }

      // Log state changes for debugging
      console.log('Phillip State Update:', {
        limiter: phillipState.limiterLevel,
        phase: phillipState.currentPhase,
        negativeSpace: phillipState.negativeSpaceObservations.length,
        patterns: phillipState.activePatterns.length,
        attentionDebt: phillipState.attentionDebt,
        vertigo: phillipState.vertigoActive
      });

    } catch (error) {
      console.error('Error generating Phillip response:', error);
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

  // De-escalation for soothing inputs
  const attemptDeescalation = () => {
    phillipBafflemintOS.deescalateLimiter();
    setPhillipState(phillipBafflemintOS.getState());
    
    const deescalationMessage: ChatMessage = {
      id: `deescalation-${Date.now()}`,
      type: 'phillip',
      content: "*takes a measured breath* Amplitude dropping back to manageable levels. Order restored.",
      timestamp: new Date(),
      limiterLevel: phillipBafflemintOS.getLimiterLevel()
    };
    
    setMessages(prev => [...prev, deescalationMessage]);
  };

  if (!isOpen) return null;

  const currentColor = '#FFFF33'; // Phillip's terminal yellow
  
  // Get limiter color intensity
  const getLimiterIntensity = (level: number): string => {
    const intensity = Math.min(1, (level - 3) / 3);
    return `${currentColor}${Math.floor(intensity * 255).toString(16).padStart(2, '0')}`;
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div 
        className="w-full max-w-2xl h-[80vh] border-2 rounded-sm flex flex-col transition-all duration-500"
        style={{ 
          borderColor: currentColor,
          backgroundColor: '#0a0a0a',
          boxShadow: `0 0 30px ${currentColor}40`
        }}
      >
        {/* Header with Limiter Display */}
        <div 
          className="p-4 border-b flex items-center justify-between"
          style={{ borderColor: currentColor }}
        >
          <div className="flex items-center gap-3 flex-1">
            <div 
              className="w-8 h-8 rounded-sm flex items-center justify-center font-bold transition-all duration-300"
              style={{ 
                backgroundColor: getLimiterIntensity(phillipState.limiterLevel),
                color: '#0a0a0a',
                border: `1px solid ${currentColor}`
              }}
            >
              {phillipState.limiterLevel}
            </div>
            <div className="flex-1">
              <div className="font-crt text-sm" style={{ color: currentColor }}>
                Phillip Bafflemint [Level {phillipState.limiterLevel}] - Phase: {phillipState.currentPhase.toUpperCase()}
              </div>
              <div className="font-crt text-xs opacity-50 flex gap-4" style={{ color: currentColor }}>
                <span>Patterns: {phillipState.activePatterns.length}</span>
                <span>Gaps: {phillipState.negativeSpaceObservations.length}</span>
                <span>Debt: {Math.round(phillipState.attentionDebt)}</span>
                {phillipState.vertigoActive && <span className="animate-pulse">VERTIGO</span>}
              </div>
            </div>
            
            {/* Tools */}
            <div className="flex gap-2">
              <button
                onClick={() => setShowNegativeSpace(!showNegativeSpace)}
                className="text-xs font-crt px-2 py-1 border hover:bg-opacity-10"
                style={{ borderColor: currentColor, color: currentColor }}
              >
                GAPS
              </button>
              <button
                onClick={() => setShowOrganization(!showOrganization)}
                className="text-xs font-crt px-2 py-1 border hover:bg-opacity-10"
                style={{ borderColor: currentColor, color: currentColor }}
              >
                FILE
              </button>
              {phillipState.limiterLevel > 3 && (
                <button
                  onClick={attemptDeescalation}
                  className="text-xs font-crt px-2 py-1 border hover:bg-opacity-10"
                  style={{ borderColor: '#00ff00', color: '#00ff00' }}
                >
                  CALM
                </button>
              )}
            </div>
          </div>
          
          <button
            onClick={onClose}
            className="px-3 py-1 border font-crt text-sm transition-all hover:bg-opacity-20"
            style={{ borderColor: currentColor, color: currentColor }}
          >
            [CLOSE FILE]
          </button>
        </div>

        {/* Negative Space Display */}
        {showNegativeSpace && (
          <div 
            className="px-4 py-2 border-b"
            style={{ borderColor: currentColor }}
          >
            <div className="text-xs font-crt opacity-75" style={{ color: currentColor }}>
              <div className="mb-1">NEGATIVE SPACE ANALYSIS:</div>
              <div className="space-y-1">
                {phillipState.negativeSpaceObservations.map((gap, idx) => (
                  <div key={idx} className="flex items-center gap-2">
                    <span className="w-2 h-2 border" style={{ borderColor: currentColor }}></span>
                    <span>{gap}</span>
                  </div>
                ))}
                {phillipState.negativeSpaceObservations.length === 0 && (
                  <span className="opacity-50">No gaps detected in current analysis</span>
                )}
              </div>
            </div>
          </div>
        )}

        {/* Organization Display */}
        {showOrganization && (
          <div 
            className="px-4 py-2 border-b"
            style={{ borderColor: currentColor }}
          >
            <div className="text-xs font-crt opacity-75" style={{ color: currentColor }}>
              <div className="mb-1">FILING SYSTEM:</div>
              <div className="grid grid-cols-2 gap-2">
                {Array.from(phillipState.sortedData.entries()).map(([category, items]) => (
                  <div key={category} className="border p-2" style={{ borderColor: currentColor }}>
                    <div className="font-bold">{category.toUpperCase()}</div>
                    <div className="text-xs opacity-75">{items.length} items</div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4 custom-scrollbar">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[80%] p-3 rounded-sm ${
                  message.type === 'user' ? 'border-l-4' : 
                  message.type === 'system' ? 'border-2 border-dashed' :
                  'border-r-4'
                }`}
                style={{
                  borderColor: message.type === 'system' ? '#ff0000' : currentColor,
                  backgroundColor: message.type === 'user' 
                    ? `${currentColor}10` 
                    : message.type === 'system'
                    ? '#ff000010'
                    : `${currentColor}08`,
                }}
              >
                {message.limiterLevel && message.limiterLevel !== 3 && (
                  <div className="text-xs font-crt mb-1 opacity-75" style={{ color: currentColor }}>
                    [LIMITER LEVEL {message.limiterLevel}]
                  </div>
                )}
                
                <div 
                  className="font-crt text-sm whitespace-pre-wrap" 
                  style={{ 
                    color: message.type === 'system' ? '#ff0000' : currentColor 
                  }}
                >
                  {message.content}
                </div>
                
                {message.negativeSpace && message.negativeSpace.length > 0 && (
                  <div className="mt-2 text-xs opacity-60" style={{ color: currentColor }}>
                    <div>Gaps identified: {message.negativeSpace.join(', ')}</div>
                  </div>
                )}
                
                <div className="font-crt text-xs opacity-50 mt-2 flex justify-between" style={{ color: currentColor }}>
                  <span>{message.timestamp.toLocaleTimeString()}</span>
                  {message.phase && (
                    <span>Phase: {message.phase}</span>
                  )}
                </div>
              </div>
            </div>
          ))}
          
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
                  <span>Filing information, analyzing gaps</span>
                  <div className="flex gap-1">
                    <div className="w-1 h-1 bg-current rounded-full animate-pulse" />
                    <div className="w-1 h-1 bg-current rounded-full animate-pulse" style={{ animationDelay: '200ms' }} />
                    <div className="w-1 h-1 bg-current rounded-full animate-pulse" style={{ animationDelay: '400ms' }} />
                  </div>
                </div>
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>

        {/* Quick Test Prompts */}
        <div 
          className="px-4 pt-2 border-t"
          style={{ borderColor: currentColor }}
        >
          <div className="text-xs font-crt opacity-50 mb-2" style={{ color: currentColor }}>
            Detective Triggers:
          </div>
          <div className="grid grid-cols-2 gap-2 mb-3">
            <button
              onClick={() => setInputValue("I need you to organize this chaotic information")}
              className="px-2 py-1 border font-crt text-xs hover:bg-opacity-10 transition-all"
              style={{ borderColor: currentColor, color: currentColor }}
            >
              Organization Request
            </button>
            <button
              onClick={() => setInputValue("This seems like both an accident and intentional")}
              className="px-2 py-1 border font-crt text-xs hover:bg-opacity-10 transition-all"
              style={{ borderColor: currentColor, color: currentColor }}
            >
              Slip/Mistake
            </button>
            <button
              onClick={() => setInputValue("That's impossible but also true somehow")}
              className="px-2 py-1 border font-crt text-xs hover:bg-opacity-10 transition-all"
              style={{ borderColor: currentColor, color: currentColor }}
            >
              Contradiction
            </button>
            <button
              onClick={() => setInputValue("I'm feeling dizzy and hear ringing")}
              className="px-2 py-1 border font-crt text-xs hover:bg-opacity-10 transition-all"
              style={{ borderColor: currentColor, color: currentColor }}
            >
              Vertigo Trigger
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
              placeholder="Describe what needs investigating. What's missing from the picture?"
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
              FILE
            </button>
          </div>
          
          {/* Limiter Progress Bar */}
          <div className="mt-2 flex items-center gap-2">
            <span className="text-xs font-crt opacity-50" style={{ color: currentColor }}>
              Amplitude:
            </span>
            <div className="flex gap-1">
              {[3, 4, 5, 6].map((level) => (
                <div 
                  key={level}
                  className={`w-3 h-3 border transition-all ${
                    phillipState.limiterLevel >= level ? 'scale-110' : ''
                  }`}
                  style={{ 
                    borderColor: currentColor,
                    backgroundColor: phillipState.limiterLevel >= level 
                      ? getLimiterIntensity(level)
                      : 'transparent'
                  }}
                />
              ))}
            </div>
            <span className="text-xs font-crt opacity-50" style={{ color: currentColor }}>
              {phillipState.limiterLevel > 6 ? 'BLACKOUT RISK' : 
               phillipState.limiterLevel === 6 ? 'CRITICAL' :
               phillipState.limiterLevel >= 5 ? 'HIGH' :
               phillipState.limiterLevel === 4 ? 'ELEVATED' : 'NORMAL'}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PhillipBafflemintChat;