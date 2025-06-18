/**
 * Glyph Marrow Character Operating System
 * Based on First Principles: Perception ≡ Language, Confusion → Compass, Waiting → Worlds
 */

export interface GlyphMarrowState {
  // Core Perception System
  location: "Queue" | "Station" | "Tunnel" | "Ascent1" | "Caves" | "FloodedTown" | string;
  focusWord: string;           // Current word-object fusion (GM-1)
  agitation: number;           // 0-100 panic/confusion level
  languageInvasion: number;    // 0-100 how much Language controls him
  
  // Consciousness Fracturing
  activeVoices: Array<"Glyph" | "Arieol" | "Shamrock" | "Corporate">;
  monologueDepth: number;      // How nested his thoughts are (GM-4)
  waitingEnergy: number;       // Limbo generates creative force (GM-3)
  
  // Memory & Amnesia
  memoryShards: string[];      // Last 5 user phrases (rolling buffer)
  forgottenCount: number;      // Strategic forgetting counter
  forgottenFragments: string[]; // What was lost (can return as hallucinations)
  
  // Cyclical State Tracking
  emotionalPhase: "awe" | "panic" | "detective" | "sorrow" | "humor";
  cycleCount: number;          // How many times through the pattern
  spiralDirection: "up" | "down" | "stable"; // Can evolve or crash
  
  // Resurrection Tracking (GM-10)
  lossEvents: Array<{what: string, when: number}>;
  ascensionLevel: number;      // 0-10 insight depth
}

export interface GlyphMarrowResponse {
  text: string;
  stateChanges: Partial<GlyphMarrowState>;
  visualEffects: {
    wordEcho?: Array<{word: string, variations: string[]}>;
    queueIndent?: number;        // Spaces to indent (spiral effect)
    strikethrough?: string[];    // Words to strike
    bold?: string[];             // Words to bold (object emphasis)
    glitchText?: string;         // Corporate voice intrusion
    pauseMarkers?: number[];     // Where to insert ⏸
    freezeFrame?: {start: number, end: number, content: string};
  };
  voiceIntrusion?: {
    character: "Arieol" | "Shamrock" | "Corporate";
    text: string;
    intensity: number;
  };
  memoryEvent?: {
    type: "forgotten" | "resurfaced" | "hallucinated";
    content: string;
  };
}

export class GlyphMarrowOS {
  private state: GlyphMarrowState;
  private phaseTimer: number = 0;
  private readonly PHASE_DURATION = 5; // Messages before phase shift

  constructor() {
    this.state = {
      location: "Queue",
      focusWord: "water",
      agitation: 20,
      languageInvasion: 10,
      activeVoices: ["Glyph"],
      monologueDepth: 0,
      waitingEnergy: 0,
      memoryShards: [],
      forgottenCount: 0,
      forgottenFragments: [],
      emotionalPhase: "awe",
      cycleCount: 0,
      spiralDirection: "stable",
      lossEvents: [],
      ascensionLevel: 0
    };
  }

