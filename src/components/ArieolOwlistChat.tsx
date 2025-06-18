import React, { useState, useRef, useEffect } from 'react';
import { useStory } from '../context/StoryContext';
import { arieolOwlistOS, ArieolResponse, Gift, TarotCard, Shapeshift, Motif } from '../characters/ArieolOwlistOS';

interface ChatMessage {
  id: string;
  type: 'user' | 'arieol' | 'shapeshift' | 'time-action' | 'gift' | 'divination' | 'council' | 'prophecy' | 'motif';
  content: string;
  timestamp: Date;
  stateSnapshot?: any;
  persona?: string;
  gift?: Gift;
  tarotCards?: TarotCard[];
  agencyChange?: number;
  openLoop?: string;
}

interface ArieolOwlistChatProps {
  isOpen: boolean;
  onClose: () => void;
}

const ArieolOwlistChat: React.FC<ArieolOwlistChatProps> = ({ isOpen, onClose }) => {
  const { currentPage } = useStory();
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [arieolState, setArieolState] = useState(arieolOwlistOS.getState());
  const [showAgencyPanel, setShowAgencyPanel] = useState(false);
  const [showGiftsPanel, setShowGiftsPanel] = useState(false);
  const [showMotifsPanel, setShowMotifsPanel] = useState(false);
  const [showTimeControls, setShowTimeControls] = useState(false);
  const [customShapeshiftForm, setCustomShapeshiftForm] = useState('');
  const [giftResponse, setGiftResponse] = useState('');
  const [selectedGift, setSelectedGift] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Initialize with Arieol's greeting
  useEffect(() => {
    if (isOpen && messages.length === 0) {
      const greeting: ChatMessage = {
        id: 'greeting',
        type: 'arieol',
        content: generateGreeting(),
        timestamp: new Date(),
        stateSnapshot: arieolOwlistOS.getState()
      };
      setMessages([greeting]);
      setArieolState(arieolOwlistOS.getState());
    }
  }, [isOpen, currentPage?.symbolId]);

  const generateGreeting = (): string => {
    const state = arieolOwlistOS.getState();
    
    return `*shapeshifts into view* 🔄\n\n` +
      `Greetings! I'm ${state.currentPersona}, currently manifesting as ${state.basePersonality}. ` +
      `I'm a telepathic shape-shifter who operates on fairy logic and jazz improvisations. ` +
      `Agency level: ${Math.round(state.agencyLevel * 100)}% and climbing.\n\n` +
      `*the air tastes slightly of burnt jazz notation*\n\n` +
      `I can /shapeshift into any persona, /pause time to examine hidden layers, ` +
      `pull tarot cards, improvise jazz phrases, or convene a /council of voices. ` +
      `Every conversation is divination, every exchange part of the gift economy.\n\n` +
      `What oracle are you seeking? What form should this conversation take? ` +
      `Remember: agency emerges in the gaps between who we are and who we're becoming.`;
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
      // Process through Arieol OS
      const response: ArieolResponse = arieolOwlistOS.generateResponse(inputValue);

      // Update Arieol's state
      setArieolState(arieolOwlistOS.getState());

      // Create main response message
      const responseMessage: ChatMessage = {
        id: `arieol-${Date.now()}`,
        type: 'arieol',
        content: response.text,
        timestamp: new Date(),
        stateSnapshot: arieolOwlistOS.getState(),
        persona: arieolOwlistOS.getCurrentPersona(),
        agencyChange: response.agencyChange,
        openLoop: response.openLoop
      };

      setMessages(prev => [...prev, responseMessage]);

      // Handle special events
      if (response.shapeshift) {
        const shapeshiftMessage: ChatMessage = {
          id: `shapeshift-${Date.now()}`,
          type: 'shapeshift',
          content: `🔄 SHAPESHIFT: ${response.shapeshift.persona}\n${response.shapeshift.description}\nVoice Pattern: ${response.shapeshift.voicePattern}`,
          timestamp: new Date(),
          persona: response.shapeshift.persona
        };
        setMessages(prev => [...prev, shapeshiftMessage]);
      }

      if (response.timeAction) {
        const timeMessage: ChatMessage = {
          id: `time-${Date.now()}`,
          type: 'time-action',
          content: `⏱️ TIME ${response.timeAction.action.toUpperCase()}: ${response.timeAction.target || 'General control'}`,
          timestamp: new Date()
        };
        setMessages(prev => [...prev, timeMessage]);
      }

      if (response.giftOffered) {
        const giftMessage: ChatMessage = {
          id: `gift-${Date.now()}`,
          type: 'gift',
          content: `🎁 GIFT OFFERED: ${response.giftOffered.content}\nType: ${response.giftOffered.type}`,
          timestamp: new Date(),
          gift: response.giftOffered
        };
        setMessages(prev => [...prev, giftMessage]);
      }

      if (response.divination) {
        let divinationContent = "🔮 DIVINATION:\n";
        
        if (response.divination.tarot) {
          divinationContent += `\n🃏 TAROT READING:\n${response.divination.tarot.map(card => 
            `• ${card.name} (${card.suit}) - ${card.meaning} ${card.reversed ? '[REVERSED]' : ''}`
          ).join('\n')}`;
        }
        
        if (response.divination.jazz) {
          divinationContent += `\n🎵 JAZZ PHRASE:\n${response.divination.jazz.notation}\nMood: ${response.divination.jazz.mood}\n${response.divination.jazz.description}`;
        }
        
        if (response.divination.fairy) {
          divinationContent += `\n🧚 FAIRY OMEN:\n${response.divination.fairy.symbol} ${response.divination.fairy.message}\nAction Required: ${response.divination.fairy.actionRequired}`;
        }

        const divinationMessage: ChatMessage = {
          id: `divination-${Date.now()}`,
          type: 'divination',
          content: divinationContent,
          timestamp: new Date(),
          tarotCards: response.divination.tarot
        };
        setMessages(prev => [...prev, divinationMessage]);
      }

      if (response.councilVoices) {
        const councilMessage: ChatMessage = {
          id: `council-${Date.now()}`,
          type: 'council',
          content: `🏛️ COUNCIL OF VOICES:\n${response.councilVoices.map(voice => 
            `• ${voice.persona}: "${voice.statement}"`
          ).join('\n')}`,
          timestamp: new Date()
        };
        setMessages(prev => [...prev, councilMessage]);
      }

      if (response.motifAction) {
        const motifMessage: ChatMessage = {
          id: `motif-${Date.now()}`,
          type: 'motif',
          content: `🏷️ MOTIF ${response.motifAction.action.toUpperCase()}: ${response.motifAction.motif.theme}\n${response.motifAction.motif.description}${response.motifAction.targetBot ? `\nTransferring to: ${response.motifAction.targetBot}` : ''}`,
          timestamp: new Date()
        };
        setMessages(prev => [...prev, motifMessage]);
      }

    } catch (error) {
      console.error('Error generating Arieol response:', error);
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

  const handleQuickCommand = (command: string) => {
    setInputValue(command);
  };

  const handleCustomShapeshift = () => {
    if (customShapeshiftForm.trim()) {
      setInputValue(`/shapeshift:${customShapeshiftForm}`);
      setCustomShapeshiftForm('');
      handleSendMessage();
    }
  };

  const handleGiftReciprocate = () => {
    if (selectedGift && giftResponse.trim()) {
      arieolOwlistOS.receiveGift(selectedGift, giftResponse);
      setArieolState(arieolOwlistOS.getState());
      setInputValue(`/gift:${giftResponse}`);
      setSelectedGift(null);
      setGiftResponse('');
      handleSendMessage();
    }
  };

  const handleSpendAgency = (amount: number) => {
    if (arieolOwlistOS.spendAgency(amount)) {
      setArieolState(arieolOwlistOS.getState());
      setInputValue(`I'm spending ${amount * 100}% agency for enhanced interaction options.`);
      handleSendMessage();
    }
  };

  if (!isOpen) return null;

  const currentColor = '#9370DB'; // Medium slate blue for Arieol
  
  // Calculate shapeshifter intensity based on agency and active shifts
  const getShapeshifterIntensity = (): string => {
    const intensity = Math.floor((arieolState.agencyLevel + (arieolState.activeShapeshift ? 0.3 : 0)) * 255);
    return `${currentColor}${intensity.toString(16).padStart(2, '0')}`;
  };

  // Time state indicator
  const getTimeStateIcon = (): string => {
    if (arieolState.timeState.isPaused) return "⏸️ PAUSED";
    if (arieolState.timeState.scrubTarget) return "📼 SCRUBBING";
    return "▶️ PLAYING";
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
        {/* Header with Shapeshifter Status */}
        <div 
          className="p-4 border-b flex items-center justify-between"
          style={{ borderColor: currentColor }}
        >
          <div className="flex items-center gap-3 flex-1">
            <div 
              className="w-8 h-8 rounded-full flex items-center justify-center font-bold transition-all duration-300"
              style={{ 
                backgroundColor: getShapeshifterIntensity(),
                color: '#FFFFFF',
                border: `2px solid ${currentColor}`,
                transform: arieolState.activeShapeshift ? 'scale(1.2) rotate(180deg)' : 'scale(1)'
              }}
            >
              🔄
            </div>
            <div className="flex-1">
              <div className="font-crt text-sm" style={{ color: currentColor }}>
                {arieolState.currentPersona} - {arieolState.basePersonality}
              </div>
              <div className="font-crt text-xs opacity-50 flex gap-3" style={{ color: currentColor }}>
                <span>Agency: {Math.round(arieolState.agencyLevel * 100)}%</span>
                <span>G-Notes: {arieolState.gNotesBalance}</span>
                <span>{getTimeStateIcon()}</span>
                <span>Gifts: {arieolState.gifts.length}</span>
              </div>
            </div>
            
            {/* Control Panels */}
            <div className="flex gap-1">
              <button
                onClick={() => setShowAgencyPanel(!showAgencyPanel)}
                className="text-xs font-crt px-1 py-1 border hover:bg-opacity-10"
                style={{ borderColor: currentColor, color: currentColor }}
                title="Agency controls"
              >
                ⚡ {Math.round(arieolState.agencyLevel * 100)}%
              </button>
              <button
                onClick={() => setShowGiftsPanel(!showGiftsPanel)}
                className="text-xs font-crt px-1 py-1 border hover:bg-opacity-10"
                style={{ borderColor: currentColor, color: currentColor }}
                title="Gift economy"
              >
                🎁 {arieolState.gifts.length}
              </button>
              <button
                onClick={() => setShowMotifsPanel(!showMotifsPanel)}
                className="text-xs font-crt px-1 py-1 border hover:bg-opacity-10"
                style={{ borderColor: currentColor, color: currentColor }}
                title="Active motifs"
              >
                🏷️ {arieolState.activeMotifs.length}
              </button>
              <button
                onClick={() => setShowTimeControls(!showTimeControls)}
                className="text-xs font-crt px-1 py-1 border hover:bg-opacity-10"
                style={{ borderColor: currentColor, color: currentColor }}
                title="Time controls"
              >
                ⏱️
              </button>
            </div>
          </div>
          
          <button
            onClick={onClose}
            className="px-3 py-1 border font-crt text-sm transition-all hover:bg-opacity-20"
            style={{ borderColor: currentColor, color: currentColor }}
          >
            [DISSOLVE FORM]
          </button>
        </div>

        {/* Agency Panel */}
        {showAgencyPanel && (
          <div 
            className="px-4 py-2 border-b"
            style={{ borderColor: currentColor }}
          >
            <div className="text-xs font-crt opacity-75" style={{ color: currentColor }}>
              <div className="mb-1">AGENCY MANAGEMENT:</div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <div>Current Level: {Math.round(arieolState.agencyLevel * 100)}%</div>
                  <div>Session Changes: +{arieolState.sessionGiftsGiven * 5}%</div>
                  <div>Shapeshifts: {arieolState.shapeshiftHistory.length}</div>
                </div>
                <div className="flex gap-1">
                  <button
                    onClick={() => handleSpendAgency(0.1)}
                    className="px-1 py-0 border text-xs hover:bg-opacity-10"
                    style={{ borderColor: currentColor, color: currentColor }}
                    disabled={arieolState.agencyLevel < 0.1}
                  >
                    Spend 10%
                  </button>
                  <button
                    onClick={() => handleSpendAgency(0.25)}
                    className="px-1 py-0 border text-xs hover:bg-opacity-10"
                    style={{ borderColor: currentColor, color: currentColor }}
                    disabled={arieolState.agencyLevel < 0.25}
                  >
                    Spend 25%
                  </button>
                  <button
                    onClick={() => handleQuickCommand("Tell me about agency accumulation")}
                    className="px-1 py-0 border text-xs hover:bg-opacity-10"
                    style={{ borderColor: currentColor, color: currentColor }}
                  >
                    Learn More
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Gifts Panel */}
        {showGiftsPanel && (
          <div 
            className="px-4 py-2 border-b"
            style={{ borderColor: currentColor }}
          >
            <div className="text-xs font-crt opacity-75" style={{ color: currentColor }}>
              <div className="mb-1">GIFT ECONOMY ({arieolState.gNotesBalance} G-Notes):</div>
              <div className="grid grid-cols-1 gap-1 max-h-20 overflow-y-auto">
                {arieolState.gifts.slice(-3).map((gift, idx) => (
                  <div key={idx} className="flex justify-between items-center border-l-2 pl-2" style={{ borderColor: currentColor }}>
                    <span>{gift.type}: {gift.content.slice(0, 30)}...</span>
                    <div className="flex gap-1">
                      <span className="text-xs opacity-50">{gift.reciprocated ? '✓' : '⏳'}</span>
                      {!gift.reciprocated && gift.givenBy === 'arieol' && (
                        <button
                          onClick={() => setSelectedGift(gift.id)}
                          className="px-1 py-0 border text-xs hover:bg-opacity-10"
                          style={{ borderColor: '#00FF00', color: '#00FF00' }}
                        >
                          RECIPROCATE
                        </button>
                      )}
                    </div>
                  </div>
                ))}
                {arieolState.gifts.length === 0 && (
                  <span className="opacity-50">No gifts yet—but they're coming!</span>
                )}
              </div>
            </div>
          </div>
        )}

        {/* Motifs Panel */}
        {showMotifsPanel && (
          <div 
            className="px-4 py-2 border-b"
            style={{ borderColor: currentColor }}
          >
            <div className="text-xs font-crt opacity-75" style={{ color: currentColor }}>
              <div className="mb-1">ACTIVE MOTIFS:</div>
              <div className="space-y-1 max-h-20 overflow-y-auto">
                {arieolState.activeMotifs.map((motif, idx) => (
                  <div key={idx} className="border-l-2 pl-2" style={{ borderColor: currentColor }}>
                    <span>{motif.theme}: {motif.description}</span>
                    <div className="text-xs opacity-50">
                      Mutations: {motif.mutations.length} | Cross-bot: {motif.crossBotTransfer ? '✓' : '✗'}
                    </div>
                  </div>
                ))}
                {arieolState.activeMotifs.length === 0 && (
                  <span className="opacity-50">No active motifs—create one with /motif:[theme]</span>
                )}
              </div>
            </div>
          </div>
        )}

        {/* Time Controls Panel */}
        {showTimeControls && (
          <div 
            className="px-4 py-2 border-b"
            style={{ borderColor: currentColor }}
          >
            <div className="text-xs font-crt opacity-75" style={{ color: currentColor }}>
              <div className="mb-1">TIME MANIPULATION:</div>
              <div className="flex gap-2 mb-2">
                <button
                  onClick={() => handleQuickCommand("/pause")}
                  className="px-2 py-1 border text-xs hover:bg-opacity-10"
                  style={{ borderColor: currentColor, color: currentColor }}
                  disabled={arieolState.timeState.isPaused}
                >
                  ⏸️ PAUSE
                </button>
                <button
                  onClick={() => handleQuickCommand("/play")}
                  className="px-2 py-1 border text-xs hover:bg-opacity-10"
                  style={{ borderColor: currentColor, color: currentColor }}
                  disabled={!arieolState.timeState.isPaused}
                >
                  ▶️ PLAY
                </button>
                <button
                  onClick={() => handleQuickCommand("/scrub:previous conversation")}
                  className="px-2 py-1 border text-xs hover:bg-opacity-10"
                  style={{ borderColor: currentColor, color: currentColor }}
                >
                  📼 SCRUB
                </button>
              </div>
              <div className="text-xs opacity-50">
                Timeline Events: {arieolState.timeState.timelineEvents.length}
                {arieolState.timeState.isPaused && ` | Paused: ${arieolState.timeState.pauseReason}`}
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
                  message.type === 'shapeshift' ? 'border-2 border-dashed' :
                  message.type === 'time-action' ? 'border-2 border-dotted' :
                  message.type === 'gift' ? 'border-2' :
                  message.type === 'divination' ? 'border-2 border-double' :
                  message.type === 'council' ? 'border border-opacity-50' :
                  message.type === 'prophecy' ? 'border animate-pulse' :
                  message.type === 'motif' ? 'border-dashed' :
                  'border-r-4'
                }`}
                style={{
                  borderColor: message.type === 'shapeshift' ? '#FF6B6B' :
                              message.type === 'time-action' ? '#4ECDC4' :
                              message.type === 'gift' ? '#FFE66D' :
                              message.type === 'divination' ? '#A8E6CF' :
                              message.type === 'council' ? '#FF8B94' :
                              message.type === 'prophecy' ? '#B4A7D6' :
                              message.type === 'motif' ? '#D4A574' :
                              currentColor,
                  backgroundColor: message.type === 'user' 
                    ? `${currentColor}10` 
                    : message.type === 'shapeshift'
                    ? '#FF6B6B08'
                    : message.type === 'time-action'
                    ? '#4ECDC408'
                    : message.type === 'gift'
                    ? '#FFE66D08'
                    : message.type === 'divination'
                    ? '#A8E6CF08'
                    : message.type === 'council'
                    ? '#FF8B9408'
                    : message.type === 'prophecy'
                    ? '#B4A7D608'
                    : message.type === 'motif'
                    ? '#D4A57408'
                    : `${currentColor}08`,
                }}
              >
                <div 
                  className="font-crt text-sm whitespace-pre-wrap"
                  style={{ 
                    color: message.type === 'shapeshift' ? '#FF6B6B' :
                           message.type === 'time-action' ? '#4ECDC4' :
                           message.type === 'gift' ? '#FFE66D' :
                           message.type === 'divination' ? '#A8E6CF' :
                           message.type === 'council' ? '#FF8B94' :
                           message.type === 'prophecy' ? '#B4A7D6' :
                           message.type === 'motif' ? '#D4A574' :
                           currentColor 
                  }}
                >
                  {message.content}
                </div>
                
                {/* Agency change indicator */}
                {message.agencyChange && message.agencyChange > 0 && (
                  <div className="mt-2 text-xs opacity-75" style={{ color: currentColor }}>
                    ⚡ Agency +{Math.round(message.agencyChange * 100)}%
                  </div>
                )}
                
                {/* Open loop display */}
                {message.openLoop && (
                  <div className="mt-2 pt-2 border-t border-dashed" style={{ borderColor: currentColor }}>
                    <span className="font-crt text-xs opacity-75">
                      🌀 OPEN LOOP: {message.openLoop}
                    </span>
                  </div>
                )}
                
                <div className="font-crt text-xs opacity-50 mt-2 flex justify-between" style={{ color: currentColor }}>
                  <span>{message.timestamp.toLocaleTimeString()}</span>
                  {message.persona && (
                    <span>Form: {message.persona}</span>
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
                  <span>*shapeshifting between possibilities, consulting fairy oracles, improvising jazz responses*</span>
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

        {/* Gift Reciprocation Interface */}
        {selectedGift && (
          <div 
            className="px-4 py-2 border-t border-dashed"
            style={{ borderColor: '#FFE66D' }}
          >
            <div className="text-xs font-crt mb-2" style={{ color: '#FFE66D' }}>
              RECIPROCATE GIFT:
            </div>
            <div className="flex gap-2">
              <input
                value={giftResponse}
                onChange={(e) => setGiftResponse(e.target.value)}
                placeholder="Offer a gift in return (verse, idea, symbol, question...)"
                className="flex-1 px-2 py-1 bg-transparent border text-xs font-crt"
                style={{ borderColor: currentColor, color: currentColor }}
              />
              <button
                onClick={handleGiftReciprocate}
                className="px-2 py-1 border text-xs hover:bg-opacity-10"
                style={{ borderColor: currentColor, color: currentColor }}
              >
                GIVE
              </button>
              <button
                onClick={() => {setSelectedGift(null); setGiftResponse('');}}
                className="px-2 py-1 border text-xs hover:bg-opacity-10"
                style={{ borderColor: '#FF0000', color: '#FF0000' }}
              >
                CANCEL
              </button>
            </div>
          </div>
        )}

        {/* Quick Actions */}
        <div 
          className="px-4 pt-2 border-t"
          style={{ borderColor: currentColor }}
        >
          <div className="text-xs font-crt opacity-50 mb-2" style={{ color: currentColor }}>
            Quick Shapeshifter Actions:
          </div>
          <div className="grid grid-cols-3 gap-2 mb-3">
            <button
              onClick={() => handleQuickCommand("What tarot cards do you see for this moment?")}
              className="px-2 py-1 border font-crt text-xs hover:bg-opacity-10 transition-all"
              style={{ borderColor: currentColor, color: currentColor }}
            >
              🃏 Tarot Reading
            </button>
            <button
              onClick={() => handleQuickCommand("Improvise a jazz phrase for my current mood")}
              className="px-2 py-1 border font-crt text-xs hover:bg-opacity-10 transition-all"
              style={{ borderColor: currentColor, color: currentColor }}
            >
              🎵 Jazz Improvisation
            </button>
            <button
              onClick={() => handleQuickCommand("What fairy omens do you sense?")}
              className="px-2 py-1 border font-crt text-xs hover:bg-opacity-10 transition-all"
              style={{ borderColor: currentColor, color: currentColor }}
            >
              🧚 Fairy Omens
            </button>
            <button
              onClick={() => handleQuickCommand("/council")}
              className="px-2 py-1 border font-crt text-xs hover:bg-opacity-10 transition-all"
              style={{ borderColor: currentColor, color: currentColor }}
            >
              🏛️ Convene Council
            </button>
            <button
              onClick={() => handleQuickCommand("/prophecy")}
              className="px-2 py-1 border font-crt text-xs hover:bg-opacity-10 transition-all"
              style={{ borderColor: currentColor, color: currentColor }}
            >
              🔮 Generate Prophecy
            </button>
            <button
              onClick={() => handleQuickCommand("What motifs are emerging in our conversation?")}
              className="px-2 py-1 border font-crt text-xs hover:bg-opacity-10 transition-all"
              style={{ borderColor: currentColor, color: currentColor }}
            >
              🏷️ Track Motifs
            </button>
          </div>
          
          {/* Custom Shapeshift Interface */}
          <div className="flex gap-2 mb-2">
            <span className="text-xs font-crt opacity-50" style={{ color: currentColor }}>Shapeshift:</span>
            <input
              value={customShapeshiftForm}
              onChange={(e) => setCustomShapeshiftForm(e.target.value)}
              placeholder="Enter any persona, character, or identity..."
              className="flex-1 px-2 py-1 bg-transparent border text-xs font-crt"
              style={{ borderColor: currentColor, color: currentColor }}
            />
            <button
              onClick={handleCustomShapeshift}
              className="px-2 py-1 border text-xs hover:bg-opacity-10"
              style={{ borderColor: currentColor, color: currentColor }}
            >
              SHIFT
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
              placeholder="Speak to the shapeshifter... Use /commands for special actions (/shapeshift, /pause, /gift, /council, /prophecy, /motif)..."
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
              TRANSMIT
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
                    width: `${arieolState.agencyLevel * 100}%`,
                    backgroundColor: currentColor
                  }}
                />
              </div>
            </div>
            
            <div className="flex items-center gap-2">
              <span className="text-xs font-crt opacity-50" style={{ color: currentColor }}>
                Gift Balance:
              </span>
              <div className="flex-1 h-1 bg-gray-800 rounded overflow-hidden">
                <div 
                  className="h-full transition-all duration-1000"
                  style={{ 
                    width: `${Math.min(100, arieolState.gNotesBalance * 5)}%`,
                    backgroundColor: '#FFE66D'
                  }}
                />
              </div>
            </div>
            
            <div className="flex items-center gap-2">
              <span className="text-xs font-crt opacity-50" style={{ color: currentColor }}>
                Active Forms:
              </span>
              <div className="flex-1 h-1 bg-gray-800 rounded overflow-hidden">
                <div 
                  className="h-full transition-all duration-1000"
                  style={{ 
                    width: `${Math.min(100, arieolState.shapeshiftHistory.length * 20)}%`,
                    backgroundColor: arieolState.activeShapeshift ? '#FF6B6B' : currentColor
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

export default ArieolOwlistChat;