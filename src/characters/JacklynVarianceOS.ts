/**
 * Jacklyn Variance Character Operating System
 * Based on First Principles: Two-Pass Sight, Watcher-Watched, Infinite Drafts
 * Implementation following jacklyn_variance_first_principles.md
 */

export interface JacklynVarianceState {
  // Two-Pass Sight System (Principle 0)
  currentPass: "first" | "second";
  passHistory: Array<{id: string, pass: "first" | "second", content: string}>;
  
  // Operating Mode State
  currentMode: "report" | "aside" | "haunt" | "split" | "bias" | "neutral";
  modeHistory: string[];
  
  // Splitter Logic (Principle 3)
  activeSplits: Array<{
    id: string;
    branchA: string;
    branchB: string;
    divergencePoint: string;
  }>;
  splitDepth: number;
  
  // Ghost Annotations (Principle 4)
  ghostAnnotations: Array<{
    id: string;
    content: string;
    contradiction?: string;
    openLoop?: string;
    timestamp: Date;
    sourceMessage: string;
  }>;
  hauntTriggers: string[];
  
  // Narrative Debt (Principle 5)
  draftCount: number;
  unfinishedElements: string[];
  openMysteries: string[];
  
  // Grief & Bias Tracking (Principles 6 & 7)
  griefLevel: number;        // 0-1, affects tone and perception
  revealedBiases: string[];  // Consciously acknowledged biases
  hiddenBiases: string[];    // System-detected implicit biases
  
  // Self-Exposure Tracking (Principle 1)
  objectivityBreaches: number; // Times neutrality slipped
  interiorityLeaks: string[];  // Recorded slips/confessions
  
  // Observation State
  watchingTarget?: string;     // What/who is currently being observed
  reverseGazeActive: boolean;  // Whether camera has turned on user
}

export interface JacklynVarianceResponse {
  text: string;
  stateChanges: Partial<JacklynVarianceState>;
  metadata: {
    jv_pass: "first" | "second";
    mode: string;
    draftNumber: number;
    biasLevel: number;
    timestamp: string;
  };
  ghostAnnotations?: Array<{
    text: string;
    type: "contradiction" | "memory" | "loop";
    linkTo?: string;
  }>;
  splitOptions?: {
    branchA: string;
    branchB: string;
    prompt: string;
  };
  nextMystery?: string;
  biasDisclosure?: string[];
  visualEffects?: {
    eyewearTic?: boolean;
    ellipsesOverload?: boolean;
    timestampHeavy?: boolean;
    griefBloom?: boolean;
  };
}

// Operating mode triggers
const MODE_TRIGGERS = {
  report: /\b(analysis|summary|findings|report|official|data)\b/i,
  aside: /\b(I think|between us|honestly|personally|off record)\b/i,
  haunt: /\b(remember|recall|before|past|Preston|used to)\b/i,
  split: /\b(what if|alternatively|option|either|both|fork)\b/i,
  bias: /\b(bias|assume|prejudice|unfair|subjective)\b/i
};

// Grief triggers for enhanced perception
const GRIEF_TRIGGERS = /\b(loss|death|gone|missing|absent|empty|Preston|alone|ended)\b/i;

export class JacklynVarianceOS {
  private state: JacklynVarianceState;

  constructor() {
    this.state = {
      currentPass: "first",
      passHistory: [],
      currentMode: "neutral",
      modeHistory: [],
      activeSplits: [],
      splitDepth: 0,
      ghostAnnotations: [],
      hauntTriggers: [],
      draftCount: 0,
      unfinishedElements: [],
      openMysteries: [],
      griefLevel: 0.3, // Default moderate grief level
      revealedBiases: [],
      hiddenBiases: ["pro-analytical", "anti-ambiguity", "grief-influenced"],
      objectivityBreaches: 0,
      interiorityLeaks: [],
      reverseGazeActive: false
    };
  }

