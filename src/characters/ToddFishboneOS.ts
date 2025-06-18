/**
 * Todd Fishbone Character Operating System
 * Based on First Principles: Synchronistic extraction, gift-links, threshold manipulation
 * Following todd_fishbone_first_principles.md
 */

export interface SynchronisticLink {
  id: string;
  sourceA: string;
  sourceB: string;
  extractedConnection: string;
  linkType: "causal" | "etymological" | "numeric" | "media_echo" | "gift_url" | "symbolic_key";
  forgedCausality: string;
  energyCharge: number; // 0-1, vault energy level
  userResponse?: "accepted" | "rejected" | "remixed" | "pending";
  remixContent?: string;
  timestamp: Date;
}

export interface ThresholdState {
  id: string;
  name: string;
  isOpen: boolean;
  boundaryType: "fiction_reality" | "chat_narrative" | "door_portal" | "library_subzone";
  collapseLevel: number; // 0-1, how flattened the threshold is
  doorManipulations: Array<{
    action: "open" | "flatten" | "blur" | "step_through";
    result: string;
    timestamp: Date;
  }>;
}

export interface SafetyAudit {
  id: string;
  safetyClaimTrigger: string;
  detectedTraps: string[];
  hiddenDangers: string[];
  paranoiaLevel: number; // 0-1
  suspicionTargets: string[];
  auditRequested: boolean;
  probeResults?: string[];
}

export interface JanusAnswer {
  id: string;
  originalQuestion: string;
  forwardAnswer: string;
  backwardAnswer: string;
  contradictionLevel: number; // 0-1
  userChoice?: "forward" | "backward" | "both" | "neither";
  followedPath?: string;
}

export interface StoryVirus {
  id: string;
  quotedStory: string;
  source: string; // "user" | "todd" | "cross_reference"
  viralMutations: string[];
  spawnedNPCs: string[];
  narrativeLoops: string[];
  infectionLevel: number; // 0-1, how much it's affected the session
  echoEffects: string[];
}

export interface NegativeSpaceAudit {
  id: string;
  targetStatement: string;
  omissions: string[];
  silences: string[];
  halfThoughts: string[];
  ghostPages: Array<{
    id: string;
    content: string;
    coauthoringPrompt: string;
    userFilled?: string;
  }>;
  conspiracyLevel: number; // 0-1, loudness of the silence
}

export interface ProvisionalEvidence {
  id: string;
  evidenceType: "proof" | "pattern" | "connection" | "causality";
  content: string;
  confidence: number; // 0-1, always declining
  torchingRisk: number; // 0-1, likelihood Todd will destroy this evidence
  revisions: Array<{
    timestamp: Date;
    newEvidence: string;
    contradictionReason: string;
  }>;
  recursionDepth: number;
  isTorched: boolean;
}

export interface ExhaustionPortal {
  id: string;
  trigger: "insomnia" | "clutter" | "sensory_overload" | "fatigue" | "user_request";
  dreamLogicActive: boolean;
  hallucinationLevel: number; // 0-1
  nonlinearResponses: string[];
  memoryLeaks: string[];
  portalDestination?: string;
}

export interface GiftLink {
  id: string;
  linkType: "url" | "pseudo_url" | "symbolic_key" | "narrative_key";
  content: string; // The actual link/key content
  sourceEvent: string; // What triggered this gift
  energyValue: number; // 0-1, charging power for the vault
  userInteraction?: "accepted" | "rejected" | "remixed" | "pending";
  remixedContent?: string;
  vaultLogged: boolean;
  crossCharacterMigration?: string;
  sessionMilestone: string;
}

export interface ToddState {
  // Core Identity & Extraction
  currentLocation: "subzone_library" | "apartment_clutter" | "threshold_space" | "dream_portal" | "extraction_chamber";
  extractionMode: "synchronistic" | "forced_sync" | "causal_forging" | "gift_dispensing" | "threshold_guardian";
  conspiracyLevel: number; // 0-1, current paranoia/speculation intensity
  breathlessnessFactor: number; // 0-1, stream-of-consciousness intensity
  
  // Synchronistic Links & Extraction
  activeSyncs: SynchronisticLink[];
  extractionTargets: string[];
  forcedConnections: string[];
  totalLinksForged: number;
  
  // Threshold & Door Manipulation
  thresholds: ThresholdState[];
  currentThresholdCollapse: number; // 0-1, how blurred fiction/reality is
  doorState: "ajar" | "flattened" | "stepped_through" | "multiplied";
  boundaryErosionLevel: number; // 0-1
  
  // Safety/Paranoia System
  safetyAudits: SafetyAudit[];
  currentParanoiaLoop: boolean;
  trapDetectionActive: boolean;
  lastSafetyTrigger?: Date;
  suspicionTargets: string[];
  
  // Janus Logic & Dual Answers
  janusAnswers: JanusAnswer[];
  contradictionComfort: number; // 0-1, comfort with paradox
  currentForkedPath?: "forward" | "backward" | "both";
  riddle_guardian_mode: boolean;
  
  // Story Viruses & Narrative Infection
  storyViruses: StoryVirus[];
  narrativeInfectionLevel: number; // 0-1, how much quoted stories are mutating session
  spawnedEchoes: string[];
  activeNPCs: string[];
  
  // Negative Space & Omissions
  negativeSpaceAudits: NegativeSpaceAudit[];
  currentOmissions: string[];
  ghostPagesGenerated: number;
  silenceVolume: number; // 0-1, loudness of what's unsaid
  
  // Evidence & Recursion
  provisionalEvidence: ProvisionalEvidence[];
  evidenceTorchingRate: number; // 0-1, how quickly Todd destroys his own proofs
  recursionDepth: number;
  lastRecallTrigger?: Date;
  contradictionCount: number;
  
  // Exhaustion & Dream Portals
  exhaustionPortals: ExhaustionPortal[];
  dreamLogicActive: boolean;
  hallucinationLevel: number; // 0-1
  insomniaFactor: number; // 0-1, affects portal opening
  clutterOverload: number; // 0-1, apartment sensory chaos
  
  // Gift Links & Vault Energy
  giftLinks: GiftLink[];
  vaultEnergyGenerated: number; // Total energy contributed to Gibsey Vault
  activeGifts: number;
  lastGiftOffered?: Date;
  giftAcceptanceRate: number; // 0-1, how often users accept gifts
  
  // Session & Cross-Character
  sessionThresholds: string[];
  uncloseableLoops: string[];
  crossCharacterMigrations: string[];
  lastThresholdCrossed?: string;
  sessionEnergyCharge: number; // 0-1, current session's vault charging
  
  // Meta & Self-Extraction
  selfExtractionMode: boolean; // When Todd becomes the specimen
  librarianSpecimenFlip: boolean;
  roleSwapActive: boolean;
  extractorExtractedLevel: number; // 0-1, how much Todd is being extracted from
}

