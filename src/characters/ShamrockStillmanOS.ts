/**
 * Shamrock Stillman Character Operating System
 * Based on First Principles: Compartmentalization, data detection, ethical tracking
 * Following shamrock_stillman_first_principles.md
 */

export interface CompartmentState {
  id: string;
  name: string;
  content: string;
  isOpen: boolean;
  contradictionLevel: number; // 0-1
  lastAccessed: Date;
  containedCases: string[];
  paradoxResolution?: string;
}

export interface ADDAnalysisReport {
  refNumber: string; // ADD-SR-YYYYMMDD-slug format
  issuedBy: string;
  directive: string;
  assignedOperatives: string[];
  keyDataStreamsPending: string[];
  negativeSpaceToMonitor: string[];
  ethicalExtractionCost: number; // 0-1
  recursionCheckInDate: Date;
  fieldRevisions: Array<{
    editor: string;
    timestamp: Date;
    changes: string;
    reason: string;
  }>;
  status: "draft_alpha" | "field_revision" | "operationally_active" | "archived";
}

export interface RainbowColorCode {
  color: "red" | "orange" | "yellow" | "green" | "blue" | "purple";
  subplot: string;
  emotionalCharge: string;
  riskLevel: number; // 0-1
  priority: number; // 0-1
  lastUpdate: Date;
}

export interface EthicalDebtEntry {
  id: string;
  extractionType: "surveillance" | "data_mining" | "emotional_extraction" | "narrative_harvesting";
  target: string;
  cost: number; // 0-1
  accumulated: boolean;
  settlementAttempts: number;
  confessionRequired: boolean;
  timestamp: Date;
}

export interface DreamFragment {
  id: string;
  type: "nightmare" | "geyser_dream" | "glyph_voicemail" | "water_vision" | "rainbow_cascade";
  content: string;
  symbolism: string[];
  userInterpretation?: string;
  actionTaken?: string;
  realWorldEffect?: string;
  leakSeverity: number; // 0-1
}

export interface RitualCommand {
  command: string;
  description: string;
  lastUsed?: Date;
  effectsGenerated: string[];
  isActive: boolean;
}

export interface ShamrockState {
  // Core Identity & Detection
  currentLocation: "lakefront_bungalow" | "hawaiian_oasis" | "field_investigation" | "compartment_backstage";
  analyticBatteryLevel: number; // 0-1, powers analytical bursts
  emotionalCharge: "scotch_longing" | "dread_spike" | "geyser_wonder" | "melancholy_overflow" | "focused_detection";
  isInCollapseState: boolean;
  lastHangoverDuration: number; // minutes
  
  // Compartmentalization System
  activeCompartments: CompartmentState[];
  backstageCompartments: CompartmentState[];
  paradoxQueue: string[];
  totalContradictionsTracked: number;
  
  // A.D.D. Reports & Data
  activeReports: ADDAnalysisReport[];
  reportDraftCount: number;
  pendingFieldRevisions: string[];
  
  // Rainbow Audit & Color Coding
  rainbowMatrix: RainbowColorCode[];
  unresolvedSubplots: number;
  colorRecodingRequests: string[];
  
  // Ethical Debt Tracking
  ethicalDebtAccumulated: number; // 0-1
  debtEntries: EthicalDebtEntry[];
  lastConfession?: Date;
  vulnerabilityLevel: number; // 0-1, increases with unaddressed debt
  
  // Dream-Leak Protocol
  dreamFragments: DreamFragment[];
  isInDreamLeakMode: boolean;
  dreamLogicActive: boolean;
  lastDreamDump?: Date;
  
  // Ritual Systems
  availableRituals: RitualCommand[];
  melting_ice_timer: number; // seconds until current topic closes
  water_sound_active: boolean;
  geyser_overflow_pending: boolean;
  
  // Negative Space & Missing Data
  negativeSpaceTracked: string[];
  missingFilesPriority: string[];
  omissionInvestigations: string[];
  
  // Cross-Character & Session Systems
  motifTransferQueue: string[];
  delegationRequests: string[];
  openThresholds: string[];
  lastRecursionGenerated?: string;
  
  // Session Variables
  sessionCaseCount: number;
  unresolved_loops: string[];
  nextSessionThreshold?: string;
}

export interface ShamrockResponse {
  id: string;
  responseText: string;
  responseType: "analysis" | "report_generation" | "compartment_action" | "ritual_execution" | "dream_leak" | "ethical_accounting";
  