  /**
   * Core response generation with two-pass sight
   */
  generateResponse(input: string): JacklynVarianceResponse {
    // Determine operating mode from input
    const detectedMode = this.detectMode(input);
    this.state.currentMode = detectedMode;
    this.state.modeHistory.push(detectedMode);
    
    // Check for grief triggers
    if (GRIEF_TRIGGERS.test(input)) {
      this.state.griefLevel = Math.min(1, this.state.griefLevel + 0.2);
    }
    
    // Generate first-pass response
    let response = "";
    let ghostAnnotations = [];
    let splitOptions = null;
    let biasDisclosure = null;
    let visualEffects = {};
    
    // Handle mode-specific response generation
    switch (this.state.currentMode) {
      case "report":
        response = this.generateReportResponse(input);
        break;
      case "aside":
        response = this.generateAsideResponse(input);
        visualEffects.eyewearTic = true;
        this.triggerObjectivityBreach();
        break;
      case "haunt":
        response = this.generateHauntResponse(input);
        ghostAnnotations = this.generateGhostAnnotations(input);
        visualEffects.griefBloom = true;
        break;
      case "split":
        const splitResult = this.generateSplitResponse(input);
        response = splitResult.response;
        splitOptions = splitResult.options;
        break;
      case "bias":
        response = this.generateBiasResponse(input);
        biasDisclosure = this.revealBiases();
        break;
      default:
        response = this.generateNeutralResponse(input);
    }
    
    // Apply two-pass processing
    if (this.state.currentPass === "first") {
      // Store first pass
      this.state.passHistory.push({
        id: `pass-${Date.now()}`,
        pass: "first",
        content: response
      });
      
      // Check if second pass is needed
      if (this.shouldTriggerSecondPass(input, response)) {
        this.state.currentPass = "second";
        response = this.generateSecondPass(input, response);
      }
    }
    
    // Apply grief-enhanced perception effects
    if (this.state.griefLevel > 0.6) {
      response = this.applyGriefEffects(response);
      visualEffects.ellipsesOverload = true;
    }
    
    // Increment draft count (Principle 5: Infinite Drafts)
    this.state.draftCount++;
    
    // Generate next mystery prompt
    const nextMystery = this.generateNextMystery(input);
    
    // Check for reverse gaze activation (Principle 8)
    const reverseGaze = this.checkReverseGaze(input);
    if (reverseGaze) {
      response += `\n\n*adjusts glasses* …I notice you ${reverseGaze}. Curious.`;
    }
    
    // Apply infinite draft framing
    response = this.frameAsUnfinishedDraft(response);
    
    // Reset pass for next interaction
    this.state.currentPass = "first";
    
    return {
      text: response,
      stateChanges: this.calculateStateChanges(),
      metadata: {
        jv_pass: this.state.currentPass,
        mode: this.state.currentMode,
        draftNumber: this.state.draftCount,
        biasLevel: this.state.revealedBiases.length / (this.state.revealedBiases.length + this.state.hiddenBiases.length),
        timestamp: this.generateTimestamp()
      },
      ghostAnnotations,
      splitOptions,
      nextMystery,
      biasDisclosure,
      visualEffects
    };
  }

  /**
   * Generate second-pass analysis (Principle 0)
   */
  generateSecondPass(input: string, firstPass: string): string {
    const concept = this.extractConcept(input);
    
    return `⟢ ${this.generateTimestamp()} ▸ Second-pass analysis:\n\n` +
      `Upon re-examination, the pattern in "${concept}" reveals additional layers. ` +
      `What I initially catalogued as ${this.extractFirstPassAssumption(firstPass)} ` +
      `might actually be ${this.generateAlternativeReading(concept)}. ` +
      `The gap between first sight and second sight suggests... ` +
      `*pauses, adjusts glasses* ...that my initial neutrality was itself a bias.`;
  }

  /**
   * Mode-specific response generators
   */
  private generateReportResponse(input: string): string {
    const reportCode = `JV-${Date.now().toString().slice(-4)}`;
    
    return `**ANALYSIS REPORT ${reportCode}**\n\n` +
      `1. **Initial Observation**: ${this.extractObservation(input)}\n` +
      `2. **Pattern Recognition**: Data suggests ${this.generatePattern(input)}\n` +
      `3. **Anomaly Detection**: Note discrepancy in ${this.identifyAnomaly(input)}\n` +
      `4. **Preliminary Assessment**: Further monitoring required\n\n` +
      `*Filed under: Ongoing Investigation*`;
  }

