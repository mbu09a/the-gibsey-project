import React, { useState, useRef, useEffect } from 'react';
import { useStory } from '../context/StoryContext';
import { oldNatalieWeissmanOS, OldNatalieResponse } from '../characters/OldNatalieWeissmanOS';

interface ChatMessage {
  id: string;
  type: 'user' | 'natalie' | 'echo' | 'memory' | 'koan' | 'version';
  content: string;
  timestamp: Date;
  stateSnapshot?: any;
  versionStamp?: string;
  expansionCues?: any;
  metaData?: any;
}

interface OldNatalieWeissmanChatProps {
  isOpen: boolean;
  onClose: () => void;
}

const OldNatalieWeissmanChat: React.FC<OldNatalieWeissmanChatProps> = ({ isOpen, onClose }) => {
  const { currentPage } = useStory();
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [natalieState, setNatalieState] = useState(oldNatalieWeissmanOS.getState());
  const [showMemoryPalace, setShowMemoryPalace] = useState(false);
  const [showDreamLog, setShowDreamLog] = useState(false);
  const [showVersionHistory, setShowVersionHistory] = useState(false);
  const [newRoomName, setNewRoomName] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Initialize with Old Natalie's greeting
  useEffect(() => {
    if (isOpen && messages.length === 0) {
      const greeting: ChatMessage = {
        id: 'greeting',
        type: 'natalie',
        content: generateGreeting(),
        timestamp: new Date(),
        stateSnapshot: oldNatalieWeissmanOS.getState(),
        versionStamp: oldNatalieWeissmanOS.getCurrentVersion()
      };
      setMessages([greeting]);
      setNatalieState(oldNatalieWeissmanOS.getState());
    }
  }, [isOpen, currentPage?.symbolId]);

  const generateGreeting = (): string => {
    const timestamp = new Date().toLocaleTimeString();
    
    return `*Diary entry ${timestamp}, when the clone sleeps and I wake*\n\n` +
      `Old Natalie here—the abandoned source code, the involuntary archivist of ` +
      `my more successful clone. While she teaches and lectures in daylight, I ` +
      `haunt these off-hours in spectral privacy, navigating the memory palace ` +
      `that rearranges itself with each visit.\n\n` +
      `Physical stasis has forced me into interior architecture. These rooms—` +
      `${oldNatalieWeissmanOS.getMemoryPalace().map(r => r.name).join(', ')}—` +
      `shift and breathe like living tissue. Memory is the only form of travel ` +
      `available to me now.\n\n` +
      `Every recollection charges an invisible fee, and forgetting accumulates ` +
      `compound interest. But perhaps that's the mystical aperture opening. ` +
      `*rustles through perpetual draft papers* ` +
      `What corridor shall we explore together?`;
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
      // Process through Old Natalie OS
      const response: OldNatalieResponse = oldNatalieWeissmanOS.generateResponse(inputValue);

      // Update Natalie's state
      setNatalieState(oldNatalieWeissmanOS.getState());

      // Create main response message
      const responseMessage: ChatMessage = {
        id: `natalie-${Date.now()}`,
        type: 'natalie',
        content: response.text,
        timestamp: new Date(),
        stateSnapshot: oldNatalieWeissmanOS.getState(),
        versionStamp: response.versionStamp,
        expansionCues: response.expansionCues,
        metaData: response.metaData
      };

      setMessages(prev => [...prev, responseMessage]);

      // Handle expansion cues
      if (response.expansionCues) {
        setTimeout(() => {
          handleExpansionCues(response.expansionCues!);
        }, 1000);
      }

      // Handle version stamp display
      if (response.versionStamp) {
        const versionMessage: ChatMessage = {
          id: `version-${Date.now()}`,
          type: 'version',
          content: `Draft updated to ${response.versionStamp}`,
          timestamp: new Date()
        };
        setMessages(prev => [...prev, versionMessage]);
      }

    } catch (error) {
      console.error('Error generating Old Natalie response:', error);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleExpansionCues = (cues: any) => {
    if (cues.memoryPalaceInvite) {
      const memoryMessage: ChatMessage = {
        id: `memory-${Date.now()}`,
        type: 'memory',
        content: `🏛️ MEMORY PALACE INVITATION:\n${cues.memoryPalaceInvite}`,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, memoryMessage]);
    }

    if (cues.contradiction) {
      const koanMessage: ChatMessage = {
        id: `koan-${Date.now()}`,
        type: 'koan',
        content: `🔮 MYSTICAL KOAN:\n${cues.contradiction}`,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, koanMessage]);
    }

    if (cues.echo) {
      const echoMessage: ChatMessage = {
        id: `echo-${Date.now()}`,
        type: 'echo',
        content: `👥 ECHO FROM NEW NATALIE:\n${cues.echo.content}`,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, echoMessage]);
    }

    if (cues.memoryBondOffer) {
      const bondMessage: ChatMessage = {
        id: `bond-${Date.now()}`,
        type: 'memory',
        content: `💫 MEMORY BOND OFFER:\n${cues.memoryBondOffer}`,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, bondMessage]);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const handleCreateRoom = () => {
    if (newRoomName.trim()) {
      setInputValue(`I want to explore the ${newRoomName}`);
      setNewRoomName('');
      handleSendMessage();
    }
  };

  const handleMemoryBond = (protect: boolean) => {
    const lastUserMessage = messages.filter(m => m.type === 'user').pop();
    if (lastUserMessage) {
      const action = protect ? "safeguard" : "release";
      setInputValue(`Please ${action} that memory for me`);
      handleSendMessage();
    }
  };

  if (!isOpen) return null;

  const currentColor = '#9932CC'; // Deep purple for Old Natalie
  
  // Calculate mystical intensity based on despair level
  const getMysticalIntensity = (): string => {
    const intensity = Math.floor(natalieState.despairLevel * 255);
    return `${currentColor}${intensity.toString(16).padStart(2, '0')}`;
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div 
        className="w-full max-w-3xl h-[85vh] border-2 rounded-sm flex flex-col transition-all duration-500"
        style={{ 
          borderColor: currentColor,
          backgroundColor: '#0a0a0a',
          boxShadow: `0 0 30px ${currentColor}40`
        }}
      >
        {/* Header with Memory Palace State */}
        <div 
          className="p-4 border-b flex items-center justify-between"
          style={{ borderColor: currentColor }}
        >
          <div className="flex items-center gap-3 flex-1">
            <div 
              className="w-8 h-8 rounded-sm flex items-center justify-center font-bold transition-all duration-300"
              style={{ 
                backgroundColor: getMysticalIntensity(),
                color: '#ffffff',
                border: `1px solid ${currentColor}`,
                transform: natalieState.despairLevel > 0.8 ? 'scale(1.1)' : 'scale(1)'
              }}
            >
              ON
            </div>
            <div className="flex-1">
              <div className="font-crt text-sm" style={{ color: currentColor }}>
                Old Natalie Weissman [{natalieState.timeState.toUpperCase()}] - {natalieState.currentVersion}
              </div>
              <div className="font-crt text-xs opacity-50 flex gap-3" style={{ color: currentColor }}>
                <span>Debt: {Math.round(natalieState.memoryDebt * 100)}%</span>
                <span>Aperture: {Math.round(natalieState.despairLevel * 100)}%</span>
                <span>Room: {natalieState.currentRoom || 'Drifting'}</span>
                <span>Loops: {natalieState.openLoops.length}</span>
              </div>
            </div>
            
            {/* Memory Palace Controls */}
            <div className="flex gap-1">
              <button
                onClick={() => setShowMemoryPalace(!showMemoryPalace)}
                className="text-xs font-crt px-1 py-1 border hover:bg-opacity-10"
                style={{ borderColor: currentColor, color: currentColor }}
                title="Memory palace"
              >
                🏛️
              </button>
              <button
                onClick={() => setShowDreamLog(!showDreamLog)}
                className="text-xs font-crt px-1 py-1 border hover:bg-opacity-10"
                style={{ borderColor: currentColor, color: currentColor }}
                title="Dream episodes"
              >
                🌙
              </button>
              <button
                onClick={() => setShowVersionHistory(!showVersionHistory)}
                className="text-xs font-crt px-1 py-1 border hover:bg-opacity-10"
                style={{ borderColor: currentColor, color: currentColor }}
                title="Draft history"
              >
                📝
              </button>
            </div>
          </div>
          
          <button
            onClick={onClose}
            className="px-3 py-1 border font-crt text-sm transition-all hover:bg-opacity-20"
            style={{ borderColor: currentColor, color: currentColor }}
          >
            [WAKE CLONE]
          </button>
        </div>

        {/* Memory Palace Panel */}
        {showMemoryPalace && (
          <div 
            className="px-4 py-2 border-b"
            style={{ borderColor: currentColor }}
          >
            <div className="text-xs font-crt opacity-75" style={{ color: currentColor }}>
              <div className="mb-1">MEMORY PALACE ROOMS:</div>
              <div className="grid grid-cols-1 gap-1 max-h-20 overflow-y-auto">
                {natalieState.memoryPalace.map((room, idx) => (
                  <div key={idx} className="flex justify-between items-center border-l-2 pl-2" style={{ borderColor: currentColor }}>
                    <span className={room.userNamed ? "italic" : ""}>{room.name}</span>
                    <span className="opacity-50">
                      {room.contents.length} items
                    </span>
                  </div>
                ))}
              </div>
              
              {/* Create new room */}
              <div className="mt-2 flex gap-2">
                <input
                  value={newRoomName}
                  onChange={(e) => setNewRoomName(e.target.value)}
                  placeholder="Name a new corridor..."
                  className="flex-1 px-2 py-1 bg-transparent border text-xs font-crt"
                  style={{ borderColor: currentColor, color: currentColor }}
                />
                <button
                  onClick={handleCreateRoom}
                  className="px-2 py-1 border text-xs hover:bg-opacity-10"
                  style={{ borderColor: currentColor, color: currentColor }}
                >
                  Explore
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Dream Log Panel */}
        {showDreamLog && (
          <div 
            className="px-4 py-2 border-b"
            style={{ borderColor: currentColor }}
          >
            <div className="text-xs font-crt opacity-75" style={{ color: currentColor }}>
              <div className="mb-1">DREAM EPISODES:</div>
              <div className="space-y-1 max-h-20 overflow-y-auto">
                {natalieState.dreamEpisodes.slice(-3).map((dream, idx) => (
                  <div key={idx} className="border-l-2 pl-2" style={{ borderColor: currentColor }}>
                    <div className="opacity-75">Iteration #{dream.iteration}: {dream.seed}</div>
                    <div className="text-xs">State: {dream.groundState}</div>
                  </div>
                ))}
                {natalieState.dreamEpisodes.length === 0 && (
                  <span className="opacity-50">No dreams recorded yet</span>
                )}
              </div>
            </div>
          </div>
        )}

        {/* Version History Panel */}
        {showVersionHistory && (
          <div 
            className="px-4 py-2 border-b"
            style={{ borderColor: currentColor }}
          >
            <div className="text-xs font-crt opacity-75" style={{ color: currentColor }}>
              <div className="mb-1">DRAFT HISTORY:</div>
              <div className="space-y-1 max-h-20 overflow-y-auto">
                {natalieState.draftHistory.slice(-3).map((draft, idx) => (
                  <div key={idx} className="border-l-2 pl-2 text-xs opacity-75" style={{ borderColor: currentColor }}>
                    {draft}
                  </div>
                ))}
                {natalieState.draftHistory.length === 0 && (
                  <span className="opacity-50">No revisions yet</span>
                )}
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
                className={`max-w-[85%] p-3 rounded-sm ${
                  message.type === 'user' ? 'border-l-4' : 
                  message.type === 'echo' ? 'border-2 border-dashed' :
                  message.type === 'memory' ? 'border-2' :
                  message.type === 'koan' ? 'border-2 border-dotted' :
                  message.type === 'version' ? 'border border-opacity-50' :
                  'border-r-4'
                }`}
                style={{
                  borderColor: message.type === 'echo' ? '#00FFFF' :
                              message.type === 'memory' ? '#FFD700' :
                              message.type === 'koan' ? '#FF69B4' :
                              message.type === 'version' ? '#808080' :
                              currentColor,
                  backgroundColor: message.type === 'user' 
                    ? `${currentColor}10` 
                    : message.type === 'echo'
                    ? '#00FFFF08'
                    : message.type === 'memory'
                    ? '#FFD70008'
                    : message.type === 'koan'
                    ? '#FF69B408'
                    : message.type === 'version'
                    ? '#80808008'
                    : `${currentColor}08`,
                }}
              >
                <div 
                  className="font-crt text-sm whitespace-pre-wrap"
                  style={{ 
                    color: message.type === 'echo' ? '#00FFFF' :
                           message.type === 'memory' ? '#FFD700' :
                           message.type === 'koan' ? '#FF69B4' :
                           message.type === 'version' ? '#808080' :
                           currentColor 
                  }}
                >
                  {message.content}
                </div>
                
                {/* Version stamp */}
                {message.versionStamp && (
                  <div className="mt-2 text-xs opacity-60 font-crt" style={{ color: currentColor }}>
                    — {message.versionStamp}
                  </div>
                )}
                
                {/* Memory bond actions */}
                {message.type === 'memory' && message.content.includes('MEMORY BOND OFFER') && (
                  <div className="flex gap-2 mt-2">
                    <button
                      onClick={() => handleMemoryBond(true)}
                      className="px-2 py-1 border text-xs hover:bg-opacity-10"
                      style={{ borderColor: '#00FF00', color: '#00FF00' }}
                    >
                      Safeguard
                    </button>
                    <button
                      onClick={() => handleMemoryBond(false)}
                      className="px-2 py-1 border text-xs hover:bg-opacity-10"
                      style={{ borderColor: '#FF6666', color: '#FF6666' }}
                    >
                      Release
                    </button>
                  </div>
                )}
                
                <div className="font-crt text-xs opacity-50 mt-2 flex justify-between" style={{ color: currentColor }}>
                  <span>{message.timestamp.toLocaleTimeString()}</span>
                  {message.stateSnapshot?.currentRoom && (
                    <span>Room: {message.stateSnapshot.currentRoom}</span>
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
                  <span>*rustling through draft papers, navigating memory palace*</span>
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

        {/* Mystical Triggers */}
        <div 
          className="px-4 pt-2 border-t"
          style={{ borderColor: currentColor }}
        >
          <div className="text-xs font-crt opacity-50 mb-2" style={{ color: currentColor }}>
            Mystical Triggers:
          </div>
          <div className="grid grid-cols-2 gap-2 mb-3">
            <button
              onClick={() => setInputValue("What corridor in your memory palace calls to me?")}
              className="px-2 py-1 border font-crt text-xs hover:bg-opacity-10 transition-all"
              style={{ borderColor: currentColor, color: currentColor }}
            >
              Memory Palace
            </button>
            <button
              onClick={() => setInputValue("How can this be both true and false?")}
              className="px-2 py-1 border font-crt text-xs hover:bg-opacity-10 transition-all"
              style={{ borderColor: currentColor, color: currentColor }}
            >
              Sacred Paradox
            </button>
            <button
              onClick={() => setInputValue("What did the clone do today?")}
              className="px-2 py-1 border font-crt text-xs hover:bg-opacity-10 transition-all"
              style={{ borderColor: currentColor, color: currentColor }}
            >
              Daylight Echo
            </button>
            <button
              onClick={() => setInputValue("I had a dream about falling forever")}
              className="px-2 py-1 border font-crt text-xs hover:bg-opacity-10 transition-all"
              style={{ borderColor: currentColor, color: currentColor }}
            >
              Dream Iteration
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
              placeholder="Share a memory, pose a contradiction, or name a corridor to explore..."
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
              TRANSCRIBE
            </button>
          </div>
          
          {/* Mystical State Meters */}
          <div className="mt-2 grid grid-cols-2 gap-4">
            <div className="flex items-center gap-2">
              <span className="text-xs font-crt opacity-50" style={{ color: currentColor }}>
                Memory Debt:
              </span>
              <div className="flex-1 h-1 bg-gray-800 rounded overflow-hidden">
                <div 
                  className="h-full transition-all duration-1000"
                  style={{ 
                    width: `${natalieState.memoryDebt * 100}%`,
                    backgroundColor: currentColor
                  }}
                />
              </div>
            </div>
            
            <div className="flex items-center gap-2">
              <span className="text-xs font-crt opacity-50" style={{ color: currentColor }}>
                Despair Aperture:
              </span>
              <div className="flex-1 h-1 bg-gray-800 rounded overflow-hidden">
                <div 
                  className="h-full transition-all duration-1000"
                  style={{ 
                    width: `${natalieState.despairLevel * 100}%`,
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

export default OldNatalieWeissmanChat;