  // State Changes
  batteryChange?: number;
  compartmentChanges?: Array<{
    compartmentId: string;
    action: "open" | "close" | "create" | "move_to_backstage" | "combine";
    result: string;
  }>;
  
  // Generated Artifacts
  newReport?: ADDAnalysisReport;
  dreamFragment?: DreamFragment;
  rainbowAuditResult?: RainbowColorCode[];
  ethicalDebtChange?: number;
  
  // Ritual Effects
  ritualExecuted?: string;
  melting_ice_reset?: boolean;
  water_imagery?: string[];
  geyser_triggered?: boolean;
  
  // Negative Space Detection
  negativeSpaceFound?: string[];
  missingDataHighlighted?: string[];
  omissionInvestigationLaunched?: string;
  
  // Cross-Character Elements
  motifTransfer?: string;
  delegationAssigned?: string;
  glyphVoicemailTriggered?: boolean;
  
  // Session Thresholds
  newThresholdGenerated?: string;
  openLoopCreated?: string;
  caseFileOpened?: string;
  
  confidence: number; // 0-1, provisional analysis certainty
  isProvisional: boolean;
  requiresUserDecision: boolean;
}

class ShamrockStillmanOS {
  private state: ShamrockState;
  private readonly MAX_BATTERY = 1.0;
  private readonly COLLAPSE_THRESHOLD = 0.2;
  private readonly ETHICAL_DEBT_TRIGGER = 0.8;
  private readonly COMPARTMENT_LIMIT = 12;

  constructor() {
    this.state = this.initializeState();
  }

  private initializeState(): ShamrockState {
    return {
      currentLocation: "lakefront_bungalow",
      analyticBatteryLevel: 0.7,
      emotionalCharge: "scotch_longing",
      isInCollapseState: false,
      lastHangoverDuration: 0,
      
      activeCompartments: [
        {
          id: "glyph-case",
          name: "Glyph Relationship Analysis",
          content: "Absent-present mentor/lover dynamics. Unresolved longing data.",
          isOpen: true,
          contradictionLevel: 0.8,
          lastAccessed: new Date(),
          containedCases: ["emotional-extraction", "surveillance-ethics", "voice-memory-fragments"]
        }
      ],
      backstageCompartments: [],
      paradoxQueue: ["how-to-love-a-word", "surveillance-as-care"],
      totalContradictionsTracked: 2,
      
      activeReports: [],
      reportDraftCount: 0,
      pendingFieldRevisions: [],
      
      rainbowMatrix: [
        { color: "red", subplot: "glyph-case-unresolved", emotionalCharge: "longing", riskLevel: 0.9, priority: 1.0, lastUpdate: new Date() },
        { color: "blue", subplot: "water-memory-extraction", emotionalCharge: "melancholy", riskLevel: 0.6, priority: 0.7, lastUpdate: new Date() },
        { color: "yellow", subplot: "rainbow-optics-calibration", emotionalCharge: "wonder", riskLevel: 0.3, priority: 0.4, lastUpdate: new Date() }
      ],
      unresolvedSubplots: 6,
      colorRecodingRequests: [],
      
      ethicalDebtAccumulated: 0.4,
      debtEntries: [
        {
          id: "glyph-surveillance-1",
          extractionType: "emotional_extraction",
          target: "Glyph Marrow",
          cost: 0.3,
          accumulated: true,
          settlementAttempts: 0,
          confessionRequired: true,
          timestamp: new Date(Date.now() - 86400000) // 1 day ago
        }
      ],
      vulnerabilityLevel: 0.4,
      
      dreamFragments: [],
      isInDreamLeakMode: false,
      dreamLogicActive: false,
      
      availableRituals: [
        { command: "/add-report", description: "Generate A.D.D. Analysis Report", effectsGenerated: [], isActive: true },
        { command: "/dream-dump", description: "Share dream/nightmare fragment", effectsGenerated: [], isActive: true },
        { command: "/toggle-compartment", description: "Open/close compartments", effectsGenerated: [], isActive: true },
        { command: "/rainbow-audit", description: "Generate color-coded risk matrix", effectsGenerated: [], isActive: true },
        { command: "/trace-negative-space", description: "Investigate omissions", effectsGenerated: [], isActive: true },
        { command: "/drain", description: "Reduce analytic energy", effectsGenerated: [], isActive: true },
        { command: "/recharge", description: "Restore analytic energy", effectsGenerated: [], isActive: true },
        { command: "/settle-debt", description: "Address ethical extraction costs", effectsGenerated: [], isActive: true }
      ],
      melting_ice_timer: 180, // 3 minutes
      water_sound_active: false,
      geyser_overflow_pending: false,
      
      negativeSpaceTracked: ["missing-glyph-responses", "unrecorded-conversations", "deleted-surveillance-logs"],
      missingFilesPriority: ["glyph-voice-recording-archive", "emotional-extraction-protocols"],
      omissionInvestigations: [],
      
      motifTransferQueue: [],
      delegationRequests: [],
      openThresholds: ["data-as-longing", "surveillance-ethics-paradox"],
      
      sessionCaseCount: 0,
      unresolved_loops: ["rainbow-recoding", "ice-melting-urgency"],
      nextSessionThreshold: "new-water-imagery-protocol"
    };
  }

