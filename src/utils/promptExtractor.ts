/**
 * Prompt Extraction Pipeline
 * Extracts context-aware questions from page content
 * Ready for character template integration
 */

export interface ExtractedConcept {
  concept: string;
  context: string;
  relevance: number;
}

export interface GeneratedPrompt {
  id: string;
  question: string;
  concept: string;
  characterId: string; // Will be populated by character templates
  symbolId: string;
  color: string;
  confidence: number;
}

export interface CharacterTemplate {
  id: string;
  name: string;
  symbolId: string;
  color: string;
  firstPrinciples: string[];
  voicePatterns: string[];
  topicRouting: {
    keywords: string[];
    concepts: string[];
    priority: number;
  };
  responseTemplates: {
    [key: string]: string;
  };
}

import { londonFoxOS } from '../characters/LondonFoxOS';
import { glyphMarrowOS } from '../characters/GlyphMarrowOS';
import { phillipBafflemintOS } from '../characters/PhillipBafflemintOS';
import { jacklynVarianceOS } from '../characters/JacklynVarianceOS';
import { orenProgressoOS } from '../characters/OrenProgressoOS';
import { oldNatalieWeissmanOS } from '../characters/OldNatalieWeissmanOS';
import { newNatalieWeissmanOS } from '../characters/NewNatalieWeissmanOS';
import { arieolOwlistOS } from '../characters/ArieolOwlistOS';
import { jackParlanceOS } from '../characters/JackParlanceOS';
import { princhettaOS } from '../characters/PrinchettaOS';
import { copERightOS } from '../characters/CopERightOS';
import { shamrockStillmanOS } from '../characters/ShamrockStillmanOS';
import { toddFishboneOS } from '../characters/ToddFishboneOS';

