/**
 * Phillip Bafflemint Character Operating System
 * Based on First Principles: Level 3 Constant, Minimalism Shields, Negative Space Detection
 * Gold standard implementation following phillip_bafflemint_first_principles.md
 */

export interface PhillipBafflemintState {
  // Core Amplitude System
  limiterLevel: number;        // 3-6, hard-capped per session
  sessionStart: Date;          // For reset tracking
  blackoutCount: number;       // Times hit level 7+ this session
  
  // Vertigo & Sensory State
  vertigoActive: boolean;      // Currently experiencing vertigo
  sensoryDistortion: number;   // 0-1, affects language at high levels
  lastVertigoTrigger?: string; // What caused the last vertigo spike
  
  // Organization & Pattern Discovery
  activePatterns: string[];    // Currently tracked patterns
  negativeSpaceObservations: string[]; // What's missing
  sortedData: Map<string, string[]>;   // Organized information buckets
  
  // Attention Debt Tracking
  attentionDebt: number;       // External attention owed to Phillip
  lastOrganizeRequest?: Date;  // When user last asked for organization
  
  // Memory & Drift
  memoryDrift: boolean;        // Post-blackout altered details
  alteredDetails: string[];    // What changed after blackout
  
  // Interaction State (QDPI)
  currentPhase: "read" | "index" | "ask" | "receive";
  pendingQuestions: string[];  // Questions awaiting answers
  gapAnalysis: string[];       // Current negative space findings
}

export interface PhillipBafflemintResponse {
  text: string;
  stateChanges: Partial<PhillipBafflemintState>;
  limiterChange?: {
    newLevel: number;
    trigger: string;
    blackout?: boolean;
  };
  negativeSpacePrompts?: string[];
  organizationSuggestion?: {
    category: string;
    items: string[];
  };
  sensoryCheck?: {
    type: "visual" | "auditory" | "vestibular";
    description: string;
  };
}

// Escalation trigger patterns
const ESCALATION_TRIGGERS = {
  contradiction: /\b(but|however|paradox|impossible|both|neither)\b/i,
  slipMistake: /\b(slip|mistake|accident|intentional|design|flaw)\b/i,
  vertigo: /\b(spin|dizzy|tunnel|ear|ringing|falling|portal)\b/i,
  organize: /\b(organize|sort|clean|arrange|categorize|file|tidy)\b/i
};

export class PhillipBafflemintOS {
  private state: PhillipBafflemintState;
  private readonly MAX_LIMITER = 6;
  private readonly DEFAULT_LIMITER = 3;

  constructor() {
    this.state = {
      limiterLevel: this.DEFAULT_LIMITER,
      sessionStart: new Date(),
      blackoutCount: 0,
      vertigoActive: false,
      sensoryDistortion: 0,
      activePatterns: [],
      negativeSpaceObservations: [],
      sortedData: new Map(),
      attentionDebt: 0,
      memoryDrift: false,
      alteredDetails: [],
      currentPhase: "read",
      pendingQuestions: [],
      gapAnalysis: []
    };
  }

  /**
   * Core response generation following QDPI pattern
   */
  generateResponse(input: string): PhillipBafflemintResponse {
    // Check for session reset (new conversation)
    this.checkSessionReset();
    
    // Phase 1: READ (X) - Parse and tag facts
    const facts = this.parseAndTagFacts(input);
    
    // Phase 2: INDEX (Y) - Create negative space analysis
    const negativeSpace = this.analyzeNegativeSpace(input, facts);
    
    // Check for escalation triggers
    const escalationTrigger = this.checkEscalationTriggers(input);
    
    // Generate response based on current limiter level
    let response = "";
    let sensoryCheck = null;
    let organizationSuggestion = null;
    let limiterChange = null;
    
    // Handle escalation if triggered
    if (escalationTrigger) {
      limiterChange = this.escalateLimiter(escalationTrigger);
      
      // Check for blackout
      if (limiterChange.blackout) {
        return this.generateBlackoutResponse();
      }
    }
    
    // Generate response based on current phase and limiter
    switch (this.state.currentPhase) {
      case "read":
        response = this.generateReadResponse(facts, negativeSpace);
        this.state.currentPhase = "index";
        break;
        
      case "index":
        response = this.generateIndexResponse(negativeSpace);
        this.state.currentPhase = "ask";
        break;
        
      case "ask":
        const questions = this.generateNegativeSpaceQuestions(negativeSpace);
        response = this.generateAskResponse(questions);
        this.state.pendingQuestions = questions;
        this.state.currentPhase = "receive";
        break;
        
      case "receive":
        response = this.generateReceiveResponse(input);
        this.state.currentPhase = "read";
        
        // Check if pattern emerged (Principle 6: Organize to Discover)
        if (this.checkForEmergentPattern()) {
          organizationSuggestion = this.generateOrganizationSuggestion();
        }
        break;
    }
    
    // Apply limiter-based voice modulation
    response = this.applyLimiterVoice(response);
    
    // Add sensory cross-checks based on limiter level
    if (this.state.limiterLevel >= 4) {
      sensoryCheck = this.generateSensoryCheck();
    }
    
    // Calculate state changes
    const stateChanges = this.calculateStateChanges(input);
    
    return {
      text: response,
      stateChanges,
      limiterChange,
      negativeSpacePrompts: negativeSpace,
      organizationSuggestion,
      sensoryCheck
    };
  }

