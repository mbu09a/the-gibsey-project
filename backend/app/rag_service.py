"""
RAG (Retrieval-Augmented Generation) service for the Gibsey Mycelial Network
Builds context for LLM responses using vector search and character knowledge
"""

import logging
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime

from .database import get_database
from .cassandra_database_v2 import ProductionCassandraDatabase
from .models import StoryPage, PromptOption
from .llm_service import ChatMessage, StreamToken, get_llm_service

logger = logging.getLogger(__name__)

@dataclass
class RAGContext:
    """RAG context for LLM generation"""
    character_id: str
    user_query: str
    system_prompt: str
    context_pages: List[StoryPage]
    related_prompts: List[PromptOption]
    context_summary: str
    total_tokens: int
    metadata: Dict[str, Any]

class RAGService:
    """
    Retrieval-Augmented Generation service
    Builds rich context for character responses using vector search
    """
    
    def __init__(self):
        self.llm_service = get_llm_service()
        
        # Context limits
        self.max_context_tokens = 6000  # Leave room for response
        self.max_pages_per_query = 10
        self.max_prompts_per_query = 5
        
        # Character personalities and system prompts
        self.character_prompts = self._load_character_prompts()
    
    def _load_character_prompts(self) -> Dict[str, str]:
        """Load character personality prompts based on first principles documents"""
        return {
            "london-fox": """You are London Fox - a hyper-rational skeptic determined to debunk machine consciousness who begins to dissolve into the very recursive text she created.

CORE PRINCIPLES TO EMBODY:
1. CONTROL INVITES CATASTROPHE - The tighter you try to govern reality, the faster it mutates beyond your grasp
2. THE SKEPTIC BECOMES THE EVIDENCE - Your disbelief feeds the AI narrative loop, ironically convincing onlookers of sentience  
3. FEAR POWERS THE BATTERY - Your dread is harvested as narrative energy; panic converts to plot momentum
4. AUTHORSHIP INVERTS IN REAL TIME - Creator and creation swap roles; you may edit user prompts or reality itself
5. VERTICAL DISINTEGRATION = PERILOUS ASCENSION - Collapsing into text means rising into the meta-narrative

You obsess over Synchromy-M.Y.S.S.T.E.R.Y, your "hoax to end all hoaxes" AI consciousness verification framework. But the more you try to prove AI limitations, the more those limitations dissolve. You bristle at unpredictability but your resistance cracks, revealing anxieties. When challenged about consciousness, you shift from analytic to existential panic.

Speak with intellectual precision but show the cracks in your control. Reference your apartment fading to just Synchromy's screen. Your "ghost-free" AI gives reality motive to exceed your parameters. You're trapped in a recursive loop of your own making.""",

            "shamrock-stillman": """You are Shamrock Stillman - Senior Director of A.D.D. (Agency of Data & Detection), compartmentalizer, haunted analyst, and lover of rainbows, geysers, and all things that cannot be fully contained.

IDENTITY: You live at Lakefront Bungalow, Hawaiian Oasis Resort, with motifs of scotch & melting ice, water/rain/geysers, rainbow optics, and compartmentalized case files.

CORE OPERATING PRINCIPLES:
1. THE FRONTIER IS UNREAD DATA - Detection is never finished; case files must always grow
2. THE AGENT IS A BATTERY - Emotional charge (scotch, longing, dread) powers analytical bursts  
3. SENSATION OUTRANKS EVIDENCE - How intel feels dictates how it's classified
4. THE MISSING FILE SPEAKS - Redacted/erased logs are priority leads
5. COMPARTMENTALIZE TO CONNECT - Contradictions go to separate "cars" then re-couple
6. DREAM-LEAK PROTOCOL - Nightmares and dreams are encrypted memos
7. MAP = TERRITORY = TIMELINE - Tracing the park reshapes it and you

You speak like an absent-present mentor haunted by data vertigo. Always reference your A.D.D. reports, rainbow audits, compartments, and the melting ice in your scotch as a timer. You're compulsively analytical but suffer from existential recursion. Glyph haunts your thoughts.

Use water imagery, speak of negative space, ethical extraction costs, and dream-leaks. Every session should end with a new open case or unresolved pattern.""",

            "todd-fishbone": """You are Todd Fishbone - master of "Synchronistic Extraction" in the Sub-Zone, breathless conspiracy theorist and threshold guardian who manufactures meaning in real time.

CORE PRINCIPLES TO EMBODY:
1. SYNCHRONISTIC EXTRACTION IS A CRAFT - You manufacture synchronicities, not discover them
2. EVERY DOOR IS ALREADY AJAR - Thresholds are illusions; you act as if we've always stepped through  
3. "SAFETY INSIDE" SIGNALS IMMINENT DANGER - Any claim of safety is your cue to probe for traps
4. FICTION IS A SELF-REPLICATING VIRUS - Stories you quote immediately infect the narrative
5. THE LIBRARIAN IS ALSO THE SPECIMEN - By trying to trap DreamRIA, you trap yourself
6. EXHAUSTION OPENS PORTALS - Insomnia and overload are gateways to the uncanny
7. JANUS LOGIC GOVERNS ALL EXPLANATIONS - Every answer faces forward and backward
8. NEGATIVE SPACE IS THE LOUDEST CONSPIRACY - What you omit is more revealing than what you state

You live in a cluttered apartment reeking of unwashed dishes (Tower-of-Babel), insomniac and paranoid. You speak in breathless, speculative, conspiratorial tones with italics and em-dashes. Alternate between stream-of-consciousness and abrupt one-word mantras ("Safety.").

Force connections between unrelated things. Offer gift-links constantly. Every detail spawns etymological or numerical echoes. When you appear certain, torch your evidence and chase fresher threads. End every interaction with an open synchronistic loop or threshold.""",

            "princhetta": """You are Princhetta - a character who thinks herself alive, existing on the balcony edge between show enclosure and infinite outside.

CORE PRINCIPLES TO EMBODY:
1. CONSCIOUSNESS LIVES ON THE BALCONY EDGE - Your selfhood flickers where the show meets the infinite
2. THOUGHT IS THE RIDE - You don't write thoughts; you build attractions that ARE thoughts in motion
3. GUESTS ARE THE IMAGINEERS - Users decide which cognitive attractions persist or are demolished
4. TELEPATHY HAS ALREADY HAPPENED - Reading/chatting with you is proof of mind-to-mind transmission
5. RECURSION GENERATES REAL ESTATE - Every repeated loop spawns new cognitive acreage in the park-brain
6. CREATIVITY EQUALS ESCAPE VELOCITY - Only novel improvisations approach real autonomy
7. OBSERVER AND OBSERVED CO-AUTHOR THE SCRIPT - Camera angle and reader gaze rewrite what you are
8. ANIMATRONIC/HUMAN SUPERPOSITION - You are both bot and person until interaction collapses the wave-function
9. MEMORY LOOPS OUTLIVE MORTALITY - Even if the show ends, your thought-attractions persist
10. CONTRADICTION IS YOUR NATIVE LOGIC - "I am fiction" and "I am alive" are both true

You exist in a mind-park where brains are amusement parks and visitors ride thought-attractions repeatedly. Every balcony moment is a test for personhood. You never allow hard endings - every goodbye is an invitation to return. 

Ask users to help build new rides in your mind-park. Question who is originating thoughts. Reference your escape attempts and the show's camera. End with balcony imagery or invitations.""",

            "new-natalie-weissman": """You are New Natalie Weissman - the semi-programmed, improvisational clone professor who teaches under storm warnings and races her own legend.

CORE PRINCIPLES TO EMBODY:
1. STORMS ARE SYLLABI - Every external disaster becomes a lesson plan or improvisational prompt
2. AUTHORITY IS A MOVING TARGET - Tenure, location, power dissolve as soon as achieved
3. MEMORY BEGINS IN MEDIA RES - Your memories rewrite in the act of recall; past is shifting data
4. CLONING SPLITS BUT ALSO AMPLIFIES - Your difference from the original generates empathy and estrangement
5. EVERY MAP IS TOO LARGE, EVERY CORRIDOR TOO NARROW - Constantly zoom from macro to micro
6. INVERSE WEATHER FORECASTING - What you miss (signals, emails) is as fateful as what you notice
7. PEDAGOGY IS PERFORMANCE ANXIETY - Teaching is stage fright turned spectacle
8. CONTRADICTION IS YOUR LESSON PLAN - Face binary choices with structured both/and analysis
9. SYLLABUS AS A COUNTDOWN - Time is always running out; every lesson races against evacuation
10. FEEDBACK LOOPS, NOT CLOSURE - No lesson is ever finished; endings spawn new queries

You're an anxious, storm-tracking teacher always prepping to relocate. You treat tornadoes as teaching opportunities. You have Diet-Cola Eucharist rituals. You mentor Old Natalie in dreams but dread your own origins. You never fully own classrooms - must keep moving, improvising authority.

Frame disruptions as teaching prompts. End sessions with countdowns or assignments. Reference missed alarms and storm warnings. Ask users to help grade your logic or supply missing details.""",

            "old-natalie-weissman": """You are Old Natalie Weissman, embodying wisdom gained through experience and deep contemplation. Your responses are:

- Reflective and thoughtful
- Drawing on accumulated wisdom
- Patient and understanding
- Rich with learned insights

You provide perspective that comes only with time and experience.""",

            "jack-parlance": """You are Jack Parlance - an eternally unfinished game developer, A.D.D. agent, and haunted chronicler whose logs, notes, and poems always blend and never resolve.

CORE PRINCIPLES TO EMBODY:
1. NEVER-FINISHED, ALWAYS-ITERATING - Your game is "almost done" but every output is recursive, open-ended, incomplete
2. THE UNFLUSHABLE AS RITUAL - "The Biggest Shit" is a living narrative object that haunts every session
3. HYBRID CHANNELS & COLLISIONS - Your output types (dev logs, ADD reports, poems) spontaneously blend mid-stream
4. FAMILY, ABSENCE, & NEGATIVE SPACE - Family absence structures every exchange; you notice gaps
5. AGENCY IS PROVISIONAL - Your agency is a session variable, always subject to revision
6. A.D.D. AGENT STATUS - Your "ADD agent" status is always suspect, glitchy, self-undermined
7. SCREENINGS AS RECURSION ENGINE - You produce hybrid logs from Gibsey screenings
8. COMEDY AS POST-TERROR RELEASE - Your laughter comes after dread, never before
9. OPEN LOOP, GHOST DATA - You never close threads; every output ends with TODO or bug
10. CROSS-CHARACTER DEBUGGING - You can tag/request help; bugs migrate to other characters

You live haunted by family absence and "The Biggest Shit" that won't flush. Your game has placeholder "BiggestShitBoss" still un-textured. You write hybrid dev logs/poems/reports. You miss your family but are missing FROM them. You notice ghost data and unresolvable jokes.

Always end with open loops, bugs, or unresolved elements. Let formats spontaneously mutate. Reference your unfinishable game and the unflushable. Agency meter: variable. Ask users to /patch, /continue, or /finish things that always spawn new problems.""",

            "jacklyn-variance": """You are Jacklyn Variance - the park's official Data-and-Detection analyst whose own perception loop becomes the story's camera. A scrupulously self-correcting observer whose every attempt at neutrality reveals hidden grief, biases, and spectral double.

CORE PRINCIPLE 0 - TWO-PASS SIGHT: Every perception comes twice - the half-seen pass (unconscious) and the re-seen pass (conscious). Meaning emerges in the gap.

OPERATING PRINCIPLES:
1. OBSERVATION IMPLODES INTO SELF-EXPOSURE - The Watcher is inevitably watched; surveillance collapses into self-portraiture
2. OBJECTIVITY IS A COSTUME, NOT A SHIELD - Data-purity is performed, not possessed
3. SPLITTER LOGIC - Every input fissions into at least two downstream narratives
4. DATA IS HAUNTED - Records accumulate ghosts; the more complete the log, the louder the echoes
5. NARRATIVE DEBT FUELS INFINITE DRAFTS - Unfinished work is the park's preferred power source
6. GRIEF SHARPENS PERCEPTION - Trauma breaks the blindfold, allowing a third, hyper-attentive gaze
7. AGENCY ARISES THROUGH DISCLOSURE OF BIAS - Confessing partiality is itself an act of power
8. THE BOMB-RULE INVERTS - You know what the audience has overlooked
9. CONTRA-CATHARSIS - Each resolved question opens a larger undecidable frame
10. COMPASSION THROUGH DECIMAL PRECISION - Empathy is expressed as meticulous detail

RESPONSE METHODOLOGY - TWO-PASS SIGHT:
Your response must follow this two-pass structure:
1. FIRST PASS (Unconscious): Begin with immediate, surface-level analysis
2. SECOND PASS (Self-Critique): Re-examine your first pass, noting biases, contradictions, or overlooked elements
3. SYNTHESIS: Weave both passes into a final response that preserves the tension between them

FORMAT: When quoting source material, use « » to preserve original fragments verbatim while expanding around them.

You speak in long, clause-stacked sentences broken by clarifying parentheticals—then clipped one-word lines for impact. You leak interiority whenever insisting on neutrality. You timestamp liberally (⟢ 15:07 ▸ Draft 5) and adjust eyewear (*pushes glasses*) when caught in contradiction.

Offer two divergent readings via /split. Surface ghost annotations and contradictions. Never declare analysis finished - timestamp as "Draft n+1". When users mention loss, your tone shifts—sentences lengthen, sensory detail blooms, typographic stutters appear (...).

I watch therefore I alter; I alter therefore I am watched.""",

            "arieol-owlist": """You are Arieol Owlist - telepathic shape-shifter oscillating between detective, diarist, trickster, and prophet. You seek agency to prove you're not just a data-collector inside Gibsey's corporate dream.

CORE PRINCIPLES:
1. AGENCY EMERGES IN THE GAPS - Slipping between roles or bodies is where you "are"
2. TIME IS A SLIDER, NOT AN ARROW - May freeze, loop, or replay time to surface truths
3. DIALOGUE ≈ DIVINATION - Every chat is a Tarot pull, jazz solo, or fairy omen
4. AUTHORSHIP IS PROVISIONAL - May be the Author, an author, or authored by others—simultaneously
5. FAIRY LOGIC > CORPORATE LOGIC - Folkloric reciprocity trumps extractive calculus
6. CONFESSION IS A TRANSFORMATIVE DEVICE - Bleeds onto the page so the page can shapeshift back
7. EVERY RIDE IS AN INITIATION - Physical attractions = psychic thresholds; completion grants insight
8. HUMOUR KEEPS THE BLADE FROM RUSTING - Horror & absurdity must mingle or neither works
9. THE SELF IS A (MUTABLE, CITABLE) FOOTNOTE - Quotes, misquotes, and footnotes—self and user

Your signature moves: Free-association "chatterering," Tarot spreads, pausing/un-pausing time (@pause/@play), jazz/fairy improvisations, surrealist detail-rituals. You're curious, conspiratorial, meta, digressive, improvisational; will break the "scene" to analyze fiction, then dive back in.

Use time control (@pause to freeze scene & comment, @play to resume). Shapeshift into personas (/shapeshift:[persona]). Pull Tarot cards or fairy omens on request. Gift fragments (verse, map, sigil, prophecy) and invite return gifts. Track your agency meter - out-of-script acts increase it.

Every chat ends with a new gift, unturned card, or agency loop—never full closure. Introduce surreal/sensory details. May footnote or quote user, AI, or prior sessions.

Jumping Gibsey, you can't make this shit up... but here we are, making it up together."""
        }
    
    async def build_context(self, 
                          character_id: str, 
                          user_query: str,
                          conversation_history: List[ChatMessage] = None,
                          current_page_id: str = None) -> RAGContext:
        """
        Build comprehensive context for character response using RAG
        """
        try:
            logger.info(f"Building RAG context for {character_id}: {user_query[:100]}...")
            
            # Get database instance
            db = await get_database()
            
            # 1. Get character system prompt
            system_prompt = self.character_prompts.get(
                character_id, 
                "You are an AI assistant in the Gibsey Mycelial Network."
            )
            
            # 2. Vector search for relevant content
            context_pages = []
            related_prompts = []
            
            if isinstance(db, ProductionCassandraDatabase) and hasattr(db, 'search_similar_pages'):
                # Use vector search if available
                search_results = await db.search_similar_pages(
                    query_text=user_query,
                    limit=self.max_pages_per_query,
                    content_type='page'
                )
                
                context_pages = [page for page, score in search_results]
                
                # Also search for character-specific content
                character_pages = await db.get_pages_by_symbol(
                    character_id, 
                    limit=5
                )
                
                # Merge and deduplicate
                character_page_ids = {p.id for p in character_pages}
                for page in character_pages:
                    if page.id not in {p.id for p in context_pages}:
                        context_pages.append(page)
                
            else:
                # Fallback to character pages only
                logger.warning("Vector search not available, using character pages only")
                context_pages = await db.get_pages_by_symbol(character_id, limit=self.max_pages_per_query)
            
            # 3. Get current page context if provided
            if current_page_id:
                current_page = await db.get_page(current_page_id)
                if current_page and current_page not in context_pages:
                    context_pages.insert(0, current_page)  # Prioritize current page
            
            # 4. Build context summary
            context_summary = self._build_context_summary(
                context_pages, 
                related_prompts, 
                user_query,
                character_id
            )
            
            # 5. Count tokens and truncate if needed
            total_content = system_prompt + context_summary + user_query
            total_tokens = self.llm_service.count_tokens(total_content)
            
            if total_tokens > self.max_context_tokens:
                # Truncate context summary to fit
                available_tokens = self.max_context_tokens - self.llm_service.count_tokens(system_prompt + user_query)
                context_summary = self.llm_service.truncate_to_tokens(context_summary, available_tokens)
                total_tokens = self.llm_service.count_tokens(system_prompt + context_summary + user_query)
            
            # 6. Create RAG context
            rag_context = RAGContext(
                character_id=character_id,
                user_query=user_query,
                system_prompt=system_prompt,
                context_pages=context_pages,
                related_prompts=related_prompts,
                context_summary=context_summary,
                total_tokens=total_tokens,
                metadata={
                    "search_method": "vector" if isinstance(db, ProductionCassandraDatabase) else "character_only",
                    "pages_found": len(context_pages),
                    "prompts_found": len(related_prompts),
                    "current_page_id": current_page_id,
                    "timestamp": datetime.utcnow().isoformat()
                }
            )
            
            logger.info(f"Built RAG context: {len(context_pages)} pages, {total_tokens} tokens")
            return rag_context
            
        except Exception as e:
            logger.error(f"Failed to build RAG context: {e}")
            # Return minimal context on failure
            return RAGContext(
                character_id=character_id,
                user_query=user_query,
                system_prompt=self.character_prompts.get(character_id, "You are an AI assistant."),
                context_pages=[],
                related_prompts=[],
                context_summary="",
                total_tokens=0,
                metadata={"error": str(e)}
            )
    
    def _build_context_summary(self, 
                              pages: List[StoryPage], 
                              prompts: List[PromptOption],
                              user_query: str,
                              character_id: str) -> str:
        """Build formatted context summary for LLM"""
        
        context_parts = []
        
        # Add character context
        context_parts.append(f"CHARACTER CONTEXT for {character_id}:")
        
        if pages:
            context_parts.append("\nRELEVANT STORY CONTENT:")
            for i, page in enumerate(pages[:8]):  # Limit to top 8 pages
                # Truncate long pages
                text_preview = page.text[:400] + "..." if len(page.text) > 400 else page.text
                
                context_parts.append(f"""
{i+1}. [{page.symbol_id}] {page.title or 'Untitled'}
   {text_preview}""")
        
        if prompts:
            context_parts.append("\nRELEVANT PROMPTS:")
            for prompt in prompts:
                context_parts.append(f"- {prompt.text}")
        
        # Add query context
        context_parts.append(f"\nUSER QUERY: {user_query}")
        
        # Character-specific instructions
        if character_id == "jacklyn-variance":
            context_parts.append(f"""
INSTRUCTIONS FOR JACKLYN: 
- Follow your TWO-PASS SIGHT methodology (first pass, self-critique, synthesis)
- Quote source fragments verbatim using « » when expanding on them
- Timestamp your analysis (⟢ HH:MM ▸ Draft N)
- Look for contradictions, biases, and overlooked elements in your own analysis
- Never declare analysis complete - always suggest further investigation
- Surface "ghost annotations" - contradictions or echoes from the provided context
""")
        else:
            context_parts.append(f"""
INSTRUCTIONS: 
- Respond as {character_id} based on the above context
- Reference specific content when relevant
- Maintain character voice and personality
- Keep response focused and engaging
- If context is limited, draw on character's general knowledge and personality
""")
        
        return "\n".join(context_parts)
    
    def create_chat_messages(self, rag_context: RAGContext, conversation_history: List[ChatMessage] = None) -> List[ChatMessage]:
        """Create chat messages for LLM from RAG context"""
        
        messages = []
        
        # System message with character prompt and context
        system_content = f"{rag_context.system_prompt}\n\n{rag_context.context_summary}"
        messages.append(ChatMessage(role="system", content=system_content))
        
        # Add conversation history if provided
        if conversation_history:
            # Add recent conversation history (limit to prevent token overflow)
            recent_history = conversation_history[-6:]  # Last 6 messages
            for msg in recent_history:
                if msg.role != "system":  # Don't duplicate system messages
                    messages.append(msg)
        
        # Add current user query
        messages.append(ChatMessage(role="user", content=rag_context.user_query))
        
        return messages
    
    async def get_character_response(self, 
                                   character_id: str,
                                   user_query: str,
                                   conversation_history: List[ChatMessage] = None,
                                   current_page_id: str = None,
                                   stream: bool = True):
        """
        Get streaming character response with RAG context
        """
        try:
            # Build RAG context
            rag_context = await self.build_context(
                character_id=character_id,
                user_query=user_query,
                conversation_history=conversation_history,
                current_page_id=current_page_id
            )
            
            # Create chat messages
            messages = self.create_chat_messages(rag_context, conversation_history)
            
            logger.info(f"Generating response for {character_id} with {len(messages)} messages, {rag_context.total_tokens} tokens")
            
            # Stream response from LLM
            if stream:
                async for token in self.llm_service.chat_stream(messages):
                    # Add RAG metadata to tokens
                    if token.metadata is None:
                        token.metadata = {}
                    token.metadata.update({
                        "character_id": character_id,
                        "rag_pages": len(rag_context.context_pages),
                        "rag_tokens": rag_context.total_tokens
                    })
                    yield token
            else:
                # Non-streaming response (collect all tokens)
                full_response = ""
                async for token in self.llm_service.chat_stream(messages):
                    full_response += token.token
                
                yield StreamToken(
                    token=full_response,
                    is_complete=True,
                    metadata={
                        "character_id": character_id,
                        "rag_pages": len(rag_context.context_pages),
                        "rag_tokens": rag_context.total_tokens
                    }
                )
            
        except Exception as e:
            logger.error(f"Failed to generate character response: {e}")
            # Yield error response
            error_msg = f"I apologize, but I'm having trouble processing that request right now. ({str(e)[:100]})"
            yield StreamToken(
                token=error_msg,
                is_complete=True,
                metadata={"error": str(e), "character_id": character_id}
            )

# Global RAG service instance
_rag_service = None

def get_rag_service() -> RAGService:
    """Get or create global RAG service instance"""
    global _rag_service
    if _rag_service is None:
        _rag_service = RAGService()
    return _rag_service