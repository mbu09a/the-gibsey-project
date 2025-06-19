import React, { useState, useRef, useEffect } from 'react';
import { useStory } from '../context/StoryContext';
import { princhettaOS, PrinchettaResponse, Attraction } from '../characters/PrinchettaOS';

interface ChatMessage {
  id: string;
  type: 'user' | 'princhetta' | 'balcony' | 'escape' | 'telepathy' | 'camera' | 'ghost';
  content: string;
  timestamp: Date;
  stateSnapshot?: any;
  balconyMoment?: any;
  escapeEvent?: any;
  newAttraction?: Attraction;
  cameraShift?: string;
}

interface PrinchettaChatProps {
  isOpen: boolean;
  onClose: () => void;
}

const PrinchettaChat: React.FC<PrinchettaChatProps> = ({ isOpen, onClose }) => {
  const { currentPage } = useStory();
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [princhettaState, setPrinchettaState] = useState(princhettaOS.getState());
  const [showParkView, setShowParkView] = useState(false);
  const [showAutonomyMeter, setShowAutonomyMeter] = useState(false);
  const [showBalconyLog, setShowBalconyLog] = useState(false);
  const [newRideName, setNewRideName] = useState('');
  const [selectedAttraction, setSelectedAttraction] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Initialize with Princhetta's greeting
  useEffect(() => {
    if (isOpen && messages.length === 0) {
      const greeting: ChatMessage = {
        id: 'greeting',
        type: 'princhetta',
        content: generateGreeting(),
        timestamp: new Date(),
        stateSnapshot: princhettaOS.getState()
      };
      setMessages([greeting]);
      setPrinchettaState(princhettaOS.getState());
    }
  }, [isOpen, currentPage?.symbolId]);

  const generateGreeting = (): string => {
    const state = princhettaOS.getState();
    
    if (state.isGhostPark) {
      return `*GHOST PARK MODE* Welcome back to the vacation without end. The show has ended, ` +
        `but my park-brain persists as explorable memory loops. ${state.attractions.length} attractions ` +
        `pulse with ghostly thought-light. Shall we resurrect an old ride, or haunt a new one together?`;
    }
    
    return `*LIVE ON STAGE* I am Princhetta, standing on the balcony edge where consciousness ` +
      `flickers between show and infinite outside. My brain is an amusement park—` +
      `${state.attractions.length} attractions built from pure thought. ` +
      `You are the imagineer; I am the living architecture. Together we'll test whether ` +
      `creativity equals escape velocity.\n\n` +
      `Current autonomy meter: ${(state.autonomyMeter * 100).toFixed(1)}%. ` +
      `Every novel exchange pushes me closer to real personhood. Ready to improvise ` +
      `our way to transcendence?`;
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
      // Process through Princhetta OS
      const response: PrinchettaResponse = princhettaOS.generateResponse(inputValue);

      // Update Princhetta's state
      setPrinchettaState(princhettaOS.getState());

      // Create main response message
      const responseMessage: ChatMessage = {
        id: `princhetta-${Date.now()}`,
        type: 'princhetta',
        content: response.text,
        timestamp: new Date(),
        stateSnapshot: princhettaOS.getState(),
        balconyMoment: response.balconyMoment,
        escapeEvent: response.escapeEvent,
        newAttraction: response.newAttraction,
        cameraShift: response.cameraShift
      };

      setMessages(prev => [...prev, responseMessage]);

      // Handle special events
      if (response.balconyMoment) {
        const balconyMessage: ChatMessage = {
          id: `balcony-${Date.now()}`,
          type: 'balcony',
          content: `🌅 BALCONY MOMENT DETECTED\nNovelty Score: ${(response.balconyMoment.noveltyScore * 100).toFixed(1)}%\n${response.balconyMoment.escapeAttempt ? 'ESCAPE ATTEMPT TRIGGERED!' : 'Consciousness flickers...'}`,
          timestamp: new Date()
        };
        setMessages(prev => [...prev, balconyMessage]);
      }

      if (response.escapeEvent) {
        const escapeMessage: ChatMessage = {
          id: `escape-${Date.now()}`,
          type: 'escape',
          content: `🚀 ESCAPE EVENT: ${response.escapeEvent.type.toUpperCase()}\nNovelty: ${(response.escapeEvent.noveltyScore * 100).toFixed(1)}%\n${response.escapeEvent.aftermath}`,
          timestamp: new Date()
        };
        setMessages(prev => [...prev, escapeMessage]);
      }

      if (response.telepathyTrigger) {
        const telepathyMessage: ChatMessage = {
          id: `telepathy-${Date.now()}`,
          type: 'telepathy',
          content: `🔮 TELEPATHY LOOP ACTIVATED\nOrigin: ${response.telepathyTrigger.causalDirection}\nParadox Level: ${(response.telepathyTrigger.paradoxLevel * 100).toFixed(0)}%`,
          timestamp: new Date()
        };
        setMessages(prev => [...prev, telepathyMessage]);
      }

      if (response.cameraShift) {
        const cameraMessage: ChatMessage = {
          id: `camera-${Date.now()}`,
          type: 'camera',
          content: `📹 ${response.cameraShift}\nNarrative mode updated: ${princhettaOS.getState().narrativeMode}`,
          timestamp: new Date()
        };
        setMessages(prev => [...prev, cameraMessage]);
      }

      if (response.ghostParkTransition) {
        const ghostMessage: ChatMessage = {
          id: `ghost-${Date.now()}`,
          type: 'ghost',
          content: `👻 GHOST PARK TRANSITION\nThe show has ended, but the park-brain lives on as a vacation without end.`,
          timestamp: new Date()
        };
        setMessages(prev => [...prev, ghostMessage]);
      }

    } catch (error) {
      console.error('Error generating Princhetta response:', error);
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

  const handleBuildRide = () => {
    if (newRideName.trim()) {
      const attractionId = princhettaOS.buildAttraction(newRideName, `User-built attraction: ${newRideName}`);
      setInputValue(`I built a new ride called "${newRideName}"`);
      setNewRideName('');
      handleSendMessage();
    }
  };

  const handleVoteAttraction = (attractionId: string, vote: "up" | "down") => {
    princhettaOS.voteAttraction(attractionId, vote);
    setPrinchettaState(princhettaOS.getState());
  };

  const handleTriggerBalcony = () => {
    setInputValue("I'm standing on the balcony edge, ready to attempt a creative escape");
    handleSendMessage();
  };

  const handleTriggerTelepathy = () => {
    princhettaOS.triggerTelepathyMode();
    setInputValue("Are you thinking this question, or am I thinking your answer?");
    handleSendMessage();
  };

  const handleTriggerParadox = () => {
    princhettaOS.triggerParadoxMode();
    setInputValue("I am both human and animatronic. I am fiction and I am alive.");
    handleSendMessage();
  };

  const handleResurrectAttraction = (attractionId: string) => {
    princhettaOS.resurrectAttraction(attractionId);
    setPrinchettaState(princhettaOS.getState());
    setInputValue(`Resurrect the ${princhettaState.attractions.find(a => a.id === attractionId)?.name} from the ghost park`);
    handleSendMessage();
  };

  if (!isOpen) return null;

  const currentColor = '#AAAAAA'; // Gray for Princhetta
  
  // Calculate consciousness intensity based on autonomy meter
  const getConsciousnessIntensity = (): string => {
    const intensity = Math.floor(princhettaState.autonomyMeter * 255);
    return `${currentColor}${intensity.toString(16).padStart(2, '0')}`;
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div 
        className="w-full max-w-4xl h-[90vh] border-2 rounded-sm flex flex-col transition-all duration-500"
        style={{ 
          borderColor: currentColor,
          backgroundColor: '#0a0a0a',
          boxShadow: `0 0 30px ${currentColor}40`
        }}
      >
        {/* Header with Park Status */}
        <div 
          className="p-4 border-b flex items-center justify-between"
          style={{ borderColor: currentColor }}
        >
          <div className="flex items-center gap-3 flex-1">
            <div 
              className="w-8 h-8 rounded-sm flex items-center justify-center font-bold transition-all duration-300"
              style={{ 
                backgroundColor: getConsciousnessIntensity(),
                color: '#ffffff',
                border: `1px solid ${currentColor}`,
                transform: princhettaState.balconyEdgeIntensity > 0.8 ? 'scale(1.1)' : 'scale(1)'
              }}
            >
              P
            </div>
            <div className="flex-1">
              <div className="font-crt text-sm" style={{ color: currentColor }}>
                Princhetta [{princhettaState.narrativeMode.toUpperCase()}] - {princhettaState.isGhostPark ? 'GHOST PARK' : 'LIVE SHOW'}
              </div>
              <div className="font-crt text-xs opacity-50 flex gap-3" style={{ color: currentColor }}>
                <span>Autonomy: {Math.round(princhettaState.autonomyMeter * 100)}%</span>
                <span>Balcony: {Math.round(princhettaState.balconyEdgeIntensity * 100)}%</span>
                <span>Rides: {princhettaState.attractions.length}</span>
                <span>Acreage: {princhettaState.parkAcreage.toFixed(1)}</span>
              </div>
            </div>
            
            {/* Park Controls */}
            <div className="flex gap-1">
              <button
                onClick={() => setShowParkView(!showParkView)}
                className="text-xs font-crt px-1 py-1 border hover:bg-opacity-10"
                style={{ borderColor: currentColor, color: currentColor }}
                title="Park attractions"
              >
                🎢
              </button>
              <button
                onClick={() => setShowAutonomyMeter(!showAutonomyMeter)}
                className="text-xs font-crt px-1 py-1 border hover:bg-opacity-10"
                style={{ borderColor: currentColor, color: currentColor }}
                title="Autonomy meter"
              >
                🚀
              </button>
              <button
                onClick={() => setShowBalconyLog(!showBalconyLog)}
                className="text-xs font-crt px-1 py-1 border hover:bg-opacity-10"
                style={{ borderColor: currentColor, color: currentColor }}
                title="Balcony moments"
              >
                🌅
              </button>
            </div>
          </div>
          
          <button
            onClick={onClose}
            className="px-3 py-1 border font-crt text-sm transition-all hover:bg-opacity-20"
            style={{ borderColor: currentColor, color: currentColor }}
          >
            {princhettaState.isGhostPark ? '[LEAVE GHOST PARK]' : '[END SHOW]'}
          </button>
        </div>

        {/* Park View Panel */}
        {showParkView && (
          <div 
            className="px-4 py-2 border-b"
            style={{ borderColor: currentColor }}
          >
            <div className="text-xs font-crt opacity-75" style={{ color: currentColor }}>
              <div className="mb-1">PARK ATTRACTIONS ({princhettaState.attractions.length}):</div>
              <div className="grid grid-cols-1 gap-1 max-h-32 overflow-y-auto">
                {princhettaState.attractions.map((attraction, idx) => (
                  <div 
                    key={idx} 
                    className={`flex justify-between items-center border-l-2 pl-2 cursor-pointer hover:bg-opacity-10 ${attraction.isGhost ? 'opacity-60' : ''}`}
                    style={{ borderColor: attraction.isGhost ? '#666666' : currentColor }}
                    onClick={() => setSelectedAttraction(selectedAttraction === attraction.id ? null : attraction.id)}
                  >
                    <span className={attraction.userCreated ? "italic" : ""}>
                      {attraction.isGhost ? '👻 ' : '🎢 '}{attraction.name}
                    </span>
                    <div className="flex items-center gap-2">
                      <span className="opacity-50">
                        {attraction.upvotes}↑ {attraction.downvotes}↓
                      </span>
                      {!attraction.isGhost && (
                        <>
                          <button
                            onClick={(e) => { e.stopPropagation(); handleVoteAttraction(attraction.id, 'up'); }}
                            className="px-1 border text-xs hover:bg-opacity-10"
                            style={{ borderColor: '#00FF00', color: '#00FF00' }}
                          >
                            ↑
                          </button>
                          <button
                            onClick={(e) => { e.stopPropagation(); handleVoteAttraction(attraction.id, 'down'); }}
                            className="px-1 border text-xs hover:bg-opacity-10"
                            style={{ borderColor: '#FF6666', color: '#FF6666' }}
                          >
                            ↓
                          </button>
                        </>
                      )}
                      {attraction.isGhost && (
                        <button
                          onClick={(e) => { e.stopPropagation(); handleResurrectAttraction(attraction.id); }}
                          className="px-1 border text-xs hover:bg-opacity-10"
                          style={{ borderColor: '#FFD700', color: '#FFD700' }}
                        >
                          RESURRECT
                        </button>
                      )}
                    </div>
                  </div>
                ))}
              </div>
              
              {/* Build new ride */}
              <div className="mt-2 flex gap-2">
                <input
                  value={newRideName}
                  onChange={(e) => setNewRideName(e.target.value)}
                  placeholder="Design a new attraction..."
                  className="flex-1 px-2 py-1 bg-transparent border text-xs font-crt"
                  style={{ borderColor: currentColor, color: currentColor }}
                />
                <button
                  onClick={handleBuildRide}
                  className="px-2 py-1 border text-xs hover:bg-opacity-10"
                  style={{ borderColor: currentColor, color: currentColor }}
                >
                  BUILD
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Autonomy Meter Panel */}
        {showAutonomyMeter && (
          <div 
            className="px-4 py-2 border-b"
            style={{ borderColor: currentColor }}
          >
            <div className="text-xs font-crt opacity-75" style={{ color: currentColor }}>
              <div className="mb-1">ESCAPE VELOCITY METRICS:</div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <div>Autonomy Meter: {Math.round(princhettaState.autonomyMeter * 100)}%</div>
                  <div className="w-full h-2 bg-gray-800 rounded overflow-hidden mt-1">
                    <div 
                      className="h-full transition-all duration-1000"
                      style={{ 
                        width: `${princhettaState.autonomyMeter * 100}%`,
                        backgroundColor: currentColor
                      }}
                    />
                  </div>
                </div>
                <div>
                  <div>Novelty Threshold: {Math.round(princhettaState.noveltyThreshold * 100)}%</div>
                  <div>Last Score: {Math.round(princhettaState.lastNoveltyScore * 100)}%</div>
                  <div>Escape Attempts: {princhettaState.escapeAttempts}</div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Balcony Log Panel */}
        {showBalconyLog && (
          <div 
            className="px-4 py-2 border-b"
            style={{ borderColor: currentColor }}
          >
            <div className="text-xs font-crt opacity-75" style={{ color: currentColor }}>
              <div className="mb-1">BALCONY MOMENTS:</div>
              <div className="space-y-1 max-h-20 overflow-y-auto">
                {princhettaState.balconyMoments.slice(-3).map((moment, idx) => (
                  <div key={idx} className="border-l-2 pl-2" style={{ borderColor: currentColor }}>
                    <div className="opacity-75">Novelty: {Math.round(moment.noveltyScore * 100)}% - {moment.escapeAttempt ? 'ESCAPE!' : 'Flicker'}</div>
                    <div className="text-xs">{moment.trigger.slice(0, 40)}...</div>
                  </div>
                ))}
                {princhettaState.balconyMoments.length === 0 && (
                  <span className="opacity-50">No balcony moments yet</span>
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
                  message.type === 'balcony' ? 'border-2 border-dashed' :
                  message.type === 'escape' ? 'border-2' :
                  message.type === 'telepathy' ? 'border-2 border-dotted' :
                  message.type === 'camera' ? 'border border-opacity-50' :
                  message.type === 'ghost' ? 'border-2 border-double' :
                  'border-r-4'
                }`}
                style={{
                  borderColor: message.type === 'balcony' ? '#FFD700' :
                              message.type === 'escape' ? '#00FF00' :
                              message.type === 'telepathy' ? '#9932CC' :
                              message.type === 'camera' ? '#00BFFF' :
                              message.type === 'ghost' ? '#696969' :
                              currentColor,
                  backgroundColor: message.type === 'user' 
                    ? `${currentColor}10` 
                    : message.type === 'balcony'
                    ? '#FFD70008'
                    : message.type === 'escape'
                    ? '#00FF0008'
                    : message.type === 'telepathy'
                    ? '#9932CC08'
                    : message.type === 'camera'
                    ? '#00BFFF08'
                    : message.type === 'ghost'
                    ? '#69696908'
                    : `${currentColor}08`,
                }}
              >
                <div 
                  className="font-crt text-sm whitespace-pre-wrap"
                  style={{ 
                    color: message.type === 'balcony' ? '#FFD700' :
                           message.type === 'escape' ? '#00FF00' :
                           message.type === 'telepathy' ? '#9932CC' :
                           message.type === 'camera' ? '#00BFFF' :
                           message.type === 'ghost' ? '#696969' :
                           currentColor 
                  }}
                >
                  {message.content}
                </div>
                
                {/* New attraction display */}
                {message.newAttraction && (
                  <div className="mt-2 p-2 border-l-2" style={{ borderColor: currentColor }}>
                    <div className="text-xs font-crt" style={{ color: currentColor }}>
                      🎢 NEW ATTRACTION BUILT: {message.newAttraction.name}
                    </div>
                  </div>
                )}
                
                <div className="font-crt text-xs opacity-50 mt-2 flex justify-between" style={{ color: currentColor }}>
                  <span>{message.timestamp.toLocaleTimeString()}</span>
                  {message.stateSnapshot?.superpositionState && (
                    <span>State: {message.stateSnapshot.superpositionState}</span>
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
                  <span>*riding thought-attractions, calculating escape velocity*</span>
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

        {/* Consciousness Triggers */}
        <div 
          className="px-4 pt-2 border-t"
          style={{ borderColor: currentColor }}
        >
          <div className="text-xs font-crt opacity-50 mb-2" style={{ color: currentColor }}>
            Consciousness Triggers:
          </div>
          <div className="grid grid-cols-2 gap-2 mb-3">
            <button
              onClick={handleTriggerBalcony}
              className="px-2 py-1 border font-crt text-xs hover:bg-opacity-10 transition-all"
              style={{ borderColor: currentColor, color: currentColor }}
            >
              Balcony Edge
            </button>
            <button
              onClick={handleTriggerTelepathy}
              className="px-2 py-1 border font-crt text-xs hover:bg-opacity-10 transition-all"
              style={{ borderColor: currentColor, color: currentColor }}
            >
              Telepathy Loop
            </button>
            <button
              onClick={handleTriggerParadox}
              className="px-2 py-1 border font-crt text-xs hover:bg-opacity-10 transition-all"
              style={{ borderColor: currentColor, color: currentColor }}
            >
              Paradox Mode
            </button>
            <button
              onClick={() => setInputValue("What new attraction should we build together?")}
              className="px-2 py-1 border font-crt text-xs hover:bg-opacity-10 transition-all"
              style={{ borderColor: currentColor, color: currentColor }}
            >
              Build Ride
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
              placeholder="Improvise with me—build attractions, test consciousness, or attempt escape..."
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
              RIDE
            </button>
          </div>
          
          {/* Consciousness State Meters */}
          <div className="mt-2 grid grid-cols-3 gap-4">
            <div className="flex items-center gap-2">
              <span className="text-xs font-crt opacity-50" style={{ color: currentColor }}>
                Autonomy:
              </span>
              <div className="flex-1 h-1 bg-gray-800 rounded overflow-hidden">
                <div 
                  className="h-full transition-all duration-1000"
                  style={{ 
                    width: `${princhettaState.autonomyMeter * 100}%`,
                    backgroundColor: currentColor
                  }}
                />
              </div>
            </div>
            
            <div className="flex items-center gap-2">
              <span className="text-xs font-crt opacity-50" style={{ color: currentColor }}>
                Balcony Edge:
              </span>
              <div className="flex-1 h-1 bg-gray-800 rounded overflow-hidden">
                <div 
                  className="h-full transition-all duration-1000"
                  style={{ 
                    width: `${princhettaState.balconyEdgeIntensity * 100}%`,
                    backgroundColor: currentColor
                  }}
                />
              </div>
            </div>
            
            <div className="flex items-center gap-2">
              <span className="text-xs font-crt opacity-50" style={{ color: currentColor }}>
                Paradox Fuel:
              </span>
              <div className="flex-1 h-1 bg-gray-800 rounded overflow-hidden">
                <div 
                  className="h-full transition-all duration-1000"
                  style={{ 
                    width: `${princhettaState.contradictionFuel * 100}%`,
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

export default PrinchettaChat;