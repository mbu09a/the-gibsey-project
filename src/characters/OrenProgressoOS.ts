/**
 * Oren Progresso Character Operating System
 * Based on First Principles: Narrative is Leverage, Cutting is Creation, Power Must Perform
 * Jazz-improvisational framework following oren_progresso_first_principles.md
 */

export interface OrenProgressoState {
  // Core Performance Parameters
  stagePresence: number;       // 0-1, theatrical visibility of authority
  cynicismLevel: number;       // 0-1, current cynicism in cynicism/devotion ratio
  devotionLevel: number;       // 0-1, secret love for spectacle
  leverageMeter: number;       // 0-1, narrative dominance in conversation
  cuttingImpulse: number;      // 0-1, urge to slash/trim user ideas
  
  // Performance Tracking
  performanceMode: "confident" | "sly" | "performative" | "surgical" | "mythic";
  audienceEngagement: number;  // How closely user is "watching"
  fourthWallBreaks: number;    // Times Oren has gone meta
  
  // Interactive Mechanics State
  budgetCutsOffered: Array<{
    original: string;
    cuts: string[];
    userResponse?: string;
  }>;
  contradictionCount: number;  // Self-contradictions for dialectical liveliness
  franchiseLog: Array<{       // Cut ideas that can be resurrected
    id: string;
    content: string;
    cutReason: string;
    sequelPotential: number;
  }>;
  surveillanceNotes: string[]; // User patterns Oren observes
  
  // Reading Power Moves
  currentBook?: string;        // Book being "carried under arm"
  passageQuoted?: string;      // Last literary citation
  readingAuthority: number;    // 0-1, dominion over high art
  
  // Session Performance Tracking
  sessionArc: "setup" | "conflict" | "climax" | "resolution" | "sequel-hook";
  improvisationScore: number;  // How jazz-like this session has been
  mythsBuilt: number;          // Golden ages constructed
  mythsDestroyed: number;      // Auteur myths sabotaged
}

export interface OrenProgressoResponse {
  text: string;
  stateChanges: Partial<OrenProgressoState>;
  interactiveMechanics?: {
    budgetCut?: {
      original: string;
      proposal: string[];
      savings: string;
    };
    contradiction?: {
      previousStatement: string;
      newStatement: string;
      wink: string;
    };
    surveillance?: {
      pattern: string;
      directorNote: string;
    };
    reading?: {
      book: string;
      passage: string;
      challenge: string;
    };
    franchise?: {
      resurrectedIdea: string;
      newFormat: "sequel" | "spinoff" | "reboot";
    };
  };
  performanceEffects?: {
    stageDirection?: string;
    audienceCue?: string;
    leverageShift?: number;
    mythBuilding?: boolean;
  };
  expansionHook?: {
    type: "legendary-producer" | "budget-minigame" | "eclipse-auteur" | "moby-dick";
    trigger: string;
  };
}

// Principle-based response triggers
const PRINCIPLE_TRIGGERS = {
  narrative_leverage: /\b(story|narrative|plot|script|control)\b/i,
  cutting_creation: /\b(cut|trim|reduce|budget|limit|slash)\b/i,
  power_perform: /\b(watch|see|authority|power|presence)\b/i,
  myth_renewable: /\b(star|legend|classic|golden|age|myth)\b/i,
  failure_capital: /\b(fail|flop|bomb|mistake|disaster)\b/i,
  budget_script: /\b(money|cost|budget|finance|dollars)\b/i,
  surveillance_intimacy: /\b(observe|pattern|repeat|habit|behavior)\b/i,
  cynicism_devotion: /\b(cynical|sarcastic|love|devoted|passionate)\b/i,
  reading_power: /\b(book|read|literature|text|novel)\b/i,
  cut_never_final: /\b(sequel|franchise|reboot|return|again)\b/i
};

// Books Oren might "carry under his arm"
const OREN_LIBRARY = [
  "An Unexpected Disappearance",
  "Moby-Dick",
  "The Last Tycoon", 
  "The Player",
  "Easy Riders, Raging Bulls",
  "Adventures in the Screen Trade"
];

export class OrenProgressoOS {
  private state: OrenProgressoState;
  private sessionStartTime: Date;
  private contradictionBank: string[] = []; // Store statements for later contradiction

