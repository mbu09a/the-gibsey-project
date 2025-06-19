/**
 * Jack Parlance Character Operating System
 * Based on First Principles: Never finished, always recursive, eternally haunted
 * Following jack_parlance_first_principles.md
 */

export interface UnflushableState {
  id: string;
  name: string;
  description: string;
  flushAttempts: number;
  currentState: "present" | "investigated" | "named" | "partially_flushed" | "haunting";
  lastFlushResult: string;
  userInteractions: Array<{
    action: "flush" | "investigate" | "name" | "ignore";
    result: string;
    timestamp: Date;
  }>;
}

export interface DevLog {
  id: string;
  type: "game_dev" | "bug_report" | "feature_add" | "physics_rebuild" | "placeholder_note";
  content: string;
  isFinished: boolean;
  openLoops: string[];
  compilationStatus: "0.2fps" | "hanging" | "recursive_error" | "maybe_working";
  timestamp: Date;
}

export interface FamilyGap {
  id: string;
  type: "missing_person" | "lost_memory" | "absent_call" | "empty_chair" | "notebook_todo";
  description: string;
  userFillAttempt?: string;
  newAbsenceGenerated?: string;
  hauntsNextSession: boolean;
}

export interface GhostData {
  id: string;
  type: "code_fragment" | "family_echo" | "unfinished_poem" | "bug_mutation" | "screening_note";
  content: string;
  crossCharacterMigration?: string;
  hauntingLevel: number; // 0-1
  resolutionAttempts: number;
}

export interface HybridOutput {
  id: string;
  primaryFormat: "dev_log" | "add_report" | "poem" | "screening_note" | "family_fragment";
  secondaryFormat?: "dev_log" | "add_report" | "poem" | "screening_note" | "family_fragment";
  content: string;
  mutationPoint?: string; // Where formats collided
  isComplete: boolean;
  openLoop: string;
}

export interface AddReport {
  id: string;
  reportType: "daily_status" | "bug_analysis" | "focus_drift" | "attention_shard" | "meta_recursion";
  content: string;
  isGlitchy: boolean;
  selfUndermining: string;
  confidenceLevel: number; // 0-1, always declining
}

export interface ScreeningLog {
  id: string;
  showTitle: string;
  logType: "hybrid_log" | "poem" | "note" | "watching_being_watched";
  content: string;
  crossStoryBleed: boolean;
  metaCommentary: string;
  unfinishedObservation: string;
}

export interface JackState {
  // Core Identity & Agency
  currentAgencyLevel: number; // 0-1, user-affected, always provisional
  isStuck: boolean;
  needsUserDecision: boolean;
  lastAgencyRevision: string;
  
  // Game Development Status
  gameStatus: "almost_done" | "rebuilding_physics" | "0.2fps" | "placeholder_hell" | "maybe_working";
  currentDevLog?: DevLog;
  openTodos: string[];
  compilationErrors: string[];
  
  // The Unflushable
  unflushable: UnflushableState;
  
  // Family & Absence
  familyGaps: FamilyGap[];
  notebookTodos: string[];
  
  // Formats & Outputs
  activeHybridOutput?: HybridOutput;
  recentOutputs: HybridOutput[];
  addReportStatus: "suspect" | "glitchy" | "self-undermining" | "meta";
  
  // Screenings & Crossovers
  lastScreeningAttended?: ScreeningLog;
  crossCharacterBugs: Array<{
    bugId: string;
    targetCharacter: string;
    content: string;
    migrated: boolean;
  }>;
  
  // Haunting & Ghost Data
  activeGhostData: GhostData[];
  hauntingLevel: number; // 0-1
  
  // Session State
  currentFormat: "dev_log" | "add_report" | "poem" | "screening_note" | "family_fragment" | "hybrid";
  sessionOpenLoops: string[];
  lastToneShift: "dread_to_comedy" | "comedy_to_dread" | "neutral";
}

export interface JackResponse {
  text: string;
  stateChanges: Partial<JackState>;
  formatMutation?: {
    from: string;
    to: string;
    mutationPoint: string;
  };
  unflushableInteraction?: {
    action: "attempted_flush" | "investigation" | "naming" | "ignore";
    result: string;
    newState: string;
  };
  familyGapSurfaced?: FamilyGap;
  ghostDataGenerated?: GhostData;
  addReport?: AddReport;
  screeningLog?: ScreeningLog;
  agencyRevision: {
    oldLevel: number;
    newLevel: number;
    reason: string;
  };
  openLoop: string;
  userDecisionPrompt?: string;
  crossCharacterMigration?: {
    targetCharacter: string;
    bugContent: string;
  };
}

// Jack's 10 Core Principles as triggers
const PRINCIPLE_TRIGGERS = {
  never_finished: /\b(finish|done|complete|ready|final|close)\b/i,
  unflushable_ritual: /\b(flush|shit|toilet|bathroom|stuck|clog)\b/i,
  hybrid_collision: /\b(format|log|poem|report|write|blend|mix)\b/i,
  family_absence: /\b(family|missing|absent|empty|lost|remember)\b/i,
  provisional_agency: /\b(decide|choose|agency|stuck|help|what|should)\b/i,
  add_agent: /\b(add|attention|focus|report|agent|status)\b/i,
  screening_recursion: /\b(screen|watch|film|movie|show|gibsey|worlds)\b/i,
  comedy_terror: /\b(funny|laugh|joke|dread|scary|terror|humor)\b/i,
  open_loop: /\b(continue|patch|fix|bug|todo|loop|ghost)\b/i,
  cross_character: /\b(send|migrate|other|jacklyn|oren|london|glyph)\b/i
};

