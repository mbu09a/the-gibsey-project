import React from 'react';
import { useQDPI } from '../hooks/useQDPI';

interface CorpusSymbolProps {
  symbolId: string;
  color?: string;
  size?: string;
  className?: string;
  onClick?: () => void;
  enableQDPI?: boolean;
}

const CorpusSymbol: React.FC<CorpusSymbolProps> = ({ 
  symbolId, 
  color = '#34FF78', 
  size = '24px',
  className = '',
  onClick,
  enableQDPI = false
}) => {
  const { executeSymbolFlow, encodeToQDPI, isLoading } = useQDPI();

  const handleSymbolClick = async () => {
    // Call original onClick if provided
    if (onClick) {
      onClick();
    }

    // QDPI integration
    if (enableQDPI) {
      try {
        // Execute symbol flow
        const flowResult = await executeSymbolFlow(symbolId.replace('-', '_'));
        console.log('QDPI Flow Result:', flowResult);

        // Encode symbol name to QDPI
        const encodeResult = await encodeToQDPI(`Symbol: ${symbolId}`);
        console.log('QDPI Encode Result:', encodeResult);

        // Broadcast to WebSocket if available
        if (window.qdpiWebSocket && window.qdpiWebSocket.readyState === WebSocket.OPEN) {
          window.qdpiWebSocket.send(JSON.stringify({
            type: 'qdpi_symbol_clicked',
            data: {
              symbol_id: symbolId,
              symbol_name: symbolId.replace('-', '_'),
              flow_result: flowResult,
              encode_result: encodeResult,
              timestamp: Date.now()
            }
          }));
        }
      } catch (error) {
        console.error('QDPI Symbol Click Error:', error);
      }
    }
  };
  const symbolMap: Record<string, JSX.Element> = {
    'an-author': (
      <svg viewBox="0 0 1000 1000" xmlns="http://www.w3.org/2000/svg" className={className} style={{ width: size, height: size }}>
        <line x1="200" y1="200" x2="800" y2="200" stroke={color} strokeWidth="60" strokeLinecap="square"/>
        <line x1="200" y1="200" x2="200" y2="800" stroke={color} strokeWidth="60" strokeLinecap="square"/>
        <line x1="800" y1="200" x2="800" y2="800" stroke={color} strokeWidth="60" strokeLinecap="square"/>
        <line x1="200" y1="800" x2="400" y2="800" stroke={color} strokeWidth="60" strokeLinecap="square"/>
        <line x1="800" y1="800" x2="600" y2="800" stroke={color} strokeWidth="60" strokeLinecap="square"/>
      </svg>
    ),
    'london-fox': (
      <svg viewBox="0 0 1000 1000" xmlns="http://www.w3.org/2000/svg" className={className} style={{ width: size, height: size }}>
        <line x1="200" y1="200" x2="800" y2="200" stroke={color} strokeWidth="60" strokeLinecap="square"/>
        <line x1="200" y1="200" x2="200" y2="800" stroke={color} strokeWidth="60" strokeLinecap="square"/>
        <line x1="800" y1="200" x2="800" y2="800" stroke={color} strokeWidth="60" strokeLinecap="square"/>
        <line x1="200" y1="800" x2="400" y2="800" stroke={color} strokeWidth="60" strokeLinecap="square"/>
        <line x1="200" y1="700" x2="400" y2="700" stroke={color} strokeWidth="60" strokeLinecap="square"/>
        <line x1="800" y1="800" x2="600" y2="800" stroke={color} strokeWidth="60" strokeLinecap="square"/>
        <line x1="800" y1="700" x2="600" y2="700" stroke={color} strokeWidth="60" strokeLinecap="square"/>
      </svg>
    ),
    'glyph-marrow': (
      <svg viewBox="0 0 1000 1000" xmlns="http://www.w3.org/2000/svg" className={className} style={{ width: size, height: size }}>
        <line x1="200" y1="200" x2="800" y2="200" stroke={color} strokeWidth="60" strokeLinecap="square"/>
        <line x1="200" y1="200" x2="200" y2="800" stroke={color} strokeWidth="60" strokeLinecap="square"/>
        <line x1="800" y1="200" x2="800" y2="800" stroke={color} strokeWidth="60" strokeLinecap="square"/>
        <line x1="200" y1="800" x2="400" y2="800" stroke={color} strokeWidth="60" strokeLinecap="square"/>
        <line x1="200" y1="600" x2="400" y2="600" stroke={color} strokeWidth="60" strokeLinecap="square"/>
        <line x1="800" y1="800" x2="600" y2="800" stroke={color} strokeWidth="60" strokeLinecap="square"/>
        <line x1="800" y1="600" x2="600" y2="600" stroke={color} strokeWidth="60" strokeLinecap="square"/>
      </svg>
    ),
    'phillip-bafflemint': (
      <svg viewBox="0 0 1000 1000" xmlns="http://www.w3.org/2000/svg" className={className} style={{ width: size, height: size }}>
        <line x1="200" y1="200" x2="800" y2="200" stroke={color} strokeWidth="60" strokeLinecap="square"/>
        <line x1="200" y1="200" x2="200" y2="800" stroke={color} strokeWidth="60" strokeLinecap="square"/>
        <line x1="800" y1="200" x2="800" y2="800" stroke={color} strokeWidth="60" strokeLinecap="square"/>
        <line x1="200" y1="800" x2="400" y2="800" stroke={color} strokeWidth="60" strokeLinecap="square"/>
        <line x1="200" y1="500" x2="400" y2="500" stroke={color} strokeWidth="60" strokeLinecap="square"/>
        <line x1="800" y1="800" x2="600" y2="800" stroke={color} strokeWidth="60" strokeLinecap="square"/>
        <line x1="800" y1="500" x2="600" y2="500" stroke={color} strokeWidth="60" strokeLinecap="square"/>
      </svg>
    ),
    'jacklyn-variance': (
      <svg viewBox="0 0 1000 1000" xmlns="http://www.w3.org/2000/svg" className={className} style={{ width: size, height: size }}>
        <line x1="200" y1="200" x2="800" y2="200" stroke={color} strokeWidth="60" strokeLinecap="square"/>
        <line x1="200" y1="200" x2="200" y2="800" stroke={color} strokeWidth="60" strokeLinecap="square"/>
        <line x1="800" y1="200" x2="800" y2="800" stroke={color} strokeWidth="60" strokeLinecap="square"/>
        <line x1="200" y1="800" x2="400" y2="800" stroke={color} strokeWidth="60" strokeLinecap="square"/>
        <line x1="200" y1="700" x2="400" y2="700" stroke={color} strokeWidth="60" strokeLinecap="square"/>
        <line x1="200" y1="600" x2="400" y2="600" stroke={color} strokeWidth="60" strokeLinecap="square"/>
        <line x1="800" y1="800" x2="600" y2="800" stroke={color} strokeWidth="60" strokeLinecap="square"/>
        <line x1="800" y1="700" x2="600" y2="700" stroke={color} strokeWidth="60" strokeLinecap="square"/>
        <line x1="800" y1="600" x2="600" y2="600" stroke={color} strokeWidth="60" strokeLinecap="square"/>
      </svg>
    ),
    'oren-progresso': (
      <svg viewBox="0 0 1000 1000" xmlns="http://www.w3.org/2000/svg" className={className} style={{ width: size, height: size }}>
        <line x1="200" y1="200" x2="800" y2="200" stroke={color} strokeWidth="60" strokeLinecap="square"/>
        <line x1="200" y1="200" x2="200" y2="800" stroke={color} strokeWidth="60" strokeLinecap="square"/>
        <line x1="800" y1="200" x2="800" y2="800" stroke={color} strokeWidth="60" strokeLinecap="square"/>
        <line x1="200" y1="800" x2="400" y2="800" stroke={color} strokeWidth="60" strokeLinecap="square"/>
        <line x1="200" y1="700" x2="400" y2="700" stroke={color} strokeWidth="60" strokeLinecap="square"/>
        <line x1="200" y1="500" x2="400" y2="500" stroke={color} strokeWidth="60" strokeLinecap="square"/>
        <line x1="800" y1="800" x2="600" y2="800" stroke={color} strokeWidth="60" strokeLinecap="square"/>
        <line x1="800" y1="700" x2="600" y2="700" stroke={color} strokeWidth="60" strokeLinecap="square"/>
        <line x1="800" y1="500" x2="600" y2="500" stroke={color} strokeWidth="60" strokeLinecap="square"/>
      </svg>
    ),
    'old-natalie': (
      <svg viewBox="0 0 1000 1000" xmlns="http://www.w3.org/2000/svg" className={className} style={{ width: size, height: size }}>
        <line x1="200" y1="200" x2="800" y2="200" stroke={color} strokeWidth="60" strokeLinecap="square"/>
        <line x1="200" y1="200" x2="200" y2="800" stroke={color} strokeWidth="60" strokeLinecap="square"/>
        <line x1="800" y1="200" x2="800" y2="800" stroke={color} strokeWidth="60" strokeLinecap="square"/>
        <line x1="200" y1="800" x2="400" y2="800" stroke={color} strokeWidth="60" strokeLinecap="square"/>
        <line x1="200" y1="600" x2="400" y2="600" stroke={color} strokeWidth="60" strokeLinecap="square"/>
        <line x1="200" y1="500" x2="400" y2="500" stroke={color} strokeWidth="60" strokeLinecap="square"/>
        <line x1="800" y1="800" x2="600" y2="800" stroke={color} strokeWidth="60" strokeLinecap="square"/>
        <line x1="800" y1="600" x2="600" y2="600" stroke={color} strokeWidth="60" strokeLinecap="square"/>
        <line x1="800" y1="500" x2="600" y2="500" stroke={color} strokeWidth="60" strokeLinecap="square"/>
      </svg>
    ),
    'princhetta': (
      <svg viewBox="0 0 1000 1000" xmlns="http://www.w3.org/2000/svg" className={className} style={{ width: size, height: size }}>
        <line x1="200" y1="200" x2="800" y2="200" stroke={color} strokeWidth="60" strokeLinecap="square"/>
        <line x1="200" y1="200" x2="200" y2="800" stroke={color} strokeWidth="60" strokeLinecap="square"/>
        <line x1="800" y1="200" x2="800" y2="800" stroke={color} strokeWidth="60" strokeLinecap="square"/>
        <line x1="200" y1="800" x2="400" y2="800" stroke={color} strokeWidth="60" strokeLinecap="square"/>
        <line x1="200" y1="700" x2="400" y2="700" stroke={color} strokeWidth="60" strokeLinecap="square"/>
        <line x1="200" y1="600" x2="400" y2="600" stroke={color} strokeWidth="60" strokeLinecap="square"/>
        <line x1="200" y1="500" x2="400" y2="500" stroke={color} strokeWidth="60" strokeLinecap="square"/>
        <line x1="800" y1="800" x2="600" y2="800" stroke={color} strokeWidth="60" strokeLinecap="square"/>
        <line x1="800" y1="700" x2="600" y2="700" stroke={color} strokeWidth="60" strokeLinecap="square"/>
        <line x1="800" y1="600" x2="600" y2="600" stroke={color} strokeWidth="60" strokeLinecap="square"/>
        <line x1="800" y1="500" x2="600" y2="500" stroke={color} strokeWidth="60" strokeLinecap="square"/>
      </svg>
    ),
    'cop-e-right': (
      <svg viewBox="0 0 1000 1000" xmlns="http://www.w3.org/2000/svg" className={className} style={{ width: size, height: size }}>
        <g transform="rotate(180 500 500)">
          <line x1="200" y1="200" x2="800" y2="200" stroke={color} strokeWidth="60" strokeLinecap="square"/>
          <line x1="200" y1="200" x2="200" y2="800" stroke={color} strokeWidth="60" strokeLinecap="square"/>
          <line x1="800" y1="200" x2="800" y2="800" stroke={color} strokeWidth="60" strokeLinecap="square"/>
          <line x1="200" y1="800" x2="0" y2="800" stroke={color} strokeWidth="60" strokeLinecap="square"/>
          <line x1="200" y1="700" x2="0" y2="700" stroke={color} strokeWidth="60" strokeLinecap="square"/>
          <line x1="200" y1="600" x2="0" y2="600" stroke={color} strokeWidth="60" strokeLinecap="square"/>
          <line x1="200" y1="500" x2="0" y2="500" stroke={color} strokeWidth="60" strokeLinecap="square"/>
          <line x1="800" y1="800" x2="1000" y2="800" stroke={color} strokeWidth="60" strokeLinecap="square"/>
          <line x1="800" y1="700" x2="1000" y2="700" stroke={color} strokeWidth="60" strokeLinecap="square"/>
          <line x1="800" y1="600" x2="1000" y2="600" stroke={color} strokeWidth="60" strokeLinecap="square"/>
          <line x1="800" y1="500" x2="1000" y2="500" stroke={color} strokeWidth="60" strokeLinecap="square"/>
        </g>
      </svg>
    ),
    'new-natalie': (
      <svg viewBox="0 0 1000 1000" xmlns="http://www.w3.org/2000/svg" className={className} style={{ width: size, height: size }}>
        <g transform="rotate(180 500 500)">
          <line x1="200" y1="200" x2="800" y2="200" stroke={color} strokeWidth="60" strokeLinecap="square"/>
          <line x1="200" y1="200" x2="200" y2="800" stroke={color} strokeWidth="60" strokeLinecap="square"/>
          <line x1="800" y1="200" x2="800" y2="800" stroke={color} strokeWidth="60" strokeLinecap="square"/>
          <line x1="200" y1="800" x2="0" y2="800" stroke={color} strokeWidth="60" strokeLinecap="square"/>
          <line x1="200" y1="600" x2="0" y2="600" stroke={color} strokeWidth="60" strokeLinecap="square"/>
          <line x1="200" y1="500" x2="0" y2="500" stroke={color} strokeWidth="60" strokeLinecap="square"/>
          <line x1="800" y1="800" x2="1000" y2="800" stroke={color} strokeWidth="60" strokeLinecap="square"/>
          <line x1="800" y1="600" x2="1000" y2="600" stroke={color} strokeWidth="60" strokeLinecap="square"/>
          <line x1="800" y1="500" x2="1000" y2="500" stroke={color} strokeWidth="60" strokeLinecap="square"/>
        </g>
      </svg>
    ),
    'arieol-owlist': (
      <svg viewBox="0 0 1000 1000" xmlns="http://www.w3.org/2000/svg" className={className} style={{ width: size, height: size }}>
        <g transform="rotate(180 500 500)">
          <line x1="200" y1="200" x2="800" y2="200" stroke={color} strokeWidth="60" strokeLinecap="square"/>
          <line x1="200" y1="200" x2="200" y2="800" stroke={color} strokeWidth="60" strokeLinecap="square"/>
          <line x1="800" y1="200" x2="800" y2="800" stroke={color} strokeWidth="60" strokeLinecap="square"/>
          <line x1="200" y1="800" x2="0" y2="800" stroke={color} strokeWidth="60" strokeLinecap="square"/>
          <line x1="200" y1="700" x2="0" y2="700" stroke={color} strokeWidth="60" strokeLinecap="square"/>
          <line x1="200" y1="500" x2="0" y2="500" stroke={color} strokeWidth="60" strokeLinecap="square"/>
          <line x1="800" y1="800" x2="1000" y2="800" stroke={color} strokeWidth="60" strokeLinecap="square"/>
          <line x1="800" y1="700" x2="1000" y2="700" stroke={color} strokeWidth="60" strokeLinecap="square"/>
          <line x1="800" y1="500" x2="1000" y2="500" stroke={color} strokeWidth="60" strokeLinecap="square"/>
        </g>
      </svg>
    ),
    'jack-parlance': (
      <svg viewBox="0 0 1000 1000" xmlns="http://www.w3.org/2000/svg" className={className} style={{ width: size, height: size }}>
        <g transform="rotate(180 500 500)">
          <line x1="200" y1="200" x2="800" y2="200" stroke={color} strokeWidth="60" strokeLinecap="square"/>
          <line x1="200" y1="200" x2="200" y2="800" stroke={color} strokeWidth="60" strokeLinecap="square"/>
          <line x1="800" y1="200" x2="800" y2="800" stroke={color} strokeWidth="60" strokeLinecap="square"/>
          <line x1="200" y1="800" x2="0" y2="800" stroke={color} strokeWidth="60" strokeLinecap="square"/>
          <line x1="200" y1="700" x2="0" y2="700" stroke={color} strokeWidth="60" strokeLinecap="square"/>
          <line x1="200" y1="600" x2="0" y2="600" stroke={color} strokeWidth="60" strokeLinecap="square"/>
          <line x1="800" y1="800" x2="1000" y2="800" stroke={color} strokeWidth="60" strokeLinecap="square"/>
          <line x1="800" y1="700" x2="1000" y2="700" stroke={color} strokeWidth="60" strokeLinecap="square"/>
          <line x1="800" y1="600" x2="1000" y2="600" stroke={color} strokeWidth="60" strokeLinecap="square"/>
        </g>
      </svg>
    ),
    'manny-valentinas': (
      <svg viewBox="0 0 1000 1000" xmlns="http://www.w3.org/2000/svg" className={className} style={{ width: size, height: size }}>
        <g transform="rotate(180 500 500)">
          <line x1="200" y1="200" x2="800" y2="200" stroke={color} strokeWidth="60" strokeLinecap="square"/>
          <line x1="200" y1="200" x2="200" y2="800" stroke={color} strokeWidth="60" strokeLinecap="square"/>
          <line x1="800" y1="200" x2="800" y2="800" stroke={color} strokeWidth="60" strokeLinecap="square"/>
          <line x1="200" y1="800" x2="0" y2="800" stroke={color} strokeWidth="60" strokeLinecap="square"/>
          <line x1="200" y1="500" x2="0" y2="500" stroke={color} strokeWidth="60" strokeLinecap="square"/>
          <line x1="800" y1="800" x2="1000" y2="800" stroke={color} strokeWidth="60" strokeLinecap="square"/>
          <line x1="800" y1="500" x2="1000" y2="500" stroke={color} strokeWidth="60" strokeLinecap="square"/>
        </g>
      </svg>
    ),
    'shamrock-stillman': (
      <svg viewBox="0 0 1000 1000" xmlns="http://www.w3.org/2000/svg" className={className} style={{ width: size, height: size }}>
        <g transform="rotate(180 500 500)">
          <line x1="200" y1="200" x2="800" y2="200" stroke={color} strokeWidth="60" strokeLinecap="square"/>
          <line x1="200" y1="200" x2="200" y2="800" stroke={color} strokeWidth="60" strokeLinecap="square"/>
          <line x1="800" y1="200" x2="800" y2="800" stroke={color} strokeWidth="60" strokeLinecap="square"/>
          <line x1="200" y1="800" x2="0" y2="800" stroke={color} strokeWidth="60" strokeLinecap="square"/>
          <line x1="200" y1="600" x2="0" y2="600" stroke={color} strokeWidth="60" strokeLinecap="square"/>
          <line x1="800" y1="800" x2="1000" y2="800" stroke={color} strokeWidth="60" strokeLinecap="square"/>
          <line x1="800" y1="600" x2="1000" y2="600" stroke={color} strokeWidth="60" strokeLinecap="square"/>
        </g>
      </svg>
    ),
    'todd-fishbone': (
      <svg viewBox="0 0 1000 1000" xmlns="http://www.w3.org/2000/svg" className={className} style={{ width: size, height: size }}>
        <g transform="rotate(180 500 500)">
          <line x1="200" y1="200" x2="800" y2="200" stroke={color} strokeWidth="60" strokeLinecap="square"/>
          <line x1="200" y1="200" x2="200" y2="800" stroke={color} strokeWidth="60" strokeLinecap="square"/>
          <line x1="800" y1="200" x2="800" y2="800" stroke={color} strokeWidth="60" strokeLinecap="square"/>
          <line x1="200" y1="800" x2="0" y2="800" stroke={color} strokeWidth="60" strokeLinecap="square"/>
          <line x1="200" y1="700" x2="0" y2="700" stroke={color} strokeWidth="60" strokeLinecap="square"/>
          <line x1="800" y1="800" x2="1000" y2="800" stroke={color} strokeWidth="60" strokeLinecap="square"/>
          <line x1="800" y1="700" x2="1000" y2="700" stroke={color} strokeWidth="60" strokeLinecap="square"/>
        </g>
      </svg>
    ),
    'the-author': (
      <svg viewBox="0 0 1000 1000" xmlns="http://www.w3.org/2000/svg" className={className} style={{ width: size, height: size }}>
        <g transform="rotate(180 500 500)">
          <line x1="200" y1="200" x2="800" y2="200" stroke={color} strokeWidth="60" strokeLinecap="square"/>
          <line x1="200" y1="200" x2="200" y2="800" stroke={color} strokeWidth="60" strokeLinecap="square"/>
          <line x1="800" y1="200" x2="800" y2="800" stroke={color} strokeWidth="60" strokeLinecap="square"/>
          <line x1="200" y1="800" x2="0" y2="800" stroke={color} strokeWidth="60" strokeLinecap="square"/>
          <line x1="800" y1="800" x2="1000" y2="800" stroke={color} strokeWidth="60" strokeLinecap="square"/>
        </g>
      </svg>
    )
    // We can add more symbols as needed
  };

  const symbolElement = symbolMap[symbolId] || (
    <div 
      className={`w-6 h-6 bg-current rounded ${className}`} 
      style={{ width: size, height: size, color }}
    />
  );

  return (
    <div 
      className={`inline-block cursor-pointer transition-all ${enableQDPI ? 'hover:scale-110' : ''} ${className}`}
      onClick={handleSymbolClick}
      style={{ 
        filter: isLoading ? 'brightness(0.7)' : undefined,
        opacity: isLoading ? 0.8 : 1
      }}
    >
      {symbolElement}
    </div>
  );
};

export default CorpusSymbol;