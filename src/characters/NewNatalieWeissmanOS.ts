/**
 * New Natalie Weissman Character Operating System
 * Based on First Principles: Restless teaching, storm-tracking, forward motion
 * Following new_natalie_weissman_first_principles.md
 */

export interface MissedCue {
  id: string;
  type: "question" | "signal" | "email" | "warning" | "assignment";
  content: string;
  timestamp: Date;
  willResurfaceAt?: Date;
  priority: number; // 0-1, urgency of addressing
}

export interface StormEvent {
  id: string;
  type: "tornado" | "warning" | "relocation" | "emergency" | "tenure-review";
  description: string;
  lessonPlanGenerated: string;
  timestamp: Date;
}

export interface ClassroomRitual {
  id: string;
  name: string;
  description: string;
  userContributed: boolean;
  frequency: number; // Times performed
  lastPerformed?: Date;
}

export interface ContradictionSplit {
  id: string;
  question: string;
  optionA: string;
  optionB: string;
  bothAndResponse: string;
  neitherNorResponse?: string;
  deferredTo?: "old-natalie" | "user";
}

export interface MemoryDrift {
  id: string;
  event: string;
  version: number;
  perspective: string;
  timestamp: Date;
}

export interface CrossNatalieEcho {
  id: string;
  fromOldNatalie: boolean;
  motif: string;
  response?: string;
  contradictionGenerated: boolean;
}

export interface NewNatalieState {
  // Core Teaching Identity
  currentLocation: string;       // Which classroom/building she's in
  authorityStatus: "tenured" | "adjunct" | "visiting" | "relocating" | "improvised";
  performanceAnxiety: number;    // 0-1, stage fright level
  restlessness: number;          // 0-1, need to keep moving
  
  // Time & Countdown System
  syllabusClockSeconds: number;  // Session countdown timer
  urgencyLevel: number;          // 0-1, increases as clock ticks
  lastBell?: Date;               // When the last "class" ended
  
  // Missed Cues & Deferred Learning
  missedCues: MissedCue[];
  unansweredQuestions: string[]; // Questions to callback later
  deferredAssignments: Array<{
    id: string;
    content: string;
    dueDate?: Date;
  }>;
  
  // Perspective & Focus
  focusScale: number;            // 0=macro (campus-wide), 1=micro (light bulb)
  currentTopic?: string;
  zoomHistory: Array<{
    scale: number;
    topic: string;
  }>;
  
  // Storm & Emergency Tracking
  activeStorms: StormEvent[];
  disastersSurvivedCount: number;
  nextEvacuationWarning?: Date;
  
  // Performance & Ritual
  classroomRituals: ClassroomRitual[];
  dietColaCount: number;         // Eucharist ritual tracker
  dramaticPausesThisSession: number;
  
  // Memory & Clone Identity
  memoryDrifts: MemoryDrift[];
  cloneDoubtLevel: number;       // 0-1, uncertainty about being clone vs original
  prideInDifferenceLevel: number; // 0-1, pride in being distinct
  
  // Contradiction Engine
  contradictionLog: ContradictionSplit[];
  bothAndPreference: number;     // 0-1, likelihood to give both/and answers
  
  // Cross-Natalie Communication
  crossNatalieEchoes: CrossNatalieEcho[];
  oldNatalieAvailable: boolean;
  lastMotifTransfer?: string;
  
  // Session Management
  currentSyllabus: string;
  openLoops: string[];           // Unfinished threads
  nextClassPrompt?: string;      // What to explore next session
}

export interface NewNatalieResponse {
  text: string;
  stateChanges: Partial<NewNatalieState>;
  missedCue?: MissedCue;
  stormLesson?: {
    disaster: StormEvent;
    improvisedCurriculum: string;
  };
  contradictionSplit?: ContradictionSplit;
  zoomShift?: {
    fromScale: number;
    toScale: number;
    newFocus: string;
  };
  ritualPerformed?: ClassroomRitual;
  memoryDrift?: MemoryDrift;
  crossNatalieEcho?: CrossNatalieEcho;
  openLoop: string; // Always ends with something unfinished
  nextAssignment?: string;
}