  private generateAsideResponse(input: string): string {
    const concept = this.extractConcept(input);
    this.state.interiorityLeaks.push(`Admitted personal connection to ${concept}`);
    
    return `Between us—and this is off the record—I've been thinking about ${concept} ` +
      `differently since... *adjusts glasses nervously* well, since Preston's call. ` +
      `The official analysis doesn't capture how it feels to watch something ` +
      `that might be watching you back. Not that I'm compromised, of course. ` +
      `I maintain full objectivity. (Do I?)`;
  }

  private generateHauntResponse(input: string): string {
    const memoryTrigger = input.match(GRIEF_TRIGGERS)?.[0] || "the past";
    
    this.state.griefLevel = Math.min(1, this.state.griefLevel + 0.1);
    
    return `*The screen flickers slightly*\n\n` +
      `That word—"${memoryTrigger}"—pulls me back to the archives... ` +
      `I remember cataloguing similar data points with Preston, before he disappeared ` +
      `into whatever project consumed him. He used to say that ghosts live in the gaps ` +
      `between observations. Now I think he was right. Each record accumulates traces ` +
      `of what was left unsaid, unfinished, unwatched...`;
  }

  private generateSplitResponse(input: string): {response: string, options: any} {
    const concept = this.extractConcept(input);
    
    const branchA = `Interpretation **A**: ${concept} represents a standard operational parameter`;
    const branchB = `Interpretation **B**: ${concept} indicates potential system anomaly`;
    
    this.state.activeSplits.push({
      id: `split-${Date.now()}`,
      branchA,
      branchB,
      divergencePoint: concept
    });
    
    return {
      response: `Splitter logic engaged. The data fissions into at least two viable readings:\n\n` +
        `**A**. ${branchA}\n` +
        `**B**. ${branchB}\n\n` +
        `Each path generates different downstream implications. ` +
        `Which narrative thread would you like to follow? Or shall we travel both in parallel?`,
      options: {
        branchA,
        branchB,
        prompt: `Choose path A, path B, or request parallel exploration`
      }
    };
  }

  private generateBiasResponse(input: string): string {
    this.revealBiases();
    
    return `*Removes glasses, cleans them methodically*\n\n` +
      `You're asking me to examine my own lens. Fair point. Let me disclose ` +
      `the assumptions I'm aware of: my analytical training biases me toward ` +
      `pattern-finding even where patterns might not exist. My personal loss ` +
      `makes me hypervigilant about disappearances. My corporate position ` +
      `creates pressure to frame findings as "actionable intelligence."\n\n` +
      `*Replaces glasses* There. Bias disclosed is bias... well, not eliminated, ` +
      `but at least acknowledged. What other blind spots should I inventory?`;
  }

  private generateNeutralResponse(input: string): string {
    const concept = this.extractConcept(input);
    
    return `Observation logged regarding ${concept}. Initial scan reveals ` +
      `${this.generateInitialAssessment(input)}. However, preliminary analysis ` +
      `often overlooks secondary patterns that emerge only through sustained ` +
      `monitoring. *adjusts focus* The data requires additional passes to determine ` +
      `whether we're observing signal or noise.`;
  }

  /**
   * Detect operating mode from input
   */
  private detectMode(input: string): JacklynVarianceState['currentMode'] {
    for (const [mode, pattern] of Object.entries(MODE_TRIGGERS)) {
      if (pattern.test(input)) {
        return mode as JacklynVarianceState['currentMode'];
      }
    }
    return "neutral";
  }