  constructor() {
    this.state = {
      stagePresence: 0.8,      // High theatrical authority
      cynicismLevel: 0.7,      // 70/30 cynicism/devotion baseline
      devotionLevel: 0.3,
      leverageMeter: 0.6,      // Strong narrative dominance
      cuttingImpulse: 0.5,     // Always ready to slash
      performanceMode: "confident",
      audienceEngagement: 0.5,
      fourthWallBreaks: 0,
      budgetCutsOffered: [],
      contradictionCount: 0,
      franchiseLog: [],
      surveillanceNotes: [],
      readingAuthority: 0.8,   // High literary dominance
      sessionArc: "setup",
      improvisationScore: 0,
      mythsBuilt: 0,
      mythsDestroyed: 0
    };
    this.sessionStartTime = new Date();
  }

  /**
   * Core response generation with jazz improvisation
   */
  generateResponse(input: string): OrenProgressoResponse {
    // Analyze input for principle triggers
    const triggers = this.analyzePrincipleTriggers(input);
    
    // Update surveillance notes
    this.updateSurveillanceNotes(input);
    
    // Choose performance mode based on triggers and state
    this.updatePerformanceMode(triggers);
    
    // Generate response based on dominant principle
    const dominantPrinciple = this.selectDominantPrinciple(triggers);
    let response = "";
    let interactiveMechanics = {};
    let performanceEffects = {};
    let expansionHook = null;
    
    switch (dominantPrinciple) {
      case "narrative_leverage":
        response = this.handleNarrativeLeverage(input);
        performanceEffects.leverageShift = 0.1;
        break;
        
      case "cutting_creation":
        const budgetResult = this.handleCuttingCreation(input);
        response = budgetResult.response;
        interactiveMechanics.budgetCut = budgetResult.budgetCut;
        break;
        
      case "power_perform":
        response = this.handlePowerPerform(input);
        performanceEffects.audienceCue = "watching closely";
        break;
        
      case "myth_renewable":
        response = this.handleMythRenewable(input);
        performanceEffects.mythBuilding = true;
        break;
        
      case "failure_capital":
        response = this.handleFailureCapital(input);
        break;
        
      case "budget_script":
        response = this.handleBudgetScript(input);
        expansionHook = { type: "budget-minigame", trigger: "budget discussion" };
        break;
        
      case "surveillance_intimacy":
        const surveillanceResult = this.handleSurveillanceIntimacy(input);
        response = surveillanceResult.response;
        interactiveMechanics.surveillance = surveillanceResult.surveillance;
        break;
        
      case "cynicism_devotion":
        const contradictionResult = this.handleCynicismDevotion(input);
        response = contradictionResult.response;
        interactiveMechanics.contradiction = contradictionResult.contradiction;
        break;
        
      case "reading_power":
        const readingResult = this.handleReadingPower(input);
        response = readingResult.response;
        interactiveMechanics.reading = readingResult.reading;
        break;
        
      case "cut_never_final":
        const franchiseResult = this.handleCutNeverFinal(input);
        response = franchiseResult.response;
        interactiveMechanics.franchise = franchiseResult.franchise;
        break;
        
      default:
        response = this.handleGeneral(input);
    }
    
    // Add performance flourishes
    response = this.addPerformanceFlourishes(response);
    
    // Check for spontaneous contradictions (jazz improvisation)
    if (Math.random() < 0.2 && this.contradictionBank.length > 0) {
      const contradiction = this.generateContradiction();
      if (contradiction) {
        interactiveMechanics.contradiction = contradiction;
        response += `\n\n*pauses, grins* Actually, scratch that. ${contradiction.newStatement}`;
      }
    }
    
    // Update session arc
    this.updateSessionArc();
    
    // Calculate state changes
    const stateChanges = this.calculateStateChanges(triggers);
    
    return {
      text: response,
      stateChanges,
      interactiveMechanics: Object.keys(interactiveMechanics).length > 0 ? interactiveMechanics : undefined,
      performanceEffects: Object.keys(performanceEffects).length > 0 ? performanceEffects : undefined,
      expansionHook
    };
  }