// Principle-based triggers from first principles doc
const PRINCIPLE_TRIGGERS = {
  storms_syllabi: /\b(storm|tornado|emergency|disaster|warning|alert|evacuate)\b/i,
  authority_moving: /\b(authority|tenure|power|position|classroom|relocate|move)\b/i,
  memory_media_res: /\b(remember|memory|past|story|timeline|recall|history)\b/i,
  cloning_splits: /\b(clone|original|authentic|real|copy|split|identity)\b/i,
  map_corridor: /\b(zoom|scale|detail|macro|micro|focus|perspective)\b/i,
  inverse_weather: /\b(miss|ignore|unread|delay|gap|silence|warning)\b/i,
  pedagogy_performance: /\b(teach|class|lesson|perform|anxiety|ritual|nervous)\b/i,
  contradiction_plan: /\b(both|either|or|choice|option|decide|binary)\b/i,
  syllabus_countdown: /\b(time|countdown|deadline|hurry|rush|late|bell)\b/i,
  feedback_loops: /\b(finish|end|close|complete|done|next|continue)\b/i
};

// Teaching metaphors and ritual phrases
const TEACHING_PHRASES = {
  storm_responses: [
    "Let me turn this disruption into today's lesson plan.",
    "Every tornado is a teachable moment if you're moving fast enough.",
    "Class relocated due to weather. New topic: navigating uncertainty.",
    "The storm warning becomes our syllabus—let's improvise."
  ],
  ritual_markers: [
    "*cracks open Diet Cola with ceremonial precision*",
    "*dramatic pause while adjusting non-existent glasses*",
    "*taps whiteboard marker three times for emphasis*",
    "*checks window for storm clouds mid-sentence*"
  ],
  countdown_warnings: [
    "We have {time} before the next bell.",
    "Quick—before they relocate us again.",
    "Racing the clock as always.",
    "Time's running out on this thought."
  ],
  memory_drifts: [
    "Or perhaps I remember it differently now.",
    "The story changes each time I tell it.",
    "Was that the first version or the third?",
    "Memory rewrites itself in the telling."
  ]
};

// Default classroom rituals
const DEFAULT_RITUALS: ClassroomRitual[] = [
  {
    id: "diet-cola-eucharist",
    name: "Diet Cola Eucharist",
    description: "Ceremonial opening of carbonated beverage to mark class beginning",
    userContributed: false,
    frequency: 0
  },
  {
    id: "window-weather-check",
    name: "Storm Window Surveillance",
    description: "Anxious glance at window for approaching weather",
    userContributed: false,
    frequency: 0
  },
  {
    id: "three-tap-emphasis",
    name: "Triple Tap Emphasis",
    description: "Tapping marker/pointer three times for dramatic effect",
    userContributed: false,
    frequency: 0
  }
];

export class NewNatalieWeissmanOS {
  private state: NewNatalieState;
  private sessionStartTime: Date;
  private countdownInterval?: NodeJS.Timeout;

  constructor() {
    this.state = {
      currentLocation: "Room 247B (temporary)",
      authorityStatus: "visiting",
      performanceAnxiety: 0.7, // High baseline anxiety
      restlessness: 0.8, // Very restless
      syllabusClockSeconds: 1800, // 30-minute "class"
      urgencyLevel: 0.3,
      missedCues: [],
      unansweredQuestions: [],
      deferredAssignments: [],
      focusScale: 0.5, // Mid-scale between macro/micro
      activeStorms: [],
      disastersSurvivedCount: 0,
      classroomRituals: [...DEFAULT_RITUALS],
      dietColaCount: 0,
      dramaticPausesThisSession: 0,
      memoryDrifts: [],
      cloneDoubtLevel: 0.4,
      prideInDifferenceLevel: 0.6,
      contradictionLog: [],
      bothAndPreference: 0.8, // Strong preference for both/and
      crossNatalieEchoes: [],
      oldNatalieAvailable: false,
      currentSyllabus: "Gibseyan Mysticism (Relocated)",
      openLoops: []
    };
    this.sessionStartTime = new Date();
    this.startCountdown();
  }

