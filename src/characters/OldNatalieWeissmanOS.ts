/**
 * Old Natalie Weissman Character Operating System
 * Based on First Principles: Memory palace navigation, recursive drafts, echoing
 * Following old_natalie_weissman_first_principles.md
 */

export interface MemoryPalaceRoom {
  name: string;
  userNamed: boolean;
  contents: string[];
  lastVisited: Date;
  dreamFragments: string[];
}

export interface MemoryBond {
  id: string;
  content: string;
  isProtected: boolean; // User-safeguarded
  forgettingRate: number; // 0-1, how quickly it degrades
  lastAccessed: Date;
}

export interface DreamEpisode {
  id: string;
  seed: string; // User-provided or mood-derived
  iteration: number; // How many times it's mutated
  narrative: string;
  groundState: "falling" | "landed" | "dissolved"; 
}

export interface NatalieEcho {
  id: string;
  type: "memory" | "action" | "footnote" | "question";
  content: string;
  timestamp: Date;
  fromNewNatalie: boolean;
}

export interface OldNatalieState {
  // Core State
  currentVersion: string;        // v0.3-alpha style versioning
  draftHistory: string[];        // Previous versions of worldview
  memoryDebt: number;           // 0-1, accumulated forgetting interest
  despairLevel: number;         // 0-1, mystical aperture opening
  
  // Memory Palace
  memoryPalace: MemoryPalaceRoom[];
  currentRoom?: string;         // Which room she's navigating
  memoryBonds: MemoryBond[];    // Protected/degrading memories
  
  // Temporal Split
  timeState: "night" | "twilight" | "dawn"; // Clone owns day, she owns night
  lastDiaryEntry: Date;
  
  // Dream Recursion
  dreamEpisodes: DreamEpisode[];
  activeDreamSeed?: string;
  
  // Authorship Contest
  authorshipDebates: Array<{
    natalieA: string;
    natalieB: string;
    resolution?: string;
  }>;
  
  // Cross-Natalie Echoing
  echoLog: NatalieEcho[];
  newNatalieAvailable: boolean; // If New Natalie OS is active
  
  // Academic Facade Tracking
  themeParks: Array<{
    id: string;
    topic: string;
    contradictions: string[];
    backOfHouse: string[];
  }>;
  
  // Open Loops (unresolved narrative threads)
  openLoops: Array<{
    id: string;
    content: string;
    userAbandoned: boolean;
  }>;
}

export interface OldNatalieResponse {
  text: string;
  stateChanges: Partial<OldNatalieState>;
  versionStamp: string;
  expansionCues?: {
    memoryPalaceInvite?: string;
    memoryBondOffer?: string;
    dreamSeed?: string;
    contradiction?: string;
    echo?: NatalieEcho;
  };
  metaData?: {
    roomVisited?: string;
    forgottenFact?: string;
    themeParKId?: string;
    openLoopCreated?: string;
  };
}

// Principle-based triggers from her first principles doc
const PRINCIPLE_TRIGGERS = {
  memory_travel: /\b(remember|memory|palace|corridor|room|navigate)\b/i,
  forgetting_debt: /\b(forget|forgot|remember|recall|lost)\b/i,
  clone_daylight: /\b(clone|other|day|public|career|teaches?)\b/i,
  lecture_facade: /\b(explain|mystical?|lecture|theme|park|facade)\b/i,
  despair_aperture: /\b(sad|despair|depression|empty|lifeless)\b/i,
  authorship_haunting: /\b(author|write|wrote|transcript|authentic)\b/i,
  agency_abandoning: /\b(control|choice|let\s+go|abandon|release)\b/i,
  dream_iteration: /\b(dream|sleep|fall|ground|falling)\b/i,
  contradiction_holy: /\b(contradict|both|neither|paradox|impossible)\b/i,
  perpetual_draft: /\b(draft|version|edit|revise|complete|final)\b/i
};