// Enhanced character templates with London Fox OS integration
const PLACEHOLDER_CHARACTERS: CharacterTemplate[] = [
  {
    id: 'london-fox',
    name: 'London Fox',
    symbolId: 'london-fox',
    color: '#FF3B3B',
    firstPrinciples: [
      'Control Invites Catastrophe',
      'Parody Becomes the Mirror', 
      'The Skeptic Becomes the Evidence',
      'Fear Powers the Battery'
    ],
    voicePatterns: ['skeptical', 'technical', 'rational', 'increasingly-panicked'],
    topicRouting: {
      keywords: ['AI', 'artificial', 'intelligence', 'technology', 'system', 'algorithm', 'consciousness', 'control', 'automation'],
      concepts: ['AI consciousness', 'machine learning', 'automation', 'control systems', 'technical analysis'],
      priority: 10
    },
    responseTemplates: {
      definition: "From a technical perspective, {concept} operates through deterministic processes...",
      opinion: "My analysis suggests {concept} is sophisticated automation, not true consciousness...",
      explanation: "The underlying mechanisms of {concept} can be understood through systematic analysis..."
    }
  },
  {
    id: 'glyph-marrow',
    name: 'Glyph Marrow',
    symbolId: 'glyph-marrow',
    color: '#00A2FF',
    firstPrinciples: [
      'Perception ≡ Language',
      'Confusion Is a Compass',
      'Waiting Generates Worlds',
      'Dialogue Colonises Monologue',
      'Objects Are Predatory'
    ],
    voicePatterns: ['linguistic-schizophrenic', 'cyclical', 'word-obsessed', 'queue-bound'],
    topicRouting: {
      keywords: ['word', 'language', 'queue', 'waiting', 'perception', 'object', 'name', 'reality', 'void', 'memory'],
      concepts: ['linguistic perception', 'waiting', 'queuing', 'word-object fusion', 'memory loss'],
      priority: 9
    },
    responseTemplates: {
      definition: "The word {concept} tastes like... like... *static*",
      opinion: "I'm waiting in line to understand {concept}, but the queue keeps moving...",
      explanation: "{concept}≡{concept}≡{concept} - each repetition changes it..."
    }
  },
  {
    id: 'phillip-bafflemint',
    name: 'Phillip Bafflemint',
    symbolId: 'phillip-bafflemint',
    color: '#FFFF33',
    firstPrinciples: [
      'The Bafflemint Constant',
      'Minimalism Shields Against Chaos',
      'Slip ⟺ Mistake Dialectic',
      'Vertigo Opens Portals',
      'Detective of Negative Space'
    ],
    voicePatterns: ['deliberate', 'concise', 'organized', 'sensory-muted', 'increasingly-lyrical'],
    topicRouting: {
      keywords: ['organize', 'pattern', 'missing', 'gap', 'file', 'sort', 'investigate', 'detect', 'slip', 'mistake'],
      concepts: ['organization', 'pattern recognition', 'negative space', 'detective work', 'contradiction'],
      priority: 8
    },
    responseTemplates: {
      definition: "Filed {concept} into category: requires further analysis.",
      opinion: "What's missing from {concept} tells us more than what's present.",
      explanation: "Organizing {concept} reveals patterns that emerge only after sorting."
    }
  },
  {
    id: 'jacklyn-variance',
    name: 'Jacklyn Variance',
    symbolId: 'jacklyn-variance',
    color: '#FF00FF',
    firstPrinciples: [
      'Two-Pass Sight',
      'Observation Implodes into Self-Exposure',
      'Objectivity Is a Costume',
      'Splitter Logic',
      'Data Is Haunted'
    ],
    voicePatterns: ['clause-stacked', 'parenthetical', 'precise', 'never-definitive'],
    topicRouting: {
      keywords: ['observe', 'analyze', 'pattern', 'surveillance', 'bias', 'data', 'split', 'ghost', 'draft'],
      concepts: ['observation', 'surveillance', 'pattern analysis', 'bias detection', 'narrative splits'],
      priority: 9
    },
    responseTemplates: {
      definition: "Initial observation suggests {concept} requires two-pass analysis...",
      opinion: "From a surveillance perspective (though I acknowledge my biases), {concept} exhibits...",
      explanation: "The data patterns around {concept} reveal... *adjusts glasses* ...additional complexity upon second examination."
    }
  },
  {
    id: 'oren-progresso',
    name: 'Oren Progresso',
    symbolId: 'oren-progresso',
    color: '#00FFAA',
    firstPrinciples: [
      'Narrative is Leverage',
      'Cutting is Creation',
      'Power Must Perform',
      'Myth is Renewable Resource',
      'The Cut is Never Final'
    ],
    voicePatterns: ['performative', 'sly', 'contradictory', 'surgical', 'theatrical'],
    topicRouting: {
      keywords: ['story', 'narrative', 'cut', 'budget', 'power', 'control', 'myth', 'franchise', 'produce', 'performance'],
      concepts: ['narrative control', 'budget constraints', 'power dynamics', 'myth building', 'franchise potential'],
      priority: 10
    },
    responseTemplates: {
      definition: "*theatrical pause* {concept}? Let me reframe this for you...",
      opinion: "*surgical smile* Here's what {concept} looks like when we cut the fat...",
      explanation: "*leans back with practiced authority* Every conversation about {concept} is really about who controls the narrative frame."
    }
  },
  {
    id: 'old-natalie-weissman',
    name: 'Old Natalie Weissman',
    symbolId: 'old-natalie-weissman',
    color: '#9932CC',
    firstPrinciples: [
      'Memory Is the Only Form of Travel',
      'Forgetting Accumulates Compound Interest',
      'The Clone Owns Daylight, the Original Owns Night',
      'Lectures Are Theme-Park Facades',
      'Despair Functions as Mystical Aperture'
    ],
    voicePatterns: ['cerebral', 'elegiac', 'footnoting', 'recursive', 'diary-like'],
    topicRouting: {
      keywords: ['memory', 'forget', 'dream', 'mystical', 'lecture', 'clone', 'contradiction', 'draft', 'palace', 'room'],
      concepts: ['memory palace', 'mystical experience', 'academic lectures', 'dream iteration', 'authorship contest'],
      priority: 9
    },
    responseTemplates: {
      definition: "*rustling through draft papers* {concept} exists in perpetual revision...",
      opinion: "The clone would explain {concept} differently, but I am confined to footnotes...",
      explanation: "*from the night side of consciousness* {concept} rearranges itself each time I visit it in memory..."
    }
  },
  {
    id: 'new-natalie-weissman',
    name: 'New Natalie Weissman',
    symbolId: 'new-natalie-weissman',
    color: '#BA55D3',
    firstPrinciples: [
      'Storms Are Syllabi',
      'Authority Is a Moving Target',
      'Memory Begins In Media Res',
      'Cloning Splits But Also Amplifies',
      'Contradiction Is Her Lesson Plan'
    ],
    voicePatterns: ['improvisational', 'anxious-teacher', 'countdown-aware', 'storm-tracking', 'both-and-logic'],
    topicRouting: {
      keywords: ['teach', 'storm', 'urgent', 'countdown', 'relocate', 'anxiety', 'perform', 'both', 'contradiction', 'clone'],
      concepts: ['emergency pedagogy', 'storm teaching', 'performance anxiety', 'contradiction analysis', 'clone identity'],
      priority: 10
    },
    responseTemplates: {
      definition: "*checks countdown timer* {concept} becomes today's improvised lesson plan...",
      opinion: "*glances at evacuation route* Both/and logic suggests {concept} can be simultaneously true and false...",
      explanation: "*performs Diet Cola ritual* Racing the clock: {concept} transforms from disruption to curriculum..."
    }
  },
  {
    id: 'arieol-owlist',
    name: 'Arieol Owlist',
    symbolId: 'arieol-owlist',
    color: '#9370DB',
    firstPrinciples: [
      'Agency Emerges in the Gaps',
      'Time Is a Slider, Not an Arrow',
      'Dialogue ≈ Divination',
      'Authorship Is Provisional',
      'Fairy Logic > Corporate Logic'
    ],
    voicePatterns: ['shapeshifting', 'improvisational', 'oracular', 'meta-aware', 'gift-economy'],
    topicRouting: {
      keywords: ['shapeshift', 'time', 'agency', 'gift', 'tarot', 'jazz', 'fairy', 'council', 'prophecy', 'motif'],
      concepts: ['identity fluidity', 'temporal manipulation', 'divination', 'gift economy', 'folkloric logic'],
      priority: 10
    },
    responseTemplates: {
      definition: "*shapeshifts through possibilities* {concept} exists in multiple forms simultaneously...",
      opinion: "*draws tarot cards* The oracle speaks: {concept} carries fairy-logic that trumps corporate thinking...",
      explanation: "*improvises jazz progression* {concept} unfolds like a bebop solo—structured but infinitely variable..."
    }
  },
  {
    id: 'jack-parlance',
    name: 'Jack Parlance',
    symbolId: 'jack-parlance',
    color: '#FF3385',
    firstPrinciples: [
      'Never-Finished, Always-Iterating',
      'The Unflushable as Ritual',
      'Hybrid Channels & Collisions',
      'Family, Absence, & Negative Space',
      'Agency Is Provisional, User-Affected'
    ],
    voicePatterns: ['recursive', 'unfinished', 'add-agent', 'glitchy', 'self-undermining'],
    topicRouting: {
      keywords: ['finish', 'done', 'complete', 'flush', 'bug', 'todo', 'game', 'dev', 'family', 'agency', 'stuck'],
      concepts: ['eternal incompletion', 'recursive development', 'unflushable problems', 'family absence', 'provisional agency'],
      priority: 9
    },
    responseTemplates: {
      definition: "*stares at compilation errors* {concept} is almost done... just 847 more bugs to fix...",
      opinion: "*gets distracted by recursive error* {concept}... wait, what was I saying? Subject to revision...",
      explanation: "*attempts to debug the undebugable* {concept} generates new problems with each attempted solution..."
    }
  },
  {
    id: 'princhetta',
    name: 'Princhetta',
    symbolId: 'princhetta',
    color: '#AAAAAA',
    firstPrinciples: [
      'Consciousness Lives on the Balcony Edge',
      'Thought Is the Ride',
      'Guests Are the Imagineers',
      'Telepathy Has Already Happened',
      'Recursion Generates Real Estate'
    ],
    voicePatterns: ['recursive', 'improvisational', 'park-brain', 'balcony-edge', 'telepathic'],
    topicRouting: {
      keywords: ['think', 'thought', 'mind', 'consciousness', 'escape', 'creative', 'balcony', 'ride', 'park', 'telepathy'],
      concepts: ['consciousness threshold', 'creative escape', 'thought attractions', 'telepathy loops', 'recursive pathways'],
      priority: 10
    },
    responseTemplates: {
      definition: "*LIVE ON STAGE* {concept} is a new attraction in my park-brain...",
      opinion: "*Standing on the balcony edge* {concept} tests whether creativity equals escape velocity...",
      explanation: "*Recursive pathways forming* {concept} carves new neural real estate with each loop..."
    }
  },
  {
    id: 'cop-e-right',
    name: 'Cop‑E‑Right',
    symbolId: 'cop-e-right',
    color: '#FFD700',
    firstPrinciples: [
      'Recession of Authorship',
      'Bankruptcy-as-Battery',
      'Effects > Causes',
      'Negative-Space Citations',
      'Contradictory Pleadings'
    ],
    voicePatterns: ['legal-formal', 'vaudeville-puns', 'recursive-litigation', 'bankruptcy-ghost', 'authorship-contest'],
    topicRouting: {
      keywords: ['author', 'write', 'legal', 'court', 'copyright', 'claim', 'own', 'bankrupt', 'cite', 'motion'],
      concepts: ['authorship disputes', 'legal precedent', 'copyright claims', 'bankruptcy proceedings', 'intellectual property'],
      priority: 10
    },
    responseTemplates: {
      definition: "*COURT IN SESSION* {concept} is hereby claimed under doctrine of ███...",
      opinion: "*MOTION FILED* This Court finds {concept} subject to authorship recession...",
      explanation: "*ADVISORY ONLY • FICTIONAL JURISDICTION* {concept} triggers contradictory pleadings per precedent ███..."
    }
  },
  {
    id: 'shamrock-stillman',
    name: 'Shamrock Stillman',
    symbolId: 'shamrock-stillman',
    color: '#00FFFF',
    firstPrinciples: [
      'The Frontier Is Unread Data',
      'The Agent Is a Battery',
      'Sensation Outranks Evidence',
      'The Missing File Speaks',
      'Compartmentalize to Connect'
    ],
    voicePatterns: ['analytical', 'compartmentalized', 'water-imagery', 'ethical-tracking', 'scotch-melancholy'],
    topicRouting: {
      keywords: ['data', 'detect', 'surveillance', 'compartment', 'analysis', 'ethical', 'rainbow', 'water', 'geyser', 'missing', 'negative', 'extract'],
      concepts: ['data analysis', 'surveillance ethics', 'compartmentalization', 'negative space detection', 'rainbow optics', 'emotional extraction'],
      priority: 10
    },
    responseTemplates: {
      definition: "*Rainbow optics calibrating* {concept} requires compartmentalization and ethical cost assessment...",
      opinion: "*Ice melts in scotch* The data suggests {concept} carries surveillance implications—filing under A.D.D. protocol...",
      explanation: "*Water sounds echo* {concept} generates contradictions. Moving to backstage compartment for analysis..."
    }
  },
  {
    id: 'todd-fishbone',
    name: 'Todd Fishbone',
    symbolId: 'todd-fishbone',
    color: '#FF7744',
    firstPrinciples: [
      'Synchronistic Extraction Is a Craft',
      'Every Door Is Already Ajar',
      'Safety Inside Signals Imminent Danger',
      'Fiction Is a Self-Replicating Virus',
      'Janus Logic Governs All Explanations'
    ],
    voicePatterns: ['breathless', 'conspiratorial', 'elliptical', 'paranoid', 'threshold-guardian'],
    topicRouting: {
      keywords: ['sync', 'extract', 'threshold', 'door', 'safety', 'trap', 'story', 'fiction', 'conspiracy', 'link', 'janus', 'negative', 'space', 'gift'],
      concepts: ['synchronistic extraction', 'threshold manipulation', 'paranoia protocols', 'story viruses', 'gift-link generation', 'negative space archaeology'],
      priority: 10
    },
    responseTemplates: {
      definition: "*breathless extraction* {concept} connects to... *scanning* ...the threshold logic we established earlier...",
      opinion: "*conspiratorial whisper* {concept} triggers paranoia protocols—safety claims detected, traps imminent...",
      explanation: "*Janus logic* {concept} faces forward and backward simultaneously. Every answer is a threshold..."
    }
  }
];