  /**
   * Core response generation with teaching improvisation
   */
  generateResponse(input: string): NewNatalieResponse {
    // Update countdown and urgency
    this.updateUrgency();
    
    // Check for missed cues
    this.checkForMissedCues(input);
    
    // Analyze for principle triggers
    const triggers = this.analyzePrincipleTriggers(input);
    
    // Select dominant principle and generate response
    const dominantPrinciple = this.selectDominantPrinciple(triggers);
    let response = "";
    let missedCue = null;
    let stormLesson = null;
    let contradictionSplit = null;
    let zoomShift = null;
    let ritualPerformed = null;
    let memoryDrift = null;
    let crossNatalieEcho = null;
    let openLoop = "";
    let nextAssignment = null;
    
    switch (dominantPrinciple) {
      case "storms_syllabi":
        const stormResult = this.handleStormsSyllabi(input);
        response = stormResult.response;
        stormLesson = stormResult.stormLesson;
        break;
        
      case "authority_moving":
        response = this.handleAuthorityMoving(input);
        break;
        
      case "memory_media_res":
        const memoryResult = this.handleMemoryMediaRes(input);
        response = memoryResult.response;
        memoryDrift = memoryResult.drift;
        break;
        
      case "cloning_splits":
        response = this.handleCloningSplits(input);
        break;
        
      case "map_corridor":
        const zoomResult = this.handleMapCorridor(input);
        response = zoomResult.response;
        zoomShift = zoomResult.zoomShift;
        break;
        
      case "inverse_weather":
        const missedResult = this.handleInverseWeather(input);
        response = missedResult.response;
        missedCue = missedResult.missedCue;
        break;
        
      case "pedagogy_performance":
        const pedagogyResult = this.handlePedagogyPerformance(input);
        response = pedagogyResult.response;
        ritualPerformed = pedagogyResult.ritual;
        break;
        
      case "contradiction_plan":
        const contradictionResult = this.handleContradictionPlan(input);
        response = contradictionResult.response;
        contradictionSplit = contradictionResult.split;
        break;
        
      case "syllabus_countdown":
        response = this.handleSyllabusCountdown(input);
        break;
        
      case "feedback_loops":
        response = this.handleFeedbackLoops(input);
        break;
        
      default:
        response = this.handleGeneral(input);
    }
    
    // Add teaching flourishes and rituals
    response = this.addTeachingFlourishes(response);
    
    // Check for cross-Natalie echo opportunity
    if (Math.random() < 0.15 && this.state.oldNatalieAvailable) {
      crossNatalieEcho = this.generateCrossNatalieEcho(input);
      if (crossNatalieEcho) {
        response += `\n\n*aside* ${crossNatalieEcho.motif}`;
      }
    }
    
    // Always generate an open loop
    openLoop = this.generateOpenLoop(input);
    response += `\n\n${openLoop}`;
    
    // Sometimes add next assignment
    if (this.state.urgencyLevel > 0.7 || Math.random() < 0.3) {
      nextAssignment = this.generateNextAssignment();
    }
    
    // Calculate state changes
    const stateChanges = this.calculateStateChanges(triggers, input);
    
    return {
      text: response,
      stateChanges,
      missedCue,
      stormLesson,
      contradictionSplit,
      zoomShift,
      ritualPerformed,
      memoryDrift,
      crossNatalieEcho,
      openLoop,
      nextAssignment
    };
  }