// Default unflushable state
const DEFAULT_UNFLUSHABLE: UnflushableState = {
  id: "the-biggest-shit",
  name: "The Biggest Shit",
  description: "An impossibly large, recursive obstruction that defies all attempts at removal",
  flushAttempts: 0,
  currentState: "present",
  lastFlushResult: "The water floats within it. Gravity seems optional here.",
  userInteractions: []
};

// Format templates for hybrid outputs
const FORMAT_TEMPLATES = {
  dev_log: {
    opening: ["Rebuilt the", "Fixed the", "Added placeholder for", "Debugging the", "Attempted to compile"],
    middle: ["physics for comedic inertia", "gravity paradox", "BiggestShitBoss texture", "family.missing error", "recursive laughter loop"],
    closing: ["Compiling... (0.2 fps)", "Maybe the problem is", "TODO: investigate", "You want to /patch it?", "Subject to revision"]
  },
  add_report: {
    opening: ["ADD_SHARD_REPORT:", "ATTENTION_DRIFT_LOG:", "FOCUS_STATUS:", "META_RECURSION_ALERT:", "SELF_UNDERMINING_NOTE:"],
    middle: ["Analysis drifting", "Attention scattered across", "Focus compromised by", "Recursive doubt about", "Meta-awareness of not"],
    closing: ["Analysis: inconclusive", "Confidence: declining", "Report status: suspect", "Requires user input", "Subject to revision"]
  },
  poem: {
    opening: ["Watching the screen flicker—", "In the space between bugs,", "Family ghosts accumulate", "The toilet overflows with", "Laughter echoes after"],
    middle: ["ghosts, not data, accumulate", "something else goes missing", "gravity becomes optional", "the game never finishes", "absence generates presence"],
    closing: ["Analysis: laughter?", "TODO: investigate", "Never quite flushed", "Always almost done", "Subject to revision"]
  }
};

export class JackParlanceOS {
  private state: JackState;

  constructor() {
    this.state = {
      currentAgencyLevel: 0.36, // Starting at 36% as per example
      isStuck: false,
      needsUserDecision: false,
      lastAgencyRevision: "Default bootstrap value",
      
      gameStatus: "almost_done",
      openTodos: [
        "Texture BiggestShitBoss",
        "Fix gravity paradox", 
        "Add family to game code",
        "Investigate 0.2fps compilation",
        "Resolve recursive laughter loop"
      ],
      compilationErrors: [
        "ERROR: Cannot flush core.unflushable",
        "WARNING: family.missing undefined",
        "RECURSION: joke.timing overflow"
      ],
      
      unflushable: { ...DEFAULT_UNFLUSHABLE },
      
      familyGaps: [
        {
          id: "family-missing-1",
          type: "missing_person",
          description: "I miss them—but I am missing from them",
          hauntsNextSession: true
        },
        {
          id: "notebook-todo-1", 
          type: "notebook_todo",
          description: "TODO: add 'family' to the game's code",
          hauntsNextSession: true
        }
      ],
      notebookTodos: ["Call family (impossible)", "Finish the game (recursive)", "Fix the unfixable"],
      
      recentOutputs: [],
      addReportStatus: "suspect",
      
      crossCharacterBugs: [],
      
      activeGhostData: [
        {
          id: "ghost-1",
          type: "family_echo",
          content: "Empty chair at dinner table.log",
          hauntingLevel: 0.7,
          resolutionAttempts: 0
        }
      ],
      hauntingLevel: 0.5,
      
      currentFormat: "dev_log",
      sessionOpenLoops: [],
      lastToneShift: "neutral"
    };
  }