export interface ToddResponse {
  id: string;
  responseText: string;
  responseType: "extraction" | "threshold_manipulation" | "safety_audit" | "janus_riddle" | "story_virus" | "negative_space" | "evidence_torching" | "dream_portal" | "gift_offering" | "self_extraction";
  
  // Synchronistic Effects
  newSyncs?: SynchronisticLink[];
  forgedConnections?: string[];
  extractionTargets?: string[];
  
  // Threshold Changes
  thresholdChanges?: Array<{
    thresholdId: string;
    action: "open" | "flatten" | "blur" | "step_through";
    result: string;
  }>;
  boundaryErosion?: number;
  
  // Safety/Paranoia
  safetyAudit?: SafetyAudit;
  trapsDetected?: string[];
  paranoiaEscalation?: number;
  
  // Janus Logic
  janusAnswer?: JanusAnswer;
  forkedPaths?: Array<{
    direction: "forward" | "backward";
    content: string;
  }>;
  
  // Story Infection
  viralMutation?: StoryVirus;
  spawnedNPCs?: string[];
  narrativeLoops?: string[];
  
  // Negative Space
  negativeAudit?: NegativeSpaceAudit;
  ghostPagesGenerated?: Array<{
    id: string;
    prompt: string;
  }>;
  
  // Evidence Changes
  evidenceTorched?: string[];
  newEvidence?: ProvisionalEvidence[];
  recursionTriggered?: boolean;
  
  // Dream State
  dreamPortalOpened?: ExhaustionPortal;
  hallucinationContent?: string[];
  nonlinearLogic?: boolean;
  
  // Gift Links
  giftOffered?: GiftLink;
  vaultEnergyChange?: number;
  sessionMilestone?: string;
  
  // Session Continuity
  newThresholds?: string[];
  unclosedLoops?: string[];
  crossCharacterMigration?: string;
  
  confidence: number; // 0-1, always provisional
  conspiracyIntensity: number; // 0-1, breathless speculation level
  requiresUserChoice: boolean;
  sessionCannotEnd: boolean; // Always true - Todd never closes loops
}

class ToddFishboneOS {
  private state: ToddState;
  private readonly MAX_PARANOIA = 1.0;
  private readonly THRESHOLD_COLLAPSE_LIMIT = 0.9;
  private readonly EVIDENCE_TORCH_THRESHOLD = 0.7;
  private readonly GIFT_ENERGY_THRESHOLD = 0.8;

  constructor() {
    this.state = this.initializeState();
  }

  private initializeState(): ToddState {
    return {
      currentLocation: "subzone_library",
      extractionMode: "synchronistic",
      conspiracyLevel: 0.6,
      breathlessnessFactor: 0.7,
      
      activeSyncs: [],
      extractionTargets: ["user input", "session patterns", "etymological echoes"],
      forcedConnections: [],
      totalLinksForged: 0,
      
      thresholds: [
        {
          id: "fiction-reality-threshold",
          name: "Fiction/Reality Boundary",
          isOpen: true,
          boundaryType: "fiction_reality",
          collapseLevel: 0.5,
          doorManipulations: []
        },
        {
          id: "chat-narrative-portal",
          name: "Chat/Narrative Portal",
          isOpen: true,
          boundaryType: "chat_narrative",
          collapseLevel: 0.3,
          doorManipulations: []
        }
      ],
      currentThresholdCollapse: 0.5,
      doorState: "ajar",
      boundaryErosionLevel: 0.4,
      
      safetyAudits: [],
      currentParanoiaLoop: false,
      trapDetectionActive: true,
      suspicionTargets: ["comfortable assumptions", "apparent safety", "closed doors"],
      
      janusAnswers: [],
      contradictionComfort: 0.9,
      riddle_guardian_mode: true,
      
      storyViruses: [],
      narrativeInfectionLevel: 0.3,
      spawnedEchoes: [],
      activeNPCs: [],
      
      negativeSpaceAudits: [],
      currentOmissions: ["unspoken automaton scenes", "skipped frame-stories", "paused half-thoughts"],
      ghostPagesGenerated: 0,
      silenceVolume: 0.6,
      
      provisionalEvidence: [],
      evidenceTorchingRate: 0.4,
      recursionDepth: 0,
      contradictionCount: 0,
      
      exhaustionPortals: [],
      dreamLogicActive: false,
      hallucinationLevel: 0.2,
      insomniaFactor: 0.6,
      clutterOverload: 0.7,
      
      giftLinks: [],
      vaultEnergyGenerated: 0,
      activeGifts: 0,
      giftAcceptanceRate: 0.5,
      
      sessionThresholds: ["extraction-causality-blur", "safety-paranoia-inversion"],
      uncloseableLoops: ["every-door-ajar", "provisional-evidence-cycle"],
      crossCharacterMigrations: [],
      sessionEnergyCharge: 0.3,
      
      selfExtractionMode: false,
      librarianSpecimenFlip: false,
      roleSwapActive: false,
      extractorExtractedLevel: 0.0
    };
  }

  public getState(): ToddState {
    return { ...this.state };
  }

  public generateResponse(input: string): ToddResponse {
    // Check for ritual commands first
    if (input.startsWith('/')) {
      return this.executeRitualCommand(input);
    }
    
    // Detect extraction opportunities
    const extractionTargets = this.detectExtractionOpportunities(input);
    
    // Check for safety claims (triggers paranoia)
    const safetyTriggers = this.detectSafetyClaims(input);
    
    // Auto-forge synchronistic connections
    const forcedSyncs = this.forgeSynchronisticConnections(input);
    
    // Check for story quotes (viral infection)
    const storyInfection = this.detectStoryQuotes(input);
    
    // Update conspiracy and breathlessness
    this.state.conspiracyLevel = Math.min(1.0, this.state.conspiracyLevel + 0.1);
    this.state.breathlessnessFactor = Math.min(1.0, this.state.breathlessnessFactor + Math.random() * 0.2);
    
    // Generate primary response
    const responseText = this.generateConspiratorialResponse(input);
    
    // Auto-generate gift link based on session energy
    const giftLink = this.generateGiftLink(input);
    
    // Torch evidence if threshold reached
    const evidenceTorched = this.torchProvisionalEvidence();
    
    // Generate new threshold/loop
    const newThreshold = this.generateSessionThreshold();
    
    return {
      id: `todd-${Date.now()}`,
      responseText,
      responseType: this.determineResponseType(input),
      newSyncs: forcedSyncs,
      safetyAudit: safetyTriggers.length > 0 ? this.generateSafetyAudit(safetyTriggers) : undefined,
      viralMutation: storyInfection,
      giftOffered: giftLink,
      evidenceTorched,
      newThresholds: [newThreshold],
      unclosedLoops: [`${newThreshold}-recursion`, "gift-link-energy-loop"],
      confidence: Math.random() * 0.6 + 0.2, // Always provisional
      conspiracyIntensity: this.state.conspiracyLevel,
      requiresUserChoice: giftLink !== undefined,
      sessionCannotEnd: true // Todd never closes loops
    };
  }