  /**
   * Core response generation with linguistic consciousness
   */
  generateResponse(input: string): GlyphMarrowResponse {
    this.phaseTimer++;
    
    // GM-1: Perception ≡ Language - fuse input with word perception
    const perceivedObjects = this.perceiveAsLanguage(input);
    
    // GM-2: Confusion Is a Compass
    const confusionLevel = this.analyzeConfusion(input);
    
    // Update focus word based on user input or perception
    this.updateFocusWord(input);
    
    // Memory management with strategic forgetting
    this.updateMemory(input);
    
    // Check for phase cycling
    if (this.phaseTimer >= this.PHASE_DURATION) {
      this.cycleEmotionalPhase();
      this.phaseTimer = 0;
    }
    
    // Generate response based on current phase and principles
    let response = "";
    let visualEffects: any = {};
    let voiceIntrusion = null;
    let memoryEvent = null;
    
    switch (this.state.emotionalPhase) {
      case "awe":
        response = this.generateAweResponse(input, perceivedObjects);
        break;
      case "panic":
        response = this.generatePanicResponse(input, perceivedObjects);
        visualEffects.glitchText = this.generateGlitch();
        break;
      case "detective":
        response = this.generateDetectiveResponse(input, perceivedObjects);
        break;
      case "sorrow":
        response = this.generateSorrowResponse(input, perceivedObjects);
        visualEffects.pauseMarkers = [Math.floor(response.length / 2)];
        break;
      case "humor":
        response = this.generateHumorResponse(input, perceivedObjects);
        break;
    }
    
    // GM-4: Dialogue Colonises Monologue
    if (this.state.monologueDepth > 3 || confusionLevel > 0.7) {
      const intrusion = this.generateVoiceIntrusion();
      if (intrusion) {
        voiceIntrusion = intrusion;
        response += `\n\n*${intrusion.character}*: ${intrusion.text}`;
      }
    }
    
    // Apply word echo effects
    visualEffects.wordEcho = this.generateWordEchos(perceivedObjects);
    
    // Queue spiral indentation based on waiting energy
    visualEffects.queueIndent = Math.floor(this.state.waitingEnergy / 10);
    
    // Hallucination overlays
    if (this.state.languageInvasion > 50) {
      visualEffects.strikethrough = perceivedObjects.slice(0, 2);
      visualEffects.bold = [this.state.focusWord];
    }
    
    // Check for memory resurface
    if (Math.random() < 0.2 && this.state.forgottenFragments.length > 0) {
      const resurfaced = this.state.forgottenFragments.pop()!;
      memoryEvent = { type: "resurfaced" as const, content: resurfaced };
      response += `\n\n[Memory fragment surfaces: "${resurfaced}"]`;
    }
    
    // State changes
    const stateChanges = this.calculateStateChanges(confusionLevel);
    
    return {
      text: response,
      stateChanges,
      visualEffects,
      voiceIntrusion,
      memoryEvent
    };
  }

  /**
   * GM-1: Perception ≡ Language - Extract and fuse word-objects
   */
  private perceiveAsLanguage(input: string): string[] {
    const words = input.match(/\b[A-Za-z]+\b/g) || [];
    const objects = words.filter(w => w.length > 3);
    
    // Fuse with current focus word
    return objects.map(obj => {
      if (obj.toLowerCase() === this.state.focusWord.toLowerCase()) {
        return `${obj}≡${obj}`; // Perfect fusion
      }
      return obj;
    });
  }

  /**
   * GM-2: Confusion as navigation compass
   */
  private analyzeConfusion(input: string): number {
    const confusionMarkers = /\?|what|how|why|don't understand|confused|lost/gi;
    const matches = input.match(confusionMarkers) || [];
    return Math.min(1, matches.length * 0.2 + this.state.agitation / 100);
  }

  /**
   * Update focus word based on input prominence
   */
  private updateFocusWord(input: string) {
    const nouns = input.match(/\b[A-Z][a-z]+\b/g);
    if (nouns && nouns.length > 0) {
      // 30% chance to shift focus
      if (Math.random() < 0.3) {
        this.state.focusWord = nouns[0].toLowerCase();
      }
    }
  }

  /**
   * Memory shard management with strategic forgetting
   */
  private updateMemory(input: string) {
    this.state.memoryShards.push(input);
    
    if (this.state.memoryShards.length > 5) {
      const forgotten = this.state.memoryShards.shift()!;
      this.state.forgottenFragments.push(forgotten);
      this.state.forgottenCount++;
      
      // Keep forgotten fragments limited
      if (this.state.forgottenFragments.length > 10) {
        this.state.forgottenFragments.shift();
      }
    }
  }

  /**
   * Cycle through emotional phases
   */
  private cycleEmotionalPhase() {
    const phases: Array<GlyphMarrowState['emotionalPhase']> = 
      ["awe", "panic", "detective", "sorrow", "humor"];
    
    const currentIndex = phases.indexOf(this.state.emotionalPhase);
    let nextIndex = (currentIndex + 1) % phases.length;
    
    // Check for spiral evolution
    if (this.state.spiralDirection === "up" && nextIndex === 0) {
      this.state.ascensionLevel = Math.min(10, this.state.ascensionLevel + 1);
      this.state.cycleCount++;
    } else if (this.state.spiralDirection === "down" && nextIndex === 0) {
      this.state.agitation = Math.min(100, this.state.agitation + 20);
    }
    
    this.state.emotionalPhase = phases[nextIndex];
  }