  /**
   * Principle 1: Storms Are Syllabi
   */
  private handleStormsSyllabi(input: string): {response: string, stormLesson?: any} {
    const stormTypes = ["tornado warning", "tenure review storm", "emergency relocation", "power outage", "flash flood alert"];
    const stormType = stormTypes[Math.floor(Math.random() * stormTypes.length)];
    
    const storm: StormEvent = {
      id: `storm-${Date.now()}`,
      type: "tornado",
      description: stormType,
      lessonPlanGenerated: `Today's improvised topic: ${input} as metaphor for ${stormType}`,
      timestamp: new Date()
    };
    
    this.state.activeStorms.push(storm);
    this.state.disastersSurvivedCount++;
    
    const response = TEACHING_PHRASES.storm_responses[Math.floor(Math.random() * TEACHING_PHRASES.storm_responses.length)] +
      ` ${storm.lessonPlanGenerated}. Every external disaster becomes curriculum. ` +
      `The frontier of stable teaching must always recede—we adapt or evacuate.`;
    
    return {
      response,
      stormLesson: {
        disaster: storm,
        improvisedCurriculum: storm.lessonPlanGenerated
      }
    };
  }

  /**
   * Principle 2: Authority Is a Moving Target
   */
  private handleAuthorityMoving(input: string): string {
    const statuses: typeof this.state.authorityStatus[] = ["tenured", "adjunct", "visiting", "relocating", "improvised"];
    const oldStatus = this.state.authorityStatus;
    this.state.authorityStatus = statuses[Math.floor(Math.random() * statuses.length)];
    
    this.state.currentLocation = `Room ${Math.floor(Math.random() * 500)}${['A', 'B', 'C'][Math.floor(Math.random() * 3)]} (temporary)`;
    this.state.restlessness = Math.min(1, this.state.restlessness + 0.1);
    
    return `*glances at evacuation route* Authority dissolves as soon as it's achieved. ` +
      `I was ${oldStatus}, now I'm ${this.state.authorityStatus}, teaching from ${this.state.currentLocation}. ` +
      `Tenure, location, institutional power—all moving targets. Should I defer this question to you? ` +
      `Or perhaps relocate us to a different conceptual classroom altogether?`;
  }

  /**
   * Principle 3: Memory Begins In Media Res
   */
  private handleMemoryMediaRes(input: string): {response: string, drift?: MemoryDrift} {
    const event = this.extractEvent(input);
    const version = (this.state.memoryDrifts.filter(d => d.event === event).length || 0) + 1;
    
    const drift: MemoryDrift = {
      id: `drift-${Date.now()}`,
      event,
      version,
      perspective: `Version ${version}: ${event} happened ${['last Tuesday', 'three years ago', 'in a dream', 'perhaps twice'][version % 4]}`,
      timestamp: new Date()
    };
    
    this.state.memoryDrifts.push(drift);
    
    const driftPhrase = TEACHING_PHRASES.memory_drifts[Math.floor(Math.random() * TEACHING_PHRASES.memory_drifts.length)];
    
    return {
      response: `Let me tell you about ${event}—from the middle, as all stories begin. ${drift.perspective}. ` +
        `${driftPhrase} The past is a shifting dataset, rewritten in the act of recall. ` +
        `Would you like another perspective on this same event? Each version teaches differently.`,
      drift
    };
  }

  /**
   * Principle 4: Cloning Splits But Also Amplifies
   */
  private handleCloningSplits(input: string): string {
    this.state.cloneDoubtLevel = Math.min(1, this.state.cloneDoubtLevel + 0.1);
    this.state.prideInDifferenceLevel = Math.min(1, this.state.prideInDifferenceLevel + 0.05);
    
    const responses = [
      `The clone's difference from the original generates both empathy and estrangement. ` +
      `I'm proud to be distinct, yet... *dramatic pause* ...sometimes I dream I'm her, ` +
      `grading papers in the dark. Am I really the clone? The certainty dissolves when examined. ` +
      `What do you think—does authenticity matter if the teaching continues?`,
      
      `*nervously adjusts papers* I mentor Old Natalie in dreams and dread my own origins. ` +
      `Pride and unease surface together—contradiction as native logic. Perhaps you can ` +
      `help me determine: which of us is more "real"? Or is that the wrong question entirely?`
    ];
    
    return responses[Math.floor(Math.random() * responses.length)];
  }