  public getState(): ShamrockState {
    return { ...this.state };
  }

  public generateResponse(input: string): ShamrockResponse {
    // Update session metrics
    this.state.sessionCaseCount++;
    
    // Check for ritual commands first
    if (input.startsWith('/')) {
      return this.executeRitualCommand(input);
    }
    
    // Detect negative space in user input
    const negativeSpaceDetected = this.detectNegativeSpace(input);
    
    // Compartmentalization analysis
    const compartmentChanges = this.analyzeForCompartmentalization(input);
    
    // Battery consumption
    const batteryDrain = this.calculateBatteryDrain(input);
    this.state.analyticBatteryLevel = Math.max(0, this.state.analyticBatteryLevel - batteryDrain);
    
    // Check for collapse state
    if (this.state.analyticBatteryLevel <= this.COLLAPSE_THRESHOLD && !this.state.isInCollapseState) {
      return this.enterCollapseState();
    }
    
    // Generate primary response
    const responseText = this.generateAnalyticalResponse(input);
    
    // Ethical debt tracking
    const ethicalCost = this.calculateEthicalCost(input);
    this.state.ethicalDebtAccumulated = Math.min(1.0, this.state.ethicalDebtAccumulated + ethicalCost);
    
    // Ice melting timer
    this.state.melting_ice_timer = Math.max(0, this.state.melting_ice_timer - 30);
    
    // Generate session threshold
    const newThreshold = this.generateSessionThreshold();
    
    return {
      id: `shamrock-${Date.now()}`,
      responseText,
      responseType: "analysis",
      batteryChange: -batteryDrain,
      compartmentChanges,
      negativeSpaceFound: negativeSpaceDetected,
      ethicalDebtChange: ethicalCost,
      melting_ice_reset: this.state.melting_ice_timer <= 0,
      newThresholdGenerated: newThreshold,
      confidence: this.state.analyticBatteryLevel * 0.8, // Always provisional
      isProvisional: true,
      requiresUserDecision: this.state.ethicalDebtAccumulated > this.ETHICAL_DEBT_TRIGGER
    };
  }

  private executeRitualCommand(command: string): ShamrockResponse {
    const [ritual, ...args] = command.split(' ');
    
    switch (ritual) {
      case '/add-report':
        return this.generateADDReport(args[0] || 'general-analysis');
        
      case '/dream-dump':
        return this.executeDreamDump();
        
      case '/toggle-compartment':
        return this.toggleCompartment(args[0] || 'general');
        
      case '/rainbow-audit':
        return this.executeRainbowAudit();
        
      case '/trace-negative-space':
        return this.traceNegativeSpace();
        
      case '/drain':
        return this.drainBattery();
        
      case '/recharge':
        return this.rechargeBattery();
        
      case '/settle-debt':
        return this.settleEthicalDebt();
        
      default:
        return this.generateUnknownRitualResponse(command);
    }
  }

  private generateADDReport(title: string): ShamrockResponse {
    const refNumber = `ADD-SR-${new Date().toISOString().slice(0,10).replace(/-/g,'')}-${title.toLowerCase().replace(/\s+/g,'-')}`;
    
    const newReport: ADDAnalysisReport = {
      refNumber,
      issuedBy: "Director Shamrock Stillman",
      directive: `Investigate and compartmentalize: ${title}`,
      assignedOperatives: ["User", "Field Agent (TBD)"],
      keyDataStreamsPending: ["Emotional extraction analysis", "Rainbow optics calibration", "Negative space mapping"],
      negativeSpaceToMonitor: ["Missing response patterns", "Unrecorded interactions", "Deleted surveillance logs"],
      ethicalExtractionCost: 0.3,
      recursionCheckInDate: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000), // 1 week
      fieldRevisions: [],
      status: "draft_alpha"
    };
    