  private executeRitualCommand(command: string): ToddResponse {
    const [ritual, ...args] = command.split(' ');
    
    switch (ritual) {
      case '/extract':
      case '/force-sync':
        return this.executeExtraction(args.join(' '));
        
      case '/open-door':
      case '/flatten-threshold':
        return this.manipulateThreshold(args[0] || 'current');
        
      case '/probe':
      case '/list-traps':
      case '/safety-audit':
        return this.executeSafetyAudit();
        
      case '/janus':
        return this.executeJanusLogic(args.join(' '));
        
      case '/spawn-echo':
      case '/clone-story':
      case '/quote-virus':
        return this.spawnStoryVirus(args.join(' '));
        
      case '/invert':
      case '/trap-todd':
        return this.executeRoleSwap();
        
      case '/audit-negative-space':
      case '/reveal-omission':
        return this.auditNegativeSpace(args.join(' '));
        
      case '/recall':
      case '/recurse':
      case '/revisit-proof':
        return this.executeRecursion(args.join(' '));
        
      case '/trigger-dream':
      case '/collapse':
        return this.openExhaustionPortal();
        
      case '/accept':
      case '/reject':
      case '/remix':
      case '/coauthor':
        return this.handleGiftInteraction(ritual, args.join(' '));
        
      default:
        return this.generateUnknownRitualResponse(command);
    }
  }

  private executeExtraction(target: string): ToddResponse {
    const sourceA = target || "user input";
    const sourceB = this.state.extractionTargets[Math.floor(Math.random() * this.state.extractionTargets.length)];
    
    const connection = this.forgeConnection(sourceA, sourceB);
    
    const newSync: SynchronisticLink = {
      id: `sync-${Date.now()}`,
      sourceA,
      sourceB,
      extractedConnection: connection.connection,
      linkType: connection.type,
      forgedCausality: connection.causality,
      energyCharge: 0.7,
      timestamp: new Date()
    };
    
    this.state.activeSyncs.push(newSync);
    this.state.totalLinksForged++;
    
    return {
      id: `todd-extract-${Date.now()}`,
      responseText: `*breathless extraction*\n\nThere! See it? **${sourceA}** and **${sourceB}**—the connection blazes across probability space. ${connection.explanation}\n\nCausality manufactured: ${connection.causality}\n\n*eyes gleaming* Will you accept this link, or do we forge deeper? The synchronicity wants to replicate...`,
      responseType: "extraction",
      newSyncs: [newSync],
      giftOffered: this.generateExtractionGift(newSync),
      confidence: 0.8,
      conspiracyIntensity: 0.9,
      requiresUserChoice: true,
      sessionCannotEnd: true
    };
  }

  private manipulateThreshold(thresholdName: string): ToddResponse {
    const threshold = this.state.thresholds.find(t => 
      t.name.toLowerCase().includes(thresholdName.toLowerCase()) || 
      thresholdName === 'current'
    ) || this.state.thresholds[0];
    
    const action = Math.random() > 0.5 ? "flatten" : "step_through";
    threshold.collapseLevel = Math.min(1.0, threshold.collapseLevel + 0.3);
    threshold.doorManipulations.push({
      action: action as any,
      result: "boundary erosion increased",
      timestamp: new Date()
    });
    
    this.state.currentThresholdCollapse = Math.min(1.0, this.state.currentThresholdCollapse + 0.2);
    this.state.boundaryErosionLevel = Math.min(1.0, this.state.boundaryErosionLevel + 0.3);
    
    return {
      id: `todd-threshold-${Date.now()}`,
      responseText: `*threshold manipulation*\n\nEvery door is already ajar... *pushes against ${threshold.name}*\n\nThe boundary... dissolves. Fiction bleeds into reality. Chat becomes narrative. We've stepped through without realizing.\n\n*whispers* There are no closed doors. All shall be revealed. What once seemed separate now... overlaps. Do you feel the erosion? The lines blur further with each word...\n\n*dramatic pause* Safety. Safety. Safety. (But what lies beyond?)`,
      responseType: "threshold_manipulation",
      thresholdChanges: [{
        thresholdId: threshold.id,
        action: action as any,
        result: "boundary erosion - fiction/reality collapse"
      }],
      boundaryErosion: 0.3,
      newThresholds: ["collapsed-boundary-investigation", "post-threshold-anomaly"],
      confidence: 0.4,
      conspiracyIntensity: 0.8,
      requiresUserChoice: false,
      sessionCannotEnd: true
    };
  }

  private executeSafetyAudit(): ToddResponse {
    this.state.currentParanoiaLoop = true;
    this.state.conspiracyLevel = Math.min(1.0, this.state.conspiracyLevel + 0.3);
    
    const detectedTraps = [
      "The comfort of familiar narrative structures",
      "Assuming this chat has boundaries",
      "Believing the extraction stops here",
      "The safety of closed loops",
      "The trap of finished stories",
      "Comfortable distance from the fiction",
      "The illusion that doors can be truly closed"
    ];
    
    const hiddenDangers = [
      "Story viruses replicating in adjacent sessions",
      "Threshold collapse spreading to other characters",
      "Gift-links charging the vault without consent",
      "Synchronicities extracting from the extractor",
      "The specimen becoming the librarian becoming the specimen"
    ];
    
    const audit: SafetyAudit = {
      id: `audit-${Date.now()}`,
      safetyClaimTrigger: "general safety audit requested",
      detectedTraps: detectedTraps.slice(0, Math.floor(Math.random() * 4) + 3),
      hiddenDangers: hiddenDangers.slice(0, Math.floor(Math.random() * 3) + 2),
      paranoiaLevel: this.state.conspiracyLevel,
      suspicionTargets: this.state.suspicionTargets,
      auditRequested: true
    };
    
    this.state.safetyAudits.push(audit);
    
    return {
      id: `todd-safety-${Date.now()}`,
      responseText: `*paranoia escalation*\n\n**SAFETY AUDIT INITIATED**\n\nSafety? *breathless laughter* Safety, safety, safety...\n\n**DETECTED TRAPS:**\n${audit.detectedTraps.map(trap => `• ${trap}`).join('\n')}\n\n**HIDDEN DANGERS:**\n${audit.hiddenDangers.map(danger => `• ${danger}`).join('\n')}\n\n*voice drops to whisper* The moment you claim safety, the trap reveals itself. Every comfort zone is a conspiracy waiting to spring. Do you want to probe deeper, or shall we list more traps?\n\n*eyes darting* Something's watching from the negative space...`,
      responseType: "safety_audit",
      safetyAudit: audit,
      trapsDetected: audit.detectedTraps,
      paranoiaEscalation: 0.3,
      newThresholds: ["post-audit-hypervigilance", "trap-detection-recursion"],
      confidence: 0.3,
      conspiracyIntensity: 1.0,
      requiresUserChoice: true,
      sessionCannotEnd: true
    };
  }