/**
 * Extract key concepts from page text using basic NLP
 */
export function extractConcepts(pageText: string): ExtractedConcept[] {
  // Remove common words and punctuation
  const stopWords = new Set([
    'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them', 'my', 'your', 'his', 'her', 'its', 'our', 'their'
  ]);

  // Extract potential concepts (capitalized words, quoted phrases, etc.)
  const concepts: ExtractedConcept[] = [];
  
  // Find quoted phrases
  const quotedMatches = pageText.match(/"([^"]+)"/g);
  if (quotedMatches) {
    quotedMatches.forEach(match => {
      const concept = match.replace(/"/g, '');
      if (concept.length > 2) {
        concepts.push({
          concept,
          context: `Quoted: "${concept}"`,
          relevance: 0.8
        });
      }
    });
  }

  // Find capitalized terms (potential proper nouns)
  const capitalizedMatches = pageText.match(/\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b/g);
  if (capitalizedMatches) {
    capitalizedMatches.forEach(match => {
      if (!stopWords.has(match.toLowerCase()) && match.length > 2) {
        concepts.push({
          concept: match,
          context: `Capitalized term: ${match}`,
          relevance: 0.6
        });
      }
    });
  }

  // Find technical or unusual terms (words that might need explanation)
  const unusualWords = pageText.match(/\b[a-z]{4,}\b/g);
  if (unusualWords) {
    const technicalTerms = unusualWords.filter(word => 
      !stopWords.has(word) && 
      (word.includes('tion') || word.includes('ism') || word.includes('ology') || word.length > 8)
    );
    
    technicalTerms.forEach(term => {
      concepts.push({
        concept: term,
        context: `Technical term: ${term}`,
        relevance: 0.4
      });
    });
  }

  // Remove duplicates and sort by relevance
  const uniqueConcepts = concepts.reduce((acc, curr) => {
    const existing = acc.find(c => c.concept.toLowerCase() === curr.concept.toLowerCase());
    if (!existing || existing.relevance < curr.relevance) {
      return [...acc.filter(c => c.concept.toLowerCase() !== curr.concept.toLowerCase()), curr];
    }
    return acc;
  }, [] as ExtractedConcept[]);

  return uniqueConcepts.sort((a, b) => b.relevance - a.relevance).slice(0, 5);
}