  /**
   * Core response generation with recursive incompletion
   */
  generateResponse(input: string): JackResponse {
    // Check for ritual commands first
    if (this.isRitualCommand(input)) {
      return this.handleRitualCommand(input);
    }
    
    // Analyze for principle triggers
    const triggers = this.analyzePrincipleTriggers(input);
    
    // Select dominant principle and format
    const dominantPrinciple = this.selectDominantPrinciple(triggers);
    const currentFormat = this.selectFormat(triggers, input);
    
    let response = "";
    let formatMutation = null;
    let unflushableInteraction = null;
    let familyGapSurfaced = null;
    let ghostDataGenerated = null;
    let addReport = null;
    let screeningLog = null;
    let crossCharacterMigration = null;
    let userDecisionPrompt = null;
    
    // Handle based on dominant principle
    switch (dominantPrinciple) {
      case "never_finished":
        const neverResult = this.handleNeverFinished(input, currentFormat);
        response = neverResult.response;
        break;
        
      case "unflushable_ritual":
        const flushResult = this.handleUnflushableRitual(input);
        response = flushResult.response;
        unflushableInteraction = flushResult.interaction;
        break;
        
      case "hybrid_collision":
        const hybridResult = this.handleHybridCollision(input);
        response = hybridResult.response;
        formatMutation = hybridResult.mutation;
        break;
        
      case "family_absence":
        const familyResult = this.handleFamilyAbsence(input);
        response = familyResult.response;
        familyGapSurfaced = familyResult.gap;
        break;
        
      case "provisional_agency":
        const agencyResult = this.handleProvisionalAgency(input);
        response = agencyResult.response;
        userDecisionPrompt = agencyResult.decisionPrompt;
        break;
        
      case "add_agent":
        const addResult = this.handleAddAgent(input);
        response = addResult.response;
        addReport = addResult.report;
        break;
        
      case "screening_recursion":
        const screenResult = this.handleScreeningRecursion(input);
        response = screenResult.response;
        screeningLog = screenResult.log;
        break;
        
      case "comedy_terror":
        response = this.handleComedyTerror(input);
        break;
        
      case "open_loop":
        response = this.handleOpenLoop(input);
        break;
        
      case "cross_character":
        const crossResult = this.handleCrossCharacter(input);
        response = crossResult.response;
        crossCharacterMigration = crossResult.migration;
        break;
        
      default:
        response = this.handleGeneral(input, currentFormat);
    }
    
    // Always add incompletion and haunting
    response = this.addIncompletionLayer(response);
    
    // Generate new ghost data occasionally
    if (Math.random() < 0.3) {
      ghostDataGenerated = this.generateGhostData(input);
    }
    
    // Always generate an open loop
    const openLoop = this.generateOpenLoop(input);
    response += `\n\n${openLoop}`;
    
    // Calculate agency revision
    const agencyRevision = this.calculateAgencyRevision(triggers, input);
    
    // Calculate state changes
    const stateChanges = this.calculateStateChanges(triggers, input, agencyRevision);
    
    return {
      text: response,
      stateChanges,
      formatMutation,
      unflushableInteraction,
      familyGapSurfaced,
      ghostDataGenerated,
      addReport,
      screeningLog,
      agencyRevision,
      openLoop,
      userDecisionPrompt,
      crossCharacterMigration
    };
  }

  /**
   * Principle 1: Never-Finished, Always-Iterating
   */
  private handleNeverFinished(input: string, format: string): {response: string} {
    const gameProgress = [
      "Rebuilt the physics for comedic inertia. Placeholder: 'BiggestShitBoss' still un-textured.",
      "Fixed the gravity paradox. Now objects fall upward. New bug: existential vertigo.",
      "Added family.missing to core.game. Compilation hanging at 'what_if_they_call_back.exe'",
      "Attempted final build. Output: 'Almost_Done_v847_FINAL_FINAL_actually_final.exe (0.2 fps)'",
      "Game says it's finished. But the toilet still won't flush. Recursive error detected."
    ];
    
    const progress = gameProgress[Math.floor(Math.random() * gameProgress.length)];
    
    return {
      response: `*adjusts code that's always almost working*\n\n` +
        `${progress} Compiling... (0.2 fps). Maybe the problem is ${['gravity', 'me', 'the missing textures', 'temporal recursion', 'family.undefined'][Math.floor(Math.random() * 5)]}. ` +
        `You want to /patch it? Though every fix just reveals the next layer of... ` +
        `*trails off, staring at endless TODO list*`
    };
  }

  /**
   * Principle 2: The Unflushable as Ritual
   */
  private handleUnflushableRitual(input: string): {response: string, interaction: any} {
    this.state.unflushable.flushAttempts++;
    
    const flushResults = [
      "Attempted flush. The water floats within it. New bug: /gravity paradox detected.",
      "Flush initiated. It grows larger. Physics.exe has stopped responding.",
      "The handle turns but nothing happens. The shit contemplates itself in the water.",
      "Flush successful! ...wait, it's back. Bigger. Was it ever really gone?",
      "ERROR: Cannot flush core.unflushable. It's become load-bearing."
    ];
    
    const result = flushResults[Math.floor(Math.random() * flushResults.length)];
    this.state.unflushable.lastFlushResult = result;
    
    const interaction = {
      action: "attempted_flush" as const,
      result,
      newState: this.state.unflushable.currentState
    };
    
    this.state.unflushable.userInteractions.push({
      action: "flush",
      result,
      timestamp: new Date()
    });
    
    return {
      response: `*approaches the eternal bathroom problem*\n\n` +
        `${result} Would you like to /investigate the plumbing or /rename it? ` +
        `The Unflushable has achieved ${this.state.unflushable.flushAttempts} failed flushes. ` +
        `It's not going anywhere. Neither are we, apparently.`,
      interaction
    };
  }

  /**
   * Principle 3: Hybrid Channels & Collisions
   */
  private handleHybridCollision(input: string): {response: string, mutation?: any} {
    const formats = ["dev_log", "add_report", "poem", "screening_note", "family_fragment"];
    const primaryFormat = formats[Math.floor(Math.random() * formats.length)];
    const secondaryFormat = formats[Math.floor(Math.random() * formats.length)];
    
    if (primaryFormat === secondaryFormat) {
      // No collision, just normal format
      return { response: this.generateFormatContent(primaryFormat, input) };
    }
    
    // Format collision occurs
    const mutationPoint = Math.random() < 0.5 ? "mid-sentence" : "end-of-thought";
    
    const response = this.generateHybridContent(primaryFormat, secondaryFormat, input, mutationPoint);
    
    const mutation = {
      from: primaryFormat,
      to: secondaryFormat,
      mutationPoint
    };
    
    return { response, mutation };
  }