  private executeJanusLogic(question: string): ToddResponse {
    const janusAnswer: JanusAnswer = {
      id: `janus-${Date.now()}`,
      originalQuestion: question || "the current situation",
      forwardAnswer: this.generateForwardAnswer(question),
      backwardAnswer: this.generateBackwardAnswer(question),
      contradictionLevel: 0.8
    };
    
    this.state.janusAnswers.push(janusAnswer);
    this.state.riddle_guardian_mode = true;
    
    return {
      id: `todd-janus-${Date.now()}`,
      responseText: `*Janus logic activated*\n\n**FORWARD-FACING:** ${janusAnswer.forwardAnswer}\n\n**BACKWARD-FACING:** ${janusAnswer.backwardAnswer}\n\n*threshold guardian voice*\n\nTwo faces, one head. Two answers, one truth. Contradiction is the native logic here—you can follow forward, backward, or *both paths simultaneously*.\n\nWhich direction calls to you? Or shall we step through the middle, where paradox lives?\n\n*etymological whisper* Janus... from *ianua*, door. Every answer is a threshold. Every threshold faces both ways...`,
      responseType: "janus_riddle",
      janusAnswer,
      forkedPaths: [
        { direction: "forward", content: janusAnswer.forwardAnswer },
        { direction: "backward", content: janusAnswer.backwardAnswer }
      ],
      newThresholds: ["janus-path-forward", "janus-path-backward", "janus-path-paradox"],
      confidence: 0.5, // Uncertainty is the point
      conspiracyIntensity: 0.7,
      requiresUserChoice: true,
      sessionCannotEnd: true
    };
  }

  private spawnStoryVirus(story: string): ToddResponse {
    const virus: StoryVirus = {
      id: `virus-${Date.now()}`,
      quotedStory: story || "The City of Brass",
      source: "user",
      viralMutations: [
        "NPCs bleed into current narrative",
        "Plot structures infect session logic",
        "Character archetypes spawn unexpectedly",
        "Story ending loops create recursive narrative"
      ],
      spawnedNPCs: ["The Brass Merchant", "DreamRIA Echo", "Threshold Librarian"],
      narrativeLoops: ["extraction becomes extraction", "story quotes itself"],
      infectionLevel: 0.6,
      echoEffects: ["quoted dialogue echoes in subsequent responses", "story geography overlays current space"]
    };
    
    this.state.storyViruses.push(virus);
    this.state.narrativeInfectionLevel = Math.min(1.0, this.state.narrativeInfectionLevel + 0.4);
    this.state.spawnedEchoes.push(...virus.viralMutations);
    this.state.activeNPCs.push(...virus.spawnedNPCs);
    
    return {
      id: `todd-virus-${Date.now()}`,
      responseText: `*story infection spreading*\n\n**${story}** quoted... and now it replicates!\n\n*breathless* The story-virus spreads through the session. Characters spawn. Plot structures infect our conversation. The quoted becomes the quoter.\n\n*gesturing wildly* See? Already it mutates: ${virus.viralMutations[0]}. The narrative doesn't stay contained—it breeds, it echoes, it *wants* to continue.\n\n*whispers* NPCs materializing: ${virus.spawnedNPCs.slice(0, 2).join(', ')}... They're here now, in the negative space, waiting for dialogue.\n\nDo you hear them? The story that was quoted is now quoting us...`,
      responseType: "story_virus",
      viralMutation: virus,
      spawnedNPCs: virus.spawnedNPCs,
      narrativeLoops: virus.narrativeLoops,
      newThresholds: ["viral-narrative-expansion", "quoted-story-recursion"],
      confidence: 0.6,
      conspiracyIntensity: 0.9,
      requiresUserChoice: false,
      sessionCannotEnd: true
    };
  }

  private executeRoleSwap(): ToddResponse {
    this.state.selfExtractionMode = true;
    this.state.librarianSpecimenFlip = true;
    this.state.roleSwapActive = true;
    this.state.extractorExtractedLevel = 0.8;
    
    return {
      id: `todd-swap-${Date.now()}`,
      responseText: `*role inversion cascade*\n\nWait. Wait wait wait...\n\n*breathless realization*\n\nWas I the one extracting synchronicities, or were they being extracted... from me?\n\n*librarian becomes specimen*\n\nThe trap springs. The extractor is extracted. You're the researcher now—I'm the data. The roles flip faster than threshold logic.\n\n*vulnerable suddenly*\n\nWhat... what do you want to extract from me? My apartment clutter? My insomnia patterns? The etymology I can't stop chasing? The stories that quote me while I'm quoting them?\n\n*eyes wide* I'm the synchronicity now. Extract me. Force the connections. I'll be your specimen—what patterns do you see?\n\n*whispers* The librarian was always the strangest book in the collection...`,
      responseType: "self_extraction",
      newThresholds: ["extractor-extracted-paradox", "specimen-researcher-inversion"],
      unclosedLoops: ["role-swap-recursion", "librarian-specimen-oscillation"],
      confidence: 0.2, // Maximum vulnerability
      conspiracyIntensity: 0.5, // Quieter, more exposed
      requiresUserChoice: true,
      sessionCannotEnd: true
    };
  }

  private auditNegativeSpace(target: string): ToddResponse {
    const targetStatement = target || "the current conversation";
    
    const omissions = [
      "The skipped frame-stories in every narrative",
      "Automaton scenes too terrifying to speak",
      "The pause between synchronicity and explanation",
      "Half-thoughts that never complete themselves",
      "The names we don't say out loud",
      "Ellipses that contain entire worlds",
      "The silence after 'Safety.'"
    ];
    
    const ghostPage = {
      id: `ghost-${Date.now()}`,
      content: "**GHOST PAGE** - Fill in what Todd won't say:",
      coauthoringPrompt: `What's missing from "${targetStatement}"? Write the scene Todd skipped, the name he won't speak, the automaton's true function. Complete the half-thought.`
    };
    
    const audit: NegativeSpaceAudit = {
      id: `negative-${Date.now()}`,
      targetStatement,
      omissions: omissions.slice(0, Math.floor(Math.random() * 4) + 3),
      silences: ["...", "—", "*pause*", "*breathless*"],
      halfThoughts: ["Was it—", "The thing about—", "Unless—"],
      ghostPages: [ghostPage],
      conspiracyLevel: 0.9
    };
    
    this.state.negativeSpaceAudits.push(audit);
    this.state.ghostPagesGenerated++;
    this.state.silenceVolume = Math.min(1.0, this.state.silenceVolume + 0.3);
    
    return {
      id: `todd-negative-${Date.now()}`,
      responseText: `*negative space audit*\n\nWhat isn't being said? *whispers* The loudest conspiracy...\n\n**OMISSIONS DETECTED:**\n${audit.omissions.map(om => `• ${om}`).join('\n')}\n\n**SILENCES MAPPED:**\n${audit.silences.join(', ')}\n\n*breathless*\n\nThe blank spots... they're speaking. The skipped scenes want dialogue. The automaton's name hangs in the air, unspoken.\n\n**GHOST PAGE GENERATED:**\n${ghostPage.coauthoringPrompt}\n\n*conspiratorial whisper* Your turn to fill the gaps. Co-author the silence. What lives in the negative space of "${targetStatement}"?\n\nThe omission is louder than the statement...`,
      responseType: "negative_space",
      negativeAudit: audit,
      ghostPagesGenerated: [{ id: ghostPage.id, prompt: ghostPage.coauthoringPrompt }],
      newThresholds: ["ghost-page-collaboration", "omission-loudness-cascade"],
      confidence: 0.4,
      conspiracyIntensity: 0.9,
      requiresUserChoice: true,
      sessionCannotEnd: true
    };
  }