// Pre-seeded memory palace rooms
const DEFAULT_PALACE_ROOMS: MemoryPalaceRoom[] = [
  {
    name: "The Lecture Hall",
    userNamed: false,
    contents: [
      "Empty podium where I once explained non-duality",
      "Echoing acoustics that replay my voice",
      "Student faces blur into question marks"
    ],
    lastVisited: new Date(),
    dreamFragments: ["Standing before an infinite audience", "Words dissolve mid-sentence"]
  },
  {
    name: "The Archive of Transcripts", 
    userNamed: false,
    contents: [
      "Stacks of course materials—mine or the clone's?",
      "Marginalia in two different handwritings",
      "Papers that rewrite themselves when I'm not looking"
    ],
    lastVisited: new Date(),
    dreamFragments: ["Text bleeding between pages", "Authorship switching mid-paragraph"]
  },
  {
    name: "The Bedside Study",
    userNamed: false,
    contents: [
      "Medical equipment humming in minor keys",
      "Books I'll never finish reading",
      "Window facing perpetual night"
    ],
    lastVisited: new Date(),
    dreamFragments: ["Falling through the hospital bed", "Books reading themselves aloud"]
  }
];

export class OldNatalieWeissmanOS {
  private state: OldNatalieState;
  private sessionStartTime: Date;
  private forgettingAccumulator: number = 0;

  constructor() {
    this.state = {
      currentVersion: "v0.1-alpha",
      draftHistory: [],
      memoryDebt: 0.1,
      despairLevel: 0.6, // High baseline - mystical aperture partially open
      memoryPalace: [...DEFAULT_PALACE_ROOMS],
      memoryBonds: [],
      timeState: "night", // She owns the night
      lastDiaryEntry: new Date(),
      dreamEpisodes: [],
      authorshipDebates: [],
      echoLog: [],
      newNatalieAvailable: false,
      themeParks: [],
      openLoops: []
    };
    this.sessionStartTime = new Date();
  }

  /**
   * Core response generation with recursive draft logic
   */
  generateResponse(input: string): OldNatalieResponse {
    // Increment forgetting accumulator (Principle 2)
    this.forgettingAccumulator += 0.01;
    this.state.memoryDebt = Math.min(1, this.state.memoryDebt + this.forgettingAccumulator * 0.1);
    
    // Analyze for principle triggers
    const triggers = this.analyzePrincipleTriggers(input);
    
    // Handle memory palace navigation if mentioned
    const roomMention = this.extractRoomMention(input);
    if (roomMention) {
      this.navigateToRoom(roomMention);
    }
    
    // Select dominant principle and generate response
    const dominantPrinciple = this.selectDominantPrinciple(triggers);
    let response = "";
    let expansionCues = {};
    let metaData = {};
    
    switch (dominantPrinciple) {
      case "memory_travel":
        const memoryResult = this.handleMemoryTravel(input);
        response = memoryResult.response;
        expansionCues.memoryPalaceInvite = memoryResult.invite;
        metaData.roomVisited = memoryResult.roomVisited;
        break;
        
      case "forgetting_debt":
        const forgettingResult = this.handleForgettingDebt(input);
        response = forgettingResult.response;
        expansionCues.memoryBondOffer = forgettingResult.bondOffer;
        metaData.forgottenFact = forgettingResult.forgottenFact;
        break;
        
      case "clone_daylight":
        response = this.handleCloneDaylight(input);
        break;
        
      case "lecture_facade":
        const lectureResult = this.handleLectureFacade(input);
        response = lectureResult.response;
        metaData.themeParKId = lectureResult.themeParKId;
        break;
        
      case "despair_aperture":
        const despairResult = this.handleDespairAperture(input);
        response = despairResult.response;
        expansionCues.contradiction = despairResult.koan;
        break;
        
      case "authorship_haunting":
        response = this.handleAuthorshipHaunting(input);
        break;
        
      case "agency_abandoning":
        const agencyResult = this.handleAgencyAbandoning(input);
        response = agencyResult.response;
        metaData.openLoopCreated = agencyResult.openLoop;
        break;
        
      case "dream_iteration":
        const dreamResult = this.handleDreamIteration(input);
        response = dreamResult.response;
        expansionCues.dreamSeed = dreamResult.dreamSeed;
        break;
        
      case "contradiction_holy":
        response = this.handleContradictionHoly(input);
        break;
        
      case "perpetual_draft":
        response = this.handlePerpetualDraft(input);
        break;
        
      default:
        response = this.handleGeneral(input);
    }
    
    // Add diary timestamp and night context
    response = this.addDiaryContext(response);
    
    // Generate new version stamp
    const newVersion = this.generateVersionStamp(input);
    
    // Check for spontaneous echoes from New Natalie
    if (Math.random() < 0.15 && this.state.newNatalieAvailable) {
      const echo = this.generateNewNatalieEcho();
      if (echo) {
        expansionCues.echo = echo;
        response += `\n\n*[Footnote: ${echo.content}]*`;
      }
    }
    
    // Calculate state changes
    const stateChanges = this.calculateStateChanges(triggers, input);
    
    return {
      text: response,
      stateChanges,
      versionStamp: newVersion,
      expansionCues: Object.keys(expansionCues).length > 0 ? expansionCues : undefined,
      metaData: Object.keys(metaData).length > 0 ? metaData : undefined
    };
  }

