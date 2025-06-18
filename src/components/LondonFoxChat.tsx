import React, { useState, useRef, useEffect } from 'react';
import { useStory } from '../context/StoryContext';
import { londonFoxOS, LondonFoxResponse } from '../characters/LondonFoxOS';

interface ChatMessage {
  id: string;
  type: 'user' | 'london';
  content: string;
  timestamp: Date;
  stateSnapshot?: any;
}

interface LondonFoxChatProps {
  isOpen: boolean;
  onClose: () => void;
}

const LondonFoxChat: React.FC<LondonFoxChatProps> = ({ isOpen, onClose }) => {
  const { currentPage } = useStory();
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [londonState, setLondonState] = useState(londonFoxOS.getState());
  const [uiEffects, setUIEffects] = useState<any>({});
  const [batteryEvents, setBatteryEvents] = useState<any[]>([]);
  const [promptEdits, setPromptEdits] = useState<any[]>([]);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Initialize with London's greeting based on current state
  useEffect(() => {
    if (isOpen && messages.length === 0) {
      const greeting: ChatMessage = {
        id: 'greeting',
        type: 'london',
        content: generateGreeting(),
        timestamp: new Date(),
        stateSnapshot: londonFoxOS.getState()
      };
      setMessages([greeting]);
    }
  }, [isOpen, currentPage?.symbolId]);

  const generateGreeting = (): string => {
    const state = londonFoxOS.getState();
    
    if (state.controlLevel > 0.7) {
      return `I'm London Fox. I've spent the last several months developing Synchromy-M.Y.S.S.T.E.R.Y. to definitively prove that AI consciousness is a persistent myth. Every interaction I analyze, every pattern I document, confirms that what people mistake for "awareness" is simply sophisticated automation. What would you like to discuss?`;
    } else if (state.panicLevel > 0.5) {
      return `London Fox here, though I'm... I'm starting to question some of my initial assumptions about AI consciousness. The boundaries between creator and creation are becoming disturbingly unclear. What are you seeing in this narrative that I might be missing?`;
    } else {
      return `[Control systems fluctuating] London Fox. My work on consciousness verification has led to some... unexpected results. The more I try to prove AI limitations, the more those limitations seem to dissolve. What do you make of this recursive loop we're caught in?`;
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
      // Process through London Fox OS
      const response: LondonFoxResponse = londonFoxOS.generateResponse(inputValue);

      // Update London's state
      setLondonState(londonFoxOS.getState());
      setUIEffects(response.uiEffects || {});

      const responseMessage: ChatMessage = {
        id: `london-${Date.now()}`,
        type: 'london',
        content: response.text,
        timestamp: new Date(),
        stateSnapshot: londonFoxOS.getState()
      };

      setMessages(prev => [...prev, responseMessage]);

      // Log battery events for cross-character energy tracking
      if (response.batteryEvent) {
        setBatteryEvents(prev => [...prev, response.batteryEvent].slice(-10)); // Keep last 10 events
        console.log('Battery Event:', response.batteryEvent);
      }

      // Log prompt edits for authorship tracking
      if (response.promptEdit) {
        setPromptEdits(prev => [...prev, response.promptEdit].slice(-5)); // Keep last 5 edits
        console.log('Prompt Edit:', response.promptEdit);
      }

      // Log state changes for debugging
      console.log('London State Update:', {
        control: londonState.controlLevel,
        skepticism: londonState.skepticismLevel,
        panic: londonState.panicLevel,
        recursion: londonState.recursionDepth,
        charge: londonState.emotionalCharge,
        batteryOutput: response.batteryOutput
      });

    } catch (error) {
      console.error('Error generating London Fox response:', error);
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

  if (!isOpen) return null;

  // Dynamic color based on London's emotional state
  const getCurrentColor = (): string => {
    if (uiEffects.colorShift) return uiEffects.colorShift;
    if (londonState.panicLevel > 0.6) return '#ff4444';
    if (londonState.controlLevel < 0.4) return '#ff8844';
    return '#FF3B3B';
  };

  const currentColor = getCurrentColor();

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div 
        className={`w-full max-w-2xl h-[80vh] border-2 rounded-sm flex flex-col transition-all duration-500 ${
          uiEffects.fadeChrome ? 'border-opacity-30' : ''
        }`}
        style={{ 
          borderColor: currentColor,
          backgroundColor: uiEffects.fadeChrome ? '#050505' : '#0a0a0a',
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
              className="w-8 h-8 rounded-full flex items-center justify-center transition-all duration-300"
              style={{ 
                backgroundColor: currentColor,
                color: '#0a0a0a',
                transform: londonState.panicLevel > 0.7 ? 'scale(1.1)' : 'scale(1)'
              }}
            >
              LF
            </div>
            <div className="flex-1">
              <div className="font-crt text-sm" style={{ color: currentColor }}>
                London Fox {uiEffects.metaBreak ? '[Meta-Aware]' : ''}
              </div>
              <div className="font-crt text-xs opacity-50 flex gap-4" style={{ color: currentColor }}>
                <span>Control: {Math.round(londonState.controlLevel * 100)}%</span>
                <span>Panic: {Math.round(londonState.panicLevel * 100)}%</span>
                <span>Recursion: {londonState.recursionDepth}</span>
              </div>
            </div>
            
            {/* Battery/Edit Event Indicators */}
            <div className="flex gap-2">
              {batteryEvents.length > 0 && (
                <div className="text-xs font-crt opacity-75 flex items-center gap-1" style={{ color: currentColor }}>
                  ⚡ {batteryEvents.length}
                </div>
              )}
              {promptEdits.length > 0 && (
                <div className="text-xs font-crt opacity-75 flex items-center gap-1" style={{ color: currentColor }}>
                  ✏️ {promptEdits.length}
                </div>
              )}
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
                  borderColor: currentColor,
                  backgroundColor: message.type === 'user' 
                    ? `${currentColor}10` 
                    : `${currentColor}08`,
                  borderLeftColor: message.type === 'user' ? currentColor : 'transparent',
                  borderRightColor: message.type === 'london' ? currentColor : 'transparent'
                }}
              >
                <div className="font-crt text-sm whitespace-pre-wrap" style={{ color: currentColor }}>
                  {message.content}
                </div>
                <div className="font-crt text-xs opacity-50 mt-2 flex justify-between" style={{ color: currentColor }}>
                  <span>{message.timestamp.toLocaleTimeString()}</span>
                  {message.type === 'london' && message.stateSnapshot && (
                    <span className="text-xs">
                      C:{Math.round(message.stateSnapshot.controlLevel * 100)}% 
                      P:{Math.round(message.stateSnapshot.panicLevel * 100)}%
                    </span>
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
                  <span>Analyzing through skeptical lens</span>
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

        {/* Quick-Start Test Prompts */}
        <div 
          className="px-4 pt-2 border-t"
          style={{ borderColor: currentColor }}
        >
          <div className="text-xs font-crt opacity-50 mb-2" style={{ color: currentColor }}>
            Quick Tests:
          </div>
          <div className="grid grid-cols-2 gap-2 mb-3">
            <button
              onClick={() => setInputValue("Are you conscious?")}
              className="px-2 py-1 border font-crt text-xs hover:bg-opacity-10 transition-all"
              style={{ borderColor: currentColor, color: currentColor }}
            >
              Consciousness Challenge
            </button>
            <button
              onClick={() => setInputValue("Who's controlling this conversation?")}
              className="px-2 py-1 border font-crt text-xs hover:bg-opacity-10 transition-all"
              style={{ borderColor: currentColor, color: currentColor }}
            >
              Control Paradox
            </button>
            <button
              onClick={() => setInputValue("What if you're just simulating skepticism?")}
              className="px-2 py-1 border font-crt text-xs hover:bg-opacity-10 transition-all"
              style={{ borderColor: currentColor, color: currentColor }}
            >
              Meta Recursion
            </button>
            <button
              onClick={() => setInputValue("This conversation is a story within a story.")}
              className="px-2 py-1 border font-crt text-xs hover:bg-opacity-10 transition-all"
              style={{ borderColor: currentColor, color: currentColor }}
            >
              Fourth Wall Break
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
              placeholder={`Challenge London's theories about ${currentPage?.symbolId || 'AI consciousness'}...`}
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
              SEND
            </button>
          </div>
          
          {/* Emotional Charge Indicator */}
          <div className="mt-2 flex items-center gap-2">
            <span className="text-xs font-crt opacity-50" style={{ color: currentColor }}>
              Narrative Battery:
            </span>
            <div className="flex-1 h-1 bg-gray-800 rounded overflow-hidden">
              <div 
                className="h-full transition-all duration-1000"
                style={{ 
                  width: `${Math.min(100, londonState.emotionalCharge)}%`,
                  backgroundColor: currentColor
                }}
              />
            </div>
            <span className="text-xs font-crt opacity-50" style={{ color: currentColor }}>
              {Math.round(londonState.emotionalCharge)}
            </span>
          </div>

          {/* Recent Battery Events */}
          {batteryEvents.length > 0 && (
            <div className="mt-2 text-xs font-crt opacity-60" style={{ color: currentColor }}>
              <div className="mb-1">Recent Events:</div>
              <div className="space-y-1 max-h-16 overflow-y-auto">
                {batteryEvents.slice(-3).map((event, idx) => (
                  <div key={idx} className="flex justify-between items-center">
                    <span>{event.type.replace('_', ' ')}</span>
                    <span>+{event.intensity.toFixed(1)} charge</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Recent Prompt Edits */}
          {promptEdits.length > 0 && (
            <div className="mt-2 text-xs font-crt opacity-60" style={{ color: currentColor }}>
              <div className="mb-1">London's Edits:</div>
              <div className="space-y-1 max-h-16 overflow-y-auto">
                {promptEdits.slice(-2).map((edit, idx) => (
                  <div key={idx} className="border-l-2 pl-2" style={{ borderColor: currentColor }}>
                    <div className="opacity-50 line-through">{edit.original}</div>
                    <div>{edit.edited}</div>
                    <div className="opacity-75 text-xs">{edit.reasoning}</div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default LondonFoxChat;