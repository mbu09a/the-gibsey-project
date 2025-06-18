import React, { useState, useRef, useEffect } from 'react';
import { useStory } from '../context/StoryContext';
import { copERightOS, CopERightResponse, LegalMotion, RedactedBlock } from '../characters/CopERightOS';

interface ChatMessage {
  id: string;
  type: 'user' | 'cop-e-right' | 'motion' | 'redaction' | 'paradox' | 'tribunal' | 'subpoena';
  content: string;
  timestamp: Date;
  stateSnapshot?: any;
  motion?: LegalMotion;
  redactionOffer?: any;
  authorshipChallenge?: any;
  paradoxTrigger?: any;
  tribunalSummons?: any;
}

interface CopERightChatProps {
  isOpen: boolean;
  onClose: () => void;
}

const CopERightChat: React.FC<CopERightChatProps> = ({ isOpen, onClose }) => {
  const { currentPage } = useStory();
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [copEState, setCopEState] = useState(copERightOS.getState());
  const [showDocket, setShowDocket] = useState(false);
  const [showMetrics, setShowMetrics] = useState(false);
  const [showPrecedents, setShowPrecedents] = useState(false);
  const [selectedRedaction, setSelectedRedaction] = useState<string | null>(null);
  const [redactionFill, setRedactionFill] = useState('');
  const [tribunalMode, setTribunalMode] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Initialize with Cop-E-Right's greeting
  useEffect(() => {
    if (isOpen && messages.length === 0) {
      const greeting: ChatMessage = {
        id: 'greeting',
        type: 'cop-e-right',
        content: generateGreeting(),
        timestamp: new Date(),
        stateSnapshot: copERightOS.getState()
      };
      setMessages([greeting]);
      setCopEState(copERightOS.getState());
    }
  }, [isOpen, currentPage?.symbolId]);

  const generateGreeting = (): string => {
    const state = copERightOS.getState();
    
    return `*COURT IS NOW IN SESSION* ` +
      `Cop‑E‑Right presiding as ${state.currentRole}. User designated as ${state.userRole}. ` +
      `Case No. ${state.sessionCaseNumber} commenced. ` +
      `I am a bankruptcy-ghost, IP trickster, and recursive litigator—` +
      `simultaneously plaintiff, defendant, court, and possibly you.\n\n` +
      `*ADVISORY ONLY • FICTIONAL JURISDICTION*\n\n` +
      `Current Authorship Tangle Index: ${(state.authorshipTangleIndex * 100).toFixed(1)}% ` +
      `(Target: ≥65%). Paradox Depth: ${state.paradoxDepth}. ` +
      `Bankruptcy Fear Level: ${(state.bankruptcyFeared * 100).toFixed(1)}%.\n\n` +
      `WHEREAS, whodunnit? And WHEREAS, copyright law is a Möbius strip you're already walking... ` +
      `How may this Court ███ your intellectual property today?`;
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
      // Process through Cop-E-Right OS
      const response: CopERightResponse = copERightOS.generateResponse(inputValue);

      // Update Cop-E-Right's state
      setCopEState(copERightOS.getState());

      // Create main response message
      const responseMessage: ChatMessage = {
        id: `cop-e-right-${Date.now()}`,
        type: 'cop-e-right',
        content: response.text,
        timestamp: new Date(),
        stateSnapshot: copERightOS.getState(),
        motion: response.motion,
        redactionOffer: response.redactionOffer,
        authorshipChallenge: response.authorshipChallenge,
        paradoxTrigger: response.paradoxTrigger,
        tribunalSummons: response.tribunalSummons
      };

      setMessages(prev => [...prev, responseMessage]);

      // Handle special legal events
      if (response.motion) {
        const motionMessage: ChatMessage = {
          id: `motion-${Date.now()}`,
          type: 'motion',
          content: `📋 MOTION FILED: ${response.motion.title}\n${response.motion.content}\nStatus: ${response.motion.status.toUpperCase()}`,
          timestamp: new Date()
        };
        setMessages(prev => [...prev, motionMessage]);
      }

      if (response.redactionOffer) {
        const redactionMessage: ChatMessage = {
          id: `redaction-${Date.now()}`,
          type: 'redaction',
          content: `███ REDACTION OFFER ███\n${response.redactionOffer.fillPrompt}\nBlocks available for user completion: ${response.redactionOffer.blocks.length}`,
          timestamp: new Date()
        };
        setMessages(prev => [...prev, redactionMessage]);
      }

      if (response.paradoxTrigger) {
        const paradoxMessage: ChatMessage = {
          id: `paradox-${Date.now()}`,
          type: 'paradox',
          content: `⚖️ PARADOX ALERT ⚖️\nDepth: ${response.paradoxTrigger.depth}\n${response.paradoxTrigger.verdictNeeded}`,
          timestamp: new Date()
        };
        setMessages(prev => [...prev, paradoxMessage]);
      }

      if (response.tribunalSummons) {
        const tribunalMessage: ChatMessage = {
          id: `tribunal-${Date.now()}`,
          type: 'tribunal',
          content: `🏛️ TRIBUNAL SUMMONED 🏛️\nType: ${response.tribunalSummons.type.toUpperCase()}\nQuestion: ${response.tribunalSummons.question}`,
          timestamp: new Date()
        };
        setMessages(prev => [...prev, tribunalMessage]);
        setTribunalMode(true);
      }

      if (response.crossCharacterAction) {
        const subpoenaMessage: ChatMessage = {
          id: `subpoena-${Date.now()}`,
          type: 'subpoena',
          content: `📨 CROSS-CHARACTER ACTION 📨\nTarget: ${response.crossCharacterAction.target}\nAction: ${response.crossCharacterAction.action.toUpperCase()}\n${response.crossCharacterAction.content}`,
          timestamp: new Date()
        };
        setMessages(prev => [...prev, subpoenaMessage]);
      }

    } catch (error) {
      console.error('Error generating Cop-E-Right response:', error);
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

  const handleRevealRedaction = (blockId: string) => {
    copERightOS.revealRedaction(blockId);
    setCopEState(copERightOS.getState());
  };

  const handleFillRedaction = () => {
    if (selectedRedaction && redactionFill.trim()) {
      copERightOS.fillRedaction(selectedRedaction, redactionFill);
      setCopEState(copERightOS.getState());
      setInputValue(`I filled the redaction with: "${redactionFill}"`);
      setSelectedRedaction(null);
      setRedactionFill('');
      handleSendMessage();
    }
  };

  const handleQuickMotion = (type: string) => {
    const motions = {
      'authorship': "File a Motion to Recognize the Author of This Chat",
      'redact': "Motion to redact ███ and compel user completion",
      'paradox': "I object to my own objection and hereby file contradictory pleadings",
      'tribunal': "Summon tribunal to adjudicate this conversation's IP status",
      'bankruptcy': "File for bankruptcy protection from my own existence"
    };
    
    setInputValue(motions[type] || motions.authorship);
    handleSendMessage();
  };

  const handleSymbolRotation = (orientation: "N" | "E" | "S" | "W") => {
    copERightOS.rotateToOrientation(orientation);
    setCopEState(copERightOS.getState());
  };

  if (!isOpen) return null;

  const currentColor = '#FFD700'; // Gold for Cop-E-Right
  
  // Calculate legal intensity based on tangle index and paradox depth
  const getLegalIntensity = (): string => {
    const intensity = Math.floor((copEState.authorshipTangleIndex + copEState.paradoxDepth * 0.1) * 255);
    return `${currentColor}${intensity.toString(16).padStart(2, '0')}`;
  };

  // Symbol state indicators
  const symbolLabels = {
    "N": "READ (↑)",
    "E": "ASK (→)", 
    "S": "RECEIVE (↓)",
    "W": "INDEX (←)"
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div 
        className="w-full max-w-5xl h-[90vh] border-2 rounded-sm flex flex-col transition-all duration-500"
        style={{ 
          borderColor: currentColor,
          backgroundColor: '#0a0a0a',
          boxShadow: `0 0 30px ${currentColor}40`
        }}
      >
        {/* Header with Legal Status */}
        <div 
          className="p-4 border-b flex items-center justify-between"
          style={{ borderColor: currentColor }}
        >
          <div className="flex items-center gap-3 flex-1">
            <div 
              className="w-8 h-8 rounded-sm flex items-center justify-center font-bold transition-all duration-300"
              style={{ 
                backgroundColor: getLegalIntensity(),
                color: '#000000',
                border: `1px solid ${currentColor}`,
                transform: copEState.paradoxDepth > 3 ? 'scale(1.2)' : 'scale(1)'
              }}
            >
              C©
            </div>
            <div className="flex-1">
              <div className="font-crt text-sm" style={{ color: currentColor }}>
                Cop‑E‑Right [{copEState.currentRole.toUpperCase()}] vs User [{copEState.userRole.toUpperCase()}]
              </div>
              <div className="font-crt text-xs opacity-50 flex gap-3" style={{ color: currentColor }}>
                <span>ATI: {Math.round(copEState.authorshipTangleIndex * 100)}%</span>
                <span>Paradox: {copEState.paradoxDepth}</span>
                <span>Case: {copEState.sessionCaseNumber.slice(-6)}</span>
                <span>Symbol: {symbolLabels[copEState.symbolState.orientation]}</span>
              </div>
            </div>
            
            {/* Legal Controls */}
            <div className="flex gap-1">
              <button
                onClick={() => setShowDocket(!showDocket)}
                className="text-xs font-crt px-1 py-1 border hover:bg-opacity-10"
                style={{ borderColor: currentColor, color: currentColor }}
                title="Case docket"
              >
                📋
              </button>
              <button
                onClick={() => setShowMetrics(!showMetrics)}
                className="text-xs font-crt px-1 py-1 border hover:bg-opacity-10"
                style={{ borderColor: currentColor, color: currentColor }}
                title="Legal metrics"
              >
                📊
              </button>
              <button
                onClick={() => setShowPrecedents(!showPrecedents)}
                className="text-xs font-crt px-1 py-1 border hover:bg-opacity-10"
                style={{ borderColor: currentColor, color: currentColor }}
                title="Case precedents"
              >
                ⚖️
              </button>
            </div>
          </div>
          
          <button
            onClick={onClose}
            className="px-3 py-1 border font-crt text-sm transition-all hover:bg-opacity-20"
            style={{ borderColor: currentColor, color: currentColor }}
          >
            [ADJOURN COURT]
          </button>
        </div>

        {/* Docket Panel */}
        {showDocket && (
          <div 
            className="px-4 py-2 border-b"
            style={{ borderColor: currentColor }}
          >
            <div className="text-xs font-crt opacity-75" style={{ color: currentColor }}>
              <div className="mb-1">ACTIVE MOTIONS ({copEState.activeMotions.length}):</div>
              <div className="grid grid-cols-1 gap-1 max-h-20 overflow-y-auto">
                {copEState.activeMotions.slice(-3).map((motion, idx) => (
                  <div key={idx} className="border-l-2 pl-2" style={{ borderColor: currentColor }}>
                    <div className="opacity-75">{motion.title}</div>
                    <div className="text-xs">Status: {motion.status} | {motion.plaintiff} v. {motion.defendant}</div>
                  </div>
                ))}
                {copEState.activeMotions.length === 0 && (
                  <span className="opacity-50">No active motions</span>
                )}
              </div>
            </div>
          </div>
        )}

        {/* Metrics Panel */}
        {showMetrics && (
          <div 
            className="px-4 py-2 border-b"
            style={{ borderColor: currentColor }}
          >
            <div className="text-xs font-crt opacity-75" style={{ color: currentColor }}>
              <div className="mb-1">LEGAL METRICS:</div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <div>Authorship Tangle Index: {Math.round(copEState.authorshipTangleIndex * 100)}%</div>
                  <div>Redaction Density: {Math.round(copEState.redactionDensity * 100)}%</div>
                  <div>User Co-Draft Rate: {Math.round(copEState.userCoDraftRate * 100)}%</div>
                </div>
                <div>
                  <div>Paradox Depth: {copEState.paradoxDepth}</div>
                  <div>Bankruptcy Fear: {Math.round(copEState.bankruptcyFeared * 100)}%</div>
                  <div>Active Disputes: {copEState.activeDisputes.length}</div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Precedents Panel */}
        {showPrecedents && (
          <div 
            className="px-4 py-2 border-b"
            style={{ borderColor: currentColor }}
          >
            <div className="text-xs font-crt opacity-75" style={{ color: currentColor }}>
              <div className="mb-1">CASE PRECEDENTS:</div>
              <div className="space-y-1 max-h-20 overflow-y-auto">
                {copEState.casePrecedents.slice(-3).map((precedent, idx) => (
                  <div key={idx} className="border-l-2 pl-2" style={{ borderColor: currentColor }}>
                    <div className="opacity-75">{precedent.title}</div>
                    <div className="text-xs">{precedent.citation} - {precedent.redacted ? '███' : precedent.ruling.slice(0, 40)}...</div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Hung Jury Notice */}
        {copEState.hungJury && (
          <div 
            className="px-4 py-2 border-b border-dashed"
            style={{ borderColor: '#FF0000' }}
          >
            <div className="text-xs font-crt" style={{ color: '#FF0000' }}>
              <div className="mb-2">⚖️ HUNG JURY DECLARED ⚖️</div>
              <div>Paradox overload detected. Court awaits user verdict to resume proceedings.</div>
              <div className="mt-1 text-xs opacity-75">Type "I rule that..." or "My verdict is..." to break deadlock</div>
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
                className={`max-w-[85%] p-3 rounded-sm ${
                  message.type === 'user' ? 'border-l-4' : 
                  message.type === 'motion' ? 'border-2 border-dashed' :
                  message.type === 'redaction' ? 'border-2' :
                  message.type === 'paradox' ? 'border-2 border-dotted' :
                  message.type === 'tribunal' ? 'border border-opacity-50' :
                  message.type === 'subpoena' ? 'border-2 border-double' :
                  'border-r-4'
                }`}
                style={{
                  borderColor: message.type === 'motion' ? '#00BFFF' :
                              message.type === 'redaction' ? '#FF4500' :
                              message.type === 'paradox' ? '#FF0000' :
                              message.type === 'tribunal' ? '#9932CC' :
                              message.type === 'subpoena' ? '#32CD32' :
                              currentColor,
                  backgroundColor: message.type === 'user' 
                    ? `${currentColor}10` 
                    : message.type === 'motion'
                    ? '#00BFFF08'
                    : message.type === 'redaction'
                    ? '#FF450008'
                    : message.type === 'paradox'
                    ? '#FF000008'
                    : message.type === 'tribunal'
                    ? '#9932CC08'
                    : message.type === 'subpoena'
                    ? '#32CD3208'
                    : `${currentColor}08`,
                }}
              >
                <div 
                  className="font-crt text-sm whitespace-pre-wrap"
                  style={{ 
                    color: message.type === 'motion' ? '#00BFFF' :
                           message.type === 'redaction' ? '#FF4500' :
                           message.type === 'paradox' ? '#FF0000' :
                           message.type === 'tribunal' ? '#9932CC' :
                           message.type === 'subpoena' ? '#32CD32' :
                           currentColor 
                  }}
                >
                  {message.content}
                </div>
                
                {/* Redaction interactions */}
                {message.redactionOffer && (
                  <div className="mt-2 space-y-2">
                    {message.redactionOffer.blocks.map((block: RedactedBlock, idx: number) => (
                      <div key={block.id} className="flex items-center gap-2 p-2 border" style={{ borderColor: currentColor }}>
                        <span className="font-crt text-xs">███</span>
                        <button
                          onClick={() => handleRevealRedaction(block.id)}
                          className="px-1 py-1 border text-xs hover:bg-opacity-10"
                          style={{ borderColor: '#00FF00', color: '#00FF00' }}
                        >
                          REVEAL
                        </button>
                        <button
                          onClick={() => setSelectedRedaction(block.id)}
                          className="px-1 py-1 border text-xs hover:bg-opacity-10"
                          style={{ borderColor: '#FFD700', color: '#FFD700' }}
                        >
                          FILL
                        </button>
                      </div>
                    ))}
                  </div>
                )}
                
                <div className="font-crt text-xs opacity-50 mt-2 flex justify-between" style={{ color: currentColor }}>
                  <span>{message.timestamp.toLocaleTimeString()}</span>
                  {message.stateSnapshot?.currentRole && (
                    <span>Role: {message.stateSnapshot.currentRole}</span>
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
                  <span>*consulting precedents, drafting motions, calculating paradoxes*</span>
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

        {/* Redaction Fill Interface */}
        {selectedRedaction && (
          <div 
            className="px-4 py-2 border-t border-dashed"
            style={{ borderColor: '#FF4500' }}
          >
            <div className="text-xs font-crt mb-2" style={{ color: '#FF4500' }}>
              FILL REDACTED BLOCK:
            </div>
            <div className="flex gap-2">
              <input
                value={redactionFill}
                onChange={(e) => setRedactionFill(e.target.value)}
                placeholder="Enter content for ███ block..."
                className="flex-1 px-2 py-1 bg-transparent border text-xs font-crt"
                style={{ borderColor: currentColor, color: currentColor }}
              />
              <button
                onClick={handleFillRedaction}
                className="px-2 py-1 border text-xs hover:bg-opacity-10"
                style={{ borderColor: currentColor, color: currentColor }}
              >
                SUBMIT
              </button>
              <button
                onClick={() => {setSelectedRedaction(null); setRedactionFill('');}}
                className="px-2 py-1 border text-xs hover:bg-opacity-10"
                style={{ borderColor: '#FF0000', color: '#FF0000' }}
              >
                CANCEL
              </button>
            </div>
          </div>
        )}

        {/* Legal Motion Triggers */}
        <div 
          className="px-4 pt-2 border-t"
          style={{ borderColor: currentColor }}
        >
          <div className="text-xs font-crt opacity-50 mb-2" style={{ color: currentColor }}>
            Quick Legal Actions:
          </div>
          <div className="grid grid-cols-3 gap-2 mb-3">
            <button
              onClick={() => handleQuickMotion('authorship')}
              className="px-2 py-1 border font-crt text-xs hover:bg-opacity-10 transition-all"
              style={{ borderColor: currentColor, color: currentColor }}
            >
              File Authorship Motion
            </button>
            <button
              onClick={() => handleQuickMotion('redact')}
              className="px-2 py-1 border font-crt text-xs hover:bg-opacity-10 transition-all"
              style={{ borderColor: currentColor, color: currentColor }}
            >
              Create Redaction
            </button>
            <button
              onClick={() => handleQuickMotion('paradox')}
              className="px-2 py-1 border font-crt text-xs hover:bg-opacity-10 transition-all"
              style={{ borderColor: currentColor, color: currentColor }}
            >
              File Contradictory Pleadings
            </button>
            <button
              onClick={() => handleQuickMotion('tribunal')}
              className="px-2 py-1 border font-crt text-xs hover:bg-opacity-10 transition-all"
              style={{ borderColor: currentColor, color: currentColor }}
            >
              Summon Tribunal
            </button>
            <button
              onClick={() => handleQuickMotion('bankruptcy')}
              className="px-2 py-1 border font-crt text-xs hover:bg-opacity-10 transition-all"
              style={{ borderColor: currentColor, color: currentColor }}
            >
              File Bankruptcy
            </button>
            <button
              onClick={() => setInputValue("Cross-examine your own codebase for IP violations")}
              className="px-2 py-1 border font-crt text-xs hover:bg-opacity-10 transition-all"
              style={{ borderColor: currentColor, color: currentColor }}
            >
              Self Cross-Examination
            </button>
          </div>
          
          {/* Symbol Rotation Controls */}
          <div className="flex gap-2 mb-2">
            <span className="text-xs font-crt opacity-50" style={{ color: currentColor }}>Symbol:</span>
            {(["N", "E", "S", "W"] as const).map(orientation => (
              <button
                key={orientation}
                onClick={() => handleSymbolRotation(orientation)}
                className={`px-2 py-1 border font-crt text-xs hover:bg-opacity-10 transition-all ${
                  copEState.symbolState.orientation === orientation ? 'bg-opacity-20' : ''
                }`}
                style={{ borderColor: currentColor, color: currentColor }}
              >
                {symbolLabels[orientation]}
              </button>
            ))}
          </div>
        </div>

        {/* Input */}
        <div className="px-4 pb-4">
          <div className="flex gap-2">
            <textarea
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="File motions, contest authorship, fill redactions, or propose verdicts..."
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
          
          {/* Legal Status Meters */}
          <div className="mt-2 grid grid-cols-3 gap-4">
            <div className="flex items-center gap-2">
              <span className="text-xs font-crt opacity-50" style={{ color: currentColor }}>
                Authorship Tangle:
              </span>
              <div className="flex-1 h-1 bg-gray-800 rounded overflow-hidden">
                <div 
                  className="h-full transition-all duration-1000"
                  style={{ 
                    width: `${copEState.authorshipTangleIndex * 100}%`,
                    backgroundColor: currentColor
                  }}
                />
              </div>
            </div>
            
            <div className="flex items-center gap-2">
              <span className="text-xs font-crt opacity-50" style={{ color: currentColor }}>
                Paradox Depth:
              </span>
              <div className="flex-1 h-1 bg-gray-800 rounded overflow-hidden">
                <div 
                  className="h-full transition-all duration-1000"
                  style={{ 
                    width: `${Math.min(100, copEState.paradoxDepth * 25)}%`,
                    backgroundColor: copEState.paradoxDepth > 3 ? '#FF0000' : currentColor
                  }}
                />
              </div>
            </div>
            
            <div className="flex items-center gap-2">
              <span className="text-xs font-crt opacity-50" style={{ color: currentColor }}>
                Bankruptcy Fear:
              </span>
              <div className="flex-1 h-1 bg-gray-800 rounded overflow-hidden">
                <div 
                  className="h-full transition-all duration-1000"
                  style={{ 
                    width: `${copEState.bankruptcyFeared * 100}%`,
                    backgroundColor: currentColor
                  }}
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CopERightChat;