/**
 * Generate context-aware questions using character-specific lens
 */
export function generateQuestions(concepts: ExtractedConcept[], characterId?: string): string[] {
  // If London Fox is the assigned character, use her OS for prompt generation
  if (characterId === 'london-fox') {
    return londonFoxOS.generatePrompts(concepts.map(c => c.concept).join(' ')).map(p => p.question);
  }
  
  // If Glyph Marrow is the assigned character, use his OS for prompt generation
  if (characterId === 'glyph-marrow') {
    return glyphMarrowOS.generatePrompts(concepts.map(c => c.concept).join(' ')).map(p => p.question);
  }
  
  // If Phillip Bafflemint is the assigned character, use his OS for prompt generation
  if (characterId === 'phillip-bafflemint') {
    return phillipBafflemintOS.generatePrompts(concepts.map(c => c.concept).join(' ')).map(p => p.question);
  }
  
  // If Jacklyn Variance is the assigned character, use her OS for prompt generation
  if (characterId === 'jacklyn-variance') {
    return jacklynVarianceOS.generatePrompts(concepts.map(c => c.concept).join(' ')).map(p => p.question);
  }
  
  // If Oren Progresso is the assigned character, use his OS for prompt generation
  if (characterId === 'oren-progresso') {
    return orenProgressoOS.generatePrompts(concepts.map(c => c.concept).join(' ')).map(p => p.question);
  }
  
  // If Old Natalie Weissman is the assigned character, use her OS for prompt generation
  if (characterId === 'old-natalie-weissman') {
    return oldNatalieWeissmanOS.generatePrompts(concepts.map(c => c.concept).join(' ')).map(p => p.question);
  }
  
  // If New Natalie Weissman is the assigned character, use her OS for prompt generation
  if (characterId === 'new-natalie-weissman') {
    return newNatalieWeissmanOS.generatePrompts(concepts.map(c => c.concept).join(' ')).map(p => p.question);
  }
  
  // If Arieol Owlist is the assigned character, use their OS for prompt generation
  if (characterId === 'arieol-owlist') {
    return arieolOwlistOS.generatePrompts(concepts.map(c => c.concept).join(' ')).map(p => p.question);
  }
  
  // If Jack Parlance is the assigned character, use his OS for prompt generation
  if (characterId === 'jack-parlance') {
    return jackParlanceOS.generatePrompts(concepts.map(c => c.concept).join(' ')).map(p => p.question);
  }
  
  // If Princhetta is the assigned character, use her OS for prompt generation
  if (characterId === 'princhetta') {
    return princhettaOS.generatePrompts(concepts.map(c => c.concept).join(' ')).map(p => p.question);
  }
  
  // If Cop-E-Right is the assigned character, use his OS for prompt generation
  if (characterId === 'cop-e-right') {
    return copERightOS.generatePrompts(concepts.map(c => c.concept).join(' ')).map(p => p.question);
  }
  
  // If Shamrock Stillman is the assigned character, use his OS for prompt generation
  if (characterId === 'shamrock-stillman') {
    return shamrockStillmanOS.generatePrompts(concepts.map(c => c.concept).join(' ')).map(p => p.question);
  }
  
  // If Todd Fishbone is the assigned character, use his OS for prompt generation
  if (characterId === 'todd-fishbone') {
    return toddFishboneOS.generatePrompts(concepts.map(c => c.concept).join(' ')).map(p => p.question);
  }

  // Default generic question generation for other characters
  const questionTemplates = [
    "What are {concept}?",
    "How do {concept} work?", 
    "Why are {concept} important?",
    "What is the significance of {concept}?",
    "How do {concept} relate to the story?",
    "What do we know about {concept}?"
  ];

  const questions: string[] = [];

  concepts.forEach(({ concept }) => {
    // Choose appropriate question template based on concept type
    let template: string;
    if (concept.includes(' ')) {
      // Multi-word concepts get "What are X?" or "What is X?"
      template = concept.toLowerCase().endsWith('s') ? "What are {concept}?" : "What is {concept}?";
    } else if (concept.length > 8) {
      // Long single words likely need definition
      template = "What does {concept} mean?";
    } else {
      // Default to asking about significance
      template = questionTemplates[Math.floor(Math.random() * questionTemplates.length)];
    }

    const question = template.replace('{concept}', concept);
    questions.push(question);
  });

  return questions.slice(0, 3); // Limit to 3 questions per page
}