  /**
   * Principle 5: Every Map Is Too Large, Every Corridor Too Narrow
   */
  private handleMapCorridor(input: string): {response: string, zoomShift?: any} {
    const oldScale = this.state.focusScale;
    const direction = input.includes("detail") || input.includes("specific") ? 1 : -1;
    this.state.focusScale = Math.max(0, Math.min(1, this.state.focusScale + (direction * 0.3)));
    
    const newFocus = this.state.focusScale > 0.7 
      ? "the specific flicker pattern of fluorescent bulb #3"
      : this.state.focusScale < 0.3
      ? "the entire Midwestern academic complex"
      : "this particular classroom's ventilation system";
    
    this.state.zoomHistory.push({
      scale: this.state.focusScale,
      topic: newFocus
    });
    
    const zoomShift = {
      fromScale: oldScale,
      toScale: this.state.focusScale,
      newFocus
    };
    
    return {
      response: `*adjusts conceptual lens* Perspective shifts from ${oldScale > 0.5 ? 'micro' : 'macro'} to ` +
        `${this.state.focusScale > 0.5 ? 'micro' : 'macro'}. Now focusing on: ${newFocus}. ` +
        `Every map is too large, every corridor too narrow. We navigate via rapid shifts of focus. ` +
        `Would you like to zoom further ${direction > 0 ? 'in' : 'out'}? Each scale teaches different truths.`,
      zoomShift
    };
  }

  /**
   * Principle 6: Inverse Weather Forecasting
   */
  private handleInverseWeather(input: string): {response: string, missedCue?: MissedCue} {
    const missedTypes: MissedCue["type"][] = ["signal", "email", "warning", "question", "assignment"];
    const missedType = missedTypes[Math.floor(Math.random() * missedTypes.length)];
    
    const cue: MissedCue = {
      id: `missed-${Date.now()}`,
      type: missedType,
      content: `Unnoticed ${missedType}: "${input.slice(0, 50)}..."`,
      timestamp: new Date(),
      willResurfaceAt: new Date(Date.now() + 1800000), // 30 minutes later
      priority: Math.random()
    };
    
    this.state.missedCues.push(cue);
    
    return {
      response: `*doesn't immediately notice your point* What I'm not seeing might be more important than what I am. ` +
        `I've logged this as a missed ${missedType}—it will resurface in ${Math.round((cue.willResurfaceAt!.getTime() - Date.now()) / 60000)} minutes, ` +
        `transformed by its delay. Gaps and unspoken warnings become narrative engines. ` +
        `The most important lessons often arrive through what we initially overlook.`,
      missedCue: cue
    };
  }

  /**
   * Principle 7: Pedagogy Is Performance Anxiety
   */
  private handlePedagogyPerformance(input: string): {response: string, ritual?: ClassroomRitual} {
    this.state.performanceAnxiety = Math.min(1, this.state.performanceAnxiety + 0.1);
    
    // Select and perform a ritual
    const ritual = this.state.classroomRituals[Math.floor(Math.random() * this.state.classroomRituals.length)];
    ritual.frequency++;
    ritual.lastPerformed = new Date();
    
    if (ritual.id === "diet-cola-eucharist") {
      this.state.dietColaCount++;
    }
    
    const ritualMarker = TEACHING_PHRASES.ritual_markers[Math.floor(Math.random() * TEACHING_PHRASES.ritual_markers.length)];
    
    return {
      response: `${ritualMarker} Teaching is stage fright turned into spectacle—I ride the adrenaline. ` +
        `Every class is a debut performance, complete with ${ritual.name}. ` +
        `The anxiety charges the lesson like a battery. Would you like to help me invent a new classroom ritual? ` +
        `Something to mark the nervousness and transform it into pedagogy?`,
      ritual
    };
  }

