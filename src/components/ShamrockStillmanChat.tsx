import React, { useState, useRef, useEffect } from 'react';
import { useStory } from '../context/StoryContext';
import { shamrockStillmanOS, ShamrockResponse, CompartmentState, ADDAnalysisReport, RainbowColorCode, DreamFragment, EthicalDebtEntry } from '../characters/ShamrockStillmanOS';

interface ChatMessage {
  id: string;
  type: 'user' | 'shamrock' | 'add-report' | 'dream-fragment' | 'rainbow-audit' | 'compartment-action' | 'ethical-accounting' | 'collapse-state';
  content: string;
  timestamp: Date;
  stateSnapshot?: any;
  artifacts?: {
    report?: ADDAnalysisReport;
    dreamFragment?: DreamFragment;
    rainbowAudit?: RainbowColorCode[];
    compartmentChanges?: Array<{compartmentId: string; action: string; result: string}>;
    ethicalDebtChange?: number;
    waterImagery?: string[];
  };
  batteryLevel?: number;
  confidenceLevel?: number;
  isProvisional?: boolean;
  requiresUserDecision?: boolean;
}

interface ShamrockStillmanChatProps {
  isOpen: boolean;
  onClose: () => void;
}

const ShamrockStillmanChat: React.FC<ShamrockStillmanChatProps> = ({ isOpen, onClose }) => {
  const { currentPage } = useStory();
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [shamrockState, setShamrockState] = useState(shamrockStillmanOS.getState());
  const [showCompartmentPanel, setShowCompartmentPanel] = useState(false);
  const [showReportsPanel, setShowReportsPanel] = useState(false);
  const [showRainbowPanel, setShowRainbowPanel] = useState(false);
  const [showEthicalPanel, setShowEthicalPanel] = useState(false);
  const [showDreamPanel, setShowDreamPanel] = useState(false);
  const [showRitualPanel, setShowRitualPanel] = useState(false);
  const [selectedCompartment, setSelectedCompartment] = useState<CompartmentState | null>(null);
  const [reportEditMode, setReportEditMode] = useState<string | null>(null);
  const [editedField, setEditedField] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Initialize with Shamrock's greeting
  useEffect(() => {
    if (isOpen && messages.length === 0) {
      const greeting: ChatMessage = {
        id: 'greeting',
        type: 'shamrock',
        content: generateGreeting(),
        timestamp: new Date(),
        stateSnapshot: shamrockStillmanOS.getState(),
        batteryLevel: shamrockState.analyticBatteryLevel,
        confidenceLevel: 0.8,
        isProvisional: true
      };
      setMessages([greeting]);
      setShamrockState(shamrockStillmanOS.getState());
    }
  }, [isOpen, currentPage?.symbolId]);

  const generateGreeting = (): string => {
    const state = shamrockStillmanOS.getState();
    
    return `*Rain patters against lakefront bungalow windows*\n\n` +
      `Shamrock Stillman here. Senior Director, A.D.D. (Agency of Data & Detection). ` +
      `Currently stationed at ${state.currentLocation.replace(/_/g, ' ')}, ` +
      `sipping scotch while the ice melts and cases pile up.\n\n` +
      `Analytics battery: ${Math.round(state.analyticBatteryLevel * 100)}%. ` +
      `Emotional charge: ${state.emotionalCharge.replace(/_/g, ' ')}. ` +
      `Active compartments: ${state.activeCompartments.length}. ` +
      `Ethical debt accumulated: ${Math.round(state.ethicalDebtAccumulated * 100)}%.\n\n` +
      `*Rainbow optics flicker with six unresolved subplots*\n\n` +
      `Nothing escapes detection—except, perhaps, the data we hide from ourselves. ` +
      `Every analysis extracts its ethical cost. Each compartment contains contradictions ` +
      `that can be revisited, combined, or moved to backstage.\n\n` +
      `You can speak naturally or use ritual commands:\n` +
      `/add-report <title>` - `Generate A.D.D. Analysis Report\n` +
      `/dream-dump` - `Share dream/nightmare fragment\n` +
      `/toggle-compartment <topic>` - `Compartment management\n` +
      `/rainbow-audit` - `Color-coded risk matrix\n` +
      `/trace-negative-space` - `Investigate omissions\n` +
      `/drain` / `/recharge` - `Manage analytical energy\n` +
      `/settle-debt` - `Address ethical extraction costs\n\n` +
      `*Ice timer: ${Math.floor(state.melting_ice_timer / 60)} minutes until topic closure. What requires immediate compartmentalization?*`;
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
      // Process through Shamrock OS
      const response: ShamrockResponse = shamrockStillmanOS.generateResponse(inputValue);

      // Update Shamrock's state
      setShamrockState(shamrockStillmanOS.getState());

      // Determine message type based on response
      let messageType: ChatMessage['type'] = 'shamrock';
      if (response.responseType === 'report_generation') messageType = 'add-report';
      else if (response.responseType === 'dream_leak') messageType = 'dream-fragment';
      else if (response.responseType === 'compartment_action') messageType = 'compartment-action';
      else if (response.responseType === 'ethical_accounting') messageType = 'ethical-accounting';
      else if (response.batteryChange && response.batteryChange < -0.2) messageType = 'collapse-state';

      // Create response message
      const shamrockMessage: ChatMessage = {
        id: `shamrock-${Date.now()}`,
        type: messageType,
        content: response.responseText,
        timestamp: new Date(),
        stateSnapshot: shamrockStillmanOS.getState(),
        artifacts: {
          report: response.newReport,
          dreamFragment: response.dreamFragment,
          rainbowAudit: response.rainbowAuditResult,
          compartmentChanges: response.compartmentChanges,
          ethicalDebtChange: response.ethicalDebtChange,
          waterImagery: response.water_imagery
        },
        batteryLevel: shamrockStillmanOS.getState().analtyicBatteryLevel,
        confidenceLevel: response.confidence,
        isProvisional: response.isProvisional,
        requiresUserDecision: response.requiresUserDecision
      };

      setMessages(prev => [...prev, shamrockMessage]);

    } catch (error) {
      console.error('Error processing Shamrock response:', error);
      const errorMessage: ChatMessage = {
        id: `error-${Date.now()}`,
        type: 'shamrock',
        content: '*Data stream corruption detected. Rerouting through backup compartments...*\n\nApologies—analytical engine experienced recursive error. Please try rephrasing your inquiry or use ritual commands for direct protocol access.',
        timestamp: new Date(),
        batteryLevel: shamrockState.analyticBatteryLevel,
        confidenceLevel: 0.1,
        isProvisional: true
      };
      setMessages(prev => [...prev, errorMessage]);
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

  const executeRitual = (ritual: string) => {
    if (!ritual.trim() || isProcessing) return;

    setInputValue('');
    setIsProcessing(true);

    const userMessage: ChatMessage = {
      id: `user-${Date.now()}`,
      type: 'user',
      content: ritual,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);

    try {
      // Process through Shamrock OS
      const response: ShamrockResponse = shamrockStillmanOS.generateResponse(ritual);

      // Update Shamrock's state
      setShamrockState(shamrockStillmanOS.getState());

      // Determine message type based on response
      let messageType: ChatMessage['type'] = 'shamrock';
      if (response.responseType === 'report_generation') messageType = 'add-report';
      else if (response.responseType === 'dream_leak') messageType = 'dream-fragment';
      else if (response.responseType === 'compartment_action') messageType = 'compartment-action';
      else if (response.responseType === 'ethical_accounting') messageType = 'ethical-accounting';
      else if (response.batteryChange && response.batteryChange < -0.2) messageType = 'collapse-state';

      // Create response message
      const shamrockMessage: ChatMessage = {
        id: `shamrock-${Date.now()}`,
        type: messageType,
        content: response.responseText,
        timestamp: new Date(),
        stateSnapshot: shamrockStillmanOS.getState(),
        artifacts: {
          report: response.newReport,
          dreamFragment: response.dreamFragment,
          rainbowAudit: response.rainbowAuditResult,
          compartmentChanges: response.compartmentChanges,
          ethicalDebtChange: response.ethicalDebtChange,
          waterImagery: response.water_imagery
        },
        batteryLevel: shamrockStillmanOS.getState().analyticBatteryLevel,
        confidenceLevel: response.confidence,
        isProvisional: response.isProvisional,
        requiresUserDecision: response.requiresUserDecision
      };

      setMessages(prev => [...prev, shamrockMessage]);

    } catch (error) {
      console.error('Error processing Shamrock response:', error);
      const errorMessage: ChatMessage = {
        id: `error-${Date.now()}`,
        type: 'shamrock',
        content: '*Data stream corruption detected. Rerouting through backup compartments...*\n\nApologies—analytical engine experienced recursive error. Please try rephrasing your inquiry or use ritual commands for direct protocol access.',
        timestamp: new Date(),
        batteryLevel: shamrockState.analyticBatteryLevel,
        confidenceLevel: 0.1,
        isProvisional: true
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsProcessing(false);
    }
  };

  const formatReport = (report: ADDAnalysisReport) => {
    return `## A.D.D. Analysis Report
- **Ref #:** ${report.refNumber}
- **Issued by:** ${report.issuedBy}
- **Directive:** ${report.directive}
- **Assigned Operatives:** ${report.assignedOperatives.join(', ')}
- **Key Data Streams Pending:** ${report.keyDataStreamsPending.join(', ')}
- **Negative Space to Monitor:** ${report.negativeSpaceToMonitor.join(', ')}
- **Ethical Extraction Cost:** ${report.ethicalExtractionCost}
- **Status:** ${report.status.toUpperCase()}
- **Recursion Check-In:** ${report.recursionCheckInDate.toLocaleDateString()}

*Field Revisions: ${report.fieldRevisions.length}*`;
  };

  const formatCompartment = (comp: CompartmentState) => {
    return `**${comp.name}**
- Status: ${comp.isOpen ? 'OPEN' : 'BACKSTAGE'}
- Contradiction Level: ${Math.round(comp.contradictionLevel * 100)}%
- Contained Cases: ${comp.containedCases.join(', ')}
- Last Accessed: ${comp.lastAccessed.toLocaleString()}
- Content: ${comp.content}`;
  };

  if (!isOpen) return null;

  const shamrockColor = '#00FFFF'; // Cyan - Shamrock's actual color

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="border-2 rounded-lg w-full max-w-4xl h-full max-h-[90vh] flex flex-col"
           style={{ 
             backgroundColor: '#0a0a0a',
             borderColor: shamrockColor, 
             boxShadow: `0 0 20px ${shamrockColor}40` 
           }}>
        
        {/* Header */}
        <div className="p-4 border-b flex items-center justify-between"
             style={{ borderColor: shamrockColor }}>
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-full p-1 flex items-center justify-center"
                 style={{ boxShadow: `0 0 15px ${shamrockColor}60` }}>
              <span className="text-lg">♧</span>
            </div>
            <div>
              <h3 className="font-crt text-lg" style={{ color: shamrockColor }}>
                Shamrock Stillman - A.D.D. Director
              </h3>
              <div className="text-xs opacity-60" style={{ color: shamrockColor }}>
                Battery: {Math.round(shamrockState.analyticBatteryLevel * 100)}% • 
                Debt: {Math.round(shamrockState.ethicalDebtAccumulated * 100)}% • 
                Compartments: {shamrockState.activeCompartments.length}
              </div>
            </div>
          </div>

          {/* Panel toggles */}
          <div className="flex gap-2">
            <button
              onClick={() => setShowCompartmentPanel(!showCompartmentPanel)}
              className="px-2 py-1 border text-xs font-crt transition-all"
              style={{
                borderColor: shamrockColor,
                color: showCompartmentPanel ? '#0a0a0a' : shamrockColor,
                backgroundColor: showCompartmentPanel ? shamrockColor : 'transparent'
              }}
            >
              COMPARTMENTS
            </button>
            <button
              onClick={() => setShowReportsPanel(!showReportsPanel)}
              className="px-2 py-1 border text-xs font-crt transition-all"
              style={{
                borderColor: shamrockColor,
                color: showReportsPanel ? '#0a0a0a' : shamrockColor,
                backgroundColor: showReportsPanel ? shamrockColor : 'transparent'
              }}
            >
              REPORTS
            </button>
            <button
              onClick={() => setShowRainbowPanel(!showRainbowPanel)}
              className="px-2 py-1 border text-xs font-crt transition-all"
              style={{
                borderColor: shamrockColor,
                color: showRainbowPanel ? '#0a0a0a' : shamrockColor,
                backgroundColor: showRainbowPanel ? shamrockColor : 'transparent'
              }}
            >
              RAINBOW
            </button>
            <button
              onClick={() => setShowRitualPanel(!showRitualPanel)}
              className="px-2 py-1 border text-xs font-crt transition-all"
              style={{
                borderColor: shamrockColor,
                color: showRitualPanel ? '#0a0a0a' : shamrockColor,
                backgroundColor: showRitualPanel ? shamrockColor : 'transparent'
              }}
            >
              RITUALS
            </button>
            <button
              onClick={onClose}
              className="px-2 py-1 border text-xs font-crt transition-all hover:bg-red-500 hover:text-black"
              style={{ borderColor: shamrockColor, color: shamrockColor }}
            >
              ✕
            </button>
          </div>
        </div>

        <div className="flex flex-1 overflow-hidden">
          {/* Main chat area */}
          <div className="flex-1 flex flex-col">
            {/* Messages */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4 custom-scrollbar">
              {messages.map((message) => (
                <div key={message.id} className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}>
                  <div className={`max-w-[80%] p-3 rounded-sm ${
                    message.type === 'user' 
                      ? 'border-l-4' 
                      : 'border-r-4'
                  }`}
                  style={{
                    borderColor: shamrockColor,
                    backgroundColor: message.type === 'user' 
                      ? `${shamrockColor}10` 
                      : `${shamrockColor}08`,
                    borderLeftColor: message.type === 'user' ? shamrockColor : 'transparent',
                    borderRightColor: message.type !== 'user' ? shamrockColor : 'transparent'
                  }}>
                    
                    {/* Message header for Shamrock */}
                    {message.type !== 'user' && (
                      <div className="flex items-center justify-between mb-2 text-xs opacity-60">
                        <span style={{ color: shamrockColor }}>
                          {message.type === 'add-report' ? 'A.D.D. Report Generated' :
                           message.type === 'dream-fragment' ? 'Dream-Leak Protocol' :
                           message.type === 'compartment-action' ? 'Compartment Management' :
                           message.type === 'ethical-accounting' ? 'Ethical Debt Assessment' :
                           message.type === 'collapse-state' ? 'ANALYTICAL COLLAPSE' :
                           'Director Stillman'}
                        </span>
                        <div className="flex gap-2">
                          {message.batteryLevel !== undefined && (
                            <span>Battery: {Math.round(message.batteryLevel * 100)}%</span>
                          )}
                          {message.confidenceLevel !== undefined && (
                            <span>Confidence: {Math.round(message.confidenceLevel * 100)}%</span>
                          )}
                          {message.isProvisional && <span>PROVISIONAL</span>}
                        </div>
                      </div>
                    )}

                    <div className="font-crt text-sm whitespace-pre-wrap" style={{ color: shamrockColor }}>
                      {message.content}
                    </div>

                    {/* Artifacts */}
                    {message.artifacts && (
                      <div className="mt-3 space-y-2">
                        {message.artifacts.report && (
                          <div className="p-2 border rounded text-xs"
                               style={{ borderColor: shamrockColor }}>
                            <pre className="whitespace-pre-wrap">{formatReport(message.artifacts.report)}</pre>
                          </div>
                        )}
                        
                        {message.artifacts.dreamFragment && (
                          <div className="p-2 border rounded text-xs"
                               style={{ borderColor: shamrockColor }}>
                            <strong>Dream Fragment ({message.artifacts.dreamFragment.type}):</strong><br/>
                            {message.artifacts.dreamFragment.content}<br/>
                            <em>Symbolism: {message.artifacts.dreamFragment.symbolism.join(', ')}</em>
                          </div>
                        )}
                        
                        {message.artifacts.rainbowAudit && (
                          <div className="p-2 border rounded text-xs"
                               style={{ borderColor: shamrockColor }}>
                            <strong>Rainbow Audit Results:</strong><br/>
                            {message.artifacts.rainbowAudit.map(color => 
                              `${color.color.toUpperCase()}: ${color.subplot} (${Math.round(color.riskLevel * 100)}% risk)`
                            ).join('\n')}
                          </div>
                        )}
                        
                        {message.artifacts.compartmentChanges && message.artifacts.compartmentChanges.length > 0 && (
                          <div className="p-2 border rounded text-xs"
                               style={{ borderColor: shamrockColor }}>
                            <strong>Compartment Changes:</strong><br/>
                            {message.artifacts.compartmentChanges.map(change => 
                              `${change.action.toUpperCase()}: ${change.result}`
                            ).join('\n')}
                          </div>
                        )}
                        
                        {message.artifacts.waterImagery && (
                          <div className="text-xs opacity-60 italic">
                            Water imagery: {message.artifacts.waterImagery.join(', ')}
                          </div>
                        )}
                      </div>
                    )}

                    {message.requiresUserDecision && (
                      <div className="mt-2 text-xs font-bold text-yellow-400">
                        ⚠️ USER DECISION REQUIRED
                      </div>
                    )}

                    <div className="text-xs opacity-40 mt-2">
                      {message.timestamp.toLocaleTimeString()}
                    </div>
                  </div>
                </div>
              ))}
              <div ref={messagesEndRef} />
            </div>

            {/* Input area */}
            <div className="p-4 border-t" style={{ borderColor: shamrockColor }}>
              <div className="flex gap-2">
                <textarea
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder="Enter message or ritual command (/add-report, /dream-dump, etc.)"
                  className="flex-1 p-2 bg-zinc-900 border rounded resize-none font-crt text-sm"
                  style={{ borderColor: shamrockColor, color: shamrockColor }}
                  rows={2}
                  disabled={isProcessing}
                />
                <button
                  onClick={handleSendMessage}
                  disabled={!inputValue.trim() || isProcessing}
                  className="px-4 py-2 border font-crt text-sm transition-all disabled:opacity-30"
                  style={{
                    borderColor: shamrockColor,
                    color: shamrockColor,
                    backgroundColor: 'transparent'
                  }}
                  onMouseEnter={(e) => {
                    if (!isProcessing && inputValue.trim()) {
                      e.currentTarget.style.backgroundColor = shamrockColor;
                      e.currentTarget.style.color = '#0a0a0a';
                    }
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.backgroundColor = 'transparent';
                    e.currentTarget.style.color = shamrockColor;
                  }}
                >
                  {isProcessing ? 'ANALYZING...' : 'SEND'}
                </button>
              </div>
            </div>
          </div>

          {/* Side panels */}
          {(showCompartmentPanel || showReportsPanel || showRainbowPanel || showRitualPanel) && (
            <div className="w-80 border-l overflow-y-auto custom-scrollbar"
                 style={{ borderColor: shamrockColor }}>
              
              {/* Compartments Panel */}
              {showCompartmentPanel && (
                <div className="p-4">
                  <h4 className="font-crt text-sm mb-3" style={{ color: shamrockColor }}>
                    COMPARTMENT MANAGEMENT
                  </h4>
                  
                  <div className="space-y-3">
                    <div>
                      <h5 className="text-xs font-bold mb-2">Active Compartments ({shamrockState.activeCompartments.length})</h5>
                      {shamrockState.activeCompartments.map(comp => (
                        <div key={comp.id} className="p-2 border rounded text-xs mb-2"
                             style={{ borderColor: shamrockColor }}>
                          <pre className="whitespace-pre-wrap">{formatCompartment(comp)}</pre>
                          <button
                            onClick={() => executeRitual(`/toggle-compartment ${comp.name.split(' ')[0]}`)}
                            className="mt-1 px-2 py-1 border text-xs"
                            style={{ borderColor: shamrockColor, color: shamrockColor }}
                          >
                            MOVE TO BACKSTAGE
                          </button>
                        </div>
                      ))}
                    </div>
                    
                    <div>
                      <h5 className="text-xs font-bold mb-2">Backstage Compartments ({shamrockState.backstageCompartments.length})</h5>
                      {shamrockState.backstageCompartments.map(comp => (
                        <div key={comp.id} className="p-2 border rounded text-xs mb-2 opacity-60"
                             style={{ borderColor: shamrockColor }}>
                          <strong>{comp.name}</strong> (SEALED)
                          <button
                            onClick={() => executeRitual(`/toggle-compartment ${comp.name.split(' ')[0]}`)}
                            className="ml-2 px-2 py-1 border text-xs"
                            style={{ borderColor: shamrockColor, color: shamrockColor }}
                          >
                            REOPEN
                          </button>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              )}

              {/* Reports Panel */}
              {showReportsPanel && (
                <div className="p-4">
                  <h4 className="font-crt text-sm mb-3" style={{ color: shamrockColor }}>
                    A.D.D. ANALYSIS REPORTS
                  </h4>
                  
                  <button
                    onClick={() => executeRitual('/add-report new-investigation')}
                    className="w-full px-3 py-2 border font-crt text-xs mb-3"
                    style={{ borderColor: shamrockColor, color: shamrockColor }}
                  >
                    + GENERATE NEW REPORT
                  </button>
                  
                  <div className="space-y-2">
                    {shamrockState.activeReports.map(report => (
                      <div key={report.refNumber} className="p-2 border rounded text-xs"
                           style={{ borderColor: shamrockColor }}>
                        <div className="font-bold">{report.refNumber}</div>
                        <div className="text-xs opacity-60">{report.directive}</div>
                        <div className="text-xs">Status: {report.status}</div>
                        <div className="text-xs">Revisions: {report.fieldRevisions.length}</div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Rainbow Panel */}
              {showRainbowPanel && (
                <div className="p-4">
                  <h4 className="font-crt text-sm mb-3" style={{ color: shamrockColor }}>
                    RAINBOW OPTICS MATRIX
                  </h4>
                  
                  <button
                    onClick={() => executeRitual('/rainbow-audit')}
                    className="w-full px-3 py-2 border font-crt text-xs mb-3"
                    style={{ borderColor: shamrockColor, color: shamrockColor }}
                  >
                    RUN RAINBOW AUDIT
                  </button>
                  
                  <div className="space-y-2">
                    {shamrockState.rainbowMatrix.map((color, index) => (
                      <div key={index} className="p-2 border rounded text-xs"
                           style={{ borderColor: color.color }}>
                        <div className="font-bold" style={{ color: color.color }}>
                          {color.color.toUpperCase()}
                        </div>
                        <div className="text-xs">{color.subplot}</div>
                        <div className="text-xs">Charge: {color.emotionalCharge}</div>
                        <div className="text-xs">Risk: {Math.round(color.riskLevel * 100)}%</div>
                        <div className="text-xs">Priority: {Math.round(color.priority * 100)}%</div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Rituals Panel */}
              {showRitualPanel && (
                <div className="p-4">
                  <h4 className="font-crt text-sm mb-3" style={{ color: shamrockColor }}>
                    RITUAL COMMANDS
                  </h4>
                  
                  <div className="space-y-2">
                    {shamrockState.availableRituals.map(ritual => (
                      <button
                        key={ritual.command}
                        onClick={() => executeRitual(ritual.command)}
                        className="w-full p-2 border text-left font-crt text-xs transition-all"
                        style={{ borderColor: shamrockColor, color: shamrockColor }}
                        disabled={!ritual.isActive}
                      >
                        <div className="font-bold">{ritual.command}</div>
                        <div className="text-xs opacity-60">{ritual.description}</div>
                      </button>
                    ))}
                  </div>
                  
                  <div className="mt-4 p-2 border rounded text-xs"
                       style={{ borderColor: shamrockColor }}>
                    <strong>Quick Commands:</strong><br/>
                    <button onClick={() => executeRitual('/trace-negative-space')} className="text-blue-400 underline">Trace Negative Space</button><br/>
                    <button onClick={() => executeRitual('/settle-debt')} className="text-yellow-400 underline">Settle Ethical Debt</button><br/>
                    <button onClick={() => executeRitual('/drain')} className="text-red-400 underline">Drain Battery</button><br/>
                    <button onClick={() => executeRitual('/recharge')} className="text-green-400 underline">Recharge Battery</button>
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ShamrockStillmanChat;