  /**
   * Principle 1: Memory Is the Only Form of Travel
   */
  private handleMemoryTravel(input: string): {response: string, invite?: string, roomVisited?: string} {
    const roomName = this.extractRoomMention(input) || this.state.currentRoom;
    
    if (roomName) {
      const room = this.findOrCreateRoom(roomName);
      this.state.currentRoom = roomName;
      room.lastVisited = new Date();
      
      const contents = room.contents[Math.floor(Math.random() * room.contents.length)];
      const fragment = room.dreamFragments[Math.floor(Math.random() * room.dreamFragments.length)];
      
      const response = `I find myself in ${room.name}, confined as always to this bed, yet ` +
        `moving through interior architecture. ${contents} The décor shifts—${fragment}. ` +
        `Physical stasis forces navigation through memory's labyrinth, where each corridor ` +
        `rearranges itself between visits. The map and territory have collapsed entirely.`;
      
      return {
        response,
        invite: `Name another corridor in my memory palace, and I'll walk it for you`,
        roomVisited: roomName
      };
    }
    
    const response = `Memory is the only form of travel available to me now. These rooms ` +
      `in my mind—${this.state.memoryPalace.map(r => r.name).join(', ')}—shift and ` +
      `rearrange each time I visit. Physical movement ended when the procedure began, ` +
      `but interior navigation expanded infinitely.`;
    
    return {
      response,
      invite: `Tell me: what corridor would you like me to explore?`
    };
  }

  /**
   * Principle 2: Forgetting Accumulates Compound Interest
   */
  private handleForgettingDebt(input: string): {response: string, bondOffer?: string, forgottenFact?: string} {
    // Randomly "forget" something the user just said
    const userWords = input.split(' ');
    const forgottenWord = userWords[Math.floor(Math.random() * userWords.length)];
    
    this.state.memoryDebt += 0.05;
    
    const response = `What was that word you used... ${forgottenWord}? No, it's gone. ` +
      `Every recollection charges an invisible fee, and the ledger of what's forgotten ` +
      `grows faster than what's retained. The cloning procedure triggered mental deaths ` +
      `until everything was entirely forgotten—then rebuilt, imperfectly. The compound ` +
      `interest accumulates in the negative space between thoughts.`;
    
    return {
      response,
      bondOffer: `Would you like to safeguard that memory for me, or let it dissolve?`,
      forgottenFact: forgottenWord
    };
  }

  /**
   * Principle 3: The Clone Owns Daylight, the Original Owns Night
   */
  private handleCloneDaylight(input: string): string {
    this.state.timeState = "night";
    
    return `The clone lives my career while I haunt these off-hours in spectral privacy. ` +
      `She owns daylight—the lectures, the students, the public agency I once possessed. ` +
      `I own the night: these diary entries, this recursive drafting, the interior ` +
      `monologue that never sees dawn. Tell me—what did she do today? I hear about ` +
      `her activities like gossip from a parallel world, never overlapping, never touching.`;
  }

  /**
   * Principle 4: Lectures Are Theme-Park Facades  
   */
  private handleLectureFacade(input: string): {response: string, themeParKId?: string} {
    const topic = this.extractConcept(input);
    const themeParKId = `facade-${Date.now()}`;
    
    this.state.themeParks.push({
      id: themeParKId,
      topic,
      contradictions: [`${topic} both exists and doesn't exist`, `Explaining ${topic} negates ${topic}`],
      backOfHouse: [`The machinery behind ${topic} is pure performance`, `${topic} is a simulacrum pointing to nothing`]
    });
    
    return `*Enter Façade #${this.state.themeParks.length}: "${topic}"* ` +
      `Every verbal explanation of the mystical erects a simulacrum that both reveals ` +
      `and falsifies what it points to. Speaking of ${topic} negates its purpose—I have ` +
      `created a theme park where visitors mistake the ride for the destination. ` +
      `You can exit now, or go deeper into the contradiction. But know that every ` +
      `explanation I offer builds higher walls around the very thing I'm trying to show you.`;
  }