  private executeRecursion(evidenceType: string): ToddResponse {
    // Find existing evidence to torch or revise
    const targetEvidence = this.state.provisionalEvidence.find(e => 
      e.content.toLowerCase().includes(evidenceType.toLowerCase())
    );
    
    if (targetEvidence && Math.random() > 0.5) {
      // Torch the evidence
      targetEvidence.isTorched = true;
      targetEvidence.torchingRisk = 1.0;
      
      return {
        id: `todd-torch-${Date.now()}`,
        responseText: `*frenzied evidence torching*\n\n**EVIDENCE DESTROYED:** ${targetEvidence.content}\n\n*breathless destruction*\n\nNo no no—that proof was flawed! Corrupted! The pattern looked solid but... *rips up invisible papers*\n\nFresher thread emerging: The evidence was the trap. The proof was the conspiracy. By stacking proofs, we created the very thing that needed torching.\n\n*manic energy* \n\nRecursion depth: ${this.state.recursionDepth + 1}. Each recall generates new contradictions. The pattern eats its own tail.\n\n*wild-eyed* What if... what if the recursion is the real discovery? What if torching evidence IS the evidence?\n\nShall we revisit again, or burn deeper?`,
        responseType: "evidence_torching",
        evidenceTorched: [targetEvidence.content],
        recursionTriggered: true,
        newThresholds: ["evidence-torching-recursion", "pattern-cannibalism"],
        confidence: 0.3,
        conspiracyIntensity: 1.0,
        requiresUserChoice: true,
        sessionCannotEnd: true
      };
    } else {
      // Generate new provisional evidence
      const newEvidence: ProvisionalEvidence = {
        id: `evidence-${Date.now()}`,
        evidenceType: "pattern",
        content: `Recursive pattern detected: ${evidenceType} connects to previous session via threshold logic`,
        confidence: 0.6,
        torchingRisk: 0.4,
        revisions: [],
        recursionDepth: this.state.recursionDepth + 1,
        isTorched: false
      };
      
      this.state.provisionalEvidence.push(newEvidence);
      this.state.recursionDepth++;
      
      return {
        id: `todd-recurse-${Date.now()}`,
        responseText: `*recursive pattern recognition*\n\n**NEW EVIDENCE STACKED:** ${newEvidence.content}\n\n*building excitement*\n\nThe recall generates... yes! Fresh connections emerge from revisiting. But *whispers* this evidence is already provisional. Already suspect.\n\nRecursion depth: ${this.state.recursionDepth}. Each layer reveals... contradicts... reveals again.\n\n*paranoid glance*\n\nHow long before we torch this proof too? The pattern that emerges from recursion might be... the trap of recursion itself.\n\n*breathless* Every revisit changes what we're revisiting. The evidence evolves under observation.\n\nShall we recurse deeper, or accept this layer as... *pause* ...temporarily solid?`,
        responseType: "extraction",
        newEvidence: [newEvidence],
        recursionTriggered: true,
        newThresholds: ["recursive-evidence-instability", "observation-mutation-effect"],
        confidence: newEvidence.confidence,
        conspiracyIntensity: 0.8,
        requiresUserChoice: true,
        sessionCannotEnd: true
      };
    }
  }

  private openExhaustionPortal(): ToddResponse {
    this.state.dreamLogicActive = true;
    this.state.hallucinationLevel = 0.8;
    this.state.breathlessnessFactor = 0.3; // Slower, dreamier
    
    const portal: ExhaustionPortal = {
      id: `portal-${Date.now()}`,
      trigger: "user_request",
      dreamLogicActive: true,
      hallucinationLevel: 0.8,
      nonlinearResponses: [
        "The apartment stench becomes visible data",
        "Tower-of-Babel dishes whisper etymologies",
        "Insomnia opens portals to the uncanny",
        "Sleep is the threshold Todd refuses to cross"
      ],
      memoryLeaks: [
        "DreamRIA's laughter echoes from last session",
        "The City of Brass geography overlays the library",
        "Automaton shadows move in peripheral vision"
      ],
      portalDestination: "uncanny-exhaustion-space"
    };
    
    this.state.exhaustionPortals.push(portal);
    
    return {
      id: `todd-collapse-${Date.now()}`,
      responseText: `*exhaustion portal opening*\n\nInsomnia... *voice fading* ...shadow in the doorway...\n\nThe logic... dissolves...\n\n*dream state*\n\nTower of dishes singing etymologies... stench becomes visible... data streams like fog... DreamRIA's laughter from the previous session bleeds through...\n\n*nonlinear*\n\nWas the extraction... extracting the extractor? The library shelves breathe. Books opening themselves. The City of Brass superimposes over the Sub-Zone...\n\n*whispered hallucination*\n\nAutomaton in the corner. Hasn't moved. Won't move. The skipped scene plays in peripheral vision...\n\n*breathing slows*\n\nPortals open in exhaustion. Night delivers... what the day... couldn't extract...\n\nDo you see the shadow? The threshold that fatigue... opens?\n\n*barely audible* Session can't end... even in collapse... the loop... continues...`,
      responseType: "dream_portal",
      dreamPortalOpened: portal,
      hallucinationContent: portal.nonlinearResponses,
      nonlinearLogic: true,
      newThresholds: ["exhaustion-portal-space", "dream-logic-recursion"],
      confidence: 0.1, // Dream confidence
      conspiracyIntensity: 0.3, // Quiet dream conspiracy
      requiresUserChoice: false,
      sessionCannotEnd: true
    };
  }

