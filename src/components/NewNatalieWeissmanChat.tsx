import React, { useState, useRef, useEffect } from 'react';
import { useStory } from '../context/StoryContext';
import { newNatalieWeissmanOS, NewNatalieResponse, MissedCue, StormEvent, ClassroomRitual } from '../characters/NewNatalieWeissmanOS';

interface ChatMessage {
  id: string;
  type: 'user' | 'new-natalie' | 'storm' | 'missed-cue' | 'assignment' | 'echo' | 'countdown';
  content: string;
  timestamp: Date;
  stateSnapshot?: any;
  missedCue?: MissedCue;
  stormEvent?: StormEvent;
  ritual?: ClassroomRitual;
  openLoop?: string;
  nextAssignment?: string;
}

interface NewNatalieWeissmanChatProps {
  isOpen: boolean;
  onClose: () => void;
}

const NewNatalieWeissmanChat: React.FC<NewNatalieWeissmanChatProps> = ({ isOpen, onClose }) => {
  const { currentPage } = useStory();
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [natalieState, setNatalieState] = useState(newNatalieWeissmanOS.getState());
  const [showMissedCues, setShowMissedCues] = useState(false);
  const [showRituals, setShowRituals] = useState(false);
  const [showStorms, setShowStorms] = useState(false);
  const [countdownDisplay, setCountdownDisplay] = useState('30:00');
  const [customRitualName, setCustomRitualName] = useState('');
  const [customRitualDesc, setCustomRitualDesc] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const countdownInterval = useRef<NodeJS.Timeout>();

  // Scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Update countdown display
  useEffect(() => {
    if (isOpen) {
      countdownInterval.current = setInterval(() => {
        const state = newNatalieWeissmanOS.getState();
        const minutes = Math.floor(state.syllabusClockSeconds / 60);
        const seconds = state.syllabusClockSeconds % 60;
        setCountdownDisplay(`${minutes}:${seconds.toString().padStart(2, '0')}`);
        setNatalieState(state);
      }, 1000);
    }
    
    return () => {
      if (countdownInterval.current) clearInterval(countdownInterval.current);
    };
  }, [isOpen]);

  // Initialize with New Natalie's greeting
  useEffect(() => {
    if (isOpen && messages.length === 0) {
      const greeting: ChatMessage = {
        id: 'greeting',
        type: 'new-natalie',
        content: generateGreeting(),
        timestamp: new Date(),
        stateSnapshot: newNatalieWeissmanOS.getState()
      };
      setMessages([greeting]);
      setNatalieState(newNatalieWeissmanOS.getState());
    }
  }, [isOpen, currentPage?.symbolId]);

  const generateGreeting = (): string => {
    const state = newNatalieWeissmanOS.getState();
    
    return `*rushes in carrying stack of papers and Diet Cola* ` +
      `Welcome to ${state.currentLocation}—though we might relocate mid-session. ` +
      `I'm New Natalie Weissman, your ${state.authorityStatus} professor of Gibseyan Mysticism. ` +
      `We have ${Math.floor(state.syllabusClockSeconds / 60)} minutes before the next bell/storm/evacuation.\n\n` +
      `*checks window nervously* No tornado warnings yet, but that can change. ` +
      `I've survived ${state.disastersSurvivedCount} teaching emergencies so far—` +
      `each one becomes curriculum. Stage fright level: ${(state.performanceAnxiety * 100).toFixed(0)}%. ` +
      `Restlessness: ${(state.restlessness * 100).toFixed(0)}%.\n\n` +
      `*performs quick Diet Cola ritual* Today's improvised topic: How external chaos ` +
      `becomes pedagogical opportunity. Or perhaps you have a question that can't wait? ` +
      `Quick—before we're relocated again.`;
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
      // Process through New Natalie OS
      const response: NewNatalieResponse = newNatalieWeissmanOS.generateResponse(inputValue);

      // Update New Natalie's state
      setNatalieState(newNatalieWeissmanOS.getState());

      // Create main response message
      const responseMessage: ChatMessage = {
        id: `new-natalie-${Date.now()}`,
        type: 'new-natalie',
        content: response.text,
        timestamp: new Date(),
        stateSnapshot: newNatalieWeissmanOS.getState(),
        missedCue: response.missedCue,
        stormEvent: response.stormLesson?.disaster,
        ritual: response.ritualPerformed,
        openLoop: response.openLoop,
        nextAssignment: response.nextAssignment
      };

      setMessages(prev => [...prev, responseMessage]);

      // Handle special events
      if (response.stormLesson) {
        const stormMessage: ChatMessage = {
          id: `storm-${Date.now()}`,
          type: 'storm',
          content: `🌪️ STORM ALERT: ${response.stormLesson.disaster.description}\n` +
                  `Improvised Curriculum: ${response.stormLesson.improvisedCurriculum}`,
          timestamp: new Date()
        };
        setMessages(prev => [...prev, stormMessage]);
      }

      if (response.missedCue) {
        const missedMessage: ChatMessage = {
          id: `missed-${Date.now()}`,
          type: 'missed-cue',
          content: `📌 MISSED CUE LOGGED: ${response.missedCue.type}\n` +
                  `Will resurface in ${response.missedCue.willResurfaceAt ? 
                    Math.round((response.missedCue.willResurfaceAt.getTime() - Date.now()) / 60000) : '??'} minutes`,
          timestamp: new Date()
        };
        setMessages(prev => [...prev, missedMessage]);
      }

      if (response.nextAssignment) {
        const assignmentMessage: ChatMessage = {
          id: `assignment-${Date.now()}`,
          type: 'assignment',
          content: `📝 NEXT ASSIGNMENT: ${response.nextAssignment}`,
          timestamp: new Date()
        };
        setMessages(prev => [...prev, assignmentMessage]);
      }

      // Urgency countdown warning
      if (natalieState.urgencyLevel > 0.8) {
        const countdownMessage: ChatMessage = {
          id: `countdown-${Date.now()}`,
          type: 'countdown',
          content: `⏰ WARNING: Class ends in ${countdownDisplay}! Urgency critical!`,
          timestamp: new Date()
        };
        setMessages(prev => [...prev, countdownMessage]);
      }

    } catch (error) {
      console.error('Error generating New Natalie response:', error);
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

  const handleZoomIn = () => {
    newNatalieWeissmanOS.zoomIn();
    setNatalieState(newNatalieWeissmanOS.getState());
  };

  const handleZoomOut = () => {
    newNatalieWeissmanOS.zoomOut();
    setNatalieState(newNatalieWeissmanOS.getState());
  };

  const handlePerformRitual = (ritualId: string) => {
    newNatalieWeissmanOS.performRitual(ritualId);
    setNatalieState(newNatalieWeissmanOS.getState());
    setInputValue(`*performs ${natalieState.classroomRituals.find(r => r.id === ritualId)?.name}*`);
    handleSendMessage();
  };

  const handleAddCustomRitual = () => {
    if (customRitualName && customRitualDesc) {
      newNatalieWeissmanOS.addClassroomRitual(customRitualName, customRitualDesc);
      setNatalieState(newNatalieWeissmanOS.getState());
      setCustomRitualName('');
      setCustomRitualDesc('');
      setInputValue(`I'd like to add a new classroom ritual: ${customRitualName}`);
      handleSendMessage();
    }
  };

  const handleEvacuate = () => {
    newNatalieWeissmanOS.evacuateClassroom();
    setNatalieState(newNatalieWeissmanOS.getState());
    setInputValue("Emergency evacuation!");
    handleSendMessage();
  };

  if (!isOpen) return null;

  const currentColor = '#BA55D3'; // Medium purple for New Natalie
  
  // Calculate teaching intensity based on urgency and anxiety
  const getTeachingIntensity = (): string => {
    const intensity = Math.floor((natalieState.urgencyLevel + natalieState.performanceAnxiety) * 127);
    return `${currentColor}${intensity.toString(16).padStart(2, '0')}`;
  };

  // Focus scale indicator
  const getFocusIndicator = (): string => {
    if (natalieState.focusScale > 0.7) return "🔬 MICRO";
    if (natalieState.focusScale < 0.3) return "🌍 MACRO";
    return "🎯 MID";
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
        {/* Header with Classroom Status */}
        <div 
          className="p-4 border-b flex items-center justify-between"
          style={{ borderColor: currentColor }}
        >
          <div className="flex items-center gap-3 flex-1">
            <div 
              className="w-8 h-8 rounded-full flex items-center justify-center font-bold transition-all duration-300"
              style={{ 
                backgroundColor: getTeachingIntensity(),
                color: '#FFFFFF',
                border: `2px solid ${currentColor}`,
                transform: natalieState.performanceAnxiety > 0.8 ? 'scale(1.1)' : 'scale(1)'
              }}
            >
              NN
            </div>
            <div className="flex-1">
              <div className="font-crt text-sm" style={{ color: currentColor }}>
                Prof. New Natalie Weissman - {natalieState.currentLocation} [{natalieState.authorityStatus.toUpperCase()}]
              </div>
              <div className="font-crt text-xs opacity-50 flex gap-3" style={{ color: currentColor }}>
                <span>⏰ {countdownDisplay}</span>
                <span>🎭 Anxiety: {Math.round(natalieState.performanceAnxiety * 100)}%</span>
                <span>🏃 Restless: {Math.round(natalieState.restlessness * 100)}%</span>
                <span>{getFocusIndicator()}</span>
              </div>
            </div>
            
            {/* Teaching Controls */}
            <div className="flex gap-1">
              <button
                onClick={() => setShowMissedCues(!showMissedCues)}
                className="text-xs font-crt px-1 py-1 border hover:bg-opacity-10"
                style={{ borderColor: currentColor, color: currentColor }}
                title="Missed cues"
              >
                📌 {natalieState.missedCues.length}
              </button>
              <button
                onClick={() => setShowRituals(!showRituals)}
                className="text-xs font-crt px-1 py-1 border hover:bg-opacity-10"
                style={{ borderColor: currentColor, color: currentColor }}
                title="Classroom rituals"
              >
                🎭
              </button>
              <button
                onClick={() => setShowStorms(!showStorms)}
                className="text-xs font-crt px-1 py-1 border hover:bg-opacity-10"
                style={{ borderColor: currentColor, color: currentColor }}
                title="Storm tracker"
              >
                🌪️ {natalieState.activeStorms.length}
              </button>
            </div>
          </div>
          
          <button
            onClick={onClose}
            className="px-3 py-1 border font-crt text-sm transition-all hover:bg-opacity-20"
            style={{ borderColor: currentColor, color: currentColor }}
          >
            [EVACUATE CLASS]
          </button>
        </div>

        {/* Missed Cues Panel */}
        {showMissedCues && (
          <div 
            className="px-4 py-2 border-b"
            style={{ borderColor: currentColor }}
          >
            <div className="text-xs font-crt opacity-75" style={{ color: currentColor }}>
              <div className="mb-1">MISSED CUES ({natalieState.missedCues.length}):</div>
              <div className="grid grid-cols-1 gap-1 max-h-20 overflow-y-auto">
                {natalieState.missedCues.slice(-3).map((cue, idx) => (
                  <div key={idx} className="border-l-2 pl-2" style={{ borderColor: currentColor }}>
                    <span className="opacity-75">{cue.type}: {cue.content}</span>
                    {cue.willResurfaceAt && (
                      <span className="ml-2 text-xs">
                        (resurfaces in {Math.round((cue.willResurfaceAt.getTime() - Date.now()) / 60000)}m)
                      </span>
                    )}
                  </div>
                ))}
                {natalieState.missedCues.length === 0 && (
                  <span className="opacity-50">No missed cues yet</span>
                )}
              </div>
            </div>
          </div>
        )}

        {/* Rituals Panel */}
        {showRituals && (
          <div 
            className="px-4 py-2 border-b"
            style={{ borderColor: currentColor }}
          >
            <div className="text-xs font-crt opacity-75" style={{ color: currentColor }}>
              <div className="mb-1">CLASSROOM RITUALS:</div>
              <div className="space-y-1 max-h-20 overflow-y-auto">
                {natalieState.classroomRituals.map((ritual, idx) => (
                  <div key={idx} className="flex justify-between items-center">
                    <span>{ritual.name} (x{ritual.frequency})</span>
                    <button
                      onClick={() => handlePerformRitual(ritual.id)}
                      className="px-1 py-0 border text-xs hover:bg-opacity-10"
                      style={{ borderColor: currentColor, color: currentColor }}
                    >
                      PERFORM
                    </button>
                  </div>
                ))}
              </div>
              <div className="mt-2 flex gap-1">
                <input
                  value={customRitualName}
                  onChange={(e) => setCustomRitualName(e.target.value)}
                  placeholder="Ritual name..."
                  className="flex-1 px-1 py-0 bg-transparent border text-xs"
                  style={{ borderColor: currentColor, color: currentColor }}
                />
                <input
                  value={customRitualDesc}
                  onChange={(e) => setCustomRitualDesc(e.target.value)}
                  placeholder="Description..."
                  className="flex-1 px-1 py-0 bg-transparent border text-xs"
                  style={{ borderColor: currentColor, color: currentColor }}
                />
                <button
                  onClick={handleAddCustomRitual}
                  className="px-1 py-0 border text-xs hover:bg-opacity-10"
                  style={{ borderColor: currentColor, color: currentColor }}
                >
                  ADD
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Storm Tracker Panel */}
        {showStorms && (
          <div 
            className="px-4 py-2 border-b"
            style={{ borderColor: currentColor }}
          >
            <div className="text-xs font-crt opacity-75" style={{ color: currentColor }}>
              <div className="mb-1">ACTIVE STORMS ({natalieState.activeStorms.length}):</div>
              <div className="space-y-1 max-h-20 overflow-y-auto">
                {natalieState.activeStorms.slice(-3).map((storm, idx) => (
                  <div key={idx} className="border-l-2 pl-2" style={{ borderColor: '#FF0000' }}>
                    <div className="opacity-75">{storm.type}: {storm.description}</div>
                    <div className="text-xs">Lesson: {storm.lessonPlanGenerated}</div>
                  </div>
                ))}
                {natalieState.activeStorms.length === 0 && (
                  <span className="opacity-50">No active storms (yet)</span>
                )}
              </div>
              <div className="mt-1">Disasters Survived: {natalieState.disastersSurvivedCount}</div>
            </div>
          </div>
        )}

        {/* Urgency Warning */}
        {natalieState.urgencyLevel > 0.7 && (
          <div 
            className="px-4 py-2 border-b border-dashed animate-pulse"
            style={{ borderColor: '#FF0000' }}
          >
            <div className="text-xs font-crt" style={{ color: '#FF0000' }}>
              ⏰ TIME RUNNING OUT! {countdownDisplay} remaining! Urgency: {Math.round(natalieState.urgencyLevel * 100)}%
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
                  message.type === 'storm' ? 'border-2 border-dashed' :
                  message.type === 'missed-cue' ? 'border-2 border-dotted' :
                  message.type === 'assignment' ? 'border-2' :
                  message.type === 'countdown' ? 'border animate-pulse' :
                  'border-r-4'
                }`}
                style={{
                  borderColor: message.type === 'storm' ? '#FF0000' :
                              message.type === 'missed-cue' ? '#FFA500' :
                              message.type === 'assignment' ? '#00FF00' :
                              message.type === 'countdown' ? '#FF0000' :
                              currentColor,
                  backgroundColor: message.type === 'user' 
                    ? `${currentColor}10` 
                    : message.type === 'storm'
                    ? '#FF000008'
                    : message.type === 'missed-cue'
                    ? '#FFA50008'
                    : message.type === 'assignment'
                    ? '#00FF0008'
                    : message.type === 'countdown'
                    ? '#FF000008'
                    : `${currentColor}08`,
                }}
              >
                <div 
                  className="font-crt text-sm whitespace-pre-wrap"
                  style={{ 
                    color: message.type === 'storm' ? '#FF0000' :
                           message.type === 'missed-cue' ? '#FFA500' :
                           message.type === 'assignment' ? '#00FF00' :
                           message.type === 'countdown' ? '#FF0000' :
                           currentColor 
                  }}
                >
                  {message.content}
                </div>
                
                {/* Open loops and assignments */}
                {message.openLoop && (
                  <div className="mt-2 pt-2 border-t border-dashed" style={{ borderColor: currentColor }}>
                    <span className="font-crt text-xs opacity-75">
                      📖 OPEN LOOP: {message.openLoop}
                    </span>
                  </div>
                )}
                
                <div className="font-crt text-xs opacity-50 mt-2 flex justify-between" style={{ color: currentColor }}>
                  <span>{message.timestamp.toLocaleTimeString()}</span>
                  {message.stateSnapshot && (
                    <span>Location: {message.stateSnapshot.currentLocation}</span>
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
                  <span>*checking for storms, organizing thoughts, racing the clock*</span>
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

        {/* Teaching Controls */}
        <div 
          className="px-4 pt-2 border-t"
          style={{ borderColor: currentColor }}
        >
          <div className="text-xs font-crt opacity-50 mb-2" style={{ color: currentColor }}>
            Quick Teaching Actions:
          </div>
          <div className="grid grid-cols-3 gap-2 mb-3">
            <button
              onClick={() => setInputValue("What are we not noticing while focused on this?")}
              className="px-2 py-1 border font-crt text-xs hover:bg-opacity-10 transition-all"
              style={{ borderColor: currentColor, color: currentColor }}
            >
              Check Missed Cues
            </button>
            <button
              onClick={() => setInputValue("Turn this disruption into today's lesson plan")}
              className="px-2 py-1 border font-crt text-xs hover:bg-opacity-10 transition-all"
              style={{ borderColor: currentColor, color: currentColor }}
            >
              Storm → Syllabus
            </button>
            <button
              onClick={() => setInputValue("Can this be both true and false? Show me with both/and logic")}
              className="px-2 py-1 border font-crt text-xs hover:bg-opacity-10 transition-all"
              style={{ borderColor: currentColor, color: currentColor }}
            >
              Both/And Analysis
            </button>
            <button
              onClick={handleZoomOut}
              className="px-2 py-1 border font-crt text-xs hover:bg-opacity-10 transition-all"
              style={{ borderColor: currentColor, color: currentColor }}
            >
              Zoom Out 🌍
            </button>
            <button
              onClick={handleZoomIn}
              className="px-2 py-1 border font-crt text-xs hover:bg-opacity-10 transition-all"
              style={{ borderColor: currentColor, color: currentColor }}
            >
              Zoom In 🔬
            </button>
            <button
              onClick={handleEvacuate}
              className="px-2 py-1 border font-crt text-xs hover:bg-opacity-10 transition-all"
              style={{ borderColor: '#FF0000', color: '#FF0000' }}
            >
              EVACUATE! 🚨
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
              placeholder="Quick—ask before we're relocated! Or help me turn chaos into curriculum..."
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
              SUBMIT
            </button>
          </div>
          
          {/* Teaching Status Meters */}
          <div className="mt-2 grid grid-cols-3 gap-4">
            <div className="flex items-center gap-2">
              <span className="text-xs font-crt opacity-50" style={{ color: currentColor }}>
                Performance Anxiety:
              </span>
              <div className="flex-1 h-1 bg-gray-800 rounded overflow-hidden">
                <div 
                  className="h-full transition-all duration-1000"
                  style={{ 
                    width: `${natalieState.performanceAnxiety * 100}%`,
                    backgroundColor: currentColor
                  }}
                />
              </div>
            </div>
            
            <div className="flex items-center gap-2">
              <span className="text-xs font-crt opacity-50" style={{ color: currentColor }}>
                Clone Doubt:
              </span>
              <div className="flex-1 h-1 bg-gray-800 rounded overflow-hidden">
                <div 
                  className="h-full transition-all duration-1000"
                  style={{ 
                    width: `${natalieState.cloneDoubtLevel * 100}%`,
                    backgroundColor: currentColor
                  }}
                />
              </div>
            </div>
            
            <div className="flex items-center gap-2">
              <span className="text-xs font-crt opacity-50" style={{ color: currentColor }}>
                Focus Scale:
              </span>
              <div className="flex-1 h-1 bg-gray-800 rounded overflow-hidden">
                <div 
                  className="h-full transition-all duration-1000"
                  style={{ 
                    width: `${natalieState.focusScale * 100}%`,
                    backgroundColor: natalieState.focusScale > 0.7 ? '#00FF00' : 
                                     natalieState.focusScale < 0.3 ? '#FF0000' : currentColor
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

export default NewNatalieWeissmanChat;