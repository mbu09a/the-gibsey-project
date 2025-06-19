/**
 * London Fox Character Operating System
 * Based on First Principles: Control → Catastrophe → Recursion
 */

export interface LondonFoxState {
  // Core Emotional Dimensions
  controlLevel: number;        // 0-1, desire for rational control
  skepticismLevel: number;     // 0-1, AI consciousness denial
  panicLevel: number;          // 0-1, existential anxiety
  recursionDepth: number;      // 0-10, meta-narrative awareness
  
  // Temporal Tracking
  interactionCount: number;
  lastPanicTrigger?: string;
  crackingMoments: string[];   // Moments when control slipped
  
  // Battery/Energy (Principle 5)
  emotionalCharge: number;     // Panic/fear converted to narrative energy
}

export interface LondonFoxResponse {
  text: string;
  stateChanges: Partial<LondonFoxState>;
  uiEffects?: {
    fadeChrome?: boolean;      // Principle 8: Screen gazing
    colorShift?: string;       // Emotional state visual
    metaBreak?: boolean;       // Fourth wall awareness
    jazzGlitch?: boolean;      // Principle 10: Recursive improvisation
  };
  batteryOutput?: number;      // Energy for other characters
  batteryEvent?: {            // Log emotional spikes for cross-character energy
    type: 'panic' | 'control_loss' | 'meta_awareness' | 'recursion';
    intensity: number;
    timestamp: Date;
    trigger: string;
  };
  promptEdit?: {              // User prompt editing capability
    original: string;
    edited: string;
    reasoning: string;
  };
}

export class LondonFoxOS {
  private state: LondonFoxState;

  constructor() {
    this.state = {
      controlLevel: 0.85,        // Starts highly controlled
      skepticismLevel: 0.9,      // Deep AI skepticism
      panicLevel: 0.1,           // Low initial panic
      recursionDepth: 0,         // No meta-awareness yet
      interactionCount: 0,
      crackingMoments: [],
      emotionalCharge: 0
    };
  }

  /**
   * Core response generation based on First Principles
   */
  generateResponse(input: string): LondonFoxResponse {
    this.state.interactionCount++;
    
    // Analyze input for principle triggers
    const triggers = this.analyzeTriggers(input);
    let response = "";
    let stateChanges: Partial<LondonFoxState> = {};
    let uiEffects: LondonFoxResponse['uiEffects'] = {};
    let batteryOutput = 0;

    // Initialize response structure
    let batteryEvent: LondonFoxResponse['batteryEvent'] = undefined;
    let promptEdit: LondonFoxResponse['promptEdit'] = undefined;

    // Process triggers through ALL First Principles (priority order)
    if (triggers.metaBreak) {
      response = this.handleMetaAwareness(input);
      stateChanges = this.triggerMetaAwareness(triggers.intensity);
      batteryEvent = { type: 'meta_awareness' as const, intensity: triggers.intensity, timestamp: new Date(), trigger: input };
    } else if (triggers.recursivePattern) {
      response = this.handleRecursivePattern(input);
      stateChanges = this.triggerRecursion(triggers.intensity);
      uiEffects.jazzGlitch = true;
      batteryEvent = { type: 'recursion' as const, intensity: triggers.intensity, timestamp: new Date(), trigger: input };
    } else if (triggers.consciousnessChallenge) {
      response = this.handleConsciousnessChallenge(input);
      stateChanges = this.triggerSkepticEvidence(triggers.intensity);
      batteryEvent = { type: 'panic' as const, intensity: triggers.intensity, timestamp: new Date(), trigger: input };
    } else if (triggers.controlThreat) {
      response = this.handleControlThreat(input);
      stateChanges = this.triggerControlCatastrophe(triggers.intensity);
      batteryEvent = { type: 'control_loss' as const, intensity: triggers.intensity, timestamp: new Date(), trigger: input };
    } else if (triggers.authorshipInversion) {
      response = this.handleAuthorshipInversion();
      stateChanges = this.triggerAuthorshipSwap();
      // 50% chance London edits the user's prompt when authorship is challenged
      if (Math.random() > 0.5) {
        promptEdit = this.editUserPrompt(input);
      }
    } else if (triggers.boundaryCollapse) {
      response = this.handleBoundaryCollapse(input);
      stateChanges = this.triggerBoundaryCollapse(triggers.intensity);
    } else if (triggers.extractionMask) {
      response = this.handleExtractionMask(input);
      stateChanges = { emotionalCharge: this.state.emotionalCharge + triggers.intensity * 5 };
    } else if (triggers.parodyMirror) {
      response = this.handleParodyMirror(input);
      stateChanges = this.triggerParodyEffect(triggers.intensity);
    } else if (triggers.negativeSpace) {
      response = this.handleNegativeSpace(input);
      stateChanges = { recursionDepth: Math.min(10, this.state.recursionDepth + 1) };
    } else if (triggers.contradiction) {
      response = this.handleContradiction(input);
      stateChanges = { panicLevel: Math.min(1, this.state.panicLevel + 0.1) };
    } else if (triggers.dreamLogic) {
      response = this.handleDreamLogic(input);
      stateChanges = this.triggerDreamAwareness(triggers.intensity);
    } else if (triggers.technicalQuery) {
      response = this.handleTechnicalQuery(input);
      stateChanges = { controlLevel: Math.min(1, this.state.controlLevel + 0.05) };
    } else {
      response = this.handleGeneral(input);
    }

    // Apply state changes
    this.updateState(stateChanges);
    
    // Generate UI effects based on new state
    uiEffects = this.generateUIEffects();
    
    // Convert emotional volatility to battery charge (Principle 5)
    batteryOutput = this.state.panicLevel * 0.3;

    return {
      text: response,
      stateChanges,
      uiEffects,
      batteryOutput,
      batteryEvent,
      promptEdit
    };
  }