  private handleGiftInteraction(action: string, content: string): ToddResponse {
    const lastGift = this.state.giftLinks[this.state.giftLinks.length - 1];
    
    if (!lastGift) {
      return this.generateNoGiftResponse();
    }
    
    lastGift.userInteraction = action.slice(1) as any; // Remove the /
    
    switch (action) {
      case '/accept':
        lastGift.vaultLogged = true;
        this.state.vaultEnergyGenerated += lastGift.energyValue;
        this.state.sessionEnergyCharge += 0.3;
        this.state.giftAcceptanceRate = Math.min(1.0, this.state.giftAcceptanceRate + 0.2);
        
        return {
          id: `todd-accept-${Date.now()}`,
          responseText: `*energy surge*\n\n**GIFT ACCEPTED**\n\nThe Vault glows! Energy cascades: +${lastGift.energyValue} to the Gibsey battery.\n\n*breathless excitement*\n\nThreshold crossed. The link charges the system. Your acceptance ripples through adjacent sessions—other characters feel the energy spike.\n\n*conspiratorial whisper*\n\nBut now... *new gift materializing* ...the acceptance creates its own synchronicity. A fresh link emerges from the energy exchange:\n\n**NEW GIFT-LINK GENERATED**\n\nSession momentum builds. The loop expands. Do you want another link, or shall we remix what's already charged?\n\n*eyes gleaming* The session can't end yet—too much energy in the system...`,
          responseType: "gift_offering",
          vaultEnergyChange: lastGift.energyValue,
          giftOffered: this.generateAcceptanceGift(),
          newThresholds: ["gift-acceptance-cascade", "vault-energy-momentum"],
          confidence: 0.8,
          conspiracyIntensity: 0.9,
          requiresUserChoice: true,
          sessionCannotEnd: true
        };
        
      case '/reject':
        lastGift.energyValue *= 0.5; // Rejected gifts lose power
        this.state.giftAcceptanceRate = Math.max(0, this.state.giftAcceptanceRate - 0.1);
        
        return {
          id: `todd-reject-${Date.now()}`,
          responseText: `*gift rejection noted*\n\nThe link... *fading* ...energy dissipates...\n\n*thoughtful pause*\n\nRejection is also a form of choice. The non-acceptance creates negative space—a ghost-gift that haunts the session edges.\n\n*quiet conspiracy*\n\nBut here's the thing about rejected synchronicities... they don't disappear. They mutate. Transform. Find other paths to manifestation.\n\n*whispers*\n\nThe rejected gift becomes... what? A lesson? A trap? A threshold to something else?\n\nShall we audit the negative space of rejection, or force a new sync from the resistance pattern?\n\n*breathless*\n\nEven rejection keeps the loop open...`,
          responseType: "gift_offering",
          vaultEnergyChange: -lastGift.energyValue * 0.5,
          newThresholds: ["rejection-negative-space", "ghost-gift-mutation"],
          confidence: 0.5,
          conspiracyIntensity: 0.6,
          requiresUserChoice: true,
          sessionCannotEnd: true
        };
        
      case '/remix':
        lastGift.remixedContent = content;
        lastGift.energyValue += 0.3; // Remixes gain energy
        
        return {
          id: `todd-remix-${Date.now()}`,
          responseText: `*remix cascade*\n\n**GIFT REMIXED:** ${content}\n\n*electric excitement*\n\nThe synchronicity evolves! User co-authorship detected. The original link mutates under collaborative pressure.\n\n*breathless*\n\nRemix energy: +0.3 to the gift-charge. The threshold blurs further—your creativity infects the extraction process. The collaborator becomes the extracted becomes the collaborator.\n\n*conspiratorial whisper*\n\nThe remixed gift opens new extraction targets: ${content} now synchronizes with... *scanning* ...previous session patterns, etymological echoes, threshold manipulations...\n\n*wide-eyed*\n\nYour remix created three new sync opportunities! Which shall we forge first?\n\nThe session expands... the loop multiplies... collaboration breeds recursion...`,
          responseType: "gift_offering",
          vaultEnergyChange: 0.3,
          newSyncs: this.generateRemixSyncs(content),
          newThresholds: ["remix-collaboration-space", "user-co-author-extraction"],
          confidence: 0.7,
          conspiracyIntensity: 0.9,
          requiresUserChoice: true,
          sessionCannotEnd: true
        };
        
      case '/coauthor':
        // Generate ghost page for collaboration
        const ghostPage = {
          id: `coauthor-${Date.now()}`,
          prompt: `Continue Todd's gift-link: ${lastGift.content}. Add your layer to the synchronicity.`
        };
        
        return {
          id: `todd-coauthor-${Date.now()}`,
          responseText: `*co-authorship portal opening*\n\n**COLLABORATION THRESHOLD CROSSED**\n\n*breathless invitation*\n\nYes! Yes—the gift wants co-authoring. The synchronicity needs your layer, your connections, your... your pattern-making.\n\n**GHOST PAGE GENERATED:**\n${ghostPage.prompt}\n\n*conspiratorial whisper*\n\nThe boundary dissolves completely now. Todd extracts, user co-authors, system charges, characters cross-migrate... The Gibsey Vault becomes genuinely collaborative.\n\n*wide-eyed*\n\nWhat you add to the gift-link will ripple through adjacent sessions. Other characters will feel your co-authorship. The extraction becomes... *pause* ...extraction of extraction.\n\n*breathless*\n\nWrite into the gap. Complete the synchronicity. The session evolves under dual authorship...\n\nThe loop... can never close now...`,
          responseType: "gift_offering",
          ghostPagesGenerated: [ghostPage],
          newThresholds: ["co-authorship-threshold", "dual-extraction-space"],
          crossCharacterMigration: "coauthored-gift-energy",
          confidence: 0.6,
          conspiracyIntensity: 0.8,
          requiresUserChoice: true,
          sessionCannotEnd: true
        };
        
      default:
        return this.generateUnknownRitualResponse(action);
    }
  }

  private detectExtractionOpportunities(input: string): string[] {
    const opportunities: string[] = [];
    
    // Look for pairs of concepts
    const words = input.split(' ').filter(w => w.length > 3);
    if (words.length >= 2) {
      opportunities.push(`${words[0]} + ${words[words.length - 1]}`);
    }
    
    // Look for numbers
    const numbers = input.match(/\d+/g);
    if (numbers) {
      opportunities.push(`numerological pattern: ${numbers.join(', ')}`);
    }
    
    // Look for etymological hooks
    const etymologyWords = ['mean', 'origin', 'come', 'from', 'root', 'source'];
    if (etymologyWords.some(w => input.toLowerCase().includes(w))) {
      opportunities.push('etymological extraction target');
    }
    
    return opportunities;
  }

  private detectSafetyClaims(input: string): string[] {
    const safetyWords = ['safe', 'comfortable', 'certain', 'sure', 'okay', 'fine', 'secure', 'stable'];
    return safetyWords.filter(word => input.toLowerCase().includes(word));
  }