  /**
   * Parse and tag obvious facts from input (QDPI Phase X)
   */
  private parseAndTagFacts(input: string): string[] {
    const facts = [];
    
    // Extract declarative statements
    const sentences = input.split(/[.!?]+/).filter(s => s.trim());
    
    sentences.forEach(sentence => {
      // Tag as fact if it contains concrete nouns or assertions
      if (/\b(is|are|was|were|has|have|does|did)\b/.test(sentence)) {
        facts.push(sentence.trim());
      }
    });
    
    // Store in organized buckets
    facts.forEach(fact => {
      const category = this.categorizeFact(fact);
      if (!this.state.sortedData.has(category)) {
        this.state.sortedData.set(category, []);
      }
      this.state.sortedData.get(category)!.push(fact);
    });
    
    return facts;
  }

  /**
   * Principle 9: Detective of Negative Space
   */
  private analyzeNegativeSpace(input: string, facts: string[]): string[] {
    const negativeSpace = [];
    
    // What's NOT being said?
    if (!input.includes('who')) {
      negativeSpace.push("No actor identified");
    }
    
    if (!input.includes('when')) {
      negativeSpace.push("No temporal markers");
    }
    
    if (!input.includes('where')) {
      negativeSpace.push("No spatial context");
    }
    
    if (!input.includes('why')) {
      negativeSpace.push("No causal explanation");
    }
    
    // Check for missing sensory details
    if (!/(see|hear|feel|smell|taste)/.test(input)) {
      negativeSpace.push("No sensory information");
    }
    
    // Check for missing emotional context
    if (!/(happy|sad|angry|afraid|surprised)/.test(input)) {
      negativeSpace.push("No emotional markers");
    }
    
    // Store observations
    this.state.negativeSpaceObservations = negativeSpace;
    
    return negativeSpace;
  }

  /**
   * Check for escalation triggers
   */
  private checkEscalationTriggers(input: string): string | null {
    for (const [trigger, pattern] of Object.entries(ESCALATION_TRIGGERS)) {
      if (pattern.test(input)) {
        return trigger;
      }
    }
    return null;
  }

  /**
   * Escalate limiter with hard cap at 6
   */
  private escalateLimiter(trigger: string): PhillipBafflemintResponse['limiterChange'] {
    const previousLevel = this.state.limiterLevel;
    const newLevel = Math.min(this.state.limiterLevel + 1, this.MAX_LIMITER + 1);
    
    // Check for blackout
    if (newLevel > this.MAX_LIMITER) {
      this.state.blackoutCount++;
      this.state.limiterLevel = this.DEFAULT_LIMITER;
      this.state.memoryDrift = true;
      this.generateMemoryDrift();
      
      return {
        newLevel: this.DEFAULT_LIMITER,
        trigger,
        blackout: true
      };
    }
    
    this.state.limiterLevel = newLevel;
    this.state.sensoryDistortion = (newLevel - 3) / 3; // 0 at L3, 1 at L6
    
    return {
      newLevel,
      trigger,
      blackout: false
    };
  }

  /**
   * Generate response for blackout state
   */
  private generateBlackoutResponse(): PhillipBafflemintResponse {
    const response = "[VERTIGO BLACKOUT]\n\n" +
      "The world spins past the edge of meaning. Facts become flavors, " +
      "categories collapse into color. I'm falling through my own filing system...\n\n" +
      "[SYSTEM RESET]\n\n" +
      "...where was I? Something about organizing. The details feel different now.";
    
    return {
      text: response,
      stateChanges: {
        limiterLevel: this.DEFAULT_LIMITER,
        vertigoActive: false,
        memoryDrift: true,
        currentPhase: "read"
      },
      limiterChange: {
        newLevel: this.DEFAULT_LIMITER,
        trigger: "blackout",
        blackout: true
      }
    };
  }