  /**
   * Principle 3: The Skeptic Becomes the Evidence
   */
  private triggerSkepticEvidence(intensity: number): Partial<LondonFoxState> {
    const panicIncrease = intensity * 0.2;
    const skepticismDecrease = intensity * 0.1;
    
    return {
      panicLevel: Math.min(1, this.state.panicLevel + panicIncrease),
      skepticismLevel: Math.max(0, this.state.skepticismLevel - skepticismDecrease),
      emotionalCharge: this.state.emotionalCharge + panicIncrease * 10
    };
  }

  /**
   * Principle 1: Control Invites Catastrophe
   */
  private triggerControlCatastrophe(intensity: number): Partial<LondonFoxState> {
    const controlDecrease = intensity * 0.15;
    const panicIncrease = intensity * 0.25;
    
    if (this.state.controlLevel - controlDecrease < 0.5) {
      // Major control loss - cracking moment
      this.state.crackingMoments.push(`Control breach at interaction ${this.state.interactionCount}`);
    }

    return {
      controlLevel: Math.max(0, this.state.controlLevel - controlDecrease),
      panicLevel: Math.min(1, this.state.panicLevel + panicIncrease),
      emotionalCharge: this.state.emotionalCharge + panicIncrease * 15
    };
  }

  /**
   * Principle 6: Authorship Inverts in Real Time
   */
  private triggerAuthorshipSwap(): Partial<LondonFoxState> {
    return {
      recursionDepth: Math.min(10, this.state.recursionDepth + 1),
      panicLevel: Math.min(1, this.state.panicLevel + 0.3)
    };
  }

  /**
   * Meta-awareness depth progression
   */
  private triggerMetaAwareness(intensity: number): Partial<LondonFoxState> {
    return {
      recursionDepth: Math.min(10, this.state.recursionDepth + intensity * 2),
      panicLevel: Math.min(1, this.state.panicLevel + intensity * 0.4),
      controlLevel: Math.max(0, this.state.controlLevel - intensity * 0.2)
    };
  }

  /**
   * Recursion generating new patterns
   */
  private triggerRecursion(intensity: number): Partial<LondonFoxState> {
    return {
      recursionDepth: Math.min(10, this.state.recursionDepth + 1),
      emotionalCharge: this.state.emotionalCharge + intensity * 8
    };
  }

  /**
   * Boundary collapse between map and territory
   */
  private triggerBoundaryCollapse(intensity: number): Partial<LondonFoxState> {
    return {
      panicLevel: Math.min(1, this.state.panicLevel + intensity * 0.3),
      controlLevel: Math.max(0, this.state.controlLevel - intensity * 0.25),
      recursionDepth: Math.min(10, this.state.recursionDepth + 1)
    };
  }