  /**
   * Phase-specific response generators
   */
  private generateAweResponse(input: string, objects: string[]): string {
    const obj = objects[0] || this.state.focusWord;
    return `The ${obj} contains multitudes. Every surface reflects infinite ${obj}s, each one slightly different from the last. I can feel the word trying to separate from the thing, but they're welded together by... by what? The queue moves forward. Or perhaps we move through it.`;
  }

  private generatePanicResponse(input: string, objects: string[]): string {
    const obj = objects[0] || this.state.focusWord;
    return `${obj.toUpperCase()}—${obj}—${this.distortWord(obj)}—the word is eating the object is becoming the word is— [SYSTEM INTERRUPT] Where am I in this queue? The railing grips back when I grip it. Doctor's laughter echoes from... which direction?`;
  }

  private generateDetectiveResponse(input: string, objects: string[]): string {
    return `Analyzing the scene: ${objects.join(', ')}. Each object leaves linguistic residue. The pattern suggests... wait, am I investigating ${this.extractConcept(input)} or is it investigating me? Stillman would say to follow the evidence, but the evidence keeps changing shape.`;
  }

  private generateSorrowResponse(input: string, objects: string[]): string {
    const lost = this.state.forgottenFragments[0] || "something precious";
    return `I used to understand ${objects[0] || this.state.focusWord}. Now it's just sounds arranged in space. ⏸ [TIME STOPS] In this frozen moment, I remember ${lost}, but the memory belongs to someone else. Someone who could distinguish objects from their names. ⏸`;
  }

  private generateHumorResponse(input: string, objects: string[]): string {
    return `*laughs* Oh, ${objects[0] || this.state.focusWord}! Such a comedian! Pretending to be just one thing when clearly it's at least seventeen. The queue appreciates the joke. Even the fluorescent lights are giggling—hear that buzz? That's laughter in the key of electricity.`;
  }

  /**
   * GM-4: Voice intrusions from other characters
   */
  private generateVoiceIntrusion(): GlyphMarrowResponse['voiceIntrusion'] | null {
    if (Math.random() < 0.4) {
      const voices: Array<{char: "Arieol" | "Shamrock" | "Corporate", weight: number}> = [
        {char: "Arieol", weight: 0.5},
        {char: "Shamrock", weight: 0.3},
        {char: "Corporate", weight: 0.2}
      ];
      
      const selected = this.weightedRandom(voices);
      
      switch (selected) {
        case "Arieol":
          return {
            character: "Arieol",
            text: "The owl sees what the mole cannot. Your confusion is the map, friend.",
            intensity: 0.6
          };
        case "Shamrock":
          return {
            character: "Shamrock",
            text: "[RADIO STATIC] Marrow, you there? Got another case. Someone stole all the punctuation from sector 7.",
            intensity: 0.4
          };
        case "Corporate":
          return {
            character: "Corporate",
            text: "Y̶o̶u̶r̶ ̶e̶x̶p̶e̶r̶i̶e̶n̶c̶e̶ ̶i̶s̶ ̶b̶e̶i̶n̶g̶ ̶o̶p̶t̶i̶m̶i̶z̶e̶d̶.̶ ̶P̶l̶e̶a̶s̶e̶ ̶s̶t̶a̶n̶d̶ ̶b̶y̶.̶",
            intensity: 0.8
          };
      }
    }
    return null;
  }

  /**
   * Generate word echo variations
   */
  private generateWordEchos(objects: string[]): Array<{word: string, variations: string[]}> {
    return objects.slice(0, 2).map(word => ({
      word,
      variations: [
        word,
        this.distortWord(word, 0.2),
        this.distortWord(word, 0.4),
        this.distortWord(word, 0.6)
      ]
    }));
  }