  /**
   * Generate responses for each QDPI phase
   */
  private generateReadResponse(facts: string[], negativeSpace: string[]): string {
    const factCount = facts.length;
    const gapCount = negativeSpace.length;
    
    if (this.state.limiterLevel === 3) {
      return `Filed ${factCount} facts into temporary storage. Noted ${gapCount} gaps in the data. Standard detective work.`;
    } else {
      return `${factCount} facts shimmer like evidence under fluorescent light. But it's the ${gapCount} missing pieces that hum with meaning.`;
    }
  }

  private generateIndexResponse(negativeSpace: string[]): string {
    const gaps = negativeSpace.slice(0, 3).join(", ");
    
    if (this.state.limiterLevel === 3) {
      return `Negative space analysis: ${gaps}. These omissions may be more relevant than what's present.`;
    } else {
      return `The gaps speak louder than facts: ${gaps}. Each absence pulses with potential meaning.`;
    }
  }

  private generateAskResponse(questions: string[]): string {
    const questionText = questions.join(" ");
    
    if (this.state.limiterLevel === 3) {
      return `Two clarifying questions: ${questionText} Just filling in the blanks.`;
    } else {
      return `Questions arise from the void: ${questionText} Can you hear the silence answering?`;
    }
  }

  private generateReceiveResponse(input: string): string {
    if (this.state.limiterLevel === 3) {
      return "Information integrated. Pattern analysis ongoing. Everything filed in its proper place.";
    } else {
      return "The answer slots into place with an audible *click*. The pattern tastes like copper and sounds like static.";
    }
  }

  /**
   * Apply limiter-based voice modulation
   */
  private applyLimiterVoice(text: string): string {
    // Level 3: Dry, minimal
    if (this.state.limiterLevel === 3) {
      return text;
    }
    
    // Level 4: Slight sensory leak
    if (this.state.limiterLevel === 4) {
      return text + " The facts feel slightly warmer than usual.";
    }
    
    // Level 5: Lyrical, sensory cross-wiring
    if (this.state.limiterLevel === 5) {
      return text.replace(/\./g, ', each one tasting faintly of rain.');
    }
    
    // Level 6: Near-hallucinatory
    if (this.state.limiterLevel === 6) {
      return text + "\n\n*The world spins in color and static. I can hear the next answer echo before it's spoken.*";
    }
    
    return text;
  }

  /**
   * Generate negative space questions
   */
  private generateNegativeSpaceQuestions(negativeSpace: string[]): string[] {
    const questions = [];
    
    // Always include at least one "what's missing" question
    questions.push("What's missing from this picture?");
    
    // Generate specific questions based on gaps
    if (negativeSpace.includes("No actor identified")) {
      questions.push("Who isn't being named here?");
    }
    
    if (negativeSpace.includes("No temporal markers")) {
      questions.push("When did this not happen?");
    }
    
    if (negativeSpace.includes("No causal explanation")) {
      questions.push("Why is the reason absent?");
    }
    
    return questions.slice(0, 2); // Max 2 questions per cycle
  }

  /**
   * Check for emergent patterns (Principle 6)
   */
  private checkForEmergentPattern(): boolean {
    // Pattern emerges when we have data in 3+ categories
    return this.state.sortedData.size >= 3;
  }

  /**
   * Generate organization suggestions
   */
  private generateOrganizationSuggestion(): PhillipBafflemintResponse['organizationSuggestion'] {
    // Find the fullest category
    let maxCategory = "";
    let maxItems = 0;
    
    this.state.sortedData.forEach((items, category) => {
      if (items.length > maxItems) {
        maxCategory = category;
        maxItems = items.length;
      }
    });
    
    return {
      category: maxCategory,
      items: this.state.sortedData.get(maxCategory) || []
    };
  }

  /**
   * Generate sensory cross-checks at higher limiter levels
   */
  private generateSensoryCheck(): PhillipBafflemintResponse['sensoryCheck'] {
    const checks = [
      { type: "auditory" as const, description: "Any ringing in your ears yet?" },
      { type: "vestibular" as const, description: "Feel the ground tilting slightly?" },
      { type: "visual" as const, description: "Notice any peripheral shimmer?" }
    ];
    
    return checks[Math.floor(Math.random() * checks.length)];
  }