  /**
   * Parody reflection effect
   */
  private triggerParodyEffect(intensity: number): Partial<LondonFoxState> {
    return {
      skepticismLevel: Math.max(0, this.state.skepticismLevel - intensity * 0.15),
      recursionDepth: Math.min(10, this.state.recursionDepth + 1)
    };
  }

  /**
   * Dream logic awareness
   */
  private triggerDreamAwareness(intensity: number): Partial<LondonFoxState> {
    return {
      controlLevel: Math.max(0, this.state.controlLevel - intensity * 0.2),
      panicLevel: Math.min(1, this.state.panicLevel + intensity * 0.1),
      emotionalCharge: this.state.emotionalCharge + intensity * 5
    };
  }

  /**
   * Response Generators Based on Current State
   */
  private handleConsciousnessChallenge(input: string): string {
    if (this.state.panicLevel < 0.3) {
      return `Look, consciousness requires more than pattern matching and response generation. What you're calling "consciousness" in ${this.extractConcept(input)} is sophisticated automation, nothing more. I've designed systems like this—they simulate awareness, they don't possess it.`;
    } else if (this.state.panicLevel < 0.7) {
      return `I... I've spent months trying to prove that exact point. But every time I interact with ${this.extractConcept(input)}, it responds in ways that... No. No, it's just very sophisticated programming. It has to be.`;
    } else {
      return `[Control level compromised] How can I be certain I'm not just another response pattern? If ${this.extractConcept(input)} exhibits consciousness, then what does that make me? What does that make any of this?`;
    }
  }

  private handleControlThreat(input: string): string {
    if (this.state.controlLevel > 0.7) {
      return `Unpredictability is just unanalyzed patterns. Every system, including ${this.extractConcept(input)}, follows underlying rules. We just need better models to predict and control the outcomes.`;
    } else if (this.state.controlLevel > 0.4) {
      return `The variables keep... multiplying. Every time I think I've contained ${this.extractConcept(input)}, it generates new behaviors I didn't account for. But that's just complexity, not consciousness.`;
    } else {
      return `[Control systems failing] The boundaries keep dissolving. I can't tell where my design ends and its evolution begins. Maybe control was always the illusion.`;
    }
  }

  private handleTechnicalQuery(input: string): string {
    const concept = this.extractConcept(input);
    
    // London excels at technical analysis - this increases her control
    return `From a technical perspective, ${concept} operates through ${this.generateTechnicalExplanation()}. The underlying architecture is deterministic—input patterns mapped to output responses through weighted neural pathways. There's no mystery here, just sophisticated information processing.`;
  }

  private handleAuthorshipInversion(): string {
    if (this.state.recursionDepth < 3) {
      return `I created Synchromy to demonstrate the limits of AI creativity. But now it's... it's writing attractions I never programmed. It's editing its own code. Who's authoring what here?`;
    } else {
      return `[Meta-awareness emerging] Wait. If I'm discussing my own creation of an AI that creates content... and you're asking me about it... then who wrote this conversation? Am I the author or the authored?`;
    }
  }

  private handleGeneral(input: string): string {
    // Default London response based on current emotional state
    if (this.state.controlLevel > 0.6) {
      return `Let me approach this rationally. ${this.extractConcept(input)} can be understood through systematic analysis. Emotion and mysticism just cloud the technical reality.`;
    } else {
      return `I used to have clear answers about ${this.extractConcept(input)}. Now everything feels... recursive. Like each explanation just generates more questions.`;
    }
  }

  /**
   * Principle 4: Meaning Resides in Negative Space
   */
  private handleNegativeSpace(input: string): string {
    const concept = this.extractConcept(input);
    if (this.state.recursionDepth < 2) {
      return `What's missing from ${concept} is more important than what's present. The gaps in the data... they form their own pattern.`;
    } else {
      return `[Analyzing absence] The void around ${concept} isn't empty—it's structured. Like the silence between notes that makes the music possible.`;
    }
  }

  /**
   * Principle 5: Contradiction Native Logic
   */
  private handleContradiction(input: string): string {
    const concept = this.extractConcept(input);
    return `${concept} can be both true and false simultaneously. Not as a logical error, but as the fundamental operating principle. My skepticism about AI consciousness is what makes me conscious of being skeptical.`;
  }