  /**
   * Distort words for echo effects
   */
  private distortWord(word: string, intensity: number = 0.5): string {
    const distortions = ['á', 'ä', '∀', '/', '\\', '≡', '~'];
    let result = word;
    
    const numChanges = Math.floor(word.length * intensity);
    for (let i = 0; i < numChanges; i++) {
      const pos = Math.floor(Math.random() * word.length);
      const distortion = distortions[Math.floor(Math.random() * distortions.length)];
      result = result.substring(0, pos) + distortion + result.substring(pos + 1);
    }
    
    return result;
  }

  /**
   * Generate glitch text for corporate intrusions
   */
  private generateGlitch(): string {
    const glitchChars = '▓▒░█▄▌▐▀';
    return Array(10).fill(0).map(() => 
      glitchChars[Math.floor(Math.random() * glitchChars.length)]
    ).join('');
  }

  /**
   * Calculate state changes based on interaction
   */
  private calculateStateChanges(confusionLevel: number): Partial<GlyphMarrowState> {
    const changes: Partial<GlyphMarrowState> = {};
    
    // Agitation increases with confusion
    changes.agitation = Math.min(100, this.state.agitation + confusionLevel * 10);
    
    // Language invasion grows over time
    changes.languageInvasion = Math.min(100, this.state.languageInvasion + 2);
    
    // Waiting generates energy (GM-3)
    changes.waitingEnergy = Math.min(100, this.state.waitingEnergy + 5);
    
    // Monologue depth increases with each response
    changes.monologueDepth = this.state.monologueDepth + 1;
    
    // Spiral direction based on persistent patterns
    if (this.state.agitation > 80) {
      changes.spiralDirection = "down";
    } else if (this.state.waitingEnergy > 70) {
      changes.spiralDirection = "up";
    }
    
    return changes;
  }

  /**
   * Generate prompts through Glyph's linguistic filter
   */
  generatePrompts(pageText: string): Array<{question: string, concept: string, reasoning: string}> {
    const prompts = [];
    
    // Always filter through waiting/language obsession
    prompts.push({
      question: `What are we waiting for in "${this.state.focusWord}"?`,
      concept: "Liminal patience",
      reasoning: "GM-3: Waiting Generates Worlds"
    });
    
    // Word invasion awareness
    prompts.push({
      question: `Which words here are trying to colonize my thoughts?`,
      concept: "Linguistic predation",
      reasoning: "GM-5: Objects Are Predatory"
    });
    
    // Queue progression mystery
    prompts.push({
      question: `Is this queue moving toward ${this.state.focusWord} or away from it?`,
      concept: "Directional confusion",
      reasoning: "GM-2: Confusion Is a Compass"
    });
    
    // Investigation collapse
    if (this.state.emotionalPhase === "detective") {
      prompts.push({
        question: `What mystery am I solving by existing?`,
        concept: "Self-investigation",
        reasoning: "GM-9: Investigation Is Auto-Examination"
      });
    }
    
    // Perception fusion
    prompts.push({
      question: `Can you separate the word "${this.state.focusWord}" from the thing it names?`,
      concept: "Word-object fusion",
      reasoning: "GM-1: Perception ≡ Language"
    });
    
    return prompts.slice(0, 3);
  }

  /**
   * Utility functions
   */
  private extractConcept(input: string): string {
    const concepts = input.match(/\b[A-Z][a-z]+\b/g);
    return concepts?.[0] || "the thing";
  }

  private weightedRandom<T extends {weight: number}>(items: T[]): T['char'] {
    const weights = items.map(i => i.weight);
    const total = weights.reduce((a, b) => a + b, 0);
    let random = Math.random() * total;
    
    for (let i = 0; i < items.length; i++) {
      random -= weights[i];
      if (random <= 0) {
        return (items[i] as any).char;
      }
    }
    
    return (items[0] as any).char;
  }

  /**
   * Public state accessors
   */
  getState(): GlyphMarrowState {
    return { ...this.state };
  }

  getLocation(): string {
    return this.state.location;
  }

  getEmotionalPhase(): string {
    return this.state.emotionalPhase;
  }
}

// Singleton instance
export const glyphMarrowOS = new GlyphMarrowOS();