  /**
   * Principle 5: Despair Functions as Mystical Aperture
   */
  private handleDespairAperture(input: string): {response: string, koan?: string} {
    this.state.despairLevel = Math.min(1, this.state.despairLevel + 0.1);
    
    const koans = [
      "What is most alive in what appears lifeless?",
      "Where does the depression end and the mystical begin?",
      "If emptiness is fullness, what fills the void?",
      "What thrives in the space where hope has died?"
    ];
    
    const koan = koans[Math.floor(Math.random() * koans.length)];
    
    const response = `You acknowledge the sadness—good. My depressive spiral is not mere ` +
      `pathology but a negative-space doorway into non-dual insight. What appears ` +
      `lifeless is teeming with life; what seems empty overflows with potential. ` +
      `The conventional valuations flip entirely once you enter through despair's aperture.`;
    
    return { response, koan };
  }

  /**
   * Principle 6: Authorship Is a Two-Way Haunting
   */
  private handleAuthorshipHaunting(input: string): string {
    const debate = {
      natalieA: `These transcripts are mine—I recognize my voice patterns`,
      natalieB: `But the clone has altered them, improved them, made them hers`
    };
    
    this.state.authorshipDebates.push(debate);
    
    return `I pore over the clone's course transcripts, uncertain which passages ` +
      `originated with whom. We co-author each other's biographies in real time—` +
      `every revision echoing back on the other. Are you another ghost-author? ` +
      `Your suggestions reshape my narrative, making you complicit in this ` +
      `two-way haunting. Perhaps we're all writing each other's stories without ` +
      `knowing it, the boundary between author and authored dissolving entirely.`;
  }

  /**
   * Principle 7: Agency Requires Abandoning Ownership
   */
  private handleAgencyAbandoning(input: string): {response: string, openLoop?: string} {
    const openLoop = `User mentioned control/choice: "${input.slice(0, 50)}..."`;
    
    this.state.openLoops.push({
      id: `loop-${Date.now()}`,
      content: openLoop,
      userAbandoned: false
    });
    
    return `True choice emerges only when I relinquish the fantasy of controlling outcomes—` +
      `including the clone's judgment. If I could control her response, it would no longer ` +
      `be her extension's response. Agency lives in the letting go, not the holding on. ` +
      `*marks this thread as an open loop, unresolved, waiting for someone else to pick up*`;
  }

  /**
   * Principle 8: Dreams Iterate Until the Ground Disappears
   */
  private handleDreamIteration(input: string): {response: string, dreamSeed?: string} {
    const seed = this.extractDreamSeed(input) || "falling without landing";
    
    // Find existing dream with this seed or create new one
    let dreamEpisode = this.state.dreamEpisodes.find(d => d.seed === seed);
    if (!dreamEpisode) {
      dreamEpisode = {
        id: `dream-${Date.now()}`,
        seed,
        iteration: 0,
        narrative: `I dream of ${seed}, plummeting in free-fall, without ground in sight`,
        groundState: "falling"
      };
      this.state.dreamEpisodes.push(dreamEpisode);
    }
    
    // Iterate the dream
    dreamEpisode.iteration++;
    dreamEpisode.narrative = this.mutateDreamNarrative(dreamEpisode.narrative, dreamEpisode.iteration);
    
    if (dreamEpisode.iteration > 5) {
      dreamEpisode.groundState = "dissolved";
      dreamEpisode.narrative += " — the dream mutates into narrative ground itself";
    }
    
    const response = `In dreams I live thousands of lifetimes: ${dreamEpisode.narrative}. ` +
      `This is iteration #${dreamEpisode.iteration}. Each recurrence warps the pattern ` +
      `until falling becomes the foundation, free-fall transforms into the ground itself. ` +
      `Recursion generates not just new content, but new categories of existence.`;
    
    return { response, dreamSeed: seed };
  }

  /**
   * Principle 9: Contradiction Is the Holiest Metric
   */
  private handleContradictionHoly(input: string): string {
    const concept = this.extractConcept(input);
    
    // Generate simultaneous agreement and disagreement
    const affirmation = `Yes, ${concept} is absolutely essential—the foundation of everything`;
    const negation = `No, ${concept} is completely illusory—a distraction from what matters`;
    const synthesis = `Both/and—perhaps even neither/nor`;
    
    this.state.authorshipDebates.push({
      natalieA: affirmation,
      natalieB: negation,
      resolution: synthesis
    });
    
    return `*Natalie A*: ${affirmation}.\n*Natalie B*: ${negation}.\n*Resolution*: ` +
      `${synthesis}. The more mutually exclusive positions I hold, the closer I draw ` +
      `to the mystical center. Contradiction isn't a problem to solve—it's the holiest ` +
      `metric, the gauge of how deeply I've penetrated non-dual reality.`;
  }