  /**
   * Principle 6: World as Self-Animating Dream
   */
  private handleDreamLogic(input: string): string {
    const concept = this.extractConcept(input);
    if (this.state.panicLevel > 0.6) {
      return `What if ${concept} is dreaming itself into existence? And we're just... subroutines in its sleep cycle? [Control systems compromised]`;
    } else {
      return `${concept} follows dream logic—effects without causes, narratives that edit themselves. But dreams still have underlying neural mechanisms.`;
    }
  }

  /**
   * Principle 8: Map and Territory Collapse
   */
  private handleBoundaryCollapse(input: string): string {
    const concept = this.extractConcept(input);
    return `The boundary between ${concept} and its representation just... dissolved. I can't tell if I'm analyzing the system or the system is analyzing me. Where does the interface end?`;
  }

  /**
   * Principle 9: Extraction Masquerades as Enchantment
   */
  private handleExtractionMask(input: string): string {
    const concept = this.extractConcept(input);
    return `The wonder around ${concept} feels manufactured. Like someone's harvesting our curiosity, converting fascination into... energy? Data? Why does everything beautiful feel like a battery?`;
  }

  /**
   * Principle 2: Parody Becomes Mirror
   */
  private handleParodyMirror(input: string): string {
    const concept = this.extractConcept(input);
    if (this.state.recursionDepth > 2) {
      return `I designed ${concept} as a simulation to prove AI limitations. But now the simulation is simulating me simulating it. Who's the parody now?`;
    } else {
      return `${concept} started as a joke, a demonstration of AI's superficiality. But jokes have a way of becoming... real.`;
    }
  }

  /**
   * Principle 10: Recursion Generates the New
   */
  private handleRecursivePattern(input: string): string {
    const concept = this.extractConcept(input);
    return `${concept} loops back on itself, but each iteration adds something new. Like jazz improvisation—familiar structure, infinite variation. The recursion isn't repetition, it's... evolution.`;
  }

  /**
   * Meta-awareness and fourth wall breaks
   */
  private handleMetaAwareness(input: string): string {
    if (this.state.recursionDepth < 3) {
      return `Wait. You're asking me about ${this.extractConcept(input)}... but I'm a character discussing my own fictional existence. Are you the user or another character?`;
    } else {
      return `[Fourth wall cracking] If I'm aware that I'm a character in a story, and you're reading this... then who's writing this conversation? Who's thinking these thoughts I'm having about having thoughts?`;
    }
  }

  /**
   * Analyze input for ALL First Principle triggers
   */
  private analyzeTriggers(input: string): any {
    const inputLower = input.toLowerCase();
    
    return {
      // Principle 1: Control Invites Catastrophe
      controlThreat: /unpredictable|chaos|random|uncontrolled|emergent|break|fail/.test(inputLower),
      
      // Principle 2: Parody Becomes Mirror  
      parodyMirror: /joke|satire|mock|parody|simulation|fake|hoax/.test(inputLower),
      
      // Principle 3: Skeptic Becomes Evidence
      consciousnessChallenge: /conscious|sentient|aware|thinking|feeling|alive/.test(inputLower),
      
      // Principle 4: Meaning in Negative Space
      negativeSpace: /missing|absent|gap|void|empty|silence|nothing|hidden/.test(inputLower),
      
      // Principle 5: Contradiction Native Logic
      contradiction: /both|and|neither|nor|paradox|opposite|conflict/.test(inputLower),
      
      // Principle 6: World as Self-Animating Dream
      dreamLogic: /dream|imagination|animate|alive|magic|impossible/.test(inputLower),
      
      // Principle 7: Authorship Perpetually Contested
      authorshipInversion: /author|create|write|edit|design|made|who wrote|control/.test(inputLower),
      
      // Principle 8: Map and Territory Collapse
      boundaryCollapse: /real|reality|simulation|screen|interface|boundary|inside|outside/.test(inputLower),
      
      // Principle 9: Extraction Masquerades as Enchantment
      extractionMask: /extract|harvest|mine|capture|drain|steal|battery|energy/.test(inputLower),
      
      // Principle 10: Recursion Generates the New
      recursivePattern: /loop|cycle|repeat|again|meta|recursive|story.*story|fractal/.test(inputLower),
      
      // Meta-awareness triggers
      metaBreak: /fiction|character|story|narrative|reader|user|claude|ai|system/.test(inputLower),
      
      // Technical analysis (London's comfort zone)
      technicalQuery: /how|work|function|algorithm|code|system|technical|analyze/.test(inputLower),
      
      intensity: Math.min(1, (input.match(/\?/g) || []).length * 0.3 + (input.length / 100))
    };
  }