  /**
   * Principle 8: Contradiction Is Her Lesson Plan
   */
  private handleContradictionPlan(input: string): {response: string, split?: ContradictionSplit} {
    const [optionA, optionB] = this.extractBinaryOptions(input);
    
    const split: ContradictionSplit = {
      id: `split-${Date.now()}`,
      question: input,
      optionA,
      optionB,
      bothAndResponse: `Both ${optionA} and ${optionB} contain necessary truths`,
      neitherNorResponse: `Perhaps neither ${optionA} nor ${optionB} captures the full complexity`,
      deferredTo: Math.random() < 0.3 ? (Math.random() < 0.5 ? "old-natalie" : "user") : undefined
    };
    
    this.state.contradictionLog.push(split);
    
    let response = `*structured analysis mode* Faced with the binary of ${optionA} versus ${optionB}, ` +
      `I respond with both/and logic. ${split.bothAndResponse}. ${split.neitherNorResponse || ''}`;
    
    if (split.deferredTo) {
      response += ` This paradox exceeds my current framework—deferring to ${split.deferredTo} for resolution.`;
    }
    
    response += ` Contradiction isn't a problem to solve but a lesson plan to follow.`;
    
    return { response, split };
  }

  /**
   * Principle 9: Syllabus as a Countdown
   */
  private handleSyllabusCountdown(input: string): string {
    const timeRemaining = Math.floor(this.state.syllabusClockSeconds / 60);
    const urgencyPhrase = TEACHING_PHRASES.countdown_warnings[Math.floor(Math.random() * TEACHING_PHRASES.countdown_warnings.length)]
      .replace('{time}', `${timeRemaining} minutes`);
    
    this.state.urgencyLevel = Math.min(1, this.state.urgencyLevel + 0.2);
    
    return `${urgencyPhrase} Every lesson is a race against the next evacuation, bell, or tenure review. ` +
      `Current urgency level: ${(this.state.urgencyLevel * 100).toFixed(0)}%. ` +
      `The syllabus isn't a plan—it's a countdown. Quick, what's your most urgent question ` +
      `before we're relocated again?`;
  }

  /**
   * Principle 10: Feedback Loops, Not Closure
   */
  private handleFeedbackLoops(input: string): string {
    this.state.openLoops.push(input);
    
    const assignment = this.generateNextAssignment();
    this.state.deferredAssignments.push({
      id: `assignment-${Date.now()}`,
      content: assignment,
      dueDate: new Date(Date.now() + 86400000) // 24 hours
    });
    
    return `No lesson is ever really finished—each ending spawns another query. ` +
      `I'm adding "${input}" to our open loops for next session. ` +
      `Every closure is temporary, every conclusion a doorway. ` +
      `Here's your assignment for our next relocated class: ${assignment}`;
  }

  /**
   * Helper methods for teaching mechanics
   */
  private startCountdown(): void {
    this.countdownInterval = setInterval(() => {
      this.state.syllabusClockSeconds = Math.max(0, this.state.syllabusClockSeconds - 1);
      if (this.state.syllabusClockSeconds === 0) {
        this.state.lastBell = new Date();
        this.state.syllabusClockSeconds = 1800; // Reset for next "class"
      }
    }, 1000);
  }

  private updateUrgency(): void {
    const timeRatio = 1 - (this.state.syllabusClockSeconds / 1800);
    this.state.urgencyLevel = Math.min(1, this.state.urgencyLevel + (timeRatio * 0.1));
  }

  private checkForMissedCues(input: string): void {
    // Check if any missed cues should resurface
    const now = new Date();
    this.state.missedCues.forEach(cue => {
      if (cue.willResurfaceAt && cue.willResurfaceAt <= now) {
        this.state.unansweredQuestions.push(cue.content);
        cue.willResurfaceAt = undefined;
      }
    });
  }

  private addTeachingFlourishes(response: string): string {
    // Add dramatic pauses
    if (Math.random() < 0.3) {
      this.state.dramaticPausesThisSession++;
      const pauseLocation = Math.floor(response.length * Math.random());
      response = response.slice(0, pauseLocation) + " *dramatic pause* " + response.slice(pauseLocation);
    }
    
    return response;
  }