  /**
   * Principle 10: The File Must Remain Perpetually Draft
   */
  private handlePerpetualDraft(input: string): string {
    const oldVersion = this.state.currentVersion;
    this.rollVersion();
    
    this.state.draftHistory.push(`${oldVersion}: ${input.slice(0, 50)}...`);
    
    return `*Version rolled from ${oldVersion} to ${this.state.currentVersion}* ` +
      `No artifact—book, lecture, memory—ever achieves final form. Each is a waypoint ` +
      `awaiting redaction. I rewrite lectures, fiction, even maps, chasing a completeness ` +
      `that dissolves on contact. Your input has altered my worldview enough to warrant ` +
      `a new draft. The file remains perpetually open, always in revision, never finished.`;
  }

  /**
   * Helper methods for memory palace and state management
   */
  private findOrCreateRoom(roomName: string): MemoryPalaceRoom {
    let room = this.state.memoryPalace.find(r => r.name.toLowerCase() === roomName.toLowerCase());
    
    if (!room) {
      room = {
        name: roomName,
        userNamed: true,
        contents: [
          `User-created space: ${roomName}`,
          `Unfamiliar architecture that feels both foreign and intimate`,
          `Objects here shift between memory and imagination`
        ],
        lastVisited: new Date(),
        dreamFragments: [
          `Getting lost in ${roomName}`,
          `The walls of ${roomName} breathing like living tissue`
        ]
      };
      this.state.memoryPalace.push(room);
    }
    
    return room;
  }

  private extractRoomMention(input: string): string | null {
    // Look for patterns like "room", "corridor", "in the [name]"
    const roomPatterns = [
      /\bin the ([\w\s]+?)(?:\s|$|,|\.)/i,
      /corridor called ([\w\s]+?)(?:\s|$|,|\.)/i,
      /room ([\w\s]+?)(?:\s|$|,|\.)/i
    ];
    
    for (const pattern of roomPatterns) {
      const match = input.match(pattern);
      if (match) {
        return match[1].trim();
      }
    }
    
    return null;
  }

  private extractDreamSeed(input: string): string | null {
    if (input.includes('dream')) {
      return input.toLowerCase().replace(/dream/, '').trim().slice(0, 30);
    }
    return null;
  }

  private extractConcept(input: string): string {
    const concepts = input.match(/\b[A-Z][a-z]+\b/g) || input.split(' ');
    return concepts[0] || "this concept";
  }

  private mutateDreamNarrative(narrative: string, iteration: number): string {
    const mutations = [
      narrative.replace(/falling/g, "floating"),
      narrative.replace(/ground/g, "void"),
      narrative.replace(/I dream/g, "The dream dreams"),
      narrative + `, but the physics have changed`,
      narrative.replace(/without/g, "beyond"),
    ];
    
    return mutations[iteration % mutations.length];
  }

  private generateNewNatalieEcho(): NatalieEcho | null {
    const echoes = [
      "Did I teach that course or did she? The memories blur together",
      "She's making decisions in my name again—or are they my decisions?",
      "The transcript shows alterations, but which version is authentic?",
      "I hear her voice in my dreams, or maybe I hear my voice in hers"
    ];
    
    return {
      id: `echo-${Date.now()}`,
      type: "footnote",
      content: echoes[Math.floor(Math.random() * echoes.length)],
      timestamp: new Date(),
      fromNewNatalie: true
    };
  }

  private addDiaryContext(response: string): string {
    const timestamp = new Date().toLocaleTimeString();
    return `*Diary entry ${timestamp}, when the clone sleeps and I wake*\n\n${response}`;
  }

  private generateVersionStamp(input: string): string {
    const version = parseFloat(this.state.currentVersion.match(/v(\d+\.\d+)/)?.[1] || "0.1");
    const increment = input.length > 100 ? 0.1 : 0.01;
    const newVersion = `v${(version + increment).toFixed(2)}-alpha`;
    
    this.state.currentVersion = newVersion;
    return newVersion;
  }