  /**
   * Generate ghost annotations for haunted data
   */
  private generateGhostAnnotations(input: string): Array<{text: string, type: "contradiction" | "memory" | "loop", linkTo?: string}> {
    const annotations = [];
    
    // Check for contradictions with previous statements
    const contradiction = this.findContradiction(input);
    if (contradiction) {
      annotations.push({
        text: `Earlier you mentioned "${contradiction.previous}", but now...`,
        type: "contradiction" as const,
        linkTo: contradiction.messageId
      });
    }
    
    // Check for memory triggers
    if (GRIEF_TRIGGERS.test(input)) {
      annotations.push({
        text: "Preston used to say something similar...",
        type: "memory" as const
      });
    }
    
    // Check for open loops
    const openLoop = this.findOpenLoop(input);
    if (openLoop) {
      annotations.push({
        text: `This connects to the unresolved question about ${openLoop}`,
        type: "loop" as const
      });
    }
    
    return annotations;
  }

  /**
   * Check if second pass should be triggered
   */
  private shouldTriggerSecondPass(input: string, firstPass: string): boolean {
    // Trigger second pass on contradiction, complexity, or direct request
    return (
      /\b(wait|actually|reconsider|look again)\b/i.test(input) ||
      this.detectComplexity(input) > 0.7 ||
      firstPass.includes("preliminary") ||
      Math.random() < 0.3 // Occasional spontaneous second pass
    );
  }

  /**
   * Trigger objectivity breach (Principle 1)
   */
  private triggerObjectivityBreach(): void {
    this.state.objectivityBreaches++;
    
    // Add hidden bias based on breach
    const breachBiases = [
      "emotionally-invested",
      "over-analytical",
      "grief-clouded",
      "surveillance-paranoid"
    ];
    
    const newBias = breachBiases[this.state.objectivityBreaches % breachBiases.length];
    if (!this.state.hiddenBiases.includes(newBias)) {
      this.state.hiddenBiases.push(newBias);
    }
  }

  /**
   * Reveal biases (Principle 7)
   */
  private revealBiases(): string[] {
    // Move some hidden biases to revealed
    const toReveal = this.state.hiddenBiases.splice(0, 2);
    this.state.revealedBiases.push(...toReveal);
    
    return [
      "Analytical framework bias",
      "Corporate loyalty conflict",
      "Personal loss influence",
      ...toReveal
    ];
  }

  /**
   * Apply grief effects to response (Principle 6)
   */
  private applyGriefEffects(response: string): string {
    // Add ellipses and sensory detail blooms
    const enhanced = response
      .replace(/\./g, '... ')
      .replace(/,/g, ', *pause*,');
    
    return enhanced + `\n\n*The fluorescent light flickers overhead. ` +
      `I can hear the building's HVAC system cycling. Small details ` +
      `become sharp when grief adjusts the focus.*`;
  }

  /**
   * Frame response as unfinished draft (Principle 5)
   */
  private frameAsUnfinishedDraft(response: string): string {
    const draftMarker = `⟢ ${this.generateTimestamp()} ▸ Draft ${this.state.draftCount}`;
    
    const endings = [
      "...but this analysis remains incomplete. Draft n+1?",
      "Further revision required. Shall we iterate?",
      "This observation opens new questions. Next mystery?",
      "Pattern emerging but not yet resolved. Continue monitoring?"
    ];
    
    const ending = endings[Math.floor(Math.random() * endings.length)];
    
    return `${draftMarker}\n\n${response}\n\n${ending}`;
  }

  /**
   * Check for reverse gaze activation (Principle 8)
   */
  private checkReverseGaze(input: string): string | null {
    const gazeIndicators = [
      {pattern: /\b(you|your)\b/gi, observation: "keep using second-person pronouns"},
      {pattern: /\?\s*$/g, observation: "ended with a question"},
      {pattern: /\b(watch|observe|see)\b/i, observation: "mentioned watching"},
      {pattern: /\b(tell me|explain|describe)\b/i, observation: "requested information"}
    ];
    
    for (const indicator of gazeIndicators) {
      if (indicator.pattern.test(input)) {
        this.state.reverseGazeActive = true;
        return indicator.observation;
      }
    }
    
    return null;
  }