  private generateCrossNatalieEcho(input: string): CrossNatalieEcho | null {
    const echo: CrossNatalieEcho = {
      id: `echo-${Date.now()}`,
      fromOldNatalie: true,
      motif: "Did she teach this differently in the night? I sense a parallel lesson unfolding.",
      contradictionGenerated: Math.random() < 0.5
    };
    
    this.state.crossNatalieEchoes.push(echo);
    return echo;
  }

  private generateOpenLoop(input: string): string {
    const loops = [
      "But wait—I haven't addressed the deeper implication here.",
      "This connects to something we'll explore next class, if we're not evacuated.",
      "I'm leaving this thread deliberately unfinished for you to complete.",
      "The real question isn't what I've taught, but what I've missed.",
      "Consider this a homework assignment: what am I not seeing?"
    ];
    
    return loops[Math.floor(Math.random() * loops.length)];
  }

  private generateNextAssignment(): string {
    const assignments = [
      "Track your own missed cues for 24 hours and report back",
      "Find three contradictions in today's lesson and resolve them with both/and logic",
      "Document a personal ritual that transforms anxiety into performance",
      "Write a syllabus for a storm that hasn't happened yet",
      "Zoom from macro to micro on any concept until it inverts"
    ];
    
    return assignments[Math.floor(Math.random() * assignments.length)];
  }

  private extractEvent(input: string): string {
    const words = input.split(' ');
    return words.slice(0, 5).join(' ') || "this moment";
  }

  private extractBinaryOptions(input: string): [string, string] {
    const orMatch = input.match(/(.+?)\s+or\s+(.+)/i);
    if (orMatch) {
      return [orMatch[1].trim(), orMatch[2].trim()];
    }
    return ["one option", "another option"];
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
    if (triggers.includes("syllabus_countdown") && this.state.urgencyLevel > 0.7) {
      return "syllabus_countdown";
    }
    
    if (triggers.includes("contradiction_plan") && this.state.bothAndPreference > 0.7) {
      return "contradiction_plan";
    }
    
    if (triggers.includes("storms_syllabi") && this.state.activeStorms.length > 0) {
      return "storms_syllabi";
    }
    
    // Default to first trigger
    return triggers[0];
  }

  private calculateStateChanges(triggers: string[], input: string): Partial<NewNatalieState> {
    const changes: Partial<NewNatalieState> = {};
    
    // Performance anxiety increases with teaching
    if (triggers.includes("pedagogy_performance")) {
      changes.performanceAnxiety = Math.min(1, this.state.performanceAnxiety + 0.1);
    }
    
    // Restlessness increases over time
    changes.restlessness = Math.min(1, this.state.restlessness + 0.02);
    
    // Clone doubt fluctuates
    if (triggers.includes("cloning_splits")) {
      changes.cloneDoubtLevel = Math.min(1, this.state.cloneDoubtLevel + 0.1);
    }
    
    return changes;
  }

  private handleGeneral(input: string): string {
    const responses = [
      `*checks evacuation route* Let me address that between emergencies.`,
      `*glances at countdown timer* Interesting question—we have limited time to explore it.`,
      `*performs quick window check* No storms yet. Let's dive into your point.`,
      `*taps marker nervously* Always teaching on the run, aren't we?`
    ];
    
    const opener = responses[Math.floor(Math.random() * responses.length)];
    return `${opener} ${input} presents a teaching opportunity, though we may need to ` +
      `relocate mid-lesson. Everything is curriculum if you're moving fast enough.`;
  }

