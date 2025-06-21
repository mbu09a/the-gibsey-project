/**
 * Debug component for testing tokenizer functionality
 */

import React, { useState } from 'react';
import { useTokenizer } from '../hooks/useTokenizer';
import { TokenCounter, InlineTokenCount, TNACostBadge } from './TokenCounter';

export function TokenizerDebug() {
  const [testText, setTestText] = useState('<X_READ>Hello jacklyn-variance, can you analyze this text?<Y_INDEX>');
  const { loading, loaded, info } = useTokenizer();
  
  return (
    <div className="p-6 bg-gray-900 text-white font-mono max-w-4xl mx-auto">
      <h2 className="text-xl font-bold mb-4 text-green-400">🔧 Gibsey Tokenizer Debug</h2>
      
      {/* Tokenizer Status */}
      <div className="mb-6 p-4 bg-gray-800 rounded-lg">
        <h3 className="font-bold mb-2 text-blue-400">Tokenizer Status</h3>
        
        {loading && (
          <div className="text-yellow-400">Loading tokenizer...</div>
        )}
        
        {!loading && (
          <div className="space-y-2">
            <div className={loaded ? 'text-green-400' : 'text-red-400'}>
              Status: {loaded ? '✓ Loaded' : '✗ Failed to load'}
            </div>
            
            {loaded && info.vocabSize && (
              <>
                <div className="text-gray-300">
                  Vocab Size: {info.vocabSize.toLocaleString()}
                </div>
                
                <div className="text-purple-400">
                  QDPI Tokens: {info.specialTokens?.qdpi.join(', ')}
                </div>
                
                <div className="text-cyan-400">
                  Character Tokens: {info.specialTokens?.characters.slice(0, 5).join(', ')}
                  {info.specialTokens && info.specialTokens.characters.length > 5 && 
                    ` ... +${info.specialTokens.characters.length - 5} more`
                  }
                </div>
              </>
            )}
          </div>
        )}
      </div>
      
      {/* Test Input */}
      <div className="mb-6">
        <h3 className="font-bold mb-2 text-blue-400">Test Input</h3>
        <textarea
          value={testText}
          onChange={(e) => setTestText(e.target.value)}
          className="w-full p-3 bg-gray-800 border border-gray-600 rounded text-white"
          rows={4}
          placeholder="Enter text to analyze..."
        />
      </div>
      
      {/* Token Analysis */}
      {testText.trim() && (
        <div className="space-y-4">
          <h3 className="font-bold text-blue-400">Token Analysis</h3>
          
          {/* Full token counter */}
          <div className="p-4 bg-gray-800 rounded-lg">
            <h4 className="font-bold mb-2 text-gray-300">Full Analysis</h4>
            <TokenCounter 
              text={testText}
              maxTokens={100}
              showDetails={true}
            />
          </div>
          
          {/* Inline components */}
          <div className="p-4 bg-gray-800 rounded-lg space-y-2">
            <h4 className="font-bold mb-2 text-gray-300">Inline Components</h4>
            
            <div>
              Text length: {testText.length} characters{' '}
              <InlineTokenCount text={testText} />
            </div>
            
            <div>
              Cost estimate: <TNACostBadge text={testText} />
            </div>
          </div>
        </div>
      )}
      
      {/* Test Cases */}
      <div className="mt-8">
        <h3 className="font-bold mb-2 text-blue-400">Quick Test Cases</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {[
            "Hello, world!",
            "<X_READ>Simple QDPI test<Y_INDEX>",
            "The london-fox character meets jacklyn-variance",
            "<A_ASK>What happens when all special tokens appear: an-author, glyph-marrow, <Z_RECEIVE>",
            "This is a longer text that should test the tokenizer's ability to handle multiple sentences and various punctuation marks. How well does it estimate token counts?"
          ].map((testCase, index) => (
            <div 
              key={index}
              className="p-3 bg-gray-800 rounded cursor-pointer hover:bg-gray-700 transition-colors"
              onClick={() => setTestText(testCase)}
            >
              <div className="text-sm text-gray-400 mb-1">Test {index + 1}:</div>
              <div className="text-sm mb-2">{testCase.slice(0, 60)}...</div>
              <InlineTokenCount text={testCase} />
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}