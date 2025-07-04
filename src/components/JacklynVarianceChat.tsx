import React, { useState, useRef, useEffect } from 'react';
import { useStory } from '../context/StoryContext';
// Removed old simulation import - now using WebSocket backend only

interface ChatMessage {
  id: string;
  type: 'user' | 'jacklyn' | 'ghost' | 'split';
  content: string;
  timestamp: Date;
  metadata?: {
    jv_pass: "first" | "second";
    mode: string;
    draftNumber: number;
    biasLevel: number;
    timestamp: string;
  };
  ghostAnnotations?: any[];
  splitOptions?: any;
  visualEffects?: any;
  biasDisclosure?: string[];
}

interface JacklynVarianceChatProps {
  isOpen: boolean;
  onClose: () => void;
}

const JacklynVarianceChat: React.FC<JacklynVarianceChatProps> = ({ isOpen, onClose }) => {
  const { currentPage } = useStory();
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [jacklynState, setJacklynState] = useState({
    currentPass: "first",
    currentMode: "neutral", 
    draftCount: 1,
    griefLevel: 0.3,
    revealedBiases: [],
    hiddenBiases: [],
    ghostAnnotations: [],
    activeSplits: []
  });
  const [showGhostPanel, setShowGhostPanel] = useState(false);
  const [showBiasPanel, setShowBiasPanel] = useState(false);
  const [activeSplit, setActiveSplit] = useState<any>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Initialize with Jacklyn's greeting
  useEffect(() => {
    if (isOpen && messages.length === 0) {
      const greeting: ChatMessage = {
        id: 'greeting',
        type: 'jacklyn',
        content: generateGreeting(),
        timestamp: new Date(),
        metadata: {
          jv_pass: "first",
          mode: "neutral",
          draftNumber: 1,
          biasLevel: 0.3,
          timestamp: "15:07"
        }
      };
      setMessages([greeting]);
      // State updated via WebSocket responses
    }
  }, [isOpen, currentPage?.symbolId]);

  const generateGreeting = (): string => {
    return `⟢ ${new Date().getHours().toString().padStart(2, '0')}:${new Date().getMinutes().toString().padStart(2, '0')} ▸ Draft 1

D.A.D.D.Y.S-H.A.R.D #001 — Analysis Report
Subject: Initial Contact Protocol

Data-and-Detection analyst Jacklyn Variance reporting for surveillance duty. All interactions logged for pattern analysis. Current systems operational, ready for query processing.

Recommend immediate engagement with analysis protocols. Standard procedures involve multi-pass evaluation - preliminary observations followed by recursive verification loops.

—JV`;
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
    const currentInput = inputValue;
    setInputValue('');
    setIsProcessing(true);

    try {
      // Use the new /api/ask endpoint
      console.log('🎭 SENDING TO JACKLYN BACKEND:', {
        message: currentInput,
        characterId: 'jacklyn-variance', 
        pageId: currentPage?.symbolId
      });

      const response = await fetch('/api/v1/ask', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: currentInput,
          character_id: 'jacklyn-variance',
          current_page_id: currentPage?.symbolId,
          include_example: false
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();
      
      // Create response message with backend data
      const responseMessage: ChatMessage = {
        id: `jacklyn-${Date.now()}`,
        type: 'jacklyn',
        content: data.answer,
        timestamp: new Date(),
        metadata: {
          jv_pass: "backend",
          mode: "D.A.D.D.Y.S-H.A.R.D",
          draftNumber: data.context_used || 1,
          biasLevel: 0.8, // Backend processed
          timestamp: new Date().toLocaleTimeString()
        }
      };

      setMessages(prev => [...prev, responseMessage]);
      setIsProcessing(false);

      // Log processing stats
      console.log('✅ Jacklyn response received:', {
        processingTime: data.processing_time_ms,
        contextUsed: data.context_used,
        modelInfo: data.model_info
      });

    } catch (error) {
      console.error('Error communicating with Jacklyn backend:', error);
      setIsProcessing(false);
      
      // Error message in Jacklyn's voice
      const errorMessage: ChatMessage = {
        id: `jacklyn-error-${Date.now()}`,
        type: 'jacklyn',
        content: `D.A.D.D.Y.S-H.A.R.D #COMM_ERROR — Analysis Report
Subject: Communication Failure

Unable to establish connection with analysis backend. Network pathways compromised. Error: ${error.message}

The tunnels echo with static. Preston would have known how to fix this.

—JV`,
        timestamp: new Date(),
        metadata: {
          jv_pass: "error",
          mode: "error", 
          draftNumber: 1,
          biasLevel: 0,
          timestamp: new Date().toLocaleTimeString()
        }
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

  // Handle split branch selection
  const selectSplitBranch = (branch: 'A' | 'B' | 'both') => {
    let followUp = '';
    
    if (branch === 'A') {
      followUp = activeSplit.branchA;
    } else if (branch === 'B') {
      followUp = activeSplit.branchB;
    } else {
      followUp = "Traveling both paths in parallel. Interesting...";
    }
    
    setInputValue(followUp);
    setActiveSplit(null);
  };

  // Manual mode switches - now handled by backend
  const switchMode = (mode: string) => {
    console.log(`Mode switch requested: ${mode} - will be handled by backend WebSocket`);
    // Mode switching now handled by backend character implementation
  };

  if (!isOpen) return null;

  const currentColor = '#FF00FF'; // Jacklyn's magenta
  
  // Get mode color
  const getModeColor = (mode: string): string => {
    switch (mode) {
      case 'report': return '#00FFFF';
      case 'aside': return '#FFB000';
      case 'haunt': return '#7A3CFF';
      case 'split': return '#00FF00';
      case 'bias': return '#FF3434';
      default: return currentColor;
    }
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
        {/* Header with Draft/Pass Indicators */}
        <div 
          className="p-4 border-b flex items-center justify-between"
          style={{ borderColor: currentColor }}
        >
          <div className="flex items-center gap-3 flex-1">
            <div 
              className="w-8 h-8 rounded-sm flex items-center justify-center font-bold transition-all duration-300"
              style={{ 
                backgroundColor: getModeColor(jacklynState.currentMode),
                color: '#0a0a0a',
                border: `1px solid ${currentColor}`
              }}
            >
              JV
            </div>
            <div className="flex-1">
              <div className="font-crt text-sm" style={{ color: currentColor }}>
                Jacklyn Variance [{jacklynState.currentMode.toUpperCase()}] - Draft {jacklynState.draftCount}
              </div>
              <div className="font-crt text-xs opacity-50 flex gap-4" style={{ color: currentColor }}>
                <span>Pass: {jacklynState.currentPass}</span>
                <span>Grief: {Math.round(jacklynState.griefLevel * 100)}%</span>
                <span>Biases: {jacklynState.revealedBiases.length}R/{jacklynState.hiddenBiases.length}H</span>
                <span>Splits: {jacklynState.activeSplits.length}</span>
              </div>
            </div>
            
            {/* Mode Controls */}
            <div className="flex gap-1">
              <button
                onClick={() => switchMode('report')}
                className="text-xs font-crt px-1 py-1 border hover:bg-opacity-10"
                style={{ borderColor: '#00FFFF', color: '#00FFFF' }}
                title="/report mode"
              >
                RPT
              </button>
              <button
                onClick={() => switchMode('aside')}
                className="text-xs font-crt px-1 py-1 border hover:bg-opacity-10"
                style={{ borderColor: '#FFB000', color: '#FFB000' }}
                title="/aside mode"
              >
                ASI
              </button>
              <button
                onClick={() => switchMode('haunt')}
                className="text-xs font-crt px-1 py-1 border hover:bg-opacity-10"
                style={{ borderColor: '#7A3CFF', color: '#7A3CFF' }}
                title="/haunt mode"
              >
                GHO
              </button>
              <button
                onClick={() => setShowGhostPanel(!showGhostPanel)}
                className="text-xs font-crt px-1 py-1 border hover:bg-opacity-10"
                style={{ borderColor: currentColor, color: currentColor }}
              >
                👻
              </button>
              <button
                onClick={() => switchMode('bias')}
                className="text-xs font-crt px-1 py-1 border hover:bg-opacity-10"
                style={{ borderColor: '#FF3434', color: '#FF3434' }}
                title="/bias reveal"
              >
                ✓✗
              </button>
            </div>
          </div>
          
          <button
            onClick={onClose}
            className="px-3 py-1 border font-crt text-sm transition-all hover:bg-opacity-20"
            style={{ borderColor: currentColor, color: currentColor }}
          >
            [END OBSERVATION]
          </button>
        </div>

        {/* Ghost Annotations Panel */}
        {showGhostPanel && (
          <div 
            className="px-4 py-2 border-b"
            style={{ borderColor: currentColor }}
          >
            <div className="text-xs font-crt opacity-60" style={{ color: currentColor }}>
              <div className="mb-1">GHOST ANNOTATIONS:</div>
              <div className="space-y-1 max-h-20 overflow-y-auto">
                {jacklynState.ghostAnnotations.map((ghost, idx) => (
                  <div key={idx} className="flex items-center gap-2 opacity-75">
                    <span className="w-1 h-1 bg-current rounded-full"></span>
                    <span className="text-xs">{ghost.content}</span>
                  </div>
                ))}
                {jacklynState.ghostAnnotations.length === 0 && (
                  <span className="opacity-50">No haunted data detected</span>
                )}
              </div>
            </div>
          </div>
        )}

        {/* Bias Disclosure Panel */}
        {showBiasPanel && (
          <div 
            className="px-4 py-2 border-b"
            style={{ borderColor: currentColor }}
          >
            <div className="text-xs font-crt opacity-75" style={{ color: currentColor }}>
              <div className="mb-1">BIAS DISCLOSURE:</div>
              <div className="grid grid-cols-2 gap-2">
                <div>
                  <div className="font-bold">Revealed ✓</div>
                  {jacklynState.revealedBiases.map((bias, idx) => (
                    <div key={idx} className="text-xs opacity-75">• {bias}</div>
                  ))}
                </div>
                <div>
                  <div className="font-bold">Hidden ✗</div>
                  <div className="text-xs opacity-50">{jacklynState.hiddenBiases.length} undisclosed</div>
                </div>
              </div>
              <button
                onClick={() => setShowBiasPanel(false)}
                className="mt-2 text-xs underline opacity-75"
              >
                Hide disclosure
              </button>
            </div>
          </div>
        )}

        {/* Active Split Options */}
        {activeSplit && (
          <div 
            className="px-4 py-2 border-b border-dashed"
            style={{ borderColor: '#00FF00' }}
          >
            <div className="text-xs font-crt" style={{ color: '#00FF00' }}>
              <div className="mb-2">SPLITTER LOGIC ACTIVE:</div>
              <div className="flex gap-2">
                <button
                  onClick={() => selectSplitBranch('A')}
                  className="px-2 py-1 border text-xs hover:bg-opacity-10"
                  style={{ borderColor: '#00FF00', color: '#00FF00' }}
                >
                  Path A
                </button>
                <button
                  onClick={() => selectSplitBranch('B')}
                  className="px-2 py-1 border text-xs hover:bg-opacity-10"
                  style={{ borderColor: '#00FF00', color: '#00FF00' }}
                >
                  Path B
                </button>
                <button
                  onClick={() => selectSplitBranch('both')}
                  className="px-2 py-1 border text-xs hover:bg-opacity-10"
                  style={{ borderColor: '#00FF00', color: '#00FF00' }}
                >
                  Both Parallel
                </button>
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
                  message.type === 'ghost' ? 'border-2 border-dashed opacity-60' :
                  message.type === 'split' ? 'border-2' :
                  'border-r-4'
                }`}
                style={{
                  borderColor: message.type === 'ghost' ? '#7A3CFF' :
                              message.type === 'split' ? '#00FF00' :
                              currentColor,
                  backgroundColor: message.type === 'user' 
                    ? `${currentColor}10` 
                    : message.type === 'ghost'
                    ? '#7A3CFF08'
                    : `${currentColor}08`,
                }}
              >
                {/* Metadata Display */}
                {message.metadata && (
                  <div className="text-xs font-crt mb-2 opacity-75 flex gap-3" style={{ color: currentColor }}>
                    <span>Pass: {message.metadata.jv_pass}</span>
                    <span>Mode: {message.metadata.mode}</span>
                    <span>Draft: {message.metadata.draftNumber}</span>
                    <span>⟢ {message.metadata.timestamp}</span>
                  </div>
                )}
                
                {/* Visual Effects */}
                {message.visualEffects?.eyewearTic && (
                  <div className="text-xs italic opacity-60 mb-1" style={{ color: currentColor }}>
                    *adjusts glasses nervously*
                  </div>
                )}
                
                <div 
                  className={`font-crt text-sm whitespace-pre-wrap ${
                    message.visualEffects?.ellipsesOverload ? 'opacity-90' : ''
                  }`}
                  style={{ 
                    color: message.type === 'ghost' ? '#7A3CFF' : currentColor 
                  }}
                >
                  {message.content}
                </div>
                
                {/* Ghost Annotations */}
                {message.ghostAnnotations && message.ghostAnnotations.length > 0 && (
                  <div className="mt-2 space-y-1">
                    {message.ghostAnnotations.map((ghost, idx) => (
                      <div 
                        key={idx} 
                        className="text-xs opacity-50 cursor-pointer hover:opacity-75 border-l-2 pl-2"
                        style={{ borderColor: '#7A3CFF', color: '#7A3CFF' }}
                        title={`Ghost annotation: ${ghost.type}`}
                      >
                        👻 {ghost.text}
                      </div>
                    ))}
                  </div>
                )}
                
                {/* Bias Disclosure */}
                {message.biasDisclosure && (
                  <div className="mt-2 text-xs opacity-60" style={{ color: currentColor }}>
                    <div>Biases revealed: {message.biasDisclosure.slice(0, 2).join(', ')}</div>
                  </div>
                )}
                
                <div className="font-crt text-xs opacity-50 mt-2" style={{ color: currentColor }}>
                  {message.timestamp.toLocaleTimeString()}
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
                  <span>Processing through analytical framework</span>
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

        {/* Quick Mode/Test Triggers */}
        <div 
          className="px-4 pt-2 border-t"
          style={{ borderColor: currentColor }}
        >
          <div className="text-xs font-crt opacity-50 mb-2" style={{ color: currentColor }}>
            Mode Triggers:
          </div>
          <div className="grid grid-cols-2 gap-2 mb-3">
            <button
              onClick={() => setInputValue("Give me the official analysis report")}
              className="px-2 py-1 border font-crt text-xs hover:bg-opacity-10 transition-all"
              style={{ borderColor: '#00FFFF', color: '#00FFFF' }}
            >
              /report trigger
            </button>
            <button
              onClick={() => setInputValue("Between us, what do you really think?")}
              className="px-2 py-1 border font-crt text-xs hover:bg-opacity-10 transition-all"
              style={{ borderColor: '#FFB000', color: '#FFB000' }}
            >
              /aside trigger
            </button>
            <button
              onClick={() => setInputValue("Remember what Preston used to say")}
              className="px-2 py-1 border font-crt text-xs hover:bg-opacity-10 transition-all"
              style={{ borderColor: '#7A3CFF', color: '#7A3CFF' }}
            >
              /haunt trigger
            </button>
            <button
              onClick={() => setInputValue("What if we consider both options?")}
              className="px-2 py-1 border font-crt text-xs hover:bg-opacity-10 transition-all"
              style={{ borderColor: '#00FF00', color: '#00FF00' }}
            >
              /split trigger
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
              placeholder="Describe what requires analysis. Data patterns, anomalies, observations..."
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
              OBSERVE
            </button>
          </div>
          
          {/* Draft Progress */}
          <div className="mt-2 flex items-center gap-2">
            <span className="text-xs font-crt opacity-50" style={{ color: currentColor }}>
              Draft Progress:
            </span>
            <div className="flex-1 h-1 bg-gray-800 rounded overflow-hidden">
              <div 
                className="h-full transition-all duration-1000"
                style={{ 
                  width: `${Math.min(100, jacklynState.draftCount * 10)}%`,
                  backgroundColor: currentColor
                }}
              />
            </div>
            <span className="text-xs font-crt opacity-50" style={{ color: currentColor }}>
              #{jacklynState.draftCount} → ∞
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default JacklynVarianceChat;