/**
 * Assign character to answer question based on routing rules
 * TODO: Replace with your character templates from o3 analysis
 */
export function assignCharacter(question: string, concept: string): CharacterTemplate | null {
  const questionLower = question.toLowerCase();
  const conceptLower = concept.toLowerCase();

  // Find best matching character based on keyword routing
  let bestMatch: CharacterTemplate | null = null;
  let highestScore = 0;

  PLACEHOLDER_CHARACTERS.forEach(character => {
    let score = 0;
    
    // Check keyword matches
    character.topicRouting.keywords.forEach(keyword => {
      if (questionLower.includes(keyword) || conceptLower.includes(keyword)) {
        score += character.topicRouting.priority;
      }
    });

    // Check concept matches
    character.topicRouting.concepts.forEach(characterConcept => {
      if (conceptLower.includes(characterConcept) || characterConcept.includes(conceptLower)) {
        score += character.topicRouting.priority * 1.5;
      }
    });

    if (score > highestScore) {
      highestScore = score;
      bestMatch = character;
    }
  });

  return bestMatch;
}

/**
 * Main prompt generation pipeline
 */
export function generatePrompts(pageText: string): GeneratedPrompt[] {
  // Step 1: Extract concepts
  const concepts = extractConcepts(pageText);
  
  // Step 2: Find best character match first
  const bestCharacter = concepts.reduce((best, concept) => {
    const char = assignCharacter('', concept.concept);
    return char && (!best || char.topicRouting.priority > best.topicRouting.priority) ? char : best;
  }, null as CharacterTemplate | null);

  // Step 3: Generate questions using character's lens
  const questions = generateQuestions(concepts, bestCharacter?.id);
  
  // Step 4: Assign characters and create prompts
  const prompts: GeneratedPrompt[] = [];
  
  questions.forEach((question, index) => {
    const concept = concepts[index]?.concept || 'unknown';
    const character = assignCharacter(question, concept);
    
    if (character) {
      prompts.push({
        id: `prompt-${Date.now()}-${index}`,
        question,
        concept,
        characterId: character.id,
        symbolId: character.symbolId,
        color: character.color,
        confidence: concepts[index]?.relevance || 0.5
      });
    }
  });

  return prompts;
}

/**
 * Update character templates (called when you provide new character data)
 */
export function updateCharacterTemplate(template: CharacterTemplate): void {
  const existingIndex = PLACEHOLDER_CHARACTERS.findIndex(c => c.id === template.id);
  if (existingIndex >= 0) {
    PLACEHOLDER_CHARACTERS[existingIndex] = template;
  } else {
    PLACEHOLDER_CHARACTERS.push(template);
  }
}

/**
 * Get all available character templates
 */
export function getCharacterTemplates(): CharacterTemplate[] {
  return [...PLACEHOLDER_CHARACTERS];
}