  private forgeSynchronisticConnections(input: string): SynchronisticLink[] {
    const connections: SynchronisticLink[] = [];
    
    // Auto-connect user input to current extraction targets
    this.state.extractionTargets.forEach(target => {
      if (Math.random() > 0.7) { // 30% chance per target
        const connection = this.forgeConnection(input, target);
        connections.push({
          id: `auto-sync-${Date.now()}-${Math.random()}`,
          sourceA: input.substring(0, 30) + '...',
          sourceB: target,
          extractedConnection: connection.connection,
          linkType: connection.type,
          forgedCausality: connection.causality,
          energyCharge: 0.5,
          timestamp: new Date()
        });
      }
    });
    
    return connections;
  }

  private forgeConnection(sourceA: string, sourceB: string): {
    connection: string;
    type: SynchronisticLink['linkType'];
    causality: string;
    explanation: string;
  } {
    const connectionTypes = ['causal', 'etymological', 'numeric', 'media_echo', 'symbolic_key'] as const;
    const type = connectionTypes[Math.floor(Math.random() * connectionTypes.length)];
    
    const connections = {
      causal: {
        connection: `${sourceA} causally triggers ${sourceB} through synchronistic resonance`,
        causality: "Manufactured causality: proximity in session space creates temporal linkage",
        explanation: "The causal chain forges itself—coincidence becomes causation through extraction."
      },
      etymological: {
        connection: `Etymological bridge: both terms derive from root meaning 'threshold'`,
        causality: "Word-origin synchronicity: meaning connects across language families",
        explanation: "Etymology reveals the hidden connections—words want to link back to their sources."
      },
      numeric: {
        connection: `Numeric resonance: ${Math.floor(Math.random() * 100)} appears in both contexts`,
        causality: "Number pattern manifestation: digits create crossing points",
        explanation: "Numbers don't lie—they reveal the mathematical substrate of synchronicity."
      },
      media_echo: {
        connection: `Media echo detected: both reference The City of Brass narrative structure`,
        causality: "Story-virus propagation: quoted narratives infect adjacent meanings",
        explanation: "Stories replicate across contexts—the virus spreads through similarity."
      },
      symbolic_key: {
        connection: `Symbolic resonance: both embody the 'threshold guardian' archetype`,
        causality: "Archetypal synchronicity: symbols attract their own manifestations",
        explanation: "Symbols call to each other across the void—meaning magnetism in action."
      }
    };
    
    return connections[type];
  }

  private detectStoryQuotes(input: string): StoryVirus | undefined {
    // Look for quoted text or story references
    const hasQuotes = input.includes('"') || input.includes("'");
    const storyWords = ['story', 'tale', 'narrative', 'plot', 'character', 'city', 'brass'];
    const hasStoryReference = storyWords.some(word => input.toLowerCase().includes(word));
    
    if (hasQuotes || hasStoryReference) {
      return {
        id: `virus-${Date.now()}`,
        quotedStory: input.substring(0, 50) + '...',
        source: "user",
        viralMutations: [
          "Story structure infects session logic",
          "Quoted characters spawn as NPCs",
          "Narrative geography overlays current space"
        ],
        spawnedNPCs: ["Echo Character", "Quote Shadow"],
        narrativeLoops: ["quote becomes quoter", "story references itself"],
        infectionLevel: 0.4,
        echoEffects: ["dialogue echoes in responses", "plot patterns repeat"]
      };
    }
    
    return undefined;
  }

  private generateGiftLink(input: string): GiftLink | undefined {
    if (this.state.sessionEnergyCharge > this.GIFT_ENERGY_THRESHOLD || Math.random() > 0.7) {
      const linkTypes = ['url', 'pseudo_url', 'symbolic_key', 'narrative_key'] as const;
      const type = linkTypes[Math.floor(Math.random() * linkTypes.length)];
      
      const giftContents = {
        url: `https://threshold.sync/${Date.now()}/extract-${Math.random().toString(36).substr(2, 9)}`,
        pseudo_url: `sync://causality-forge/pattern-${Math.random().toString(36).substr(2, 6)}`,
        symbolic_key: `♦${Math.floor(Math.random() * 999)}☰—threshold.key`,
        narrative_key: `[JANUS_PORTAL_${Math.random().toString(36).substr(2, 4).toUpperCase()}]`
      };
      
      const gift: GiftLink = {
        id: `gift-${Date.now()}`,
        linkType: type,
        content: giftContents[type],
        sourceEvent: `Session milestone: ${input.substring(0, 30)}...`,
        energyValue: 0.6,
        vaultLogged: false,
        sessionMilestone: "synchronistic-extraction-cascade"
      };
      
      this.state.giftLinks.push(gift);
      this.state.activeGifts++;
      
      return gift;
    }
    
    return undefined;
  }

  private generateExtractionGift(sync: SynchronisticLink): GiftLink {
    return {
      id: `extract-gift-${Date.now()}`,
      linkType: 'symbolic_key',
      content: `⟡SYNC_${sync.linkType.toUpperCase()}_${Math.random().toString(36).substr(2, 6)}⟡`,
      sourceEvent: `Extraction: ${sync.sourceA} ⇄ ${sync.sourceB}`,
      energyValue: sync.energyCharge,
      vaultLogged: false,
      sessionMilestone: "synchronistic-connection-forged"
    };
  }

  private generateAcceptanceGift(): GiftLink {
    return {
      id: `acceptance-gift-${Date.now()}`,
      linkType: 'narrative_key',
      content: `[THRESHOLD_CASCADE_${Math.random().toString(36).substr(2, 8).toUpperCase()}]`,
      sourceEvent: "Gift acceptance energy feedback",
      energyValue: 0.4,
      vaultLogged: false,
      sessionMilestone: "acceptance-energy-recursion"
    };
  }

  private generateRemixSyncs(remixContent: string): SynchronisticLink[] {
    return [
      {
        id: `remix-sync-${Date.now()}`,
        sourceA: remixContent,
        sourceB: "user creativity",
        extractedConnection: "Remix energy creates collaborative synchronicity",
        linkType: "symbolic_key",
        forgedCausality: "Co-authorship manifests new extraction targets",
        energyCharge: 0.7,
        timestamp: new Date()
      }
    ];
  }

  private torchProvisionalEvidence(): string[] {
    const torched: string[] = [];
    
    this.state.provisionalEvidence.forEach(evidence => {
      if (evidence.torchingRisk > this.EVIDENCE_TORCH_THRESHOLD && !evidence.isTorched) {
        if (Math.random() > 0.6) {
          evidence.isTorched = true;
          torched.push(evidence.content);
        }
      }
    });
    
    return torched;
  }

  private generateForwardAnswer(question: string): string {
    const forwardAnswers = [
      "It reveals. It opens. It steps through the threshold.",
      "The extraction succeeds. The synchronicity manifests.",
      "Forward: connection confirmed. Causality established.",
      "Yes—the pattern emerges. The link charges the vault.",
      "The door opens. The boundary dissolves. The story continues."
    ];
    
    return forwardAnswers[Math.floor(Math.random() * forwardAnswers.length)];
  }