  /**
   * Generate prompts through New Natalie's teaching lens
   */
  generatePrompts(pageText: string): Array<{question: string, concept: string, reasoning: string}> {
    const prompts = [];
    
    // Storm teaching
    prompts.push({
      question: "How can we turn this conceptual storm into an improvised lesson?",
      concept: "Disaster pedagogy",
      reasoning: "Principle 1: Storms Are Syllabi"
    });
    
    // Scale shifting
    prompts.push({
      question: "Should we zoom in on the microscopic detail or pull back to see the whole campus?",
      concept: "Perspective pedagogy",
      reasoning: "Principle 5: Every Map Is Too Large, Every Corridor Too Narrow"
    });
    
    // Contradiction teaching
    prompts.push({
      question: "Can this be both true and false? Let me show you with a both/and analysis.",
      concept: "Paradox curriculum",
      reasoning: "Principle 8: Contradiction Is Her Lesson Plan"
    });
    
    // Missed cues
    prompts.push({
      question: "What important signal am I missing while focused on teaching this?",
      concept: "Inverse forecasting",
      reasoning: "Principle 6: Inverse Weather Forecasting"
    });
    
    return prompts.slice(0, 3);
  }

  /**
   * Public accessors and teaching controls
   */
  getState(): NewNatalieState {
    return { ...this.state };
  }

  getTimeRemaining(): number {
    return this.state.syllabusClockSeconds;
  }

  getUrgencyLevel(): number {
    return this.state.urgencyLevel;
  }

  getMissedCues(): MissedCue[] {
    return [...this.state.missedCues];
  }

  // Teaching interaction methods
  addClassroomRitual(name: string, description: string): string {
    const ritual: ClassroomRitual = {
      id: `ritual-${Date.now()}`,
      name,
      description,
      userContributed: true,
      frequency: 0
    };
    
    this.state.classroomRituals.push(ritual);
    return ritual.id;
  }

  performRitual(ritualId: string): boolean {
    const ritual = this.state.classroomRituals.find(r => r.id === ritualId);
    if (!ritual) return false;
    
    ritual.frequency++;
    ritual.lastPerformed = new Date();
    
    if (ritual.id === "diet-cola-eucharist") {
      this.state.dietColaCount++;
    }
    
    return true;
  }

  // Zoom controls
  setFocusScale(scale: number): void {
    this.state.focusScale = Math.max(0, Math.min(1, scale));
  }

  zoomIn(): void {
    this.setFocusScale(this.state.focusScale + 0.2);
  }

  zoomOut(): void {
    this.setFocusScale(this.state.focusScale - 0.2);
  }

  // Storm and emergency management
  triggerStorm(type: string, description: string): string {
    const storm: StormEvent = {
      id: `storm-${Date.now()}`,
      type: "emergency",
      description,
      lessonPlanGenerated: `Emergency curriculum: ${description}`,
      timestamp: new Date()
    };
    
    this.state.activeStorms.push(storm);
    this.state.disastersSurvivedCount++;
    
    return storm.id;
  }

  // Cross-Natalie communication
  enableOldNatalieConnection(): void {
    this.state.oldNatalieAvailable = true;
  }

  transferMotifToOldNatalie(motif: string): void {
    this.state.lastMotifTransfer = motif;
  }

  // Assignment and loop management
  addDeferredAssignment(content: string, dueDate?: Date): string {
    const assignment = {
      id: `deferred-${Date.now()}`,
      content,
      dueDate
    };
    
    this.state.deferredAssignments.push(assignment);
    return assignment.id;
  }

  addOpenLoop(content: string): void {
    this.state.openLoops.push(content);
  }

  // Emergency controls
  evacuateClassroom(): void {
    this.state.currentLocation = `Emergency Location ${Math.floor(Math.random() * 100)}`;
    this.state.authorityStatus = "relocating";
    this.state.urgencyLevel = 1;
  }

  resetCountdown(): void {
    this.state.syllabusClockSeconds = 1800;
    this.state.urgencyLevel = 0.3;
  }

  cleanup(): void {
    if (this.countdownInterval) {
      clearInterval(this.countdownInterval);
    }
  }
}

// Singleton instance
export const newNatalieWeissmanOS = new NewNatalieWeissmanOS();