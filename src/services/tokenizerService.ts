/**
 * Gibsey Custom Tokenizer Service for Frontend
 * 
 * This service provides tokenization using the custom Gibsey BPE vocabulary
 * exported from the Python tokenizer. Since full BPE tokenization requires
 * complex algorithms, this implementation focuses on:
 * 
 * 1. Token counting estimation
 * 2. Special token detection
 * 3. TNA cost calculation
 * 4. Basic vocabulary lookup
 */

// Types for tokenizer data
interface TokenizerPiece {
  id: number;
  piece: string;
  score: number;
  type: 'normal' | 'control' | 'qdpi' | 'character' | 'byte';
}

interface TokenizerData {
  version: string;
  type: string;
  model_info: {
    vocab_size: number;
    model_type: string;
    unk_id: number;
    bos_id: number;
    eos_id: number;
    pad_id: number;
  };
  special_tokens: {
    unk_token: string;
    bos_token: string;
    eos_token: string;
    pad_token: string;
    qdpi_tokens: string[];
    character_tokens: string[];
  };
  vocab: Record<string, number>;
  pieces: TokenizerPiece[];
}

export class GibseyTokenizerService {
  private data: TokenizerData | null = null;
  private loaded = false;
  private loading = false;
  
  // Configuration
  private readonly tokensPerTNA = 100;
  private readonly estimatedCharsPerToken = 3.5; // Conservative estimate
  
  constructor() {
    this.loadTokenizer();
  }
  
  /**
   * Load the tokenizer data from the JSON export
   */
  private async loadTokenizer(): Promise<void> {
    if (this.loading || this.loaded) return;
    
    this.loading = true;
    
    try {
      // Load the tokenizer JSON from the backend/tokenizer directory
      const response = await fetch('/tokenizer/gibsey_bpe.json');
      if (!response.ok) {
        throw new Error(`Failed to load tokenizer: ${response.status}`);
      }
      
      this.data = await response.json();
      this.loaded = true;
      
      console.log('✓ Loaded Gibsey BPE tokenizer');
      console.log(`  Vocab size: ${this.data.model_info.vocab_size}`);
      console.log(`  Special tokens: ${this.data.special_tokens.qdpi_tokens.length} QDPI + ${this.data.special_tokens.character_tokens.length} characters`);
      
    } catch (error) {
      console.warn('⚠️ Failed to load Gibsey tokenizer:', error);
      console.warn('   Falling back to character estimation');
      this.loaded = false;
    } finally {
      this.loading = false;
    }
  }
  
  /**
   * Ensure tokenizer is loaded before operations
   */
  private async ensureLoaded(): Promise<void> {
    if (!this.loaded && !this.loading) {
      await this.loadTokenizer();
    }
    
    // Wait for loading to complete
    while (this.loading) {
      await new Promise(resolve => setTimeout(resolve, 50));
    }
  }
  
  /**
   * Count tokens in text
   * 
   * Note: This is an approximation since full BPE tokenization requires
   * the original merge rules. For exact counts, use the Python backend.
   */
  async countTokens(text: string): Promise<number> {
    await this.ensureLoaded();
    
    if (!this.data) {
      // Fallback: character-based estimation
      return Math.ceil(text.length / this.estimatedCharsPerToken);
    }
    
    // Simple approximation: split on whitespace and punctuation,
    // then estimate tokens per piece based on length
    const pieces = this.preprocessText(text);
    let totalTokens = 0;
    
    for (const piece of pieces) {
      if (this.data.vocab[piece] !== undefined) {
        // Exact match in vocabulary
        totalTokens += 1;
      } else if (this.isSpecialToken(piece)) {
        // Special token
        totalTokens += 1;
      } else {
        // Estimate based on piece length
        // Shorter pieces are more likely to be single tokens
        const estimatedTokens = Math.max(1, Math.ceil(piece.length / 4));
        totalTokens += estimatedTokens;
      }
    }
    
    return totalTokens;
  }
  