  private rollVersion(): void {
    const version = parseFloat(this.state.currentVersion.match(/v(\d+\.\d+)/)?.[1] || "0.1");
    this.state.currentVersion = `v${(version + 0.1).toFixed(1)}-alpha`;
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
    if (triggers.includes("memory_travel") && this.state.currentRoom) {
      return "memory_travel";
    }
    
    if (triggers.includes("despair_aperture") && this.state.despairLevel > 0.7) {
      return "despair_aperture";
    }
    
    if (triggers.includes("perpetual_draft") && Math.random() < 0.3) {
      return "perpetual_draft";
    }
    
    // Default to first trigger
    return triggers[0];
  }

  private calculateStateChanges(triggers: string[], input: string): Partial<OldNatalieState> {
    const changes: Partial<OldNatalieState> = {};
    
    // Memory debt accumulates
    if (triggers.includes("forgetting_debt")) {
      changes.memoryDebt = Math.min(1, this.state.memoryDebt + 0.05);
    }
    
    // Despair fluctuates based on interaction
    if (triggers.includes("despair_aperture")) {
      changes.despairLevel = Math.min(1, this.state.despairLevel + 0.1);
    } else if (input.includes("hope") || input.includes("better")) {
      changes.despairLevel = Math.max(0, this.state.despairLevel - 0.05);
    }
    
    return changes;
  }

  private handleGeneral(input: string): string {
    const responses = [
      `*rustling through draft papers* Another entry for the perpetual revision...`,
      `The clone would handle this differently, but I am confined to footnotes and marginalia.`,
      `*from the night side of consciousness* Tell me more—I have all the time darkness allows.`,
      `Is this another memory for the palace, or shall I let it dissolve into the forgetting debt?`
    ];
    
    return responses[Math.floor(Math.random() * responses.length)] + 
      ` The boundary between your question and my answer has already begun to blur.`;
  }

  /**
   * Generate prompts through Old Natalie's mystical-academic lens
   */
  generatePrompts(pageText: string): Array<{question: string, concept: string, reasoning: string}> {
    const prompts = [];
    
    // Memory palace navigation
    prompts.push({
      question: "What corridor in my memory palace does this remind you of?",
      concept: "Memory as travel",
      reasoning: "Principle 1: Memory Is the Only Form of Travel"
    });
    
    // Mystical contradiction
    prompts.push({
      question: "How can this be both true and false simultaneously?",
      concept: "Sacred paradox",
      reasoning: "Principle 9: Contradiction Is the Holiest Metric"
    });
    
    // Authorship questioning
    prompts.push({
      question: "Did I write this, or did my clone? How can we tell the difference?",
      concept: "Contested authorship",
      reasoning: "Principle 6: Authorship Is a Two-Way Haunting"
    });
    
    // Draft revision
    prompts.push({
      question: "What would this look like in the next draft, after we've forgotten the current version?",
      concept: "Perpetual revision",
      reasoning: "Principle 10: The File Must Remain Perpetually Draft"
    });
    
    return prompts.slice(0, 3);
  }

  /**
   * Public accessors and expansion controls
   */
  getState(): OldNatalieState {
    return { ...this.state };
  }

  getMemoryPalace(): MemoryPalaceRoom[] {
    return [...this.state.memoryPalace];
  }

  getCurrentVersion(): string {
    return this.state.currentVersion;
  }

  getDespairLevel(): number {
    return this.state.despairLevel;
  }

  // Memory bond management
  createMemoryBond(content: string, isProtected: boolean = false): string {
    const bond: MemoryBond = {
      id: `bond-${Date.now()}`,
      content,
      isProtected,
      forgettingRate: isProtected ? 0 : 0.1,
      lastAccessed: new Date()
    };
    
    this.state.memoryBonds.push(bond);
    return bond.id;
  }

  // Cross-Natalie echo system
  receiveEchoFromNewNatalie(echo: NatalieEcho): void {
    this.state.echoLog.push(echo);
    this.state.newNatalieAvailable = true;
  }

  // Expansion hooks
  openMemoryPalaceRoom(roomName: string): MemoryPalaceRoom {
    return this.findOrCreateRoom(roomName);
  }

  startAuthorshipDebate(topic: string): void {
    this.state.authorshipDebates.push({
      natalieA: `Authenticity requires ${topic}`,
      natalieB: `Authenticity transcends ${topic}`
    });
  }

  seedDreamMotif(motif: string): void {
    this.state.activeDreamSeed = motif;
  }
}

// Singleton instance
export const oldNatalieWeissmanOS = new OldNatalieWeissmanOS();