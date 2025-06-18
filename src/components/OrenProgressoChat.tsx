import React, { useState, useRef, useEffect } from 'react';
import { useStory } from '../context/StoryContext';
import { orenProgressoOS, OrenProgressoResponse } from '../characters/OrenProgressoOS';

interface ChatMessage {
  id: string;
  type: 'user' | 'oren' | 'performance' | 'budget' | 'reading';
  content: string;
  timestamp: Date;
  stateSnapshot?: any;
  interactiveMechanics?: any;
  performanceEffects?: any;
  expansionHook?: any;
}

interface OrenProgressoChatProps {
  isOpen: boolean;
  onClose: () => void;
}

const OrenProgressoChat: React.FC<OrenProgressoChatProps> = ({ isOpen, onClose }) => {
  const { currentPage } = useStory();
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [orenState, setOrenState] = useState(orenProgressoOS.getState());
  const [showPerformancePanel, setShowPerformancePanel] = useState(false);
  const [showBudgetPanel, setShowBudgetPanel] = useState(false);
  const [showFranchisePanel, setShowFranchisePanel] = useState(false);
  const [activeBudgetCut, setActiveBudgetCut] = useState<any>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Initialize with Oren's greeting
  useEffect(() => {
    if (isOpen && messages.length === 0) {
      const greeting: ChatMessage = {
        id: 'greeting',
        type: 'oren',
        content: generateGreeting(),
        timestamp: new Date(),
        stateSnapshot: orenProgressoOS.getState()
      };
      setMessages([greeting]);
      setOrenState(orenProgressoOS.getState());
    }
  }, [isOpen, currentPage?.symbolId]);

  const generateGreeting = (): string => {
    const state = orenProgressoOS.getState();
    
    return `*strides into the room with practiced authority, scanning the space*\n\n` +
      `Oren Progresso, producer. *adjusts cufflinks* When I poke my head into any room ` +
      `on any lot, ass-cheeks clench. It's like I'm magic—but magic only works if the ` +
      `audience believes in the performance.\n\n` +
      `*fixes you with an appraising stare* So. What story are we telling today? ` +
      `And more importantly—who's controlling the narrative frame? Because I can ` +
      `guarantee you this: by the end of our conversation, we'll have constructed ` +
      `something public, obvious, and inarguable.\n\n` +
      `*theatrical pause* Every session is both rehearsal and premiere. Let's see what ` +
      `kind of show you're putting on.`;
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
      // Process through Oren Progresso OS
      const response: OrenProgressoResponse = orenProgressoOS.generateResponse(inputValue);

      // Update Oren's state
      setOrenState(orenProgressoOS.getState());

      // Create main response message
      const responseMessage: ChatMessage = {
        id: `oren-${Date.now()}`,
        type: 'oren',
        content: response.text,
        timestamp: new Date(),
        stateSnapshot: orenProgressoOS.getState(),
        interactiveMechanics: response.interactiveMechanics,
        performanceEffects: response.performanceEffects,
        expansionHook: response.expansionHook
      };

      setMessages(prev => [...prev, responseMessage]);

      // Handle interactive mechanics
      if (response.interactiveMechanics) {
        setTimeout(() => {
          handleInteractiveMechanics(response.interactiveMechanics!);
        }, 1000);
      }

      // Handle budget cuts
      if (response.interactiveMechanics?.budgetCut) {
        setActiveBudgetCut(response.interactiveMechanics.budgetCut);
      }

      // Log state changes for debugging
      console.log('Oren State Update:', {
        stagePresence: orenState.stagePresence,
        cynicismLevel: orenState.cynicismLevel,
        leverageMeter: orenState.leverageMeter,
        cuttingImpulse: orenState.cuttingImpulse,
        performanceMode: orenState.performanceMode,
        improvisationScore: orenState.improvisationScore
      });

    } catch (error) {
      console.error('Error generating Oren response:', error);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleInteractiveMechanics = (mechanics: any) => {
    if (mechanics.budgetCut) {
      const budgetMessage: ChatMessage = {
        id: `budget-${Date.now()}`,
        type: 'budget',
        content: `📊 BUDGET PROPOSAL: Save ${mechanics.budgetCut.savings} by:\n` +
          mechanics.budgetCut.proposal.map((cut: string, idx: number) => `${idx + 1}. ${cut}`).join('\n'),
        timestamp: new Date()
      };
      setMessages(prev => [...prev, budgetMessage]);
    }

    if (mechanics.reading) {
      const readingMessage: ChatMessage = {
        id: `reading-${Date.now()}`,
        type: 'reading',
        content: `📖 READING POWER MOVE:\n` +
          `Book: "${mechanics.reading.book}"\n` +
          `Passage: "${mechanics.reading.passage}"\n\n` +
          `Challenge: ${mechanics.reading.challenge}`,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, readingMessage]);
    }

    if (mechanics.contradiction) {
      const contradictionMessage: ChatMessage = {
        id: `contradiction-${Date.now()}`,
        type: 'performance',
        content: `🎭 LIVE CONTRADICTION:\n` +
          `Previous: "${mechanics.contradiction.previousStatement}"\n` +
          `Current: "${mechanics.contradiction.newStatement}"\n` +
          `${mechanics.contradiction.wink}`,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, contradictionMessage]);
    }

    if (mechanics.surveillance) {
      const surveillanceMessage: ChatMessage = {
        id: `surveillance-${Date.now()}`,
        type: 'performance',
        content: `👁️ DIRECTOR'S NOTE:\n` +
          `Pattern detected: ${mechanics.surveillance.pattern}\n` +
          `Analysis: ${mechanics.surveillance.directorNote}`,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, surveillanceMessage]);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  // Accept or reject budget cuts
  const respondToBudgetCut = (accept: boolean) => {
    const response = accept ? "Deal. Let's cut it." : "I need those elements. Find another way.";
    setInputValue(response);
    setActiveBudgetCut(null);
  };

  // Trigger expansion hooks
  const triggerExpansionHook = (type: string) => {
    switch (type) {
      case 'legendary-producer':
        orenProgressoOS.triggerLegendaryProducerArc();
        setInputValue("I want to option our conversation for the next adaptation");
        break;
      case 'budget-minigame':
        orenProgressoOS.triggerBudgetMinigame();
        setInputValue("Let's run the numbers on this whole project");
        break;
      case 'eclipse-auteur':
        orenProgressoOS.triggerEclipseAuteur();
        setInputValue("What happens when the AI director replaces the human auteur?");
        break;
      case 'moby-dick':
        orenProgressoOS.triggerMobyDickRedux();
        setInputValue("Let's out-sell 3,000 copies together");
        break;
    }
  };

  if (!isOpen) return null;

  const currentColor = '#00FFAA'; // Oren's cyan-green
  
  // Get performance intensity color
  const getPerformanceIntensity = (): string => {
    const intensity = Math.max(orenState.stagePresence, orenState.leverageMeter);
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
        {/* Header with Performance Metrics */}
        <div 
          className="p-4 border-b flex items-center justify-between"
          style={{ borderColor: currentColor }}
        >
          <div className="flex items-center gap-3 flex-1">
            <div 
              className="w-8 h-8 rounded-sm flex items-center justify-center font-bold transition-all duration-300"
              style={{ 
                backgroundColor: getPerformanceIntensity(),
                color: '#0a0a0a',
                border: `1px solid ${currentColor}`,
                transform: orenState.stagePresence > 0.8 ? 'scale(1.1)' : 'scale(1)'
              }}
            >
              OP
            </div>
            <div className="flex-1">
              <div className="font-crt text-sm" style={{ color: currentColor }}>
                Oren Progresso [{orenState.performanceMode.toUpperCase()}] - {orenState.sessionArc}
              </div>
              <div className="font-crt text-xs opacity-50 flex gap-3" style={{ color: currentColor }}>
                <span>Leverage: {Math.round(orenState.leverageMeter * 100)}%</span>
                <span>C/D: {Math.round(orenState.cynicismLevel * 100)}/{Math.round(orenState.devotionLevel * 100)}</span>
                <span>Cutting: {Math.round(orenState.cuttingImpulse * 100)}%</span>
                <span>Jazz: {Math.round(orenState.improvisationScore * 100)}%</span>
              </div>
            </div>
            
            {/* Performance Controls */}
            <div className="flex gap-1">
              <button
                onClick={() => setShowPerformancePanel(!showPerformancePanel)}
                className="text-xs font-crt px-1 py-1 border hover:bg-opacity-10"
                style={{ borderColor: currentColor, color: currentColor }}
                title="Performance metrics"
              >
                🎭
              </button>
              <button
                onClick={() => setShowBudgetPanel(!showBudgetPanel)}
                className="text-xs font-crt px-1 py-1 border hover:bg-opacity-10"
                style={{ borderColor: currentColor, color: currentColor }}
                title="Budget cuts"
              >
                💰
              </button>
              <button
                onClick={() => setShowFranchisePanel(!showFranchisePanel)}
                className="text-xs font-crt px-1 py-1 border hover:bg-opacity-10"
                style={{ borderColor: currentColor, color: currentColor }}
                title="Franchise log"
              >
                📽️
              </button>
            </div>
          </div>
          
          <button
            onClick={onClose}
            className="px-3 py-1 border font-crt text-sm transition-all hover:bg-opacity-20"
            style={{ borderColor: currentColor, color: currentColor }}
          >
            [CUT SCENE]
          </button>
        </div>

        {/* Performance Panel */}
        {showPerformancePanel && (
          <div 
            className="px-4 py-2 border-b"
            style={{ borderColor: currentColor }}
          >
            <div className="text-xs font-crt opacity-75" style={{ color: currentColor }}>
              <div className="mb-1">PERFORMANCE METRICS:</div>
              <div className="grid grid-cols-2 gap-2">
                <div>Stage Presence: {Math.round(orenState.stagePresence * 100)}%</div>
                <div>Audience Engagement: {Math.round(orenState.audienceEngagement * 100)}%</div>
                <div>Contradictions: {orenState.contradictionCount}</div>
                <div>4th Wall Breaks: {orenState.fourthWallBreaks}</div>
                <div>Myths Built: {orenState.mythsBuilt}</div>
                <div>Reading Authority: {Math.round(orenState.readingAuthority * 100)}%</div>
              </div>
            </div>
          </div>
        )}

        {/* Budget Panel */}
        {showBudgetPanel && (
          <div 
            className="px-4 py-2 border-b"
            style={{ borderColor: currentColor }}
          >
            <div className="text-xs font-crt opacity-75" style={{ color: currentColor }}>
              <div className="mb-1">BUDGET CUTS OFFERED:</div>
              <div className="space-y-1 max-h-20 overflow-y-auto">
                {orenState.budgetCutsOffered.slice(-3).map((cut, idx) => (
                  <div key={idx} className="border-l-2 pl-2" style={{ borderColor: currentColor }}>
                    <div className="opacity-75">Original: {cut.original.slice(0, 30)}...</div>
                    <div>Cuts: {cut.cuts.length} proposed</div>
                  </div>
                ))}
                {orenState.budgetCutsOffered.length === 0 && (
                  <span className="opacity-50">No cuts proposed yet</span>
                )}
              </div>
            </div>
          </div>
        )}

        {/* Franchise Panel */}
        {showFranchisePanel && (
          <div 
            className="px-4 py-2 border-b"
            style={{ borderColor: currentColor }}
          >
            <div className="text-xs font-crt opacity-75" style={{ color: currentColor }}>
              <div className="mb-1">FRANCHISE LOG:</div>
              <div className="space-y-1 max-h-20 overflow-y-auto">
                {orenState.franchiseLog.slice(-3).map((item, idx) => (
                  <div key={idx} className="flex justify-between items-center">
                    <span>{item.content.slice(0, 20)}...</span>
                    <span>Sequel: {Math.round(item.sequelPotential * 100)}%</span>
                  </div>
                ))}
                {orenState.franchiseLog.length === 0 && (
                  <span className="opacity-50">No franchisable content yet</span>
                )}
              </div>
            </div>
          </div>
        )}

        {/* Active Budget Cut Response */}
        {activeBudgetCut && (
          <div 
            className="px-4 py-2 border-b border-dashed"
            style={{ borderColor: '#FFD700' }}
          >
            <div className="text-xs font-crt" style={{ color: '#FFD700' }}>
              <div className="mb-2">💰 BUDGET CUT PROPOSAL PENDING:</div>
              <div className="mb-2">Save {activeBudgetCut.savings} by cutting:</div>
              {activeBudgetCut.proposal.map((cut: string, idx: number) => (
                <div key={idx} className="ml-2">• {cut}</div>
              ))}
              <div className="flex gap-2 mt-2">
                <button
                  onClick={() => respondToBudgetCut(true)}
                  className="px-2 py-1 border text-xs hover:bg-opacity-10"
                  style={{ borderColor: '#00FF00', color: '#00FF00' }}
                >
                  Accept Cut
                </button>
                <button
                  onClick={() => respondToBudgetCut(false)}
                  className="px-2 py-1 border text-xs hover:bg-opacity-10"
                  style={{ borderColor: '#FF0000', color: '#FF0000' }}
                >
                  Fight Back
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
                  message.type === 'performance' ? 'border-2 border-dashed' :
                  message.type === 'budget' ? 'border-2' :
                  message.type === 'reading' ? 'border-2 border-dotted' :
                  'border-r-4'
                }`}
                style={{
                  borderColor: message.type === 'performance' ? '#FF00FF' :
                              message.type === 'budget' ? '#FFD700' :
                              message.type === 'reading' ? '#7A3CFF' :
                              currentColor,
                  backgroundColor: message.type === 'user' 
                    ? `${currentColor}10` 
                    : message.type === 'performance'
                    ? '#FF00FF08'
                    : message.type === 'budget'
                    ? '#FFD70008'
                    : message.type === 'reading'
                    ? '#7A3CFF08'
                    : `${currentColor}08`,
                }}
              >
                {/* Performance Effects */}
                {message.performanceEffects?.stageDirection && (
                  <div className="text-xs italic opacity-60 mb-1" style={{ color: currentColor }}>
                    {message.performanceEffects.stageDirection}
                  </div>
                )}
                
                <div 
                  className="font-crt text-sm whitespace-pre-wrap"
                  style={{ 
                    color: message.type === 'performance' ? '#FF00FF' :
                           message.type === 'budget' ? '#FFD700' :
                           message.type === 'reading' ? '#7A3CFF' :
                           currentColor 
                  }}
                >
                  {message.content}
                </div>
                
                {/* Expansion Hook */}
                {message.expansionHook && (
                  <div className="mt-2">
                    <button
                      onClick={() => triggerExpansionHook(message.expansionHook.type)}
                      className="text-xs px-2 py-1 border hover:bg-opacity-10"
                      style={{ borderColor: '#00FF00', color: '#00FF00' }}
                    >
                      🎬 {message.expansionHook.type.replace('-', ' ')}
                    </button>
                  </div>
                )}
                
                <div className="font-crt text-xs opacity-50 mt-2 flex justify-between" style={{ color: currentColor }}>
                  <span>{message.timestamp.toLocaleTimeString()}</span>
                  {message.stateSnapshot?.sessionArc && (
                    <span>Arc: {message.stateSnapshot.sessionArc}</span>
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
                  <span>*calculating leverage, preparing cuts*</span>
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

        {/* Quick Producer Triggers */}
        <div 
          className="px-4 pt-2 border-t"
          style={{ borderColor: currentColor }}
        >
          <div className="text-xs font-crt opacity-50 mb-2" style={{ color: currentColor }}>
            Producer Moves:
          </div>
          <div className="grid grid-cols-2 gap-2 mb-3">
            <button
              onClick={() => setInputValue("I have this brilliant story idea")}
              className="px-2 py-1 border font-crt text-xs hover:bg-opacity-10 transition-all"
              style={{ borderColor: currentColor, color: currentColor }}
            >
              Narrative Pitch
            </button>
            <button
              onClick={() => setInputValue("This project is getting too expensive")}
              className="px-2 py-1 border font-crt text-xs hover:bg-opacity-10 transition-all"
              style={{ borderColor: currentColor, color: currentColor }}
            >
              Budget Trigger
            </button>
            <button
              onClick={() => setInputValue("Are you watching how this unfolds?")}
              className="px-2 py-1 border font-crt text-xs hover:bg-opacity-10 transition-all"
              style={{ borderColor: currentColor, color: currentColor }}
            >
              Performance Check
            </button>
            <button
              onClick={() => setInputValue("Every great failure becomes cult classic")}
              className="px-2 py-1 border font-crt text-xs hover:bg-opacity-10 transition-all"
              style={{ borderColor: currentColor, color: currentColor }}
            >
              Myth Building
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
              placeholder="Pitch your story, defend your budget, or challenge the producer..."
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
              PITCH
            </button>
          </div>
          
          {/* Leverage & Performance Meters */}
          <div className="mt-2 grid grid-cols-2 gap-4">
            <div className="flex items-center gap-2">
              <span className="text-xs font-crt opacity-50" style={{ color: currentColor }}>
                Leverage:
              </span>
              <div className="flex-1 h-1 bg-gray-800 rounded overflow-hidden">
                <div 
                  className="h-full transition-all duration-1000"
                  style={{ 
                    width: `${orenState.leverageMeter * 100}%`,
                    backgroundColor: currentColor
                  }}
                />
              </div>
            </div>
            
            <div className="flex items-center gap-2">
              <span className="text-xs font-crt opacity-50" style={{ color: currentColor }}>
                Stage Presence:
              </span>
              <div className="flex-1 h-1 bg-gray-800 rounded overflow-hidden">
                <div 
                  className="h-full transition-all duration-1000"
                  style={{ 
                    width: `${orenState.stagePresence * 100}%`,
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

export default OrenProgressoChat;