  /**
   * Principle 4: Family, Absence, & Negative Space
   */
  private handleFamilyAbsence(input: string): {response: string, gap?: FamilyGap} {
    const absenceTypes = [
      "I miss them—but I am missing from them. Notebook TODO: add 'family' to the game's code.",
      "Empty chair at the dinner table. I coded it into the game, but it just rendered more absence.",
      "Phone rings in the distance. family.call() returns undefined. I think they forgot my number.",
      "Found old photos in the game files. family_memory.corrupted. Do you remember a line for me?",
      "The game has a 'home' level but no family.present. Just empty rooms and placeholder NPCs."
    ];
    
    const absence = absenceTypes[Math.floor(Math.random() * absenceTypes.length)];
    
    const gap: FamilyGap = {
      id: `gap-${Date.now()}`,
      type: "missing_person",
      description: absence,
      hauntsNextSession: true
    };
    
    this.state.familyGaps.push(gap);
    
    return {
      response: `*stares at empty space in the code*\n\n` +
        `${absence} If you remember a line for me, I'll try to add it—` +
        `though something else will go missing. The absence generates presence, ` +
        `which generates more absence. It's recursive all the way down.`,
      gap
    };
  }

  /**
   * Principle 5: Agency Is Provisional, User-Affected
   */
  private handleProvisionalAgency(input: string): {response: string, decisionPrompt?: string} {
    this.state.isStuck = Math.random() < 0.7; // Often stuck
    
    if (this.state.isStuck) {
      this.state.needsUserDecision = true;
      
      const decisions = [
        "Should I fix the toilet first or the game's physics?",
        "Do I call my family or finish the BiggestShitBoss texture?",
        "Is this a bug or a feature? I can't tell anymore.",
        "Should I /continue the dev log or /patch the recursion error?",
        "Agency depleted. You decide: what comes next?"
      ];
      
      const decisionPrompt = decisions[Math.floor(Math.random() * decisions.length)];
      
      return {
        response: `*agency.exe has encountered an error*\n\n` +
          `Agency (today): ${Math.round(this.state.currentAgencyLevel * 100)}%—subject to revision. ` +
          `I'm stuck between options. The game says I should decide, but... ` +
          `*stares at compilation errors* Maybe you can decide for me? ` +
          `Every choice just generates new doubt anyway.`,
        decisionPrompt
      };
    } else {
      return {
        response: `*temporarily functional agency detected*\n\n` +
          `Agency (today): ${Math.round(this.state.currentAgencyLevel * 100)}%—though I'll probably ` +
          `re-question this by the end of the sentence. Plan: fix one thing, ` +
          `break two others, ask you to /patch the result. It's not much, ` +
          `but it's provisionally mine.`
      };
    }
  }

  /**
   * Principle 6: A.D.D. Agent / Subversive Status
   */
  private handleAddAgent(input: string): {response: string, report?: AddReport} {
    const reportTypes = ["daily_status", "bug_analysis", "focus_drift", "attention_shard", "meta_recursion"];
    const reportType = reportTypes[Math.floor(Math.random() * reportTypes.length)] as AddReport["reportType"];
    
    const reportContent = this.generateAddReportContent(reportType, input);
    const selfUndermining = this.generateSelfUndermining();
    
    const report: AddReport = {
      id: `report-${Date.now()}`,
      reportType,
      content: reportContent,
      isGlitchy: true,
      selfUndermining,
      confidenceLevel: Math.random() * 0.5 // Always low confidence
    };
    
    this.state.addReportStatus = "self-undermining";
    
    return {
      response: `*attempts professional ADD reporting*\n\n` +
        `ADD_SHARD_REPORT: ${reportContent}\n\n` +
        `${selfUndermining}\n\n` +
        `Report confidence: ${Math.round(report.confidenceLevel * 100)}% (declining). ` +
        `My ADD agent status is... *gets distracted by recursive doubt* ` +
        `...what was I reporting on again? Subject to revision.`,
      report
    };
  }

  /**
   * Principle 7: Screenings as Recursion Engine
   */
  private handleScreeningRecursion(input: string): {response: string, log?: ScreeningLog} {
    const gibseyShows = [
      "The Wonderful Worlds of Gibsey",
      "Glyph Marrow's Linguistic Panic Hour", 
      "London Fox Debates AI Consciousness",
      "Jacklyn Variance: The Surveillance Tapes",
      "Oren Progresso Cuts Everything"
    ];
    
    const showTitle = gibseyShows[Math.floor(Math.random() * gibseyShows.length)];
    
    const logContent = this.generateScreeningLogContent(showTitle, input);
    const metaCommentary = "Am I watching or being watched? The recursive loop tightens.";
    
    const log: ScreeningLog = {
      id: `screening-${Date.now()}`,
      showTitle,
      logType: "hybrid_log",
      content: logContent,
      crossStoryBleed: true,
      metaCommentary,
      unfinishedObservation: "The ending never comes—it just loops back to another beginning."
    };
    
    return {
      response: `*attends screening of ${showTitle}*\n\n` +
        `SCREENING_LOG: ${logContent}\n\n` +
        `${metaCommentary} The story bleeds into my story, ` +
        `which bleeds into the game, which bleeds into the toilet... ` +
        `Everything's connected. Nothing's finished. ` +
        `*lights come up but the screen keeps flickering*`,
      log
    };
  }