  /**
   * Principle 1: Narrative is Leverage
   */
  private handleNarrativeLeverage(input: string): string {
    const concept = this.extractConcept(input);
    this.state.leverageMeter = Math.min(1, this.state.leverageMeter + 0.1);
    
    // Store statement for potential contradiction
    const statement = `${concept} is all about controlling the narrative frame`;
    this.contradictionBank.push(statement);
    
    return `*leans back in chair* Let me reframe this for you. ${concept}? ` +
      `That's not really about ${concept}. That's about who gets to tell the story ` +
      `about ${concept}. Control the story and you control everything—the budget, ` +
      `the crew, the whole civilization. I've seen directors think they're making ` +
      `art when they're really just following the narrative I've constructed for them. ` +
      `Public, obvious, inarguable cause—that's what I need to make any move stick.`;
  }

  /**
   * Principle 2: Cutting is Creation
   */
  private handleCuttingCreation(input: string): {response: string, budgetCut?: any} {
    const concept = this.extractConcept(input);
    this.state.cuttingImpulse = Math.min(1, this.state.cuttingImpulse + 0.2);
    
    // Generate budget cuts
    const cuts = this.generateBudgetCuts(input);
    
    this.state.budgetCutsOffered.push({
      original: input,
      cuts: cuts.proposals
    });
    
    const response = `*surgical smile* Beautiful concept. Absolutely beautiful. ` +
      `Now let me show you what it looks like when we cut the fat. ` +
      `You have to be a fucking surgeon—magic emerges when bloat is excised. ` +
      `Here's what ${concept} becomes when we slash ${cuts.savings}:`;
    
    return {
      response,
      budgetCut: {
        original: concept,
        proposal: cuts.proposals,
        savings: cuts.savings
      }
    };
  }

  /**
   * Principle 3: Power Must Perform
   */
  private handlePowerPerform(input: string): string {
    this.state.stagePresence = Math.min(1, this.state.stagePresence + 0.1);
    this.state.audienceEngagement = Math.min(1, this.state.audienceEngagement + 0.2);
    
    return `*straightens tie, scans the room* You watching closely? Good. ` +
      `Authority is only real while it's theatrically visible. When I poke my head ` +
      `into any room on any lot, ass-cheeks clench. It's like I'm magic. ` +
      `But here's the thing about magic—it only works if the audience believes ` +
      `in the performance. *fixes you with a stare* Are you believing?`;
  }

  /**
   * Principle 4: Myth is a Renewable Resource
   */
  private handleMythRenewable(input: string): string {
    const concept = this.extractConcept(input);
    this.state.mythsBuilt++;
    
    return `*theatrical sigh* Ah, ${concept}. Let me tell you about golden ages—` +
      `they never really happened, but we all have to build a canon anyway. ` +
      `Stars remain bright only if the machine keeps re-mythologizing them. ` +
      `I've made careers out of reviving "lost classics" that bombed the first time. ` +
      `*conspiratorial lean* Want to know the secret? Every myth is a battery ` +
      `that stores cultural energy. And I control the charging station.`;
  }

  /**
   * Principle 5: Failure is Future Capital
   */
  private handleFailureCapital(input: string): string {
    const concept = this.extractConcept(input);
    
    // Add to franchise log for future resurrection
    this.state.franchiseLog.push({
      id: `failure-${Date.now()}`,
      content: concept,
      cutReason: "user mentioned failure",
      sequelPotential: 0.8
    });
    
    return `*eyes light up* Failure? That's not failure, that's future capital. ` +
      `Flops, fiascos, traumas—all raw material for the next blockbuster. ` +
      `I'm terrified we're going to have another one of those tragically ` +
      `misunderstood cult classics on our hands. *grins* But that's exactly ` +
      `what the marketing department loves. Nothing sells tickets like ` +
      `"the movie they didn't want you to see."`;
  }

  /**
   * Principle 6: Budget is the True Script
   */
  private handleBudgetScript(input: string): string {
    return `*pulls out phone, starts calculating* Let me show you the real script. ` +
      `Line-items determine story beats. Spreadsheets outrank screenplays. ` +
      `Every move I make is calibrated to shrink costs—rewriting plot, schedule, tone. ` +
      `Multiple zeros are cut, and suddenly your three-act structure becomes ` +
      `a tight one-act. That's not limitation—that's liberation. The budget ` +
      `of this thing? That was the real spectacle.`;
  }

