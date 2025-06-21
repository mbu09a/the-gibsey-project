/**
 * TokenCounter Component
 * 
 * Displays token count, TNA cost, and special token information for text input
 */

import React from 'react';
import { useTokenCount } from '../hooks/useTokenizer';

interface TokenCounterProps {
  text: string;
  maxTokens?: number;
  showDetails?: boolean;
  className?: string;
}

export function TokenCounter({ 
  text, 
  maxTokens, 
  showDetails = false, 
  className = '' 
}: TokenCounterProps) {
  const { tokenCount, tnaCost, specialTokens, calculating } = useTokenCount(text);
  
  // Calculate usage percentage if max tokens provided
  const usagePercentage = maxTokens ? (tokenCount / maxTokens) * 100 : 0;
  const isNearLimit = usagePercentage > 80;
  const isOverLimit = usagePercentage > 100;
  
  // Status colors
  const getStatusColor = () => {
    if (isOverLimit) return 'text-red-400';
    if (isNearLimit) return 'text-yellow-400';
    return 'text-green-400';
  };
  
  const getBarColor = () => {
    if (isOverLimit) return 'bg-red-500';
    if (isNearLimit) return 'bg-yellow-500';
    return 'bg-green-500';
  };
  
  return (
    <div className={`text-sm font-mono ${className}`}>
      {/* Main token count display */}
      <div className={`flex items-center gap-2 ${getStatusColor()}`}>
        <span className="opacity-60">TOKENS:</span>
        <span className="font-bold">
          {calculating ? '...' : tokenCount.toLocaleString()}
        </span>
        
        {maxTokens && (
          <>
            <span className="opacity-40">/</span>
            <span className="opacity-60">{maxTokens.toLocaleString()}</span>
          </>
        )}
        
        {/* Usage bar */}
        {maxTokens && (
          <div className="flex-1 max-w-24 bg-gray-700 rounded-full h-1.5">
            <div 
              className={`h-full rounded-full transition-all ${getBarColor()}`}
              style={{ width: `${Math.min(100, usagePercentage)}%` }}
            />
          </div>
        )}
      </div>
      
      {/* TNA cost */}
      <div className="text-blue-400 opacity-80">
        <span className="opacity-60">TNA COST:</span>
        <span className="ml-2 font-bold">
          {calculating ? '...' : tnaCost.toFixed(3)}
        </span>
      </div>
      
      {/* Special tokens detected */}
      {showDetails && (specialTokens.qdpi.length > 0 || specialTokens.character.length > 0) && (
        <div className="mt-2 space-y-1">
          {specialTokens.qdpi.length > 0 && (
            <div className="text-purple-400">
              <span className="opacity-60">QDPI:</span>
              <span className="ml-2">{specialTokens.qdpi.join(', ')}</span>
            </div>
          )}
          
          {specialTokens.character.length > 0 && (
            <div className="text-cyan-400">
              <span className="opacity-60">CHARS:</span>
              <span className="ml-2">{specialTokens.character.join(', ')}</span>
            </div>
          )}
        </div>
      )}
      
      {/* Warning messages */}
      {isOverLimit && (
        <div className="text-red-400 text-xs mt-1 opacity-80">
          ⚠️ Exceeds token limit
        </div>
      )}
      
      {isNearLimit && !isOverLimit && (
        <div className="text-yellow-400 text-xs mt-1 opacity-80">
          ⚠️ Approaching token limit
        </div>
      )}
    </div>
  );
}

/**
 * Simple inline token count display
 */
interface InlineTokenCountProps {
  text: string;
  className?: string;
}

export function InlineTokenCount({ text, className = '' }: InlineTokenCountProps) {
  const { tokenCount, calculating } = useTokenCount(text);
  
  return (
    <span className={`text-xs font-mono text-gray-400 ${className}`}>
      {calculating ? '...' : `${tokenCount} tokens`}
    </span>
  );
}

/**
 * TNA cost badge
 */
interface TNACostBadgeProps {
  text: string;
  className?: string;
}

export function TNACostBadge({ text, className = '' }: TNACostBadgeProps) {
  const { tnaCost, calculating } = useTokenCount(text);
  
  return (
    <span className={`inline-block px-2 py-1 bg-blue-900/30 text-blue-300 text-xs font-mono rounded ${className}`}>
      {calculating ? '...' : `${tnaCost.toFixed(3)} TNA`}
    </span>
  );
}