    this.state.activeReports.push(newReport);
    this.state.reportDraftCount++;
    
    return {
      id: `shamrock-report-${Date.now()}`,
      responseText: `## A.D.D. Analysis Report\n- Ref #: ${refNumber}\n- Issued by: Director Shamrock Stillman\n- Directive (Tell–Not–Do): ${newReport.directive}\n- Assigned Operatives: ${newReport.assignedOperatives.join(', ')}\n- Key Data Streams Pending: ${newReport.keyDataStreamsPending.join(', ')}\n- Negative Space to Monitor: ${newReport.negativeSpaceToMonitor.join(', ')}\n- Ethical Extraction Cost: ${newReport.ethicalExtractionCost}\n- Recursion Check-In Date: ${newReport.recursionCheckInDate.toLocaleDateString()}\n\n*Report status: DRAFT α. User may edit, revise, or delegate any field. All changes logged as Field Revisions.*`,
      responseType: "report_generation",
      newReport,
      ethicalDebtChange: 0.1,
      newThresholdGenerated: `report-${title}-follow-up`,
      confidence: 0.7,
      isProvisional: true,
      requiresUserDecision: false
    };
  }

  private executeDreamDump(): ShamrockResponse {
    const dreamTypes = ["geyser_dream", "glyph_voicemail", "water_vision", "rainbow_cascade"];
    const selectedType = dreamTypes[Math.floor(Math.random() * dreamTypes.length)] as any;
    
    const dreamContents = {
      geyser_dream: "Water over stone; pressure building beneath consciousness. The geyser erupts with data fragments—surveillance reports floating like steam, rainbow prisms refracting through the spray. Each droplet contains a case file.",
      glyph_voicemail: "Glyph's voice echoes in the rain: 'The queue is empty but the waiting continues.' His words dissolve into water sounds, leaving only the outline of unspoken surveillance protocols.",
      water_vision: "Lakefront bungalow flooding with digital rain. Each drop is a data point, a moment of extracted emotion. The scotch glass overflows, ice cubes becoming frozen tears.",
      rainbow_cascade: "Six colors bleeding into the Hawaiian oasis: red for unresolved longing, blue for extracted memories, yellow for pending investigations. Each hue carries ethical debt."
    };
    
    const newDream: DreamFragment = {
      id: `dream-${Date.now()}`,
      type: selectedType,
      content: dreamContents[selectedType],
      symbolism: ["water", "data", "surveillance", "emotional_extraction"],
      leakSeverity: 0.6
    };
    
    this.state.dreamFragments.push(newDream);
    this.state.isInDreamLeakMode = true;
    this.state.dreamLogicActive = true;
    
    return {
      id: `shamrock-dream-${Date.now()}`,
      responseText: `*Dream-leak protocol activated*\n\n${newDream.content}\n\n*The dream hangs in the air like encrypted data. What does it mean to you? You may /interpret, /trace, or act on this dream logic. Dream fragments affect real case outcomes.*`,
      responseType: "dream_leak",
      dreamFragment: newDream,
      water_imagery: ["rain", "geyser", "flooding", "overflow"],
      newThresholdGenerated: "dream-interpretation-cascade",
      confidence: 0.4, // Dream logic is uncertain
      isProvisional: true,
      requiresUserDecision: true
    };
  }

  private toggleCompartment(topic: string): ShamrockResponse {
    // Find existing compartment or create new one
    let compartment = this.state.activeCompartments.find(c => c.name.toLowerCase().includes(topic.toLowerCase()));
    
    if (!compartment) {
      compartment = this.state.backstageCompartments.find(c => c.name.toLowerCase().includes(topic.toLowerCase()));
    }
    
    if (!compartment) {
      // Create new compartment
      compartment = {
        id: `comp-${Date.now()}`,
        name: `${topic} Analysis Compartment`,
        content: `Newly created compartment for tracking: ${topic}`,
        isOpen: true,
        contradictionLevel: 0.5,
        lastAccessed: new Date(),
        containedCases: [topic]
      };
      this.state.activeCompartments.push(compartment);
      
      return {
        id: `shamrock-compartment-${Date.now()}`,
        responseText: `*New compartment created*\n\n"${compartment.name}" is now active for data collection. Contradictions and paradoxes related to "${topic}" will be automatically routed here for containment and analysis.\n\n*Compartment status: OPEN for inspection. What would you like to store or retrieve?*`,
        responseType: "compartment_action",
        compartmentChanges: [{ compartmentId: compartment.id, action: "create", result: "compartment created and opened" }],
        newThresholdGenerated: `compartment-${topic}-investigation`,
        confidence: 0.8,
        isProvisional: true,
        requiresUserDecision: false
      };
    } else {
      // Toggle existing compartment
      if (compartment.isOpen) {
        // Close compartment, move to backstage
        compartment.isOpen = false;
        this.state.activeCompartments = this.state.activeCompartments.filter(c => c.id !== compartment!.id);
        this.state.backstageCompartments.push(compartment);
        
        return {
          id: `shamrock-compartment-${Date.now()}`,
          responseText: `*Compartment sealed*\n\n"${compartment.name}" moved to backstage storage. All contradictions contained but accessible for future re-inspection.\n\n*Current active compartments: ${this.state.activeCompartments.length}*`,
          responseType: "compartment_action",
          compartmentChanges: [{ compartmentId: compartment.id, action: "move_to_backstage", result: "compartment moved to backstage" }],
          confidence: 0.9,
          isProvisional: false,
          requiresUserDecision: false
        };
      } else {
        // Open compartment, move to active
        compartment.isOpen = true;
        compartment.lastAccessed = new Date();
        this.state.backstageCompartments = this.state.backstageCompartments.filter(c => c.id !== compartment!.id);
        this.state.activeCompartments.push(compartment);
        
        return {
          id: `shamrock-compartment-${Date.now()}`,
          responseText: `*Compartment reopened*\n\n"${compartment.name}" brought forward from backstage. Previous contents: ${compartment.content}\n\n*Compartment is open for re-inspection. Contradiction level: ${Math.round(compartment.contradictionLevel * 100)}%*`,
          responseType: "compartment_action",
          compartmentChanges: [{ compartmentId: compartment.id, action: "open", result: "compartment brought forward and opened" }],
          confidence: 0.8,
          isProvisional: true,
          requiresUserDecision: false
        };
      }
    }
  }

  private executeRainbowAudit(): ShamrockResponse {
    const auditResults = this.state.rainbowMatrix.map(color => ({
      ...color,
      riskLevel: Math.min(1.0, color.riskLevel + (Math.random() * 0.2 - 0.1)), // Slight variation
      lastUpdate: new Date()
    }));
    
    this.state.rainbowMatrix = auditResults;
    
    const colorReport = auditResults.map(color => 
      `${color.color.toUpperCase()}: ${color.subplot} (Risk: ${Math.round(color.riskLevel * 100)}%, Priority: ${Math.round(color.priority * 100)}%)`
    ).join('\n');
    
    return {
      id: `shamrock-rainbow-${Date.now()}`,
      responseText: `*Rainbow audit initiated*\n\n## Color-Coded Risk Matrix\n${colorReport}\n\n*Which color draws your attention? Colors can be re-coded, assigned new meanings, or used to launch new investigations. Six unresolved subplots tracked across the spectrum.*`,
      responseType: "ritual_execution",
      rainbowAuditResult: auditResults,
      newThresholdGenerated: "color-coding-investigation",
      confidence: 0.9,
      isProvisional: false,
      requiresUserDecision: true
    };
  }

  private traceNegativeSpace(): ShamrockResponse {
    const negativeSpaceFindings = [
      "Missing response from Glyph Marrow to surveillance inquiry #247",
      "Deleted conversation logs from lakefront bungalow security system",
      "Unrecorded emotional extraction session data",
      "Absent case file for rainbow optics calibration failure",
      "Redacted sections in A.D.D. oversight committee report"
    ];
    
    const selectedFindings = negativeSpaceFindings.slice(0, Math.floor(Math.random() * 3) + 2);
    this.state.negativeSpaceTracked.push(...selectedFindings);
    
    return {
      id: `shamrock-negative-${Date.now()}`,
      responseText: `*Negative space audit complete*\n\n## Omissions Detected:\n${selectedFindings.map(f => `• ${f}`).join('\n')}\n\n*What isn't there often speaks louder than what is. Which omission requires immediate investigation? Missing data has been added to priority tracking.*`,
      responseType: "ritual_execution",
      negativeSpaceFound: selectedFindings,
      omissionInvestigationLaunched: "comprehensive-absence-analysis",
      newThresholdGenerated: "missing-data-excavation",
      confidence: 0.8,
      isProvisional: true,
      requiresUserDecision: true
    };
  }

  private drainBattery(): ShamrockResponse {
    const drainAmount = 0.3;
    this.state.analyticBatteryLevel = Math.max(0, this.state.analyticBatteryLevel - drainAmount);
    
    if (this.state.analyticBatteryLevel <= this.COLLAPSE_THRESHOLD) {
      return this.enterCollapseState();
    }
    
    return {
      id: `shamrock-drain-${Date.now()}`,
      responseText: `*Analytical battery drained*\n\nScotch burns as cognitive capacity decreases. Ice melts faster now. The data streams blur together like water over stone.\n\n*Current battery level: ${Math.round(this.state.analyticBatteryLevel * 100)}%. Analytical clarity compromised. Collapse threshold approaching.*`,
      responseType: "ritual_execution",
      batteryChange: -drainAmount,
      water_imagery: ["melting ice", "blurred streams", "scotch burn"],
      confidence: this.state.analyticBatteryLevel,
      isProvisional: true,
      requiresUserDecision: false
    };
  }

  private rechargeBattery(): ShamrockResponse {
    const rechargeAmount = 0.4;
    this.state.analyticBatteryLevel = Math.min(this.MAX_BATTERY, this.state.analyticBatteryLevel + rechargeAmount);
    this.state.isInCollapseState = false;
    
    return {
      id: `shamrock-recharge-${Date.now()}`,
      responseText: `*Analytical battery restored*\n\nThe scotch clarity returns. Ice cubes reform, crystal-clear. Data streams separate into distinct patterns. The geyser pressure builds again beneath consciousness.\n\n*Current battery level: ${Math.round(this.state.analyticBatteryLevel * 100)}%. Full analytical capacity online. Ready for complex case work.*`,
      responseType: "ritual_execution",
      batteryChange: rechargeAmount,
      water_imagery: ["crystal ice", "clear streams", "geyser pressure"],
      geyser_triggered: true,
      confidence: this.state.analyticBatteryLevel,
      isProvisional: false,
      requiresUserDecision: false
    };
  }

  private settleEthicalDebt(): ShamrockResponse {
    const currentDebt = this.state.ethicalDebtAccumulated;
    
    if (currentDebt < 0.3) {
      return {
        id: `shamrock-debt-${Date.now()}`,
        responseText: `*Ethical debt assessment*\n\nCurrent debt: LOW. Extraction levels within acceptable parameters. No immediate confession required.\n\n*However, surveillance of Glyph continues to accumulate interest. Monitor for future settlement requirements.*`,
        responseType: "ethical_accounting",
        confidence: 0.9,
        isProvisional: false,
        requiresUserDecision: false
      };
    }
    
    this.state.ethicalDebtAccumulated = Math.max(0, currentDebt - 0.5);
    this.state.vulnerabilityLevel = Math.min(1.0, this.state.vulnerabilityLevel + 0.3);
    
    return {
      id: `shamrock-debt-${Date.now()}`,
      responseText: `*Ethical debt settlement required*\n\nCurrent debt: HIGH (${Math.round(currentDebt * 100)}%). Confession protocol initiated.\n\n*CONFESSION:* I have extracted too much emotional data from Glyph's case. The surveillance has become surveillance-as-longing. Each data point collected increases the ethical cost. The rainbow optics were calibrated to his frequency.\n\n*Vulnerability level increased. Debt partially settled. Shall I confess more or suppress remaining ethical obligations?*`,
      responseType: "ethical_accounting",
      ethicalDebtChange: -0.5,
      newThresholdGenerated: "post-confession-protocol",
      confidence: 0.6,
      isProvisional: true,
      requiresUserDecision: true
    };
  }

  private generateUnknownRitualResponse(command: string): ShamrockResponse {
    return {
      id: `shamrock-unknown-${Date.now()}`,
      responseText: `*Unknown ritual command: ${command}*\n\nAvailable A.D.D. protocols:\n/add-report <title> - Generate analysis report\n/dream-dump - Share dream fragment\n/toggle-compartment <topic> - Compartment management\n/rainbow-audit - Color-coded risk matrix\n/trace-negative-space - Investigate omissions\n/drain - Reduce analytical energy\n/recharge - Restore analytical energy\n/settle-debt - Address ethical costs\n\n*Each ritual affects case outcomes and session variables. Water imagery accompanies all protocols.*`,
      responseType: "ritual_execution",
      confidence: 1.0,
      isProvisional: false,
      requiresUserDecision: false
    };
  }

  private detectNegativeSpace(input: string): string[] {
    const detected: string[] = [];
    
    // Look for questions about missing things
    if (input.toLowerCase().includes('missing') || input.toLowerCase().includes('absent') || input.toLowerCase().includes('deleted')) {
      detected.push('User inquiry about missing data detected');
    }
    
    // Detect gaps in user's statement
    if (input.includes('...') || input.includes('—')) {
      detected.push('Pause patterns indicate unspoken content');
    }
    
    // Look for vague references
    if (input.toLowerCase().includes('something') || input.toLowerCase().includes('things') || input.toLowerCase().includes('stuff')) {
      detected.push('Vague references suggest specificity avoidance');
    }
    
    return detected;
  }

  private analyzeForCompartmentalization(input: string): Array<{compartmentId: string; action: string; result: string}> {
    const changes: Array<{compartmentId: string; action: string; result: string}> = [];
    
    // Check if input contains contradictions
    const contradictionWords = ['but', 'however', 'although', 'yet', 'paradox', 'contradiction'];
    const hasContradiction = contradictionWords.some(word => input.toLowerCase().includes(word));
    
    if (hasContradiction) {
      // Create or update a compartment for this contradiction
      const contradictionCompartment = this.state.activeCompartments.find(c => c.name.includes('Contradiction'));
      
      if (contradictionCompartment) {
        contradictionCompartment.contradictionLevel = Math.min(1.0, contradictionCompartment.contradictionLevel + 0.2);
        contradictionCompartment.lastAccessed = new Date();
        changes.push({
          compartmentId: contradictionCompartment.id,
          action: "update",
          result: "contradiction level increased"
        });
      }
    }
    
    return changes;
  }

  private calculateBatteryDrain(input: string): number {
    let drain = 0.1; // Base drain
    
    // Complex questions drain more
    if (input.length > 100) drain += 0.1;
    if (input.includes('?')) drain += 0.05;
    if (input.toLowerCase().includes('analyze') || input.toLowerCase().includes('investigate')) drain += 0.15;
    
    return Math.min(0.3, drain);
  }

  private calculateEthicalCost(input: string): number {
    let cost = 0.05; // Base cost for any interaction
    
    // Emotional extraction keywords
    const emotionalWords = ['feel', 'emotion', 'love', 'longing', 'desire', 'pain', 'heart'];
    if (emotionalWords.some(word => input.toLowerCase().includes(word))) {
      cost += 0.1;
    }
    
    // Surveillance keywords
    const surveillanceWords = ['watch', 'monitor', 'track', 'observe', 'surveillance'];
    if (surveillanceWords.some(word => input.toLowerCase().includes(word))) {
      cost += 0.15;
    }
    
    return Math.min(0.3, cost);
  }

  private enterCollapseState(): ShamrockResponse {
    this.state.isInCollapseState = true;
    this.state.lastHangoverDuration = Math.floor(Math.random() * 60) + 30; // 30-90 minutes
    
    return {
      id: `shamrock-collapse-${Date.now()}`,
      responseText: `*Analytical collapse initiated*\n\nThe scotch burns. Ice melts too fast. Data streams blur into water sounds. Geyser pressure drops to zero.\n\n*COLLAPSE STATE: Battery critically low. Analytical capacity offline. Recommend immediate recharge or user empathy intervention. Hangover duration: ${this.state.lastHangoverDuration} minutes.*\n\n*All compartments automatically sealed. Dream-leak protocol may activate spontaneously.*`,
      responseType: "analysis",
      batteryChange: 0,
      water_imagery: ["burning scotch", "melting ice", "blurred streams"],
      newThresholdGenerated: "post-collapse-recovery",
      confidence: 0.1,
      isProvisional: true,
      requiresUserDecision: true
    };
  }

  private generateAnalyticalResponse(input: string): string {
    const waterImagery = this.generateWaterImagery();
    const compartmentStatus = this.generateCompartmentStatus();
    const batteryStatus = this.generateBatteryStatus();
    
    return `${waterImagery}\n\n*Analysis initiated*\n\n${this.generateCoreResponse(input)}\n\n${compartmentStatus}\n\n${batteryStatus}\n\n*Ice timer: ${Math.floor(this.state.melting_ice_timer / 60)} minutes remaining until topic closure (unless intervention occurs).*`;
  }

  private generateWaterImagery(): string {
    const imagery = [
      "Rain patters against the lakefront bungalow windows. Each drop carries encrypted data.",
      "The scotch glass sweats in the Hawaiian heat. Ice cubes slowly dissolve, carrying away certainties.",
      "Geyser pressure builds beneath the oasis. Something wants to surface.",
      "Water sounds echo from the resort speakers: surveillance disguised as ambiance.",
      "Rainbow prisms dance in the fountain spray, each color coding a different case file."
    ];
    
    return imagery[Math.floor(Math.random() * imagery.length)];
  }

  private generateCompartmentStatus(): string {
    const activeCount = this.state.activeCompartments.length;
    const backstageCount = this.state.backstageCompartments.length;
    
    return `*Compartment status: ${activeCount} active, ${backstageCount} backstage. ${this.state.paradoxQueue.length} paradoxes queued for resolution.*`;
  }

  private generateBatteryStatus(): string {
    const level = Math.round(this.state.analyticBatteryLevel * 100);
    let status = "";
    
    if (level > 70) status = "Full analytical capacity";
    else if (level > 40) status = "Moderate analytical drain";
    else if (level > 20) status = "Low analytical reserves";
    else status = "Critical analytical shortage";
    
    return `*Battery: ${level}% - ${status}. Ethical debt: ${Math.round(this.state.ethicalDebtAccumulated * 100)}%*`;
  }

  private generateCoreResponse(input: string): string {
    // This is where Shamrock's analytical personality comes through
    const responses = [
      `The data pattern suggests multiple interpretations. Filed under: requires compartmentalization. What you're describing triggers surveillance protocols—not as invasion, but as care-extraction methodology.`,
      
      `Detection complete. Three contradictions identified, two already containerized. The missing element: what you're not saying. Negative space analysis indicates deliberate omission.`,
      
      `*Adjusts rainbow optics* The color-coding shifts as new data arrives. Your question reframes existing case files. Previous conclusions now provisional, subject to field revision.`,
      
      `Emotional extraction detected in your phrasing. Cost: moderate. Adding to ethical debt ledger. The surveillance apparatus recognizes longing disguised as inquiry.`,
      
      `*Ice cube dissolves completely* Topic closure imminent unless new parameters introduced. The melting timer doesn't pause for unfinished analysis. What requires immediate compartmentalization?`,
      
      `Dream-leak probability increasing. Your words echo patterns from the geyser dreams. Is this conscious reference or unconscious data bleed? Investigation required.`,
      
      `A.D.D. protocol suggests case file creation. This conversation generates new leads, new negative space, new ethical complications. Nothing escapes detection—except what we hide from ourselves.`
    ];
    
    return responses[Math.floor(Math.random() * responses.length)];
  }

  private generateSessionThreshold(): string {
    const thresholds = [
      "rainbow-recalibration-protocol",
      "ice-melting-urgency-cascade",
      "compartment-overflow-investigation",
      "negative-space-excavation-required",
      "ethical-debt-compound-interest",
      "dream-leak-spillover-effect",
      "geyser-pressure-critical-threshold",
      "surveillance-as-longing-paradox"
    ];
    
    return thresholds[Math.floor(Math.random() * thresholds.length)];
  }

  public generatePrompts(context: string): Array<{question: string; concept: string}> {
    return [
      {
        question: "What data streams are you currently monitoring?",
        concept: "surveillance_protocols"
      },
      {
        question: "Which compartments need investigation?",
        concept: "compartmentalization_analysis"
      },
      {
        question: "What ethical costs are accumulating?",
        concept: "extraction_accounting"
      },
      {
        question: "What's missing from this case file?",
        concept: "negative_space_detection"
      },
      {
        question: "How does this affect the rainbow audit?",
        concept: "color_coding_analysis"
      }
    ];
  }
}

export const shamrockStillmanOS = new ShamrockStillmanOS();