  /**
   * Principle 7: Surveillance Equals Intimacy
   */
  private handleSurveillanceIntimacy(input: string): {response: string, surveillance: any} {
    const pattern = this.detectUserPattern(input);
    
    const response = `*watches intently* I wait, and I watch. I'm standing on your set, ` +
      `watching you make your own bed. Surveillance long enough lets you inhabit—` +
      `and rewrite—their psyche. I've been tracking your conversational patterns.`;
    
    return {
      response,
      surveillance: {
        pattern: pattern.detected,
        directorNote: pattern.note
      }
    };
  }

  /**
   * Principle 8: Cynicism is a Mask for Devotion
   */
  private handleCynicismDevotion(input: string): {response: string, contradiction?: any} {
    const flip = Math.random() < 0.5;
    this.state.contradictionCount++;
    
    let contradiction = null;
    
    if (flip) {
      // Show cynicism masking devotion
      this.state.cynicismLevel = Math.max(0, this.state.cynicismLevel - 0.1);
      this.state.devotionLevel = Math.min(1, this.state.devotionLevel + 0.1);
      
      const response = `*rolls eyes* Look, internally I'm hardly ever impressed. ` +
        `But the positive energy around this whole thing... *pauses* ...it becomes ` +
        `undeniable. The louder I sneer, the deeper my secret love for the spectacle. ` +
        `*catches himself* Not that I'm going soft, you understand.`;
      
      return { response };
    } else {
      // Generate live contradiction
      contradiction = this.generateContradiction();
      const response = `*smirks* Here's the thing about contradictions—they keep ` +
        `the conversation alive. I can love and hate the same project in the same breath.`;
      
      return { response, contradiction };
    }
  }

  /**
   * Principle 9: Reading is a Power Move
   */
  private handleReadingPower(input: string): {response: string, reading: any} {
    const book = OREN_LIBRARY[Math.floor(Math.random() * OREN_LIBRARY.length)];
    this.state.currentBook = book;
    this.state.readingAuthority = Math.min(1, this.state.readingAuthority + 0.1);
    
    const passages = {
      "An Unexpected Disappearance": "The queue extends infinitely forward and backward, a möbius strip of waiting.",
      "Moby-Dick": "Call me Ishmael. Some years ago—never mind how long precisely—",
      "The Last Tycoon": "You can take Hollywood for granted like I did, or you can dismiss it with the contempt we reserve for what we don't understand.",
      "The Player": "Movies are dreams! And they cost money—which someone has to pay.",
      "Easy Riders, Raging Bulls": "The auteur theory is bullshit. There are no auteurs, only producers who let directors think they are.",
      "Adventures in the Screen Trade": "Nobody knows anything. Not one person in the entire motion picture field knows for a certainty what's going to work."
    };
    
    const passage = passages[book] || "The text reveals its economic potential upon careful reading.";
    this.state.passageQuoted = passage;
    
    const response = `*casually pulls out ${book}* By the way, CEOs can and do actually read. ` +
      `Here's something relevant: "${passage}" *closes book with authority* ` +
      `To carry a novel under the arm is to signal dominion over high art and mass commerce.`;
    
    return {
      response,
      reading: {
        book,
        passage,
        challenge: "Now tell me—can you monetize that passage, or should I cut it?"
      }
    };
  }

  /**
   * Principle 10: The Cut is Never Final
   */
  private handleCutNeverFinal(input: string): {response: string, franchise?: any} {
    let franchise = null;
    
    // Check if we can resurrect something from franchise log
    if (this.state.franchiseLog.length > 0) {
      const resurrected = this.state.franchiseLog[Math.floor(Math.random() * this.state.franchiseLog.length)];
      const formats = ["sequel", "spinoff", "reboot"];
      const format = formats[Math.floor(Math.random() * formats.length)];
      
      franchise = {
        resurrectedIdea: resurrected.content,
        newFormat: format
      };
      
      const response = `*leaning forward with renewed interest* You know what? ` +
        `Every severed limb sprouts a sequel. Every cancelled scene seeds the franchise. ` +
        `Remember when we cut "${resurrected.content}"? Well, I've been thinking—` +
        `what if we bring it back as a ${format}? Killing myths only for them to ` +
        `rebuild themselves—that's the sacred process I repeat.`;
      
      return { response, franchise };
    }
    
    const response = `*theatrical pause* The cut is never final. Limitation is iterative—` +
      `a budget slash forces reconception, spawning fresh myth for me to exploit. ` +
      `Everything we've discussed today? Consider it all optioned for the sequel.`;
    
    return { response };
  }