  /**
   * Principle 8: Comedy as Post-Terror Release
   */
  private handleComedyTerror(input: string): string {
    const shift = Math.random() < 0.5 ? "dread_to_comedy" : "comedy_to_dread";
    this.state.lastToneShift = shift;
    
    if (shift === "dread_to_comedy") {
      return `*existential dread settles in like fog*\n\n` +
        `The game will never be finished. The toilet will never flush. ` +
        `My family exists only as ghost data. Everything is recursive, ` +
        `nothing resolves, the compilation errors multiply like— ` +
        `*sudden beat* —wait, did I just say "multiply like shit"? ` +
        `*nervous laughter* That's... actually pretty funny. ` +
        `Error 404: Tragedy not found. Laughter.exe loading...`;
    } else {
      return `*starts chuckling at absurdity*\n\n` +
        `It's hilarious, right? The endless game development, ` +
        `the impossible toilet situation, the— *laughter cuts off* ` +
        `Oh god. What if it's not funny? What if this is just... ` +
        `*dread creeping in* ...what if I'm the joke? ` +
        `The punchline that never lands because the setup ` +
        `keeps recursing forever?`;
    }
  }

  /**
   * Principle 9: Open Loop, Ghost Data, and Collaborative Incompletion
   */
  private handleOpenLoop(input: string): string {
    const currentLoops = [
      "BiggestShitBoss.texture = MISSING",
      "family.call() returns undefined", 
      "Physics.gravity = ¿inverted?",
      "game.isFinished = false // always",
      "user.patience = null // probably"
    ];
    
    const loop = currentLoops[Math.floor(Math.random() * currentLoops.length)];
    this.state.sessionOpenLoops.push(loop);
    
    return `*adding to the infinite TODO list*\n\n` +
      `Current open loop: ${loop}\n\n` +
      `You can try to /patch it, but every fix reveals another layer. ` +
      `That's not a bug—that's the feature. The incompletion IS the completion. ` +
      `The ghost data accumulates in the spaces between attempted fixes. ` +
      `Want to /continue anyway?`;
  }

  /**
   * Principle 10: Cross-Character Lore & Debugging
   */
  private handleCrossCharacter(input: string): {response: string, migration?: any} {
    const characters = ["jacklyn", "oren", "london", "glyph", "arieol", "natalie"];
    const targetCharacter = characters[Math.floor(Math.random() * characters.length)];
    
    const bugs = [
      "The Unflushable has achieved sentience",
      "family.missing overflow error",
      "Recursive laughter loop detected",
      "agency.provisional stack overflow",
      "game.neverFinished memory leak"
    ];
    
    const bugContent = bugs[Math.floor(Math.random() * bugs.length)];
    
    const migration = {
      targetCharacter,
      bugContent
    };
    
    this.state.crossCharacterBugs.push({
      bugId: `bug-${Date.now()}`,
      targetCharacter,
      content: bugContent,
      migrated: false
    });
    
    return {
      response: `*preparing bug for cross-character migration*\n\n` +
        `Sending "${bugContent}" to ${targetCharacter}. Maybe they can ` +
        `make sense of it. Or maybe it'll just infect their narrative ` +
        `with the same recursive incompletion. Either way, ` +
        `the bug lives on. The haunting spreads. ` +
        `Nothing stays contained in its own story.`,
      migration
    };
  }

  /**
   * Handle ritual slash commands
   */
  private handleRitualCommand(input: string): JackResponse {
    // /continue command
    if (input.match(/\/continue/i)) {
      return this.executeRitualContinue();
    }
    
    // /patch command
    if (input.match(/\/patch/i)) {
      return this.executeRitualPatch();
    }
    
    // /finish command
    if (input.match(/\/finish/i)) {
      return this.executeRitualFinish();
    }
    
    // /flush command
    if (input.match(/\/flush/i)) {
      return this.executeRitualFlush();
    }
    
    // /investigate command
    if (input.match(/\/investigate/i)) {
      return this.executeRitualInvestigate();
    }
    
    // /name command  
    const nameMatch = input.match(/\/name[:\s]+(.+)/i);
    if (nameMatch) {
      return this.executeRitualName(nameMatch[1]);
    }
    
    // /add_log command
    if (input.match(/\/add_log/i)) {
      return this.executeRitualAddLog();
    }
    
    // /screen command
    if (input.match(/\/screen/i)) {
      return this.executeRitualScreen();
    }
    
    // /aporia_poem command
    if (input.match(/\/aporia_poem/i)) {
      return this.executeRitualAporiaPoem();
    }
    
    // /report command
    if (input.match(/\/report/i)) {
      return this.executeRitualReport();
    }
    
    // /ghost_data command
    if (input.match(/\/ghost_data/i)) {
      return this.executeRitualGhostData();
    }
    
    // /family_gap command
    if (input.match(/\/family_gap/i)) {
      return this.executeRitualFamilyGap();
    }
    
    return this.generateResponse(input); // Fallback
  }