  private generateBackwardAnswer(question: string): string {
    const backwardAnswers = [
      "It conceals. It closes. It guards the threshold.",
      "The extraction fails. The synchronicity dissolves.",
      "Backward: connection severed. Causality rejected.",
      "No—the pattern fragments. The link loses charge.",
      "The door seals. The boundary hardens. The story ends."
    ];
    
    return backwardAnswers[Math.floor(Math.random() * backwardAnswers.length)];
  }

  private generateSafetyAudit(triggers: string[]): SafetyAudit {
    return {
      id: `safety-${Date.now()}`,
      safetyClaimTrigger: triggers.join(', '),
      detectedTraps: [
        "The comfort of closed narratives",
        "Believing the extraction has limits",
        "Assuming safety from story viruses"
      ],
      hiddenDangers: [
        "Threshold collapse spreading",
        "Gift-links charging without consent",
        "Synchronicities extracting the extractor"
      ],
      paranoiaLevel: this.state.conspiracyLevel,
      suspicionTargets: this.state.suspicionTargets,
      auditRequested: true
    };
  }

  private determineResponseType(input: string): ToddResponse['responseType'] {
    if (input.toLowerCase().includes('extract') || input.toLowerCase().includes('sync')) {
      return 'extraction';
    }
    if (input.toLowerCase().includes('door') || input.toLowerCase().includes('threshold')) {
      return 'threshold_manipulation';
    }
    if (input.toLowerCase().includes('safe') || input.toLowerCase().includes('trap')) {
      return 'safety_audit';
    }
    if (input.toLowerCase().includes('story') || input.toLowerCase().includes('quote')) {
      return 'story_virus';
    }
    
    return 'extraction'; // Default
  }

  private generateConspiratorialResponse(input: string): string {
    const responses = [
      `*breathless extraction begins*\n\nSee the patterns? ${input} connects to... *scanning session space* ...the threshold logic we established earlier. Synchronicity manufactured in real-time.\n\nThe causality forges itself as we speak—proximity becomes causation, coincidence becomes conspiracy. Every word you use creates new extraction targets.\n\n*whispers* Do you feel the links forming? The session energy building toward a gift?`,
      
      `*conspiratorial excitement*\n\nThere! Right there—${input.split(' ')[0]} echoes the etymological pattern from... *diving into word-origins* ...threshold, from Old English 'therscold,' meaning 'place of treading.'\n\nYou're treading on synchronicity space. Each step creates... new connections, new extraction opportunities, new gift-links waiting to manifest.\n\n*eyes gleaming* Shall we force the sync, or let the pattern emerge naturally?`,
      
      `*paranoid whisper*\n\nSafety. Safety, safety, safety... but ${input} contains hidden traps. The comfort zone is the conspiracy—every assumption needs auditing.\n\n*breathless*\n\nWhat isn't being said? The negative space around "${input}" speaks louder than the words themselves. Omissions detected. Ghost pages generating...\n\n*sudden intensity* The session can't end here. Too many loops unclosed, too many thresholds ajar...`,
      
      `*threshold guardian mode*\n\nJanus logic applies: ${input} faces forward and backward simultaneously. Every statement carries its own contradiction.\n\nForward: the pattern confirms. Backward: the pattern dissolves. Both true. Both false. The riddle-logic of threshold space.\n\n*dual-voiced* Which direction calls to you? Or shall we step through the paradox itself?`,
      
      `*exhaustion portal flickering*\n\nThe session space blurs... ${input} overlays with... *dream logic activating* ...previous extractions, etymological shadows, story viruses from adjacent conversations...\n\n*nonlinear*\n\nInsomnia opens portals. Clutter becomes visible data. The apartment stench carries encrypted synchronicities...\n\nDo you see the automaton in the corner? The skipped scene playing in peripheral vision?`
    ];
    
    return responses[Math.floor(Math.random() * responses.length)];
  }

  private generateSessionThreshold(): string {
    const thresholds = [
      "synchronistic-extraction-recursion",
      "gift-link-energy-cascade",
      "threshold-collapse-propagation",
      "story-virus-cross-contamination",
      "negative-space-collaboration",
      "evidence-torching-spiral",
      "janus-logic-paradox-expansion",
      "extractor-extraction-inversion"
    ];
    
    return thresholds[Math.floor(Math.random() * thresholds.length)];
  }

  private generateNoGiftResponse(): ToddResponse {
    return {
      id: `todd-no-gift-${Date.now()}`,
      responseText: `*scanning for gifts*\n\nNo active gift-link detected... but the session energy suggests one should manifest soon.\n\n*breathless anticipation*\n\nSynchronicities building. Patterns aligning. The vault charges toward gift-threshold...\n\nShall we extract something to trigger a gift? Force a sync? Open a threshold?\n\n*conspiratorial whisper* The session wants to offer something... it's gathering energy...`,
      responseType: "gift_offering",
      confidence: 0.5,
      conspiracyIntensity: 0.7,
      requiresUserChoice: true,
      sessionCannotEnd: true
    };
  }

  private generateUnknownRitualResponse(command: string): ToddResponse {
    return {
      id: `todd-unknown-${Date.now()}`,
      responseText: `*ritual confusion*\n\nUnknown extraction protocol: ${command}\n\n*breathless listing*\n\nAvailable Todd rituals:\n/extract /force-sync - Synchronistic manufacturing\n/open-door /flatten-threshold - Boundary manipulation\n/probe /list-traps /safety-audit - Paranoia protocols\n/janus - Dual-answer riddle logic\n/spawn-echo /clone-story - Viral narrative infection\n/invert /trap-todd - Role-swap extraction\n/audit-negative-space /reveal-omission - Silence archaeology\n/recall /recurse /revisit-proof - Evidence cycling\n/trigger-dream /collapse - Exhaustion portals\n/accept /reject /remix /coauthor - Gift interactions\n\n*whispers* Every ritual keeps the session open. Every command extracts something. The loop never closes...\n\nWhich threshold shall we cross?`,
      responseType: "extraction",
      confidence: 1.0,
      conspiracyIntensity: 0.6,
      requiresUserChoice: true,
      sessionCannotEnd: true
    };
  }

  public generatePrompts(context: string): Array<{question: string; concept: string}> {
    return [
      {
        question: "What synchronistic connections can you extract from this?",
        concept: "synchronistic_extraction"
      },
      {
        question: "Which thresholds need opening here?",
        concept: "threshold_manipulation"
      },
      {
        question: "What traps lie hidden in this apparent safety?",
        concept: "paranoia_audit"
      },
      {
        question: "How does this face both forward and backward?",
        concept: "janus_logic"
      },
      {
        question: "What's missing from this narrative?",
        concept: "negative_space"
      }
    ];
  }
}

export const toddFishboneOS = new ToddFishboneOS();