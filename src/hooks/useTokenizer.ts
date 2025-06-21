/**
 * React hook for using the Gibsey tokenizer in components
 */

import { useState, useEffect, useCallback } from 'react';
import { getTokenizerService } from '../services/tokenizerService';

interface TokenizerInfo {
  loaded: boolean;
  vocabSize?: number;
  specialTokens?: {
    qdpi: string[];
    characters: string[];
  };
  tokensPerTNA: number;
}

interface SpecialTokens {
  qdpi: string[];
  character: string[];
}

/**
 * Hook for tokenizer functionality
 */
export function useTokenizer() {
  const [info, setInfo] = useState<TokenizerInfo>({ loaded: false, tokensPerTNA: 100 });
  const [loading, setLoading] = useState(true);
  
  // Load tokenizer info on mount
  useEffect(() => {
    const loadInfo = async () => {
      try {
        const tokenizerInfo = await getTokenizerService().getInfo();
        setInfo(tokenizerInfo);
      } catch (error) {
        console.error('Failed to load tokenizer info:', error);
      } finally {
        setLoading(false);
      }
    };
    
    loadInfo();
  }, []);
  
  // Token counting function
  const countTokens = useCallback(async (text: string): Promise<number> => {
    if (!text) return 0;
    return getTokenizerService().countTokens(text);
  }, []);
  
  // TNA cost calculation
  const calculateTNACost = useCallback(async (text: string): Promise<number> => {
    if (!text) return 0;
    return getTokenizerService().calculateTNACost(text);
  }, []);
  
  // Special token detection
  const detectSpecialTokens = useCallback(async (text: string): Promise<SpecialTokens> => {
    if (!text) return { qdpi: [], character: [] };
    return getTokenizerService().detectSpecialTokens(text);
  }, []);
  
  // Check if text exceeds token limit
  const wouldExceedLimit = useCallback(async (text: string, maxTokens: number): Promise<boolean> => {
    if (!text) return false;
    return getTokenizerService().wouldExceedLimit(text, maxTokens);
  }, []);
  
  // Truncate text to approximate token limit
  const truncateToTokens = useCallback(async (text: string, maxTokens: number): Promise<string> => {
    if (!text) return '';
    return getTokenizerService().truncateToApproxTokens(text, maxTokens);
  }, []);
  
  return {
    // Status
    loading,
    loaded: info.loaded,
    info,
    
    // Functions
    countTokens,
    calculateTNACost,
    detectSpecialTokens,
    wouldExceedLimit,
    truncateToTokens
  };
}

/**
 * Hook for real-time token counting of text input
 */
export function useTokenCount(text: string) {
  const [tokenCount, setTokenCount] = useState(0);
  const [tnaCost, setTnaCost] = useState(0);
  const [specialTokens, setSpecialTokens] = useState<SpecialTokens>({ qdpi: [], character: [] });
  const [calculating, setCalculating] = useState(false);
  
  const { countTokens, calculateTNACost, detectSpecialTokens } = useTokenizer();
  
  useEffect(() => {
    if (!text) {
      setTokenCount(0);
      setTnaCost(0);
      setSpecialTokens({ qdpi: [], character: [] });
      return;
    }
    
    const calculateMetrics = async () => {
      setCalculating(true);
      
      try {
        const [tokens, cost, special] = await Promise.all([
          countTokens(text),
          calculateTNACost(text),
          detectSpecialTokens(text)
        ]);
        
        setTokenCount(tokens);
        setTnaCost(cost);
        setSpecialTokens(special);
      } catch (error) {
        console.error('Failed to calculate token metrics:', error);
      } finally {
        setCalculating(false);
      }
    };
    
    // Debounce the calculation
    const timeoutId = setTimeout(calculateMetrics, 300);
    return () => clearTimeout(timeoutId);
  }, [text, countTokens, calculateTNACost, detectSpecialTokens]);
  
  return {
    tokenCount,
    tnaCost,
    specialTokens,
    calculating
  };
}