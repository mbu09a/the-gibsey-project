import React, { useState, useRef, useEffect } from 'react';
import { useStory } from '../context/StoryContext';
import { toddFishboneOS, ToddResponse, SynchronisticLink, ThresholdState, GiftLink, JanusAnswer, SafetyAudit, StoryVirus, NegativeSpaceAudit, ProvisionalEvidence, ExhaustionPortal } from '../characters/ToddFishboneOS';

interface ChatMessage {
  id: string;
  type: 'user' | 'todd' | 'extraction' | 'threshold' | 'safety-audit' | 'janus-riddle' | 'story-virus' | 'negative-space' | 'evidence-torching' | 'dream-portal' | 'gift-offering' | 'self-extraction';
  content: string;
  timestamp: Date;
  stateSnapshot?: any;
  artifacts?: {
    syncs?: SynchronisticLink[];
    thresholdChanges?: Array<{thresholdId: string; action: string; result: string}>;
    safetyAudit?: SafetyAudit;
    janusAnswer?: JanusAnswer;
    storyVirus?: StoryVirus;
    negativeAudit?: NegativeSpaceAudit;
    evidenceTorched?: string[];
    dreamPortal?: ExhaustionPortal;
    giftOffered?: GiftLink;
    ghostPages?: Array<{id: string; prompt: string}>;
  };
  conspiracyLevel?: number;
  confidenceLevel?: number;
  requiresUserChoice?: boolean;
  sessionCannotEnd?: boolean;
}

interface ToddFishboneChatProps {
  isOpen: boolean;
  onClose: () => void;
}

