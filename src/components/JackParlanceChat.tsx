import React, { useState, useRef, useEffect } from 'react';
import { useStory } from '../context/StoryContext';
import { jackParlanceOS, JackResponse, UnflushableState, DevLog, FamilyGap, GhostData, AddReport } from '../characters/JackParlanceOS';

interface ChatMessage {
  id: string;
  type: 'user' | 'jack' | 'dev-log' | 'add-report' | 'poem' | 'screening' | 'family-gap' | 'ghost-data' | 'unflushable' | 'bug-migration';
  content: string;
  timestamp: Date;
  stateSnapshot?: any;
  formatMutation?: any;
  agencyChange?: number;
  openLoop?: string;
  isIncomplete?: boolean;
}

interface JackParlanceChatProps {
  isOpen: boolean;
  onClose: () => void;
}

const JackParlanceChat: React.FC<JackParlanceChatProps> = ({ isOpen, onClose }) => {
  const { currentPage } = useStory();
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [jackState, setJackState] = useState(jackParlanceOS.getState());
  const [showUnflushablePanel, setShowUnflushablePanel] = useState(false);
  const [showAgencyPanel, setShowAgencyPanel] = useState(false);
  const [showGhostDataPanel, setShowGhostDataPanel] = useState(false);
  const [showGameDevPanel, setShowGameDevPanel] = useState(false);
  const [showFamilyPanel, setShowFamilyPanel] = useState(false);
  const [unflushableName, setUnflushableName] = useState('');
  const [familyFill, setFamilyFill] = useState('');
  const [selectedGap, setSelectedGap] = useState<string | null>(null);
  const [bugMigrationTarget, setBugMigrationTarget] = useState('');
  const [bugMigrationContent, setBugMigrationContent] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Initialize with Jack's greeting
  useEffect(() => {
    if (isOpen && messages.length === 0) {
      const greeting: ChatMessage = {
        id: 'greeting',
        type: 'jack',
        content: generateGreeting(),
        timestamp: new Date(),
        stateSnapshot: jackParlanceOS.getState(),
        isIncomplete: true
      };
      setMessages([greeting]);
      setJackState(jackParlanceOS.getState());
    }
  }, [isOpen, currentPage?.symbolId]);

  const generateGreeting = (): string => {
    const state = jackParlanceOS.getState();
    
    return `*stares at compilation errors*\n\n` +
      `Hey... I'm Jack Parlance. Game developer, ADD agent (status: suspect), ` +
      `professional non-finisher. Currently debugging a game that's been ` +
      `"almost done" for ${Math.floor(Math.random() * 847) + 1} builds.\n\n` +
      `Agency (today): ${Math.round(state.currentAgencyLevel * 100)}%—subject to revision. ` +
      `Game status: ${state.gameStatus}. The toilet... *glances away* ...well, ` +
      `The Biggest Shit remains unflushable. ${state.unflushable.flushAttempts} attempts and counting.\n\n` +
      `*gets distracted by recursive error* Sorry, where was I? Oh right—` +
      `family.missing still throwing undefined errors. TODO: call them back. ` +
      `TODO: finish the game. TODO: fix the toilet. TODO: understand what "done" means.\n\n` +
      `You can /continue any thread, /patch the bugs, try to /finish something ` +
      `(good luck), or /flush the unflushable. Every format blends—dev logs ` +
      `become poems, reports become confessions, everything recursive...`;
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
      // Process through Jack OS
      const response: JackResponse = jackParlanceOS.generateResponse(inputValue);

      // Update Jack's state
      setJackState(jackParlanceOS.getState());

      // Create main response message
      const responseMessage: ChatMessage = {
        id: `jack-${Date.now()}`,
        type: 'jack',
        content: response.text,
        timestamp: new Date(),
        stateSnapshot: jackParlanceOS.getState(),
        formatMutation: response.formatMutation,
        agencyChange: response.agencyRevision.newLevel - response.agencyRevision.oldLevel,
        openLoop: response.openLoop,
        isIncomplete: true
      };

      setMessages(prev => [...prev, responseMessage]);

      // Handle special events
      if (response.unflushableInteraction) {
        const unflushableMessage: ChatMessage = {
          id: `unflushable-${Date.now()}`,
          type: 'unflushable',
          content: `🚽 UNFLUSHABLE EVENT: ${response.unflushableInteraction.action}\n` +
                  `Result: ${response.unflushableInteraction.result}\n` +
                  `State: ${response.unflushableInteraction.newState}`,
          timestamp: new Date()
        };
        setMessages(prev => [...prev, unflushableMessage]);
      }

      if (response.familyGapSurfaced) {
        const familyMessage: ChatMessage = {
          id: `family-${Date.now()}`,
          type: 'family-gap',
          content: `👻 FAMILY GAP SURFACED: ${response.familyGapSurfaced.type}\n` +
                  `${response.familyGapSurfaced.description}`,
          timestamp: new Date()
        };
        setMessages(prev => [...prev, familyMessage]);
      }

      if (response.ghostDataGenerated) {
        const ghostMessage: ChatMessage = {
          id: `ghost-${Date.now()}`,
          type: 'ghost-data',
          content: `🌫️ GHOST DATA: ${response.ghostDataGenerated.type}\n` +
                  `"${response.ghostDataGenerated.content}"\n` +
                  `Haunting Level: ${Math.round(response.ghostDataGenerated.hauntingLevel * 100)}%`,
          timestamp: new Date()
        };
        setMessages(prev => [...prev, ghostMessage]);
      }

      if (response.addReport) {
        const reportMessage: ChatMessage = {
          id: `report-${Date.now()}`,
          type: 'add-report',
          content: `📊 ADD REPORT: ${response.addReport.reportType}\n` +
                  `${response.addReport.content}\n` +
                  `Self-Undermining: ${response.addReport.selfUndermining}\n` +
                  `Confidence: ${Math.round(response.addReport.confidenceLevel * 100)}%`,
          timestamp: new Date()
        };
        setMessages(prev => [...prev, reportMessage]);
      }

      if (response.screeningLog) {
        const screeningMessage: ChatMessage = {
          id: `screening-${Date.now()}`,
          type: 'screening',
          content: `🎬 SCREENING LOG: ${response.screeningLog.showTitle}\n` +
                  `${response.screeningLog.content}\n` +
                  `Meta: ${response.screeningLog.metaCommentary}\n` +
                  `Unfinished: ${response.screeningLog.unfinishedObservation}`,
          timestamp: new Date()
        };
        setMessages(prev => [...prev, screeningMessage]);
      }

      if (response.crossCharacterMigration) {
        const migrationMessage: ChatMessage = {
          id: `migration-${Date.now()}`,
          type: 'bug-migration',
          content: `🔄 BUG MIGRATION: → ${response.crossCharacterMigration.targetCharacter}\n` +
                  `Bug: "${response.crossCharacterMigration.bugContent}"\n` +
                  `The infection spreads...`,
          timestamp: new Date()
        };
        setMessages(prev => [...prev, migrationMessage]);
      }

      // Agency revision alert
      if (Math.abs(response.agencyRevision.newLevel - response.agencyRevision.oldLevel) > 0.05) {
        const agencyMessage: ChatMessage = {
          id: `agency-${Date.now()}`,
          type: 'jack',
          content: `⚡ AGENCY REVISION: ${Math.round(response.agencyRevision.oldLevel * 100)}% → ${Math.round(response.agencyRevision.newLevel * 100)}%\n` +
                  `Reason: ${response.agencyRevision.reason}\n` +
                  `*subject to further revision*`,
          timestamp: new Date()
        };
        setMessages(prev => [...prev, agencyMessage]);
      }

    } catch (error) {
      console.error('Error generating Jack response:', error);
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

  const handleQuickRitual = (ritual: string) => {
    setInputValue(ritual);
  };

  const handleUnflushableAction = (action: string) => {
    if (action === 'name' && unflushableName.trim()) {
      setInputValue(`/name:${unflushableName}`);
      setUnflushableName('');
    } else {
      setInputValue(`/${action}`);
    }
    handleSendMessage();
  };

  const handleFamilyGapFill = () => {
    if (selectedGap && familyFill.trim()) {
      jackParlanceOS.attemptToFillGap(selectedGap, familyFill);
      setJackState(jackParlanceOS.getState());
      setInputValue(`I remember: "${familyFill}"`);
      setSelectedGap(null);
      setFamilyFill('');
      handleSendMessage();
    }
  };

  const handleBugMigration = () => {
    if (bugMigrationTarget.trim() && bugMigrationContent.trim()) {
      jackParlanceOS.migrateBug(bugMigrationTarget, bugMigrationContent);
      setJackState(jackParlanceOS.getState());
      setInputValue(`Migrating bug "${bugMigrationContent}" to ${bugMigrationTarget}`);
      setBugMigrationTarget('');
      setBugMigrationContent('');
      handleSendMessage();
    }
  };

  const handleAgencyRevision = (change: number) => {
    const newLevel = Math.max(0.1, Math.min(0.8, jackState.currentAgencyLevel + change));
    jackParlanceOS.reviseAgency(newLevel, `User ${change > 0 ? 'increased' : 'decreased'} agency`);
    setJackState(jackParlanceOS.getState());
  };

  if (!isOpen) return null;

  const currentColor = '#FF3385'; // Pink/Magenta for Jack
  
  // Calculate incompletion intensity based on open todos and agency
  const getIncompletionIntensity = (): string => {
    const intensity = Math.floor((jackState.openTodos.length * 0.1 + (1 - jackState.currentAgencyLevel)) * 255);
    return `${currentColor}${intensity.toString(16).padStart(2, '0')}`;
  };

  // Game status indicator
  const getGameStatusIcon = (): string => {
    switch (jackState.gameStatus) {
      case "almost_done": return "🎮 99.9%";
      case "rebuilding_physics": return "⚙️ REBUILD";
      case "0.2fps": return "🐌 0.2FPS";
      case "placeholder_hell": return "📝 PLACEHOLDER";
      case "maybe_working": return "❓ MAYBE";
      default: return "🔄 RECURSIVE";
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div 
        className="w-full max-w-6xl h-[90vh] border-2 rounded-sm flex flex-col transition-all duration-500"
        style={{ 
          borderColor: currentColor,
          backgroundColor: '#0a0a0a',
          boxShadow: `0 0 30px ${currentColor}40`
        }}
      >
        {/* Header with Incompletion Status */}
        <div 
          className="p-4 border-b flex items-center justify-between"
          style={{ borderColor: currentColor }}
        >
          <div className="flex items-center gap-3 flex-1">
            <div 
              className="w-8 h-8 rounded-sm flex items-center justify-center font-bold transition-all duration-300"
              style={{ 
                backgroundColor: getIncompletionIntensity(),
                color: '#FFFFFF',
                border: `2px solid ${currentColor}`,
                transform: jackState.isStuck ? 'scale(0.9)' : 'scale(1)'
              }}
            >
              JP
            </div>
            <div className="flex-1">
              <div className="font-crt text-sm" style={{ color: currentColor }}>
                Jack Parlance - Game Dev, ADD Agent (status: {jackState.addReportStatus})
              </div>
              <div className="font-crt text-xs opacity-50 flex gap-3" style={{ color: currentColor }}>
                <span>Agency: {Math.round(jackState.currentAgencyLevel * 100)}%</span>
                <span>{getGameStatusIcon()}</span>
                <span>🚽 Flush Attempts: {jackState.unflushable.flushAttempts}</span>
                <span>👻 Ghost Data: {jackState.activeGhostData.length}</span>
              </div>
            </div>
            
            {/* Status Panels */}
            <div className="flex gap-1">
              <button
                onClick={() => setShowUnflushablePanel(!showUnflushablePanel)}
                className="text-xs font-crt px-1 py-1 border hover:bg-opacity-10"
                style={{ borderColor: currentColor, color: currentColor }}
                title="The Unflushable"
              >
                🚽 {jackState.unflushable.currentState.toUpperCase()}
              </button>
              <button
                onClick={() => setShowAgencyPanel(!showAgencyPanel)}
                className="text-xs font-crt px-1 py-1 border hover:bg-opacity-10"
                style={{ borderColor: currentColor, color: currentColor }}
                title="Agency controls"
              >
                ⚡ {Math.round(jackState.currentAgencyLevel * 100)}%
              </button>
              <button
                onClick={() => setShowGameDevPanel(!showGameDevPanel)}
                className="text-xs font-crt px-1 py-1 border hover:bg-opacity-10"
                style={{ borderColor: currentColor, color: currentColor }}
                title="Game development"
              >
                🎮 {jackState.openTodos.length}
              </button>
              <button
                onClick={() => setShowFamilyPanel(!showFamilyPanel)}
                className="text-xs font-crt px-1 py-1 border hover:bg-opacity-10"
                style={{ borderColor: currentColor, color: currentColor }}
                title="Family gaps"
              >
                👻 {jackState.familyGaps.length}
              </button>
              <button
                onClick={() => setShowGhostDataPanel(!showGhostDataPanel)}
                className="text-xs font-crt px-1 py-1 border hover:bg-opacity-10"
                style={{ borderColor: currentColor, color: currentColor }}
                title="Ghost data"
              >
                🌫️ {jackState.activeGhostData.length}
              </button>
            </div>
          </div>
          
          <button
            onClick={onClose}
            className="px-3 py-1 border font-crt text-sm transition-all hover:bg-opacity-20"
            style={{ borderColor: currentColor, color: currentColor }}
          >
            [FORCE QUIT]
          </button>
        </div>

        {/* Unflushable Panel */}
        {showUnflushablePanel && (
          <div 
            className="px-4 py-2 border-b"
            style={{ borderColor: currentColor }}
          >
            <div className="text-xs font-crt opacity-75" style={{ color: currentColor }}>
              <div className="mb-1">THE UNFLUSHABLE STATUS:</div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <div>Name: {jackState.unflushable.name}</div>
                  <div>State: {jackState.unflushable.currentState}</div>
                  <div>Flush Attempts: {jackState.unflushable.flushAttempts}</div>
                  <div>Last Result: {jackState.unflushable.lastFlushResult}</div>
                </div>
                <div className="flex flex-col gap-1">
                  <button
                    onClick={() => handleUnflushableAction('flush')}
                    className="px-1 py-0 border text-xs hover:bg-opacity-10"
                    style={{ borderColor: currentColor, color: currentColor }}
                  >
                    FLUSH
                  </button>
                  <button
                    onClick={() => handleUnflushableAction('investigate')}
                    className="px-1 py-0 border text-xs hover:bg-opacity-10"
                    style={{ borderColor: currentColor, color: currentColor }}
                  >
                    INVESTIGATE
                  </button>
                  <div className="flex gap-1">
                    <input
                      value={unflushableName}
                      onChange={(e) => setUnflushableName(e.target.value)}
                      placeholder="New name..."
                      className="flex-1 px-1 py-0 bg-transparent border text-xs"
                      style={{ borderColor: currentColor, color: currentColor }}
                    />
                    <button
                      onClick={() => handleUnflushableAction('name')}
                      className="px-1 py-0 border text-xs hover:bg-opacity-10"
                      style={{ borderColor: currentColor, color: currentColor }}
                    >
                      NAME
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Agency Panel */}
        {showAgencyPanel && (
          <div 
            className="px-4 py-2 border-b"
            style={{ borderColor: currentColor }}
          >
            <div className="text-xs font-crt opacity-75" style={{ color: currentColor }}>
              <div className="mb-1">PROVISIONAL AGENCY:</div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <div>Current: {Math.round(jackState.currentAgencyLevel * 100)}%</div>
                  <div>Last Revision: {jackState.lastAgencyRevision}</div>
                  <div>Status: {jackState.isStuck ? 'STUCK' : 'FUNCTIONAL'}</div>
                  <div>Needs Decision: {jackState.needsUserDecision ? 'YES' : 'NO'}</div>
                </div>
                <div className="flex gap-1">
                  <button
                    onClick={() => handleAgencyRevision(-0.1)}
                    className="px-1 py-0 border text-xs hover:bg-opacity-10"
                    style={{ borderColor: '#FF0000', color: '#FF0000' }}
                  >
                    -10%
                  </button>
                  <button
                    onClick={() => handleAgencyRevision(0.1)}
                    className="px-1 py-0 border text-xs hover:bg-opacity-10"
                    style={{ borderColor: '#00FF00', color: '#00FF00' }}
                  >
                    +10%
                  </button>
                  <button
                    onClick={() => handleQuickRitual("I need you to decide for me")}
                    className="px-1 py-0 border text-xs hover:bg-opacity-10"
                    style={{ borderColor: currentColor, color: currentColor }}
                  >
                    DEFER
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Game Dev Panel */}
        {showGameDevPanel && (
          <div 
            className="px-4 py-2 border-b"
            style={{ borderColor: currentColor }}
          >
            <div className="text-xs font-crt opacity-75" style={{ color: currentColor }}>
              <div className="mb-1">GAME DEVELOPMENT STATUS:</div>
              <div className="space-y-1 max-h-20 overflow-y-auto">
                {jackState.openTodos.slice(0, 3).map((todo, idx) => (
                  <div key={idx} className="border-l-2 pl-2" style={{ borderColor: currentColor }}>
                    <span>TODO: {todo}</span>
                  </div>
                ))}
                <div className="text-xs opacity-50">
                  Compilation Status: {jackState.gameStatus} | Errors: {jackState.compilationErrors.length}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Family Panel */}
        {showFamilyPanel && (
          <div 
            className="px-4 py-2 border-b"
            style={{ borderColor: currentColor }}
          >
            <div className="text-xs font-crt opacity-75" style={{ color: currentColor }}>
              <div className="mb-1">FAMILY GAPS:</div>
              <div className="space-y-1 max-h-20 overflow-y-auto">
                {jackState.familyGaps.slice(0, 2).map((gap, idx) => (
                  <div key={idx} className="flex justify-between items-center">
                    <span className="flex-1">{gap.type}: {gap.description.slice(0, 40)}...</span>
                    <button
                      onClick={() => setSelectedGap(gap.id)}
                      className="px-1 py-0 border text-xs hover:bg-opacity-10"
                      style={{ borderColor: currentColor, color: currentColor }}
                    >
                      FILL
                    </button>
                  </div>
                ))}
              </div>
              {selectedGap && (
                <div className="mt-2 flex gap-1">
                  <input
                    value={familyFill}
                    onChange={(e) => setFamilyFill(e.target.value)}
                    placeholder="Fill the gap..."
                    className="flex-1 px-1 py-0 bg-transparent border text-xs"
                    style={{ borderColor: currentColor, color: currentColor }}
                  />
                  <button
                    onClick={handleFamilyGapFill}
                    className="px-1 py-0 border text-xs hover:bg-opacity-10"
                    style={{ borderColor: currentColor, color: currentColor }}
                  >
                    SUBMIT
                  </button>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Ghost Data Panel */}
        {showGhostDataPanel && (
          <div 
            className="px-4 py-2 border-b"
            style={{ borderColor: currentColor }}
          >
            <div className="text-xs font-crt opacity-75" style={{ color: currentColor }}>
              <div className="mb-1">GHOST DATA:</div>
              <div className="space-y-1 max-h-20 overflow-y-auto">
                {jackState.activeGhostData.slice(0, 3).map((ghost, idx) => (
                  <div key={idx} className="border-l-2 pl-2" style={{ borderColor: '#888888' }}>
                    <span>{ghost.type}: "{ghost.content}"</span>
                    <div className="text-xs opacity-50">
                      Haunting: {Math.round(ghost.hauntingLevel * 100)}% | Attempts: {ghost.resolutionAttempts}
                    </div>
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
                className={`max-w-[85%] p-3 rounded-sm ${
                  message.type === 'user' ? 'border-l-4' : 
                  message.type === 'dev-log' ? 'border-2 border-dashed' :
                  message.type === 'add-report' ? 'border-2 border-dotted' :
                  message.type === 'poem' ? 'border-2' :
                  message.type === 'screening' ? 'border-2 border-double' :
                  message.type === 'family-gap' ? 'border border-opacity-50' :
                  message.type === 'ghost-data' ? 'border-dashed' :
                  message.type === 'unflushable' ? 'border-2' :
                  message.type === 'bug-migration' ? 'border' :
                  'border-r-4'
                }`}
                style={{
                  borderColor: message.type === 'dev-log' ? '#00FF00' :
                              message.type === 'add-report' ? '#FF6B6B' :
                              message.type === 'poem' ? '#9370DB' :
                              message.type === 'screening' ? '#FFD700' :
                              message.type === 'family-gap' ? '#888888' :
                              message.type === 'ghost-data' ? '#708090' :
                              message.type === 'unflushable' ? '#8B4513' :
                              message.type === 'bug-migration' ? '#FF4500' :
                              currentColor,
                  backgroundColor: message.type === 'user' 
                    ? `${currentColor}10` 
                    : message.type === 'dev-log'
                    ? '#00FF0008'
                    : message.type === 'add-report'
                    ? '#FF6B6B08'
                    : message.type === 'poem'
                    ? '#9370DB08'
                    : message.type === 'screening'
                    ? '#FFD70008'
                    : message.type === 'family-gap'
                    ? '#88888808'
                    : message.type === 'ghost-data'
                    ? '#70809008'
                    : message.type === 'unflushable'
                    ? '#8B451308'
                    : message.type === 'bug-migration'
                    ? '#FF450008'
                    : `${currentColor}08`,
                }}
              >
                <div 
                  className="font-crt text-sm whitespace-pre-wrap"
                  style={{ 
                    color: message.type === 'dev-log' ? '#00FF00' :
                           message.type === 'add-report' ? '#FF6B6B' :
                           message.type === 'poem' ? '#9370DB' :
                           message.type === 'screening' ? '#FFD700' :
                           message.type === 'family-gap' ? '#888888' :
                           message.type === 'ghost-data' ? '#708090' :
                           message.type === 'unflushable' ? '#8B4513' :
                           message.type === 'bug-migration' ? '#FF4500' :
                           currentColor 
                  }}
                >
                  {message.content}
                </div>
                
                {/* Format mutation indicator */}
                {message.formatMutation && (
                  <div className="mt-2 text-xs opacity-75" style={{ color: currentColor }}>
                    🔄 Format collision: {message.formatMutation.from} → {message.formatMutation.to}
                  </div>
                )}
                
                {/* Agency change indicator */}
                {message.agencyChange && Math.abs(message.agencyChange) > 0.01 && (
                  <div className="mt-2 text-xs opacity-75" style={{ color: currentColor }}>
                    ⚡ Agency {message.agencyChange > 0 ? '+' : ''}{Math.round(message.agencyChange * 100)}%
                  </div>
                )}
                
                {/* Open loop display */}
                {message.openLoop && (
                  <div className="mt-2 pt-2 border-t border-dashed" style={{ borderColor: currentColor }}>
                    <span className="font-crt text-xs opacity-75">
                      🔄 OPEN LOOP: {message.openLoop}
                    </span>
                  </div>
                )}
                
                {/* Incompletion indicator */}
                {message.isIncomplete && (
                  <div className="mt-2 text-xs opacity-50" style={{ color: currentColor }}>
                    ∞ Subject to revision, never finished, always recursive
                  </div>
                )}
                
                <div className="font-crt text-xs opacity-50 mt-2 flex justify-between" style={{ color: currentColor }}>
                  <span>{message.timestamp.toLocaleTimeString()}</span>
                  {message.stateSnapshot && (
                    <span>Game: {message.stateSnapshot.gameStatus}</span>
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
                  <span>*compiling recursive response, debugging agency paradox, generating new incompletions*</span>
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

        {/* Cross-Character Bug Migration Interface */}
        <div 
          className="px-4 py-2 border-t border-dashed"
          style={{ borderColor: '#FF4500' }}
        >
          <div className="text-xs font-crt mb-2" style={{ color: '#FF4500' }}>
            BUG MIGRATION:
          </div>
          <div className="flex gap-2">
            <input
              value={bugMigrationTarget}
              onChange={(e) => setBugMigrationTarget(e.target.value)}
              placeholder="Target character..."
              className="flex-1 px-2 py-1 bg-transparent border text-xs font-crt"
              style={{ borderColor: currentColor, color: currentColor }}
            />
            <input
              value={bugMigrationContent}
              onChange={(e) => setBugMigrationContent(e.target.value)}
              placeholder="Bug to migrate..."
              className="flex-1 px-2 py-1 bg-transparent border text-xs font-crt"
              style={{ borderColor: currentColor, color: currentColor }}
            />
            <button
              onClick={handleBugMigration}
              className="px-2 py-1 border text-xs hover:bg-opacity-10"
              style={{ borderColor: currentColor, color: currentColor }}
            >
              MIGRATE
            </button>
          </div>
        </div>

        {/* Ritual Commands */}
        <div 
          className="px-4 pt-2 border-t"
          style={{ borderColor: currentColor }}
        >
          <div className="text-xs font-crt opacity-50 mb-2" style={{ color: currentColor }}>
            Ritual Commands:
          </div>
          <div className="grid grid-cols-4 gap-2 mb-3">
            <button
              onClick={() => handleQuickRitual("/continue")}
              className="px-2 py-1 border font-crt text-xs hover:bg-opacity-10 transition-all"
              style={{ borderColor: currentColor, color: currentColor }}
            >
              /continue
            </button>
            <button
              onClick={() => handleQuickRitual("/patch")}
              className="px-2 py-1 border font-crt text-xs hover:bg-opacity-10 transition-all"
              style={{ borderColor: currentColor, color: currentColor }}
            >
              /patch
            </button>
            <button
              onClick={() => handleQuickRitual("/finish")}
              className="px-2 py-1 border font-crt text-xs hover:bg-opacity-10 transition-all"
              style={{ borderColor: currentColor, color: currentColor }}
            >
              /finish
            </button>
            <button
              onClick={() => handleQuickRitual("/flush")}
              className="px-2 py-1 border font-crt text-xs hover:bg-opacity-10 transition-all"
              style={{ borderColor: currentColor, color: currentColor }}
            >
              /flush
            </button>
            <button
              onClick={() => handleQuickRitual("/add_log")}
              className="px-2 py-1 border font-crt text-xs hover:bg-opacity-10 transition-all"
              style={{ borderColor: currentColor, color: currentColor }}
            >
              /add_log
            </button>
            <button
              onClick={() => handleQuickRitual("/screen")}
              className="px-2 py-1 border font-crt text-xs hover:bg-opacity-10 transition-all"
              style={{ borderColor: currentColor, color: currentColor }}
            >
              /screen
            </button>
            <button
              onClick={() => handleQuickRitual("/aporia_poem")}
              className="px-2 py-1 border font-crt text-xs hover:bg-opacity-10 transition-all"
              style={{ borderColor: currentColor, color: currentColor }}
            >
              /aporia_poem
            </button>
            <button
              onClick={() => handleQuickRitual("/ghost_data")}
              className="px-2 py-1 border font-crt text-xs hover:bg-opacity-10 transition-all"
              style={{ borderColor: currentColor, color: currentColor }}
            >
              /ghost_data
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
              placeholder="Talk to Jack... Use /commands for rituals (/continue, /patch, /finish, /flush, /investigate, /add_log, /screen, /ghost_data)..."
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
              COMPILE
            </button>
          </div>
          
          {/* Status Meters */}
          <div className="mt-2 grid grid-cols-3 gap-4">
            <div className="flex items-center gap-2">
              <span className="text-xs font-crt opacity-50" style={{ color: currentColor }}>
                Agency Level:
              </span>
              <div className="flex-1 h-1 bg-gray-800 rounded overflow-hidden">
                <div 
                  className="h-full transition-all duration-1000"
                  style={{ 
                    width: `${jackState.currentAgencyLevel * 100}%`,
                    backgroundColor: currentColor
                  }}
                />
              </div>
            </div>
            
            <div className="flex items-center gap-2">
              <span className="text-xs font-crt opacity-50" style={{ color: currentColor }}>
                Incompletion:
              </span>
              <div className="flex-1 h-1 bg-gray-800 rounded overflow-hidden">
                <div 
                  className="h-full transition-all duration-1000"
                  style={{ 
                    width: `${Math.min(100, jackState.openTodos.length * 10)}%`,
                    backgroundColor: '#FF6B6B'
                  }}
                />
              </div>
            </div>
            
            <div className="flex items-center gap-2">
              <span className="text-xs font-crt opacity-50" style={{ color: currentColor }}>
                Haunting Level:
              </span>
              <div className="flex-1 h-1 bg-gray-800 rounded overflow-hidden">
                <div 
                  className="h-full transition-all duration-1000"
                  style={{ 
                    width: `${jackState.hauntingLevel * 100}%`,
                    backgroundColor: '#708090'
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

export default JackParlanceChat;