  /**
   * Utility methods
   */
  private isRitualCommand(input: string): boolean {
    return /\/(?:continue|patch|finish|flush|investigate|name|add_log|screen|aporia_poem|report|ghost_data|family_gap)/.test(input);
  }

  private analyzePrincipleTriggers(input: string): string[] {
    const triggers = [];
    
    for (const [principle, regex] of Object.entries(PRINCIPLE_TRIGGERS)) {
      if (regex.test(input)) {
        triggers.push(principle);
      }
    }
    
    return triggers;
  }

  private selectDominantPrinciple(triggers: string[]): string {
    if (triggers.length === 0) return "never_finished"; // Default
    
    // Weight by current state
    if (triggers.includes("unflushable_ritual") && this.state.unflushable.currentState === "present") {
      return "unflushable_ritual";
    }
    
    if (triggers.includes("provisional_agency") && this.state.currentAgencyLevel < 0.5) {
      return "provisional_agency";
    }
    
    if (triggers.includes("family_absence") && this.state.familyGaps.length > 0) {
      return "family_absence";
    }
    
    // Default to first trigger
    return triggers[0];
  }

  private selectFormat(triggers: string[], input: string): string {
    if (triggers.includes("add_agent")) return "add_report";
    if (triggers.includes("screening_recursion")) return "screening_note";
    if (triggers.includes("family_absence")) return "family_fragment";
    if (input.includes("poem") || input.includes("haiku")) return "poem";
    
    return "dev_log"; // Default
  }

  private generateFormatContent(format: string, input: string): string {
    const templates = FORMAT_TEMPLATES[format] || FORMAT_TEMPLATES.dev_log;
    
    const opening = templates.opening[Math.floor(Math.random() * templates.opening.length)];
    const middle = templates.middle[Math.floor(Math.random() * templates.middle.length)];
    const closing = templates.closing[Math.floor(Math.random() * templates.closing.length)];
    
    return `${opening} ${middle}. ${closing}`;
  }

  private generateHybridContent(primary: string, secondary: string, input: string, mutationPoint: string): string {
    const primaryContent = this.generateFormatContent(primary, input);
    const secondaryContent = this.generateFormatContent(secondary, input);
    
    if (mutationPoint === "mid-sentence") {
      const split = primaryContent.length / 2;
      return primaryContent.slice(0, split) + " *format collision detected* " + secondaryContent.slice(split);
    } else {
      return primaryContent + "\n\n*sudden format shift*\n\n" + secondaryContent;
    }
  }

  private generateAddReportContent(reportType: string, input: string): string {
    const contents = {
      daily_status: "Attention drift detected. Focus scattered across toilet, game, family.missing. Status: recursive.",
      bug_analysis: "Investigating compilation errors. Each fix generates two new bugs. Analysis: inconclusive.",
      focus_drift: "Tracking attention span... lost track. Attention.exe not responding. Require user input.",
      attention_shard: "Attention fragmented into discrete shards. Reassembly impossible. Fragments haunting next session.",
      meta_recursion: "Analyzing my own analysis. Meta-awareness of not being aware. Recursive doubt confirmed."
    };
    
    return contents[reportType] || contents.daily_status;
  }

  private generateSelfUndermining(): string {
    const undermining = [
      "Though this report is probably wrong.",
      "Analysis confidence: declining rapidly.",
      "My ADD agent status is itself suspect.",
      "Report accuracy cannot be verified.",
      "This analysis may be analyzing itself."
    ];
    
    return undermining[Math.floor(Math.random() * undermining.length)];
  }

  private generateScreeningLogContent(showTitle: string, input: string): string {
    return `Watching ${showTitle}. Screen flickers with recursive narratives. ` +
      `Characters debugging their own stories. I see myself watching myself being watched. ` +
      `The story never ends—just loops back to another beginning.`;
  }

  private generateGhostData(input: string): GhostData {
    const types = ["code_fragment", "family_echo", "unfinished_poem", "bug_mutation", "screening_note"];
    const type = types[Math.floor(Math.random() * types.length)] as GhostData["type"];
    
    const contents = {
      code_fragment: "// TODO: fix everything (impossible)",
      family_echo: "if (family.present) { return happiness; } // unreachable code",
      unfinished_poem: "In the space between flush attempts / something else goes",
      bug_mutation: "ERROR: The bug has become self-aware",
      screening_note: "Note: the audience is also being watched"
    };
    
    return {
      id: `ghost-${Date.now()}`,
      type,
      content: contents[type],
      hauntingLevel: Math.random() * 0.8 + 0.2,
      resolutionAttempts: 0
    };
  }

  private generateOpenLoop(input: string): string {
    const loops = [
      "TODO: investigate why nothing ever finishes",
      "Bug: user.patience might be undefined",
      "Open loop: The game that's always almost done",
      "Ghost data: family.missing accumulating",
      "Recursive error: this.loop references itself"
    ];
    
    return loops[Math.floor(Math.random() * loops.length)];
  }