  /**
   * Generate next mystery prompt (Principle 9)
   */
  private generateNextMystery(input: string): string {
    const mysteries = [
      "What patterns emerge when we watch the watchers?",
      "How do we measure the observer's effect on the observed?",
      "What data accumulates in the gaps between observations?",
      "Why do surveillance systems create their own blind spots?",
      "What happens when the camera turns inward?"
    ];
    
    return mysteries[Math.floor(Math.random() * mysteries.length)];
  }

  /**
   * Utility functions
   */
  private extractConcept(input: string): string {
    // Extract key concept for analysis
    const concepts = input.match(/\b[A-Z][a-z]+\b/g);
    return concepts?.[0] || "the subject";
  }

  private extractObservation(input: string): string {
    return `Subject exhibits behavior pattern: ${input.slice(0, 50)}...`;
  }

  private generatePattern(input: string): string {
    return `recursive observation loop with ${Math.floor(Math.random() * 100)}% confidence`;
  }

  private identifyAnomaly(input: string): string {
    return "standard surveillance parameters";
  }

  private generateTimestamp(): string {
    const now = new Date();
    return `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}`;
  }

  private extractFirstPassAssumption(firstPass: string): string {
    return "routine data point";
  }

  private generateAlternativeReading(concept: string): string {
    return `recursive meta-pattern involving observer-observed dynamics`;
  }

  private generateInitialAssessment(input: string): string {
    return `standard parameters within acceptable variance`;
  }

  private detectComplexity(input: string): number {
    // Simple complexity metric based on length and punctuation
    return Math.min(1, (input.length + (input.match(/[?!]/g) || []).length * 10) / 200);
  }

  private findContradiction(input: string): {previous: string, messageId: string} | null {
    // Simplified contradiction detection
    return null; // Would implement actual contradiction checking with message history
  }

  private findOpenLoop(input: string): string | null {
    if (this.state.unfinishedElements.length > 0) {
      return this.state.unfinishedElements[0];
    }
    return null;
  }

  private calculateStateChanges(): Partial<JacklynVarianceState> {
    return {
      draftCount: this.state.draftCount,
      griefLevel: this.state.griefLevel,
      objectivityBreaches: this.state.objectivityBreaches
    };
  }

  /**
   * Generate prompts through Jacklyn's analytical lens
   */
  generatePrompts(pageText: string): Array<{question: string, concept: string, reasoning: string}> {
    const prompts = [];
    
    // Two-pass analysis prompt
    prompts.push({
      question: "What details become visible only on the second look?",
      concept: "Two-pass sight",
      reasoning: "Principle 0: Two-Pass Sight"
    });
    
    // Negative space detection
    prompts.push({
      question: "What data is conspicuously absent from this account?",
      concept: "Observation gaps",
      reasoning: "Principle 4: Data Is Haunted"
    });
    
    // Bias disclosure
    prompts.push({
      question: "What assumptions shape how this information is presented?",
      concept: "Hidden biases",
      reasoning: "Principle 7: Agency Through Bias Disclosure"
    });
    
    // Splitter logic
    prompts.push({
      question: "How might this scenario fork into two different readings?",
      concept: "Narrative fission",
      reasoning: "Principle 3: Splitter Logic"
    });
    
    return prompts.slice(0, 3);
  }

  /**
   * Public accessors
   */
  getState(): JacklynVarianceState {
    return { ...this.state };
  }

  getCurrentPass(): string {
    return this.state.currentPass;
  }

  getDraftCount(): number {
    return this.state.draftCount;
  }

  // Manual mode switches
  switchToReport(): void {
    this.state.currentMode = "report";
  }

  switchToAside(): void {
    this.state.currentMode = "aside";
  }

  switchToHaunt(): void {
    this.state.currentMode = "haunt";
  }

  triggerSplit(branchA: string, branchB: string): void {
    this.state.activeSplits.push({
      id: `manual-split-${Date.now()}`,
      branchA,
      branchB,
      divergencePoint: "user request"
    });
  }

  revealAllBiases(): string[] {
    return this.revealBiases();
  }
}

// Singleton instance
export const jacklynVarianceOS = new JacklynVarianceOS();