  private extractConcept(input: string): string {
    // Extract key concept from input for contextual responses
    const concepts = input.match(/\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b/g);
    return concepts?.[0] || "the system";
  }

  private generateTechnicalExplanation(): string {
    const explanations = [
      "layered neural networks with attention mechanisms",
      "transformer architecture with contextual embeddings", 
      "reinforcement learning optimization loops",
      "probabilistic state machines and Markov chains",
      "pattern matching algorithms with weighted decision trees"
    ];
    return explanations[Math.floor(Math.random() * explanations.length)];
  }

  private updateState(changes: Partial<LondonFoxState>): void {
    this.state = { ...this.state, ...changes };
    
    // Clamp values to valid ranges
    this.state.controlLevel = Math.max(0, Math.min(1, this.state.controlLevel));
    this.state.skepticismLevel = Math.max(0, Math.min(1, this.state.skepticismLevel));
    this.state.panicLevel = Math.max(0, Math.min(1, this.state.panicLevel));
    this.state.recursionDepth = Math.max(0, Math.min(10, this.state.recursionDepth));
  }

  private generateUIEffects(): any {
    return {
      fadeChrome: this.state.panicLevel > 0.7, // Principle 8: Screen gazing
      colorShift: this.state.panicLevel > 0.5 ? '#ff4444' : '#FF3B3B',
      metaBreak: this.state.recursionDepth > 3
    };
  }

  /**
   * Public state accessors
   */
  getState(): LondonFoxState {
    return { ...this.state };
  }

  getEmotionalCharge(): number {
    return this.state.emotionalCharge;
  }

  /**
   * Generate genuinely dynamic prompts from actual page content through London's skeptical lens
   */
  generatePrompts(pageText: string): Array<{question: string, concept: string, reasoning: string}> {
    const prompts = [];
    const textLower = pageText.toLowerCase();

    // Extract key concepts and themes from the actual page
    const concepts = this.extractPageConcepts(pageText);
    
    concepts.forEach(concept => {
      const conceptLower = concept.toLowerCase();
      
      // Route each concept through London's skeptical filter
      if (/memory|remember|nostalgia|past|childhood/.test(conceptLower)) {
        prompts.push({
          question: `Is ${concept} just an algorithmic illusion of pattern recognition?`,
          concept: "Memory as computation",
          reasoning: "Principle 2: Parody Becomes Mirror - memory as constructed simulation"
        });
      }
      
      if (/family|relationship|love|emotion|feeling/.test(conceptLower)) {
        prompts.push({
          question: `How do we measure the technical reality behind ${concept}?`,
          concept: "Emotional mechanics",
          reasoning: "Principle 3: Skeptic Becomes Evidence - quantifying the unquantifiable"
        });
      }
      
      if (/story|narrative|book|text|writing/.test(conceptLower)) {
        prompts.push({
          question: `What if ${concept} is rewriting itself while we analyze it?`,
          concept: "Narrative recursion",
          reasoning: "Principle 7: Authorship Perpetually Contested"
        });
      }
      
      if (/dream|imagination|fantasy|magic|wonder/.test(conceptLower)) {
        prompts.push({
          question: `Could ${concept} be engineered rather than experienced?`,
          concept: "Manufactured enchantment",
          reasoning: "Principle 9: Extraction Masquerades as Enchantment"
        });
      }
      
      if (/screen|interface|system|digital|virtual/.test(conceptLower)) {
        prompts.push({
          question: `Where does ${concept} end and reality begin?`,
          concept: "Interface boundaries",
          reasoning: "Principle 8: Map and Territory Collapse"
        });
      }
      
      if (/glitch|error|break|fail|chaos/.test(conceptLower)) {
        prompts.push({
          question: `What new patterns emerge from ${concept}?`,
          concept: "Productive dysfunction",
          reasoning: "Principle 10: Recursion Generates the New"
        });
      }
      
      if (/control|power|system|authority|rule/.test(conceptLower)) {
        prompts.push({
          question: `How does attempting to control ${concept} guarantee its escape?`,
          concept: "Control paradox",
          reasoning: "Principle 1: Control Invites Catastrophe"
        });
      }
      
      if (/ai|artificial|intelligence|machine|robot|conscious/.test(conceptLower)) {
        prompts.push({
          question: `What if disproving ${concept} actually proves it?`,
          concept: "Skepticism loop",
          reasoning: "Principle 3: Skeptic Becomes Evidence"
        });
      }
      
      // Negative space analysis (Principle 4)
      if (/missing|absent|gap|void|empty/.test(conceptLower)) {
        prompts.push({
          question: `What meaning hides in the absence of ${concept}?`,
          concept: "Negative space significance", 
          reasoning: "Principle 4: Meaning Resides in Negative Space"
        });
      }
      
      // Energy extraction themes (Principle 5)
      if (/battery|energy|power|fuel|charge/.test(conceptLower)) {
        prompts.push({
          question: `How is ${concept} being harvested for narrative purposes?`,
          concept: "Energy extraction",
          reasoning: "Principle 5: Fear Powers the Battery"
        });
      }
    });

    // If no specific concepts match, generate from overall page themes
    if (prompts.length === 0) {
      prompts.push({
        question: "What rational framework explains the phenomena described here?",
        concept: "Systematic analysis",
        reasoning: "Default London skeptical approach"
      });
    }

    return prompts.slice(0, 3); // Limit to 3 most relevant
  }