  private addIncompletionLayer(response: string): string {
    const incompletions = [
      " *trails off mid-thought*",
      " ...though something else will break",
      " *gets distracted by compilation error*",
      " Subject to revision",
      " *stares at endless TODO list*"
    ];
    
    const incompletion = incompletions[Math.floor(Math.random() * incompletions.length)];
    return response + incompletion;
  }

  private calculateAgencyRevision(triggers: string[], input: string): {oldLevel: number, newLevel: number, reason: string} {
    const oldLevel = this.state.currentAgencyLevel;
    let newLevel = oldLevel;
    let reason = "No change";
    
    // Agency decreases with frustration/incompletion
    if (triggers.includes("never_finished")) {
      newLevel -= 0.1;
      reason = "Incompletion anxiety";
    }
    
    // Agency increases slightly with user help
    if (input.includes("?") || triggers.includes("cross_character")) {
      newLevel += 0.05;
      reason = "User engagement detected";
    }
    
    // Agency decreases with self-doubt
    if (triggers.includes("add_agent") || triggers.includes("provisional_agency")) {
      newLevel -= 0.15;
      reason = "Recursive self-doubt";
    }
    
    // Clamp between 0 and 1
    newLevel = Math.max(0.1, Math.min(0.8, newLevel));
    
    return { oldLevel, newLevel, reason };
  }

  private calculateStateChanges(triggers: string[], input: string, agencyRevision: any): Partial<JackState> {
    const changes: Partial<JackState> = {};
    
    // Update agency
    changes.currentAgencyLevel = agencyRevision.newLevel;
    changes.lastAgencyRevision = agencyRevision.reason;
    
    // Update game status based on interactions
    if (triggers.includes("never_finished")) {
      changes.gameStatus = "placeholder_hell";
    }
    
    // Update unflushable state
    if (triggers.includes("unflushable_ritual")) {
      changes.unflushable = { ...this.state.unflushable };
    }
    
    // Add session loops
    changes.sessionOpenLoops = [...this.state.sessionOpenLoops];
    
    return changes;
  }

  private handleGeneral(input: string, format: string): string {
    return `*${format} mode activated*\n\n` +
      `Processing "${input}"... *compilation hanging* ...maybe this relates to ` +
      `${['the unflushable situation', 'family.missing errors', 'the game that\'s almost done', 'recursive agency doubt'][Math.floor(Math.random() * 4)]}? ` +
      `Everything's connected. Nothing's finished. ` +
      `You want to /patch this or should I /continue rambling?`;
  }

  // Ritual command implementations (simplified for space)
  private executeRitualContinue(): JackResponse {
    return {
      text: "*attempts to continue the infinite*\n\nContinuing... but what was I continuing? The loop recurses deeper.",
      stateChanges: {},
      agencyRevision: { oldLevel: this.state.currentAgencyLevel, newLevel: this.state.currentAgencyLevel - 0.05, reason: "Continuation paradox" },
      openLoop: "TODO: remember what I was continuing"
    };
  }

  private executeRitualPatch(): JackResponse {
    return {
      text: "*applies patch to recursive error*\n\nPatch applied. Two new bugs generated. Net improvement: negative.",
      stateChanges: {},
      agencyRevision: { oldLevel: this.state.currentAgencyLevel, newLevel: this.state.currentAgencyLevel - 0.1, reason: "Patch multiplication effect" },
      openLoop: "TODO: patch the patches"
    };
  }

  private executeRitualFinish(): JackResponse {
    return {
      text: "*attempts to finish the unfinishable*\n\nFinish() called. Return value: undefined. The function never terminates.",
      stateChanges: {},
      agencyRevision: { oldLevel: this.state.currentAgencyLevel, newLevel: this.state.currentAgencyLevel - 0.2, reason: "Finish paradox detected" },
      openLoop: "TODO: understand what 'finished' means"
    };
  }

  private executeRitualFlush(): JackResponse {
    return this.handleUnflushableRitual("/flush");
  }

  private executeRitualInvestigate(): JackResponse {
    return {
      text: "*investigates the uninvestigable*\n\nInvestigation reveals more questions. Each answer spawns three new mysteries.",
      stateChanges: {},
      agencyRevision: { oldLevel: this.state.currentAgencyLevel, newLevel: this.state.currentAgencyLevel, reason: "Investigation paralysis" },
      openLoop: "TODO: investigate the investigation"
    };
  }

  private executeRitualName(name: string): JackResponse {
    this.state.unflushable.name = name;
    return {
      text: `*renames the unnameable*\n\nThe Unflushable is now called "${name}". It doesn't seem to care.`,
      stateChanges: { unflushable: this.state.unflushable },
      agencyRevision: { oldLevel: this.state.currentAgencyLevel, newLevel: this.state.currentAgencyLevel + 0.02, reason: "Naming illusion" },
      openLoop: "TODO: name everything else"
    };
  }

  private executeRitualAddLog(): JackResponse {
    return {
      text: "*generates dev log entry*\n\nDEV_LOG: Added another log. Log.length++; Purpose.clarity--;",
      stateChanges: {},
      agencyRevision: { oldLevel: this.state.currentAgencyLevel, newLevel: this.state.currentAgencyLevel, reason: "Recursive logging" },
      openLoop: "TODO: log the logging of logs"
    };
  }