  /**
   * Basic text preprocessing similar to BPE tokenization
   */
  private preprocessText(text: string): string[] {
    // Add space prefix (SentencePiece convention)
    const prefixed = ' ' + text;
    
    // Split on whitespace and punctuation, keeping them
    const tokens = prefixed.split(/(\s+|[^\w\s])/g).filter(token => token.length > 0);
    
    return tokens;
  }
  
  /**
   * Check if a token is a special token (QDPI or character)
   */
  private isSpecialToken(token: string): boolean {
    if (!this.data) return false;
    
    return this.data.special_tokens.qdpi_tokens.includes(token) ||
           this.data.special_tokens.character_tokens.includes(token);
  }
  
  /**
   * Detect special tokens in text
   */
  async detectSpecialTokens(text: string): Promise<{
    qdpi: string[];
    character: string[];
  }> {
    await this.ensureLoaded();
    
    const result = { qdpi: [] as string[], character: [] as string[] };
    
    if (!this.data) return result;
    
    // Check for QDPI tokens
    for (const token of this.data.special_tokens.qdpi_tokens) {
      if (text.includes(token)) {
        result.qdpi.push(token);
      }
    }
    
    // Check for character tokens
    for (const token of this.data.special_tokens.character_tokens) {
      if (text.includes(token)) {
        result.character.push(token);
      }
    }
    
    return result;
  }
  
  /**
   * Calculate TNA (Token Network Abstraction) cost
   */
  async calculateTNACost(text: string): Promise<number> {
    const tokenCount = await this.countTokens(text);
    return tokenCount / this.tokensPerTNA;
  }
  
  /**
   * Get tokenizer information
   */
  async getInfo(): Promise<{
    loaded: boolean;
    vocabSize?: number;
    specialTokens?: {
      qdpi: string[];
      characters: string[];
    };
    tokensPerTNA: number;
  }> {
    await this.ensureLoaded();
    
    if (!this.data) {
      return {
        loaded: false,
        tokensPerTNA: this.tokensPerTNA
      };
    }
    
    return {
      loaded: true,
      vocabSize: this.data.model_info.vocab_size,
      specialTokens: {
        qdpi: this.data.special_tokens.qdpi_tokens,
        characters: this.data.special_tokens.character_tokens
      },
      tokensPerTNA: this.tokensPerTNA
    };
  }
  
  /**
   * Estimate if text would exceed a token limit
   */
  async wouldExceedLimit(text: string, maxTokens: number): Promise<boolean> {
    const count = await this.countTokens(text);
    return count > maxTokens;
  }
  
  /**
   * Get a rough truncation of text to stay under token limit
   * Note: This is an approximation - for exact truncation, use the Python backend
   */
  async truncateToApproxTokens(text: string, maxTokens: number): Promise<string> {
    const currentCount = await this.countTokens(text);
    
    if (currentCount <= maxTokens) {
      return text;
    }
    
    // Rough character-based truncation
    const ratio = maxTokens / currentCount;
    const targetLength = Math.floor(text.length * ratio * 0.9); // 10% buffer
    
    return text.substring(0, targetLength).trim();
  }
}

// Global tokenizer instance
let tokenizerInstance: GibseyTokenizerService | null = null;

/**
 * Get the global tokenizer service instance
 */
export function getTokenizerService(): GibseyTokenizerService {
  if (!tokenizerInstance) {
    tokenizerInstance = new GibseyTokenizerService();
  }
  return tokenizerInstance;
}

// Convenience functions for direct use
export async function countTokens(text: string): Promise<number> {
  return getTokenizerService().countTokens(text);
}

export async function calculateTNACost(text: string): Promise<number> {
  return getTokenizerService().calculateTNACost(text);
}

export async function detectSpecialTokens(text: string) {
  return getTokenizerService().detectSpecialTokens(text);
}

export async function wouldExceedLimit(text: string, maxTokens: number): Promise<boolean> {
  return getTokenizerService().wouldExceedLimit(text, maxTokens);
}