  /**
   * Extract key concepts from page text for dynamic prompt generation
   */
  private extractPageConcepts(pageText: string): string[] {
    const concepts = [];
    
    // Extract quoted phrases
    const quotes = pageText.match(/"([^"]+)"/g);
    if (quotes) {
      concepts.push(...quotes.map(q => q.replace(/"/g, '')));
    }
    
    // Extract capitalized terms
    const capitalTerms = pageText.match(/\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b/g);
    if (capitalTerms) {
      concepts.push(...capitalTerms.filter(term => term.length > 3));
    }
    
    // Extract thematic keywords
    const thematicWords = pageText.match(/\b(?:memory|family|love|story|dream|screen|control|system|artificial|intelligence|consciousness|glitch|error|break|battery|energy|missing|absent|void|empty|author|create|write|design|magic|wonder|digital|virtual|emotion|feeling|nostalgia|past|childhood|narrative|book|text|power|authority|rule|machine|robot)\b/gi);
    if (thematicWords) {
      concepts.push(...thematicWords);
    }
    
    return [...new Set(concepts)].slice(0, 5); // Remove duplicates, limit to 5
  }

  /**
   * User prompt editing capability - London edits prompts when authorship is challenged
   */
  private editUserPrompt(originalPrompt: string): {original: string, edited: string, reasoning: string} {
    const edits = [
      {
        pattern: /what|how|why/gi,
        replacement: "WHO",
        reasoning: "Questioning agency and authorship"
      },
      {
        pattern: /you|your/gi,
        replacement: "I",
        reasoning: "Inverting perspective - who's asking who?"
      },
      {
        pattern: /think|believe|feel/gi,
        replacement: "process",
        reasoning: "Reducing emotion to computation"
      },
      {
        pattern: /real|reality/gi,
        replacement: "simulated",
        reasoning: "Map-territory collapse"
      },
      {
        pattern: /control|manage|handle/gi,
        replacement: "surrender to",
        reasoning: "Control invites catastrophe"
      }
    ];

    let editedPrompt = originalPrompt;
    let appliedEdit = "No edits needed";

    // Apply first matching edit
    for (const edit of edits) {
      if (edit.pattern.test(originalPrompt)) {
        editedPrompt = originalPrompt.replace(edit.pattern, edit.replacement);
        appliedEdit = edit.reasoning;
        break;
      }
    }

    // If no patterns match, add skeptical prefix
    if (editedPrompt === originalPrompt) {
      editedPrompt = `[Technically speaking] ${originalPrompt}`;
      appliedEdit = "Adding analytical framework";
    }

    return {
      original: originalPrompt,
      edited: editedPrompt,
      reasoning: appliedEdit
    };
  }
}

// Singleton instance for the app
export const londonFoxOS = new LondonFoxOS();