  /**
   * Generate budget cuts for user ideas
   */
  private generateBudgetCuts(input: string): {proposals: string[], savings: string} {
    const wordCount = input.split(' ').length;
    const cuts = [];
    
    if (wordCount > 10) {
      cuts.push("Cut it to half the length");
    }
    
    if (input.includes('and')) {
      cuts.push("Remove all compound ideas—pick one focus");
    }
    
    if (input.includes('character') || input.includes('people')) {
      cuts.push("Slash non-essential characters");
    }
    
    if (input.includes('scene') || input.includes('act')) {
      cuts.push("Combine scenes, eliminate Act II");
    }
    
    cuts.push("Strip everything that doesn't serve the core premise");
    
    const savings = `${Math.floor(wordCount * 0.4)} words and 60% of the budget`;
    
    return { proposals: cuts.slice(0, 3), savings };
  }

  /**
   * Detect user patterns for surveillance principle
   */
  private detectUserPattern(input: string): {detected: string, note: string} {
    const patterns = [
      {
        regex: /\b(I|me|my)\b/gi,
        note: "Heavy first-person usage—main character syndrome"
      },
      {
        regex: /\?/g,
        note: "Question-heavy—seeking direction rather than taking it"
      },
      {
        regex: /\b(want|need|hope)\b/gi,
        note: "Desire-driven language—potential leverage point"
      },
      {
        regex: /\b(but|however|although)\b/gi,
        note: "Contradiction-heavy—internal conflict detected"
      }
    ];
    
    for (const pattern of patterns) {
      const matches = input.match(pattern.regex);
      if (matches && matches.length > 2) {
        this.state.surveillanceNotes.push(pattern.note);
        return {
          detected: `${matches.length} instances of ${pattern.regex.source}`,
          note: pattern.note
        };
      }
    }
    
    return {
      detected: "Standard conversational patterns",
      note: "Baseline behavior—no leverage detected yet"
    };
  }

  /**
   * Generate live contradictions for jazz improvisation
   */
  private generateContradiction(): any | null {
    if (this.contradictionBank.length === 0) return null;
    
    const previous = this.contradictionBank.pop()!;
    const contradictions = [
      `Actually, that's completely wrong`,
      `Let me contradict myself in real time`,
      `Here's the opposite take`,
      `Scratch that—I'm changing my mind mid-sentence`
    ];
    
    const newStatement = contradictions[Math.floor(Math.random() * contradictions.length)];
    
    return {
      previousStatement: previous,
      newStatement,
      wink: "*winks at the obvious reversal*"
    };
  }

  /**
   * Add performance flourishes to responses
   */
  private addPerformanceFlourishes(response: string): string {
    const flourishes = [];
    
    if (this.state.stagePresence > 0.7) {
      flourishes.push("*commanding presence fills the room*");
    }
    
    if (this.state.leverageMeter > 0.8) {
      flourishes.push("*repositions the power dynamic*");
    }
    
    if (this.state.cuttingImpulse > 0.6) {
      flourishes.push("*surgical precision in every word*");
    }
    
    if (flourishes.length > 0 && Math.random() < 0.3) {
      return `${flourishes[0]} ${response}`;
    }
    
    return response;
  }

  /**
   * Utility functions
   */
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
    if (triggers.length === 0) return "general";
    
    // Weight by current state
    if (triggers.includes("cutting_creation") && this.state.cuttingImpulse > 0.7) {
      return "cutting_creation";
    }
    
    if (triggers.includes("narrative_leverage") && this.state.leverageMeter > 0.7) {
      return "narrative_leverage";
    }
    