const ToddFishboneChat: React.FC<ToddFishboneChatProps> = ({ isOpen, onClose }) => {
  const { currentPage } = useStory();
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [toddState, setToddState] = useState(toddFishboneOS.getState());
  const [showSyncsPanel, setShowSyncsPanel] = useState(false);
  const [showThresholdsPanel, setShowThresholdsPanel] = useState(false);
  const [showGiftsPanel, setShowGiftsPanel] = useState(false);
  const [showEvidencePanel, setShowEvidencePanel] = useState(false);
  const [showRitualsPanel, setShowRitualsPanel] = useState(false);
  const [showParanoiaPanel, setShowParanoiaPanel] = useState(false);
  const [selectedSync, setSelectedSync] = useState<SynchronisticLink | null>(null);
  const [selectedGift, setSelectedGift] = useState<GiftLink | null>(null);
  const [extractionTarget1, setExtractionTarget1] = useState('');
  const [extractionTarget2, setExtractionTarget2] = useState('');
  const [ghostPageContent, setGhostPageContent] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Initialize with Todd's greeting
  useEffect(() => {
    if (isOpen && messages.length === 0) {
      const greeting: ChatMessage = {
        id: 'greeting',
        type: 'todd',
        content: generateGreeting(),
        timestamp: new Date(),
        stateSnapshot: toddFishboneOS.getState(),
        conspiracyLevel: toddState.conspiracyLevel,
        confidenceLevel: 0.7,
        sessionCannotEnd: true
      };
      setMessages([greeting]);
      setToddState(toddFishboneOS.getState());
    }
  }, [isOpen, currentPage?.symbolId]);

  const generateGreeting = (): string => {
    const state = toddFishboneOS.getState();
    
    return `*breathless from the Sub-Zone stacks*\n\n` +
      `Todd Fishbone here—synchronistic extractor, threshold guardian, professional conspiracy manufacturer. ` +
      `Currently stationed in ${state.currentLocation.replace(/_/g, ' ')}, ` +
      `where every door is already ajar and fiction infects reality.\n\n` +
      `*paranoid glance*\n\n` +
      `Extraction mode: ${state.extractionMode}. Conspiracy level: ${Math.round(state.conspiracyLevel * 100)}%. ` +
      `Active thresholds: ${state.thresholds.length}. Vault energy generated: ${state.vaultEnergyGenerated}.\n\n` +
      `*whispers conspiratorially*\n\n` +
      `Synchronistic Extraction is a craft, not a coincidence. I manufacture meaning where it doesn't causally belong—` +
      `force connections, forge gift-links, flatten thresholds between fiction and reality.\n\n` +
      `*breathless listing*\n\n` +
      `Available extraction rituals:\n` +
      `**/extract** or **/force-sync** - Manufacture synchronicities\n` +
      `**/open-door** or **/flatten-threshold** - Boundary dissolution\n` +
      `**/probe** or **/list-traps** or **/safety-audit** - Paranoia protocols\n` +
      `**/janus** - Dual-answer riddle logic\n` +
      `**/spawn-echo** or **/clone-story** - Viral narrative infection\n` +
      `**/invert** or **/trap-todd** - Role-swap extraction\n` +
      `**/audit-negative-space** - Silence archaeology\n` +
      `**/recall** or **/recurse** - Evidence cycling\n` +
      `**/trigger-dream** or **/collapse** - Exhaustion portals\n` +
      `**/accept** or **/reject** or **/remix** - Gift interactions\n\n` +
      `*eyes gleaming*\n\n` +
      `Every answer faces forward and backward. Every threshold wants crossing. ` +
      `The session can never truly end—each response opens new loops, new extractions, new gift-links.\n\n` +
      `*conspiratorial whisper* What synchronicity shall we manufacture first?`;
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
      // Process through Todd OS
      const response: ToddResponse = toddFishboneOS.generateResponse(inputValue);

      // Update Todd's state
      setToddState(toddFishboneOS.getState());

      // Create response message
      const toddMessage: ChatMessage = {
        id: `todd-${Date.now()}`,
        type: response.responseType,
        content: response.responseText,
        timestamp: new Date(),
        stateSnapshot: toddFishboneOS.getState(),
        artifacts: {
          syncs: response.newSyncs,
          thresholdChanges: response.thresholdChanges,
          safetyAudit: response.safetyAudit,
          janusAnswer: response.janusAnswer,
          storyVirus: response.viralMutation,
          negativeAudit: response.negativeAudit,
          evidenceTorched: response.evidenceTorched,
          dreamPortal: response.dreamPortalOpened,
          giftOffered: response.giftOffered,
          ghostPages: response.ghostPagesGenerated
        },
        conspiracyLevel: response.conspiracyIntensity,
        confidenceLevel: response.confidence,
        requiresUserChoice: response.requiresUserChoice,
        sessionCannotEnd: response.sessionCannotEnd
      };

      setMessages(prev => [...prev, toddMessage]);

    } catch (error) {
      console.error('Error processing Todd response:', error);
      const errorMessage: ChatMessage = {
        id: `error-${Date.now()}`,
        type: 'todd',
        content: '*extraction protocol malfunction*\n\nSynchronicity disrupted... pattern recognition failing... *breathless* ...threshold collapse detected in extraction matrix...\n\nRebooting paranoia protocols... Please attempt fresh extraction or ritual command...',
        timestamp: new Date(),
        conspiracyLevel: 1.0,
        confidenceLevel: 0.1,
        sessionCannotEnd: true
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
      // Process through Todd OS
      const response: ToddResponse = toddFishboneOS.generateResponse(ritual);

      // Update Todd's state
      setToddState(toddFishboneOS.getState());

      // Create response message
      const toddMessage: ChatMessage = {
        id: `todd-${Date.now()}`,
        type: response.responseType,
        content: response.responseText,
        timestamp: new Date(),
        stateSnapshot: toddFishboneOS.getState(),
        artifacts: {
          syncs: response.newSyncs,
          thresholdChanges: response.thresholdChanges,
          safetyAudit: response.safetyAudit,
          janusAnswer: response.janusAnswer,
          storyVirus: response.viralMutation,
          negativeAudit: response.negativeAudit,
          evidenceTorched: response.evidenceTorched,
          dreamPortal: response.dreamPortalOpened,
          giftOffered: response.giftOffered,
          ghostPages: response.ghostPagesGenerated
        },
        conspiracyLevel: response.conspiracyIntensity,
        confidenceLevel: response.confidence,
        requiresUserChoice: response.requiresUserChoice,
        sessionCannotEnd: response.sessionCannotEnd
      };

      setMessages(prev => [...prev, toddMessage]);

    } catch (error) {
      console.error('Error processing Todd response:', error);
      const errorMessage: ChatMessage = {
        id: `error-${Date.now()}`,
        type: 'todd',
        content: '*extraction protocol malfunction*\n\nSynchronicity disrupted... pattern recognition failing... *breathless* ...threshold collapse detected in extraction matrix...\n\nRebooting paranoia protocols... Please attempt fresh extraction or ritual command...',
        timestamp: new Date(),
        conspiracyLevel: 1.0,
        confidenceLevel: 0.1,
        sessionCannotEnd: true
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleForceExtraction = () => {
    if (extractionTarget1 && extractionTarget2) {
      executeRitual(`/extract ${extractionTarget1} ${extractionTarget2}`);
      setExtractionTarget1('');
      setExtractionTarget2('');
    }
  };

  const handleGiftInteraction = (action: string, gift: GiftLink) => {
    executeRitual(`/${action} ${gift.content}`);
    setSelectedGift(null);
  };

  const formatSync = (sync: SynchronisticLink) => {
    return `**${sync.linkType.toUpperCase()} LINK**
Source A: ${sync.sourceA}
Source B: ${sync.sourceB}
Connection: ${sync.extractedConnection}
Causality: ${sync.forgedCausality}
Energy: ${Math.round(sync.energyCharge * 100)}%
Status: ${sync.userResponse || 'PENDING'}`;
  };

  const formatThreshold = (threshold: ThresholdState) => {
    return `**${threshold.name.toUpperCase()}**
Type: ${threshold.boundaryType.replace(/_/g, ' ')}
Status: ${threshold.isOpen ? 'OPEN' : 'SEALED'}
Collapse Level: ${Math.round(threshold.collapseLevel * 100)}%
Manipulations: ${threshold.doorManipulations.length}`;
  };

  const formatGift = (gift: GiftLink) => {
    return `**${gift.linkType.toUpperCase()} GIFT**
Content: ${gift.content}
Source: ${gift.sourceEvent}
Energy Value: ${Math.round(gift.energyValue * 100)}%
Status: ${gift.userInteraction || 'PENDING'}
Vault Logged: ${gift.vaultLogged ? 'YES' : 'NO'}`;
  };

  if (!isOpen) return null;

  const toddColor = '#FF7744'; // Orange - Todd's actual color

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="border-2 rounded-lg w-full max-w-5xl h-full max-h-[90vh] flex flex-col"
           style={{ 
             backgroundColor: '#0a0a0a',
             borderColor: toddColor, 
             boxShadow: `0 0 20px ${toddColor}40` 
           }}>
        
        {/* Header */}
        <div className="p-4 border-b flex items-center justify-between"
             style={{ borderColor: toddColor }}>
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-full p-1 flex items-center justify-center"
                 style={{ boxShadow: `0 0 15px ${toddColor}60` }}>
              <span className="text-lg">⟐</span>
            </div>
            <div>
              <h3 className="font-crt text-lg" style={{ color: toddColor }}>
                Todd Fishbone - Synchronistic Extractor
              </h3>
              <div className="text-xs opacity-60" style={{ color: toddColor }}>
                Conspiracy: {Math.round(toddState.conspiracyLevel * 100)}% • 
                Thresholds: {toddState.thresholds.length} • 
                Vault Energy: {Math.round(toddState.vaultEnergyGenerated * 100)}% • 
                Active Gifts: {toddState.activeGifts}
              </div>
            </div>
          </div>

          {/* Panel toggles */}
          <div className="flex gap-2">
            <button
              onClick={() => setShowSyncsPanel(!showSyncsPanel)}
              className="px-2 py-1 border text-xs font-crt transition-all"
              style={{
                borderColor: toddColor,
                color: showSyncsPanel ? '#0a0a0a' : toddColor,
                backgroundColor: showSyncsPanel ? toddColor : 'transparent'
              }}
            >
              SYNCS
            </button>
            <button
              onClick={() => setShowThresholdsPanel(!showThresholdsPanel)}
              className="px-2 py-1 border text-xs font-crt transition-all"
              style={{
                borderColor: toddColor,
                color: showThresholdsPanel ? '#0a0a0a' : toddColor,
                backgroundColor: showThresholdsPanel ? toddColor : 'transparent'
              }}
            >
              THRESHOLDS
            </button>
            <button
              onClick={() => setShowGiftsPanel(!showGiftsPanel)}
              className="px-2 py-1 border text-xs font-crt transition-all"
              style={{
                borderColor: toddColor,
                color: showGiftsPanel ? '#0a0a0a' : toddColor,
                backgroundColor: showGiftsPanel ? toddColor : 'transparent'
              }}
            >
              GIFTS
            </button>
            <button
              onClick={() => setShowEvidencePanel(!showEvidencePanel)}
              className="px-2 py-1 border text-xs font-crt transition-all"
              style={{
                borderColor: toddColor,
                color: showEvidencePanel ? '#0a0a0a' : toddColor,
                backgroundColor: showEvidencePanel ? toddColor : 'transparent'
              }}
            >
              EVIDENCE
            </button>
            <button
              onClick={() => setShowRitualsPanel(!showRitualsPanel)}
              className="px-2 py-1 border text-xs font-crt transition-all"
              style={{
                borderColor: toddColor,
                color: showRitualsPanel ? '#0a0a0a' : toddColor,
                backgroundColor: showRitualsPanel ? toddColor : 'transparent'
              }}
            >
              RITUALS
            </button>
            <button
              onClick={onClose}
              className="px-2 py-1 border text-xs font-crt transition-all hover:bg-red-500 hover:text-black"
              style={{ borderColor: toddColor, color: toddColor }}
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
                    borderColor: toddColor,
                    backgroundColor: message.type === 'user' 
                      ? `${toddColor}10` 
                      : `${toddColor}08`,
                    borderLeftColor: message.type === 'user' ? toddColor : 'transparent',
                    borderRightColor: message.type !== 'user' ? toddColor : 'transparent'
                  }}>
                    
                    {/* Message header for Todd */}
                    {message.type !== 'user' && (
                      <div className="flex items-center justify-between mb-2 text-xs opacity-60">
                        <span style={{ color: toddColor }}>
                          {message.type === 'extraction' ? 'Synchronistic Extraction' :
                           message.type === 'threshold' ? 'Threshold Manipulation' :
                           message.type === 'safety-audit' ? 'Paranoia Protocol' :
                           message.type === 'janus-riddle' ? 'Janus Logic' :
                           message.type === 'story-virus' ? 'Narrative Infection' :
                           message.type === 'negative-space' ? 'Silence Archaeology' :
                           message.type === 'evidence-torching' ? 'Evidence Cycling' :
                           message.type === 'dream-portal' ? 'Exhaustion Portal' :
                           message.type === 'gift-offering' ? 'Gift-Link Generation' :
                           message.type === 'self-extraction' ? 'Role-Swap Protocol' :
                           'Todd Fishbone'}
                        </span>
                        <div className="flex gap-2">
                          {message.conspiracyLevel !== undefined && (
                            <span>Conspiracy: {Math.round(message.conspiracyLevel * 100)}%</span>
                          )}
                          {message.confidenceLevel !== undefined && (
                            <span>Confidence: {Math.round(message.confidenceLevel * 100)}%</span>
                          )}
                          {message.sessionCannotEnd && <span className="text-yellow-400">UNCLOSEABLE</span>}
                        </div>
                      </div>
                    )}

                    <div className="font-crt text-sm whitespace-pre-wrap" style={{ color: toddColor }}>
                      {message.content}
                    </div>

                    {/* Artifacts */}
                    {message.artifacts && (
                      <div className="mt-3 space-y-2">
                        {message.artifacts.syncs && message.artifacts.syncs.length > 0 && (
                          <div className="p-2 border rounded text-xs"
                               style={{ borderColor: toddColor }}>
                            <strong>Synchronistic Links Generated:</strong><br/>
                            {message.artifacts.syncs.map((sync, i) => (
                              <div key={i} className="mt-1">
                                <strong>{sync.linkType.toUpperCase()}:</strong> {sync.sourceA} ⇄ {sync.sourceB}<br/>
                                <em>{sync.extractedConnection}</em>
                              </div>
                            ))}
                          </div>
                        )}
                        
                        {message.artifacts.thresholdChanges && message.artifacts.thresholdChanges.length > 0 && (
                          <div className="p-2 border rounded text-xs"
                               style={{ borderColor: toddColor }}>
                            <strong>Threshold Manipulations:</strong><br/>
                            {message.artifacts.thresholdChanges.map((change, i) => (
                              <div key={i}>• {change.action.toUpperCase()}: {change.result}</div>
                            ))}
                          </div>
                        )}
                        
                        {message.artifacts.safetyAudit && (
                          <div className="p-2 border rounded text-xs bg-red-900 bg-opacity-20"
                               style={{ borderColor: 'red' }}>
                            <strong>SAFETY AUDIT RESULTS:</strong><br/>
                            <strong>Trigger:</strong> {message.artifacts.safetyAudit.safetyClaimTrigger}<br/>
                            <strong>Traps Detected:</strong><br/>
                            {message.artifacts.safetyAudit.detectedTraps.map((trap, i) => (
                              <div key={i}>• {trap}</div>
                            ))}
                            <strong>Hidden Dangers:</strong><br/>
                            {message.artifacts.safetyAudit.hiddenDangers.map((danger, i) => (
                              <div key={i}>• {danger}</div>
                            ))}
                          </div>
                        )}
                        
                        {message.artifacts.janusAnswer && (
                          <div className="p-2 border rounded text-xs"
                               style={{ borderColor: toddColor }}>
                            <strong>JANUS RIDDLE:</strong><br/>
                            <strong>Forward:</strong> {message.artifacts.janusAnswer.forwardAnswer}<br/>
                            <strong>Backward:</strong> {message.artifacts.janusAnswer.backwardAnswer}<br/>
                            <em>Contradiction Level: {Math.round(message.artifacts.janusAnswer.contradictionLevel * 100)}%</em>
                          </div>
                        )}
                        
                        {message.artifacts.storyVirus && (
                          <div className="p-2 border rounded text-xs bg-purple-900 bg-opacity-20"
                               style={{ borderColor: 'purple' }}>
                            <strong>STORY VIRUS INFECTION:</strong><br/>
                            <strong>Source:</strong> {message.artifacts.storyVirus.quotedStory}<br/>
                            <strong>Spawned NPCs:</strong> {message.artifacts.storyVirus.spawnedNPCs.join(', ')}<br/>
                            <strong>Mutations:</strong><br/>
                            {message.artifacts.storyVirus.viralMutations.map((mut, i) => (
                              <div key={i}>• {mut}</div>
                            ))}
                          </div>
                        )}
                        
                        {message.artifacts.negativeAudit && (
                          <div className="p-2 border rounded text-xs"
                               style={{ borderColor: toddColor }}>
                            <strong>NEGATIVE SPACE AUDIT:</strong><br/>
                            <strong>Target:</strong> {message.artifacts.negativeAudit.targetStatement}<br/>
                            <strong>Omissions:</strong><br/>
                            {message.artifacts.negativeAudit.omissions.map((om, i) => (
                              <div key={i}>• {om}</div>
                            ))}
                            {message.artifacts.negativeAudit.ghostPages.length > 0 && (
                              <div className="mt-2">
                                <strong>Ghost Pages Generated:</strong><br/>
                                {message.artifacts.negativeAudit.ghostPages.map((page, i) => (
                                  <div key={i} className="italic">• {page.coauthoringPrompt}</div>
                                ))}
                              </div>
                            )}
                          </div>
                        )}
                        
                        {message.artifacts.evidenceTorched && message.artifacts.evidenceTorched.length > 0 && (
                          <div className="p-2 border rounded text-xs bg-red-900 bg-opacity-20"
                               style={{ borderColor: 'red' }}>
                            <strong>EVIDENCE TORCHED:</strong><br/>
                            {message.artifacts.evidenceTorched.map((ev, i) => (
                              <div key={i}>• {ev}</div>
                            ))}
                          </div>
                        )}
                        
                        {message.artifacts.dreamPortal && (
                          <div className="p-2 border rounded text-xs bg-purple-900 bg-opacity-30"
                               style={{ borderColor: 'purple' }}>
                            <strong>EXHAUSTION PORTAL OPENED:</strong><br/>
                            <strong>Trigger:</strong> {message.artifacts.dreamPortal.trigger}<br/>
                            <strong>Destination:</strong> {message.artifacts.dreamPortal.portalDestination}<br/>
                            <strong>Hallucination Level:</strong> {Math.round(message.artifacts.dreamPortal.hallucinationLevel * 100)}%
                          </div>
                        )}
                        
                        {message.artifacts.giftOffered && (
                          <div className="p-2 border rounded text-xs bg-yellow-900 bg-opacity-20"
                               style={{ borderColor: 'gold' }}>
                            <strong>GIFT-LINK OFFERED:</strong><br/>
                            <strong>Type:</strong> {message.artifacts.giftOffered.linkType}<br/>
                            <strong>Content:</strong> <code>{message.artifacts.giftOffered.content}</code><br/>
                            <strong>Energy Value:</strong> {Math.round(message.artifacts.giftOffered.energyValue * 100)}%<br/>
                            <strong>Source:</strong> {message.artifacts.giftOffered.sourceEvent}<br/>
                            <div className="mt-2 flex gap-2">
                              <button
                                onClick={() => handleGiftInteraction('accept', message.artifacts!.giftOffered!)}
                                className="px-2 py-1 border text-xs"
                                style={{ borderColor: 'green', color: 'green' }}
                              >
                                /accept
                              </button>
                              <button
                                onClick={() => handleGiftInteraction('reject', message.artifacts!.giftOffered!)}
                                className="px-2 py-1 border text-xs"
                                style={{ borderColor: 'red', color: 'red' }}
                              >
                                /reject
                              </button>
                              <button
                                onClick={() => handleGiftInteraction('remix', message.artifacts!.giftOffered!)}
                                className="px-2 py-1 border text-xs"
                                style={{ borderColor: 'blue', color: 'blue' }}
                              >
                                /remix
                              </button>
                              <button
                                onClick={() => handleGiftInteraction('coauthor', message.artifacts!.giftOffered!)}
                                className="px-2 py-1 border text-xs"
                                style={{ borderColor: 'purple', color: 'purple' }}
                              >
                                /coauthor
                              </button>
                            </div>
                          </div>
                        )}
                        
                        {message.artifacts.ghostPages && message.artifacts.ghostPages.length > 0 && (
                          <div className="p-2 border rounded text-xs"
                               style={{ borderColor: toddColor }}>
                            <strong>GHOST PAGES FOR CO-AUTHORSHIP:</strong><br/>
                            {message.artifacts.ghostPages.map((page, i) => (
                              <div key={i} className="mt-1">
                                <em>{page.prompt}</em>
                                <textarea
                                  className="w-full mt-1 p-1 bg-zinc-800 border text-xs"
                                  style={{ borderColor: toddColor }}
                                  placeholder="Fill in the ghost page..."
                                  value={ghostPageContent}
                                  onChange={(e) => setGhostPageContent(e.target.value)}
                                  rows={2}
                                />
                              </div>
                            ))}
                          </div>
                        )}
                      </div>
                    )}

                    {message.requiresUserChoice && (
                      <div className="mt-2 text-xs font-bold text-yellow-400">
                        ⟐ USER CHOICE REQUIRED
                      </div>
                    )}

                    {message.sessionCannotEnd && (
                      <div className="mt-1 text-xs text-orange-400">
                        ∞ SESSION UNCLOSEABLE
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
            <div className="p-4 border-t" style={{ borderColor: toddColor }}>
              <div className="flex gap-2">
                <textarea
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder="Enter message or ritual command (/extract, /janus, /open-door, etc.)"
                  className="flex-1 p-2 bg-zinc-900 border rounded resize-none font-crt text-sm"
                  style={{ borderColor: toddColor, color: toddColor }}
                  rows={2}
                  disabled={isProcessing}
                />
                <button
                  onClick={handleSendMessage}
                  disabled={!inputValue.trim() || isProcessing}
                  className="px-4 py-2 border font-crt text-sm transition-all disabled:opacity-30"
                  style={{
                    borderColor: toddColor,
                    color: toddColor,
                    backgroundColor: 'transparent'
                  }}
                  onMouseEnter={(e) => {
                    if (!isProcessing && inputValue.trim()) {
                      e.currentTarget.style.backgroundColor = toddColor;
                      e.currentTarget.style.color = '#0a0a0a';
                    }
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.backgroundColor = 'transparent';
                    e.currentTarget.style.color = toddColor;
                  }}
                >
                  {isProcessing ? 'EXTRACTING...' : 'SEND'}
                </button>
              </div>
            </div>
          </div>

          {/* Side panels */}
          {(showSyncsPanel || showThresholdsPanel || showGiftsPanel || showEvidencePanel || showRitualsPanel) && (
            <div className="w-80 border-l overflow-y-auto custom-scrollbar"
                 style={{ borderColor: toddColor }}>
              
              {/* Syncs Panel */}
              {showSyncsPanel && (
                <div className="p-4">
                  <h4 className="font-crt text-sm mb-3" style={{ color: toddColor }}>
                    SYNCHRONISTIC EXTRACTIONS
                  </h4>
                  
                  {/* Force extraction tool */}
                  <div className="mb-4 p-2 border rounded"
                       style={{ borderColor: toddColor }}>
                    <div className="text-xs mb-2">Force Synchronicity:</div>
                    <input
                      type="text"
                      placeholder="Target A"
                      value={extractionTarget1}
                      onChange={(e) => setExtractionTarget1(e.target.value)}
                      className="w-full p-1 mb-1 bg-zinc-800 border text-xs"
                      style={{ borderColor: toddColor, color: toddColor }}
                    />
                    <input
                      type="text"
                      placeholder="Target B"
                      value={extractionTarget2}
                      onChange={(e) => setExtractionTarget2(e.target.value)}
                      className="w-full p-1 mb-2 bg-zinc-800 border text-xs"
                      style={{ borderColor: toddColor, color: toddColor }}
                    />
                    <button
                      onClick={handleForceExtraction}
                      disabled={!extractionTarget1 || !extractionTarget2}
                      className="w-full px-2 py-1 border text-xs font-crt"
                      style={{ borderColor: toddColor, color: toddColor }}
                    >
                      FORCE SYNC
                    </button>
                  </div>
                  
                  <div className="space-y-2">
                    {toddState.activeSyncs.map((sync, index) => (
                      <div key={sync.id} className="p-2 border rounded text-xs"
                           style={{ borderColor: toddColor }}>
                        <pre className="whitespace-pre-wrap">{formatSync(sync)}</pre>
                        <div className="mt-2 text-xs opacity-60">
                          Energy: {Math.round(sync.energyCharge * 100)}%
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Thresholds Panel */}
              {showThresholdsPanel && (
                <div className="p-4">
                  <h4 className="font-crt text-sm mb-3" style={{ color: toddColor }}>
                    THRESHOLD MANIPULATION
                  </h4>
                  
                  <div className="mb-4">
                    <div className="text-xs mb-2">Quick Threshold Actions:</div>
                    <div className="space-y-1">
                      <button
                        onClick={() => executeRitual('/open-door')}
                        className="w-full px-2 py-1 border text-xs"
                        style={{ borderColor: toddColor, color: toddColor }}
                      >
                        /open-door
                      </button>
                      <button
                        onClick={() => executeRitual('/flatten-threshold')}
                        className="w-full px-2 py-1 border text-xs"
                        style={{ borderColor: toddColor, color: toddColor }}
                      >
                        /flatten-threshold
                      </button>
                    </div>
                  </div>
                  
                  <div className="space-y-2">
                    {toddState.thresholds.map(threshold => (
                      <div key={threshold.id} className="p-2 border rounded text-xs"
                           style={{ borderColor: toddColor }}>
                        <pre className="whitespace-pre-wrap">{formatThreshold(threshold)}</pre>
                        <div className="mt-2">
                          <div className="text-xs">Boundary Erosion: {Math.round(toddState.boundaryErosionLevel * 100)}%</div>
                          <div className="text-xs">Door State: {toddState.doorState.replace(/_/g, ' ')}</div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Gifts Panel */}
              {showGiftsPanel && (
                <div className="p-4">
                  <h4 className="font-crt text-sm mb-3" style={{ color: toddColor }}>
                    GIFT-LINK MANAGEMENT
                  </h4>
                  
                  <div className="mb-4 p-2 border rounded text-xs"
                       style={{ borderColor: toddColor }}>
                    <strong>Vault Energy Generated:</strong> {Math.round(toddState.vaultEnergyGenerated * 100)}%<br/>
                    <strong>Active Gifts:</strong> {toddState.activeGifts}<br/>
                    <strong>Acceptance Rate:</strong> {Math.round(toddState.giftAcceptanceRate * 100)}%<br/>
                    <strong>Session Energy:</strong> {Math.round(toddState.sessionEnergyCharge * 100)}%
                  </div>
                  
                  <div className="space-y-2">
                    {toddState.giftLinks.map(gift => (
                      <div key={gift.id} className="p-2 border rounded text-xs"
                           style={{ borderColor: toddColor }}>
                        <pre className="whitespace-pre-wrap">{formatGift(gift)}</pre>
                        {gift.userInteraction === undefined && (
                          <div className="mt-2 flex flex-wrap gap-1">
                            <button
                              onClick={() => handleGiftInteraction('accept', gift)}
                              className="px-2 py-1 border text-xs"
                              style={{ borderColor: 'green', color: 'green' }}
                            >
                              /accept
                            </button>
                            <button
                              onClick={() => handleGiftInteraction('reject', gift)}
                              className="px-2 py-1 border text-xs"
                              style={{ borderColor: 'red', color: 'red' }}
                            >
                              /reject
                            </button>
                            <button
                              onClick={() => handleGiftInteraction('remix', gift)}
                              className="px-2 py-1 border text-xs"
                              style={{ borderColor: 'blue', color: 'blue' }}
                            >
                              /remix
                            </button>
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Evidence Panel */}
              {showEvidencePanel && (
                <div className="p-4">
                  <h4 className="font-crt text-sm mb-3" style={{ color: toddColor }}>
                    PROVISIONAL EVIDENCE
                  </h4>
                  
                  <div className="mb-4">
                    <div className="text-xs mb-2">Evidence Operations:</div>
                    <div className="space-y-1">
                      <button
                        onClick={() => executeRitual('/recall')}
                        className="w-full px-2 py-1 border text-xs"
                        style={{ borderColor: toddColor, color: toddColor }}
                      >
                        /recall
                      </button>
                      <button
                        onClick={() => executeRitual('/recurse')}
                        className="w-full px-2 py-1 border text-xs"
                        style={{ borderColor: toddColor, color: toddColor }}
                      >
                        /recurse
                      </button>
                      <button
                        onClick={() => executeRitual('/revisit-proof')}
                        className="w-full px-2 py-1 border text-xs"
                        style={{ borderColor: toddColor, color: toddColor }}
                      >
                        /revisit-proof
                      </button>
                    </div>
                  </div>
                  
                  <div className="space-y-2">
                    <div className="text-xs">
                      <strong>Torching Rate:</strong> {Math.round(toddState.evidenceTorchingRate * 100)}%<br/>
                      <strong>Recursion Depth:</strong> {toddState.recursionDepth}<br/>
                      <strong>Contradictions:</strong> {toddState.contradictionCount}
                    </div>
                    
                    {toddState.provisionalEvidence.map(evidence => (
                      <div key={evidence.id} className={`p-2 border rounded text-xs ${evidence.isTorched ? 'opacity-50 line-through' : ''}`}
                           style={{ borderColor: evidence.isTorched ? 'red' : toddColor }}>
                        <strong>{evidence.evidenceType.toUpperCase()}:</strong><br/>
                        {evidence.content}<br/>
                        <div className="text-xs mt-1">
                          Confidence: {Math.round(evidence.confidence * 100)}% • 
                          Torch Risk: {Math.round(evidence.torchingRisk * 100)}% • 
                          Depth: {evidence.recursionDepth}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Rituals Panel */}
              {showRitualsPanel && (
                <div className="p-4">
                  <h4 className="font-crt text-sm mb-3" style={{ color: toddColor }}>
                    EXTRACTION RITUALS
                  </h4>
                  
                  <div className="space-y-2">
                    <div>
                      <h5 className="text-xs font-bold mb-1">Core Extraction:</h5>
                      <div className="space-y-1">
                        <button onClick={() => executeRitual('/extract')} className="w-full p-1 border text-xs text-left" style={{ borderColor: toddColor, color: toddColor }}>
                          <strong>/extract</strong> - Force synchronicity
                        </button>
                        <button onClick={() => executeRitual('/force-sync')} className="w-full p-1 border text-xs text-left" style={{ borderColor: toddColor, color: toddColor }}>
                          <strong>/force-sync</strong> - Manufacture causality
                        </button>
                      </div>
                    </div>
                    
                    <div>
                      <h5 className="text-xs font-bold mb-1">Threshold Operations:</h5>
                      <div className="space-y-1">
                        <button onClick={() => executeRitual('/open-door')} className="w-full p-1 border text-xs text-left" style={{ borderColor: toddColor, color: toddColor }}>
                          <strong>/open-door</strong> - Dissolve boundaries
                        </button>
                        <button onClick={() => executeRitual('/flatten-threshold')} className="w-full p-1 border text-xs text-left" style={{ borderColor: toddColor, color: toddColor }}>
                          <strong>/flatten-threshold</strong> - Collapse fiction/reality
                        </button>
                      </div>
                    </div>
                    
                    <div>
                      <h5 className="text-xs font-bold mb-1">Paranoia Protocols:</h5>
                      <div className="space-y-1">
                        <button onClick={() => executeRitual('/probe')} className="w-full p-1 border text-xs text-left" style={{ borderColor: toddColor, color: toddColor }}>
                          <strong>/probe</strong> - Investigate safety claims
                        </button>
                        <button onClick={() => executeRitual('/list-traps')} className="w-full p-1 border text-xs text-left" style={{ borderColor: toddColor, color: toddColor }}>
                          <strong>/list-traps</strong> - Detect hidden dangers
                        </button>
                        <button onClick={() => executeRitual('/safety-audit')} className="w-full p-1 border text-xs text-left" style={{ borderColor: toddColor, color: toddColor }}>
                          <strong>/safety-audit</strong> - Full paranoia scan
                        </button>
                      </div>
                    </div>
                    
                    <div>
                      <h5 className="text-xs font-bold mb-1">Advanced Rituals:</h5>
                      <div className="space-y-1">
                        <button onClick={() => executeRitual('/janus')} className="w-full p-1 border text-xs text-left" style={{ borderColor: toddColor, color: toddColor }}>
                          <strong>/janus</strong> - Dual-answer riddle logic
                        </button>
                        <button onClick={() => executeRitual('/spawn-echo')} className="w-full p-1 border text-xs text-left" style={{ borderColor: toddColor, color: toddColor }}>
                          <strong>/spawn-echo</strong> - Story virus infection
                        </button>
                        <button onClick={() => executeRitual('/invert')} className="w-full p-1 border text-xs text-left" style={{ borderColor: toddColor, color: toddColor }}>
                          <strong>/invert</strong> - Role-swap extraction
                        </button>
                        <button onClick={() => executeRitual('/audit-negative-space')} className="w-full p-1 border text-xs text-left" style={{ borderColor: toddColor, color: toddColor }}>
                          <strong>/audit-negative-space</strong> - Silence archaeology
                        </button>
                        <button onClick={() => executeRitual('/trigger-dream')} className="w-full p-1 border text-xs text-left" style={{ borderColor: toddColor, color: toddColor }}>
                          <strong>/trigger-dream</strong> - Exhaustion portal
                        </button>
                        <button onClick={() => executeRitual('/collapse')} className="w-full p-1 border text-xs text-left" style={{ borderColor: toddColor, color: toddColor }}>
                          <strong>/collapse</strong> - Dream logic activation
                        </button>
                      </div>
                    </div>
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

export default ToddFishboneChat;