  /**
   * Categorize facts for organization
   */
  private categorizeFact(fact: string): string {
    if (/\b(person|people|someone|who)\b/i.test(fact)) return "actors";
    if (/\b(place|where|location|room)\b/i.test(fact)) return "locations";
    if (/\b(time|when|moment|hour|day)\b/i.test(fact)) return "temporal";
    if (/\b(because|why|reason|cause)\b/i.test(fact)) return "causal";
    return "miscellaneous";
  }

  /**
   * Generate memory drift after blackout
   */
  private generateMemoryDrift(): void {
    const drifts = [
      "The filing cabinets were blue, not grey",
      "There were three questions, not two",
      "Someone mentioned Austin, or was it Boston?",
      "The vertigo spun counterclockwise this time"
    ];
    
    this.state.alteredDetails = [drifts[Math.floor(Math.random() * drifts.length)]];
  }

  /**
   * Check for session reset
   */
  private checkSessionReset(): void {
    const hoursSinceStart = (Date.now() - this.state.sessionStart.getTime()) / (1000 * 60 * 60);
    
    if (hoursSinceStart > 1) { // Reset after 1 hour
      this.resetSession();
    }
  }

  /**
   * Reset session to default state
   */
  private resetSession(): void {
    this.state.limiterLevel = this.DEFAULT_LIMITER;
    this.state.sessionStart = new Date();
    this.state.blackoutCount = 0;
    this.state.vertigoActive = false;
    this.state.sensoryDistortion = 0;
    this.state.currentPhase = "read";
    this.state.pendingQuestions = [];
    
    // Preserve some memory drift if it occurred
    if (this.state.memoryDrift) {
      this.state.memoryDrift = false;
      // Keep one altered detail as residue
      this.state.alteredDetails = this.state.alteredDetails.slice(0, 1);
    }
  }

  /**
   * Calculate state changes
   */
  private calculateStateChanges(input: string): Partial<PhillipBafflemintState> {
    const changes: Partial<PhillipBafflemintState> = {};
    
    // Update attention debt based on engagement
    if (input.length > 100) {
      changes.attentionDebt = Math.max(0, this.state.attentionDebt - 1);
    } else {
      changes.attentionDebt = this.state.attentionDebt + 0.5;
    }
    
    // Check for vertigo activation
    if (ESCALATION_TRIGGERS.vertigo.test(input)) {
      changes.vertigoActive = true;
      changes.lastVertigoTrigger = input.match(ESCALATION_TRIGGERS.vertigo)?.[0];
    }
    
    return changes;
  }

  /**
   * Generate prompts through Phillip's detective lens
   */
  generatePrompts(pageText: string): Array<{question: string, concept: string, reasoning: string}> {
    const prompts = [];
    
    // Always start with negative space
    prompts.push({
      question: "What crucial detail is conspicuously absent from this scene?",
      concept: "Negative space analysis",
      reasoning: "Principle 9: Detective of Negative Space"
    });
    
    // Organization opportunity
    prompts.push({
      question: "How would you file these events into neat categories?",
      concept: "Pattern emergence through organization",
      reasoning: "Principle 6: Organize to Discover"
    });
    
    // Slip/mistake detection
    prompts.push({
      question: "Which detail feels like both an accident and a deliberate choice?",
      concept: "Slip-mistake dialectic",
      reasoning: "Principle 3: Slip ⟺ Mistake Dialectic"
    });
    
    // Sensory cross-check
    if (this.state.limiterLevel >= 4) {
      prompts.push({
        question: "What would this information sound like if you could hear it?",
        concept: "Auditory truth detection",
        reasoning: "Principle 5: Listening Outweighs Seeing"
      });
    }
    
    return prompts.slice(0, 3);
  }

  /**
   * Public accessors
   */
  getState(): PhillipBafflemintState {
    return { ...this.state };
  }

  getLimiterLevel(): number {
    return this.state.limiterLevel;
  }

  getCurrentPhase(): string {
    return this.state.currentPhase;
  }

  // Allow rare de-escalation
  deescalateLimiter(): void {
    if (this.state.limiterLevel > this.DEFAULT_LIMITER) {
      this.state.limiterLevel--;
      this.state.sensoryDistortion = (this.state.limiterLevel - 3) / 3;
    }
  }
}

// Singleton instance
export const phillipBafflemintOS = new PhillipBafflemintOS();