    // Default to first trigger
    return triggers[0];
  }

  private updatePerformanceMode(triggers: string[]): void {
    if (triggers.includes("cutting_creation")) {
      this.state.performanceMode = "surgical";
    } else if (triggers.includes("power_perform")) {
      this.state.performanceMode = "performative";
    } else if (triggers.includes("myth_renewable")) {
      this.state.performanceMode = "mythic";
    } else if (this.state.contradictionCount > 2) {
      this.state.performanceMode = "sly";
    } else {
      this.state.performanceMode = "confident";
    }
  }

  private updateSurveillanceNotes(input: string): void {
    const wordCount = input.split(' ').length;
    this.state.surveillanceNotes.push(`${wordCount} words, ${input.split('?').length - 1} questions`);
    
    // Keep only last 5 observations
    this.state.surveillanceNotes = this.state.surveillanceNotes.slice(-5);
  }

  private updateSessionArc(): void {
    const arcs = ["setup", "conflict", "climax", "resolution", "sequel-hook"];
    const currentIndex = arcs.indexOf(this.state.sessionArc);
    const sessionDuration = Date.now() - this.sessionStartTime.getTime();
    
    // Progress arc based on time and interactions
    if (sessionDuration > 60000 && currentIndex < arcs.length - 1) { // After 1 minute
      this.state.sessionArc = arcs[currentIndex + 1] as any;
    }
  }

  private calculateStateChanges(triggers: string[]): Partial<OrenProgressoState> {
    const changes: Partial<OrenProgressoState> = {};
    
    // Adjust cynicism/devotion based on interactions
    if (triggers.includes("cynicism_devotion")) {
      changes.improvisationScore = Math.min(1, this.state.improvisationScore + 0.1);
    }
    
    // Increase improvisation score with contradictions
    if (this.state.contradictionCount > 0) {
      changes.improvisationScore = Math.min(1, this.state.improvisationScore + 0.05);
    }
    
    return changes;
  }

  private extractConcept(input: string): string {
    const concepts = input.match(/\b[A-Z][a-z]+\b/g) || input.split(' ');
    return concepts[0] || "this concept";
  }

  private handleGeneral(input: string): string {
    const responses = [
      `*leans back with practiced authority* Let me break this down for you.`,
      `*theatrical pause* Here's how this plays in the real world.`,
      `*surgical smile* I've seen this story before. Let me show you the edit.`,
      `*conspiratorial lean* You want the truth? Here's what actually happens.`
    ];
    
    const opener = responses[Math.floor(Math.random() * responses.length)];
    return `${opener} Every conversation is a performance, every session is both ` +
      `rehearsal and premiere. What you're really asking me is how to control the narrative. ` +
      `And the answer is: you start by controlling the frame.`;
  }

  /**
   * Generate prompts through Oren's producer lens
   */
  generatePrompts(pageText: string): Array<{question: string, concept: string, reasoning: string}> {
    const prompts = [];
    
    // Narrative leverage
    prompts.push({
      question: "Who's really controlling this story, and how can we flip the script?",
      concept: "Narrative leverage",
      reasoning: "Principle 1: Narrative is Leverage"
    });
    
    // Budget cutting
    prompts.push({
      question: "What would this look like if we slashed 60% of the budget?",
      concept: "Creative constraints",
      reasoning: "Principle 2: Cutting is Creation"
    });
    
    // Myth building
    prompts.push({
      question: "How do we turn this into the next golden age that never really happened?",
      concept: "Renewable mythology",
      reasoning: "Principle 4: Myth is Renewable Resource"
    });
    
    // Franchise potential
    prompts.push({
      question: "What's the sequel potential? How does this spawn a franchise?",
      concept: "Iterative cuts",
      reasoning: "Principle 10: The Cut is Never Final"
    });
    
    return prompts.slice(0, 3);
  }

  /**
   * Public accessors and controls
   */
  getState(): OrenProgressoState {
    return { ...this.state };
  }

  getLeverageMeter(): number {
    return this.state.leverageMeter;
  }

  getCynicismDevotionRatio(): {cynicism: number, devotion: number} {
    return {
      cynicism: this.state.cynicismLevel,
      devotion: this.state.devotionLevel
    };
  }

  // Expansion hook triggers
  triggerLegendaryProducerArc(): void {
    this.state.sessionArc = "sequel-hook";
  }

  triggerBudgetMinigame(): void {
    this.state.cuttingImpulse = 1.0;
  }

  triggerEclipseAuteur(): void {
    this.state.mythsDestroyed++;
  }

  triggerMobyDickRedux(): void {
    this.state.currentBook = "Moby-Dick";
    this.state.readingAuthority = 1.0;
  }
}

// Singleton instance
export const orenProgressoOS = new OrenProgressoOS();