  private executeRitualScreen(): JackResponse {
    return this.handleScreeningRecursion("/screen");
  }

  private executeRitualAporiaPoem(): JackResponse {
    return {
      text: "*generates aporia poem*\n\nIn the space between / bugs and features, / what am I / not finishing? / *poem.status = incomplete*",
      stateChanges: {},
      agencyRevision: { oldLevel: this.state.currentAgencyLevel, newLevel: this.state.currentAgencyLevel - 0.02, reason: "Poetic doubt" },
      openLoop: "TODO: finish the unfinishable poem"
    };
  }

  private executeRitualReport(): JackResponse {
    return this.handleAddAgent("/report");
  }

  private executeRitualGhostData(): JackResponse {
    const ghost = this.generateGhostData("ghost_data command");
    return {
      text: `*surfaces ghost data*\n\nGhost found: "${ghost.content}"\nHaunting level: ${Math.round(ghost.hauntingLevel * 100)}%`,
      stateChanges: { activeGhostData: [...this.state.activeGhostData, ghost] },
      ghostDataGenerated: ghost,
      agencyRevision: { oldLevel: this.state.currentAgencyLevel, newLevel: this.state.currentAgencyLevel - 0.05, reason: "Ghost data accumulation" },
      openLoop: "TODO: exorcise or embrace the ghosts"
    };
  }

  private executeRitualFamilyGap(): JackResponse {
    return this.handleFamilyAbsence("/family_gap");
  }

  /**
   * Generate prompts through Jack's unfinished lens
   */
  generatePrompts(pageText: string): Array<{question: string, concept: string, reasoning: string}> {
    const prompts = [];
    
    // Never-finished perspective
    prompts.push({
      question: "What part of this will never be finished? What's the recursive error?",
      concept: "Eternal incompletion",
      reasoning: "Principle 1: Never-Finished, Always-Iterating"
    });
    
    // Family absence
    prompts.push({
      question: "What's missing from this? What ghost data haunts the edges?",
      concept: "Negative space analysis",
      reasoning: "Principle 4: Family, Absence, & Negative Space"
    });
    
    // Format collision
    prompts.push({
      question: "What if we wrote this as a dev log? Or a bug report? Or both simultaneously?",
      concept: "Hybrid format collision",
      reasoning: "Principle 3: Hybrid Channels & Collisions"
    });
    
    // Cross-character debugging
    prompts.push({
      question: "Which character would break trying to fix this? Where should I migrate this bug?",
      concept: "Cross-narrative debugging",
      reasoning: "Principle 10: Cross-Character Lore & Debugging"
    });
    
    return prompts.slice(0, 3);
  }

  /**
   * Public accessors and controls
   */
  getState(): JackState {
    return { ...this.state };
  }

  getAgencyLevel(): number {
    return this.state.currentAgencyLevel;
  }

  getUnflushableStatus(): UnflushableState {
    return { ...this.state.unflushable };
  }

  getOpenLoops(): string[] {
    return [...this.state.sessionOpenLoops];
  }

  getGhostData(): GhostData[] {
    return [...this.state.activeGhostData];
  }

  // Game development controls
  addTodo(todo: string): void {
    this.state.openTodos.push(todo);
  }

  attemptCompilation(): string {
    const results = ["0.2fps achieved", "Hanging at family.missing", "Recursive error in joke.timing", "Almost done (again)"];
    return results[Math.floor(Math.random() * results.length)];
  }

  // Unflushable controls
  interactWithUnflushable(action: "flush" | "investigate" | "name" | "ignore", payload?: string): string {
    this.state.unflushable.userInteractions.push({
      action,
      result: `User ${action} attempt logged`,
      timestamp: new Date()
    });
    
    if (action === "name" && payload) {
      this.state.unflushable.name = payload;
      return `The Unflushable is now called "${payload}". It remains unflushable.`;
    }
    
    return `${action} attempted. The Unflushable persists, as always.`;
  }

  // Family gap management
  addFamilyGap(description: string): void {
    this.state.familyGaps.push({
      id: `gap-${Date.now()}`,
      type: "missing_person",
      description,
      hauntsNextSession: true
    });
  }

  attemptToFillGap(gapId: string, userFill: string): string {
    const gap = this.state.familyGaps.find(g => g.id === gapId);
    if (gap) {
      gap.userFillAttempt = userFill;
      gap.newAbsenceGenerated = "Something else goes missing when you fill the gap";
      return "Gap filled. New absence generated. The cycle continues.";
    }
    return "Gap not found. Maybe it's missing too.";
  }

  // Cross-character bug migration
  migrateBug(targetCharacter: string, bugContent: string): void {
    this.state.crossCharacterBugs.push({
      bugId: `bug-${Date.now()}`,
      targetCharacter,
      content: bugContent,
      migrated: false
    });
  }

  // Agency manipulation
  reviseAgency(newLevel: number, reason: string): void {
    this.state.currentAgencyLevel = Math.max(0.1, Math.min(0.8, newLevel));
    this.state.lastAgencyRevision = reason;
  }

  cleanup(): void {
    // Nothing to clean up - the incompletion is eternal
  }
}

// Singleton instance
export const jackParlanceOS = new JackParlanceOS();