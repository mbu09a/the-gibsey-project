import React, { useState, useEffect, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

interface QDPISymbol {
  name: string;
  id: number;
  orientation: 'n' | 'u';
  rotation: number;
  parity: number;
  rows: [string, string, string, string];
  glyph_id: number;
  extended_glyph_id: number;
}

interface QDPIState {
  mode: 'read' | 'ask' | 'index' | 'receive';
  orientation: 'n' | 'u';
  active_symbols: QDPISymbol[];
  context: Record<string, any>;
  timestamp: string;
}

interface QDPIFlowResult {
  flow: string;
  flow_type: string;
  status: string;
  action?: string;
  [key: string]: any;
}

interface QDPISearchMatch {
  symbol: QDPISymbol;
  similarity: number;
  function?: string;
  description?: string;
  domain?: string;
}

interface QDPIInterfaceProps {
  sessionId: string;
  websocket?: WebSocket;
  onStateChange?: (state: QDPIState) => void;
  onSymbolActivated?: (symbol: QDPISymbol) => void;
  className?: string;
}

const QDPI_MODE_COLORS = {
  read: '#4ade80',    // green
  ask: '#3b82f6',     // blue  
  index: '#f59e0b',   // amber
  receive: '#ef4444'  // red
};

const QDPI_MODE_DESCRIPTIONS = {
  read: 'Consuming & analyzing existing content',
  ask: 'Querying & requesting information', 
  index: 'Creating & cataloging new content',
  receive: 'Accepting & processing incoming data'
};

export const QDPIInterface: React.FC<QDPIInterfaceProps> = ({
  sessionId,
  websocket,
  onStateChange,
  onSymbolActivated,
  className = ''
}) => {
  const [state, setState] = useState<QDPIState>({
    mode: 'read',
    orientation: 'n',
    active_symbols: [],
    context: {},
    timestamp: new Date().toISOString()
  });
  
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState<QDPISearchMatch[]>([]);
  const [encodeInputData, setEncodeInputData] = useState('');
  const [encodedSymbols, setEncodedSymbols] = useState<QDPISymbol[]>([]);
  const [flowHistory, setFlowHistory] = useState<QDPIFlowResult[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  
  // API base URL
  const API_BASE = '/api/v1/qdpi';
  
  // Fetch current QDPI state
  const fetchState = useCallback(async () => {
    try {
      const response = await fetch(`${API_BASE}/mode/${sessionId}`);
      if (response.ok) {
        const sessionState = await response.json();
        const newState: QDPIState = {
          mode: sessionState.mode,
          orientation: sessionState.orientation,
          active_symbols: sessionState.active_symbols || [],
          context: sessionState.context || {},
          timestamp: sessionState.updated_at
        };
        setState(newState);
        onStateChange?.(newState);
      }
    } catch (error) {
      console.error('Failed to fetch QDPI state:', error);
    }
  }, [sessionId, onStateChange]);
  
  // Set QDPI mode
  const setMode = useCallback(async (mode: QDPIState['mode'], flipOrientation: boolean = false) => {
    setIsLoading(true);
    try {
      const response = await fetch(`${API_BASE}/mode/${sessionId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          mode,
          orientation: flipOrientation ? (state.orientation === 'n' ? 'u' : 'n') : undefined
        })
      });
      
      if (response.ok) {
        const sessionState = await response.json();
        const newState: QDPIState = {
          mode: sessionState.mode,
          orientation: sessionState.orientation,
          active_symbols: sessionState.active_symbols || [],
          context: sessionState.context || {},
          timestamp: sessionState.updated_at
        };
        setState(newState);
        onStateChange?.(newState);
        
        // Send WebSocket notification for real-time updates
        if (websocket && websocket.readyState === WebSocket.OPEN) {
          websocket.send(JSON.stringify({
            type: 'qdpi_mode_change',
            data: { mode, orientation: newState.orientation }
          }));
        }
      }
    } catch (error) {
      console.error('Failed to set QDPI mode:', error);
    } finally {
      setIsLoading(false);
    }
  }, [sessionId, state.orientation, onStateChange, websocket]);
  
  // Flip orientation
  const flipOrientation = useCallback(async () => {
    await setMode(state.mode, true);
  }, [state.mode, setMode]);
  
  // Encode data into symbols
  const encodeData = useCallback(async (data: string, executeFlows: boolean = false) => {
    setIsLoading(true);
    try {
      const response = await fetch(`${API_BASE}/encode/${sessionId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          data,
          execute_flows: executeFlows
        })
      });
      
      if (response.ok) {
        const result = await response.json();
        setEncodedSymbols(result.encoded_symbols);
        
        if (result.flow_results && result.flow_results.length > 0) {
          setFlowHistory(prev => [...prev, ...result.flow_results.flatMap((r: any) => r.flows)]);
        }
        
        // Send WebSocket notification
        if (websocket && websocket.readyState === WebSocket.OPEN) {
          websocket.send(JSON.stringify({
            type: 'qdpi_symbol_sequence',
            data: { symbols: result.encoded_symbols, context: result.state }
          }));
        }
      }
    } catch (error) {
      console.error('Failed to encode data:', error);
    } finally {
      setIsLoading(false);
    }
  }, [sessionId, websocket]);
  
  // Search for symbols
  const searchSymbols = useCallback(async (query: string) => {
    if (!query.trim()) {
      setSearchResults([]);
      return;
    }
    
    setIsLoading(true);
    try {
      const response = await fetch(`${API_BASE}/search/${sessionId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query, limit: 10 })
      });
      
      if (response.ok) {
        const result = await response.json();
        setSearchResults(result.matches);
        
        // Send WebSocket notification
        if (websocket && websocket.readyState === WebSocket.OPEN) {
          websocket.send(JSON.stringify({
            type: 'qdpi_search',
            data: { query, results: result }
          }));
        }
      }
    } catch (error) {
      console.error('Failed to search symbols:', error);
    } finally {
      setIsLoading(false);
    }
  }, [sessionId, websocket]);
  
  // Execute symbol flows
  const executeSymbolFlows = useCallback(async (symbolName: string, context: Record<string, any> = {}) => {
    setIsLoading(true);
    try {
      const response = await fetch(`${API_BASE}/execute/${sessionId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          symbol_name: symbolName,
          context
        })
      });
      
      if (response.ok) {
        const result = await response.json();
        
        if (result.execution_result && result.execution_result.flows) {
          setFlowHistory(prev => [...prev, ...result.execution_result.flows]);
        }
        
        // Update active symbol
        if (result.state && result.state.active_symbol) {
          onSymbolActivated?.(result.state.active_symbol);
        }
        
        // Send WebSocket notification
        if (websocket && websocket.readyState === WebSocket.OPEN) {
          websocket.send(JSON.stringify({
            type: 'qdpi_symbol_execute',
            data: { symbol_name: symbolName, context }
          }));
        }
      }
    } catch (error) {
      console.error('Failed to execute symbol flows:', error);
    } finally {
      setIsLoading(false);
    }
  }, [sessionId, websocket, onSymbolActivated]);
  
  // Subscribe to WebSocket events on mount
  useEffect(() => {
    if (websocket && websocket.readyState === WebSocket.OPEN) {
      websocket.send(JSON.stringify({
        type: 'qdpi_subscribe',
        data: {
          events: {
            mode_changes: true,
            orientation_flips: true,
            symbol_activations: true,
            flow_executions: true,
            search_results: true
          }
        }
      }));
    }
    
    fetchState();
  }, [websocket, fetchState]);
  
  // WebSocket event handlers
  useEffect(() => {
    if (!websocket) return;
    
    const handleMessage = (event: MessageEvent) => {
      try {
        const message = JSON.parse(event.data);
        
        switch (message.type) {
          case 'qdpi_mode_changed':
            setState(prev => ({
              ...prev,
              mode: message.data.new_mode,
              timestamp: message.data.timestamp
            }));
            break;
            
          case 'qdpi_orientation_flipped':
            setState(prev => ({
              ...prev,
              orientation: message.data.new_orientation,
              timestamp: message.data.timestamp
            }));
            break;
            
          case 'qdpi_symbol_activated':
            onSymbolActivated?.(message.data.symbol);
            break;
            
          case 'qdpi_flow_executed':
            if (message.data.flow_results && message.data.flow_results.flows) {
              setFlowHistory(prev => [...prev, ...message.data.flow_results.flows]);
            }
            break;
            
          case 'qdpi_search_results':
            setSearchResults(message.data.results.matches || []);
            break;
        }
      } catch (error) {
        console.error('Error handling WebSocket message:', error);
      }
    };
    
    websocket.addEventListener('message', handleMessage);
    return () => websocket.removeEventListener('message', handleMessage);
  }, [websocket, onSymbolActivated]);
  
  return (
    <div className={`qdpi-interface ${className}`}>
      {/* QDPI State Display */}
      <div className="qdpi-state-panel mb-6 p-4 bg-gray-900 rounded-lg border">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-white">QDPI State</h3>
          <motion.div
            className="flex items-center gap-2"
            animate={{ rotate: state.orientation === 'u' ? 180 : 0 }}
            transition={{ duration: 0.6, ease: "cubicBezier(0.175, 0.885, 0.32, 1.275)" }}
          >
            <div 
              className="w-3 h-3 rounded-full"
              style={{ backgroundColor: QDPI_MODE_COLORS[state.mode] }}
            />
            <span className="text-white font-mono uppercase">{state.mode}</span>
            <button
              onClick={flipOrientation}
              className="ml-2 p-1 text-gray-400 hover:text-white transition-colors"
              title="Flip orientation"
            >
              🔄
            </button>
          </motion.div>
        </div>
        
        {/* Mode Selector */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-2 mb-4">
          {Object.entries(QDPI_MODE_COLORS).map(([mode, color]) => (
            <motion.button
              key={mode}
              onClick={() => setMode(mode as QDPIState['mode'])}
              className={`p-2 rounded text-sm font-medium transition-all ${
                state.mode === mode 
                  ? 'text-white shadow-lg' 
                  : 'text-gray-400 hover:text-white bg-gray-800 hover:bg-gray-700'
              }`}
              style={state.mode === mode ? { backgroundColor: color } : {}}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              disabled={isLoading}
            >
              <div className="uppercase font-mono text-xs">{mode}</div>
              <div className="text-xs opacity-80 mt-1">
                {QDPI_MODE_DESCRIPTIONS[mode as keyof typeof QDPI_MODE_DESCRIPTIONS]}
              </div>
            </motion.button>
          ))}
        </div>
        
        <div className="text-xs text-gray-400">
          Orientation: {state.orientation === 'n' ? 'Normal' : 'Upside'} | 
          Updated: {new Date(state.timestamp).toLocaleTimeString()}
        </div>
      </div>
      
      {/* Encode Data Panel */}
      <div className="qdpi-encode-panel mb-6 p-4 bg-gray-900 rounded-lg border">
        <h4 className="text-md font-semibold text-white mb-3">Encode Data</h4>
        <div className="flex gap-2 mb-3">
          <input
            type="text"
            value={encodeInputData}
            onChange={(e) => setEncodeInputData(e.target.value)}
            placeholder="Enter data to encode into QDPI symbols..."
            className="flex-1 px-3 py-2 bg-gray-800 text-white rounded border border-gray-700 focus:border-blue-500"
          />
          <button
            onClick={() => encodeData(encodeInputData, false)}
            disabled={!encodeInputData.trim() || isLoading}
            className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
          >
            Encode
          </button>
          <button
            onClick={() => encodeData(encodeInputData, true)}
            disabled={!encodeInputData.trim() || isLoading}
            className="px-4 py-2 bg-orange-600 text-white rounded hover:bg-orange-700 disabled:opacity-50"
          >
            Encode + Execute
          </button>
        </div>
        
        {/* Encoded Symbols Display */}
        {encodedSymbols.length > 0 && (
          <div className="mt-3">
            <div className="text-sm text-gray-400 mb-2">
              Encoded into {encodedSymbols.length} symbols:
            </div>
            <div className="flex flex-wrap gap-2">
              {encodedSymbols.map((symbol, index) => (
                <motion.div
                  key={index}
                  className="px-2 py-1 bg-gray-800 rounded text-xs text-white border border-gray-700"
                  initial={{ opacity: 0, scale: 0.8 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ delay: index * 0.1 }}
                  onClick={() => executeSymbolFlows(symbol.name)}
                  style={{ cursor: 'pointer' }}
                >
                  {symbol.name} ({symbol.glyph_id})
                </motion.div>
              ))}
            </div>
          </div>
        )}
      </div>
      
      {/* Symbol Search Panel */}
      <div className="qdpi-search-panel mb-6 p-4 bg-gray-900 rounded-lg border">
        <h4 className="text-md font-semibold text-white mb-3">Symbol Search</h4>
        <div className="flex gap-2 mb-3">
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && searchSymbols(searchQuery)}
            placeholder="Search for symbols by meaning..."
            className="flex-1 px-3 py-2 bg-gray-800 text-white rounded border border-gray-700 focus:border-green-500"
          />
          <button
            onClick={() => searchSymbols(searchQuery)}
            disabled={!searchQuery.trim() || isLoading}
            className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700 disabled:opacity-50"
          >
            Search
          </button>
        </div>
        
        {/* Search Results */}
        {searchResults.length > 0 && (
          <div className="mt-3">
            <div className="text-sm text-gray-400 mb-2">
              Found {searchResults.length} matches:
            </div>
            <div className="space-y-2 max-h-40 overflow-y-auto">
              {searchResults.map((match, index) => (
                <motion.div
                  key={index}
                  className="p-2 bg-gray-800 rounded border border-gray-700 hover:border-green-500 cursor-pointer"
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.1 }}
                  onClick={() => executeSymbolFlows(match.symbol.name)}
                >
                  <div className="flex justify-between items-center">
                    <span className="text-white text-sm font-medium">
                      {match.symbol.name}
                    </span>
                    <span className="text-gray-400 text-xs">
                      {(match.similarity * 100).toFixed(1)}%
                    </span>
                  </div>
                  {match.description && (
                    <div className="text-gray-400 text-xs mt-1">
                      {match.description}
                    </div>
                  )}
                  {match.domain && (
                    <div className="text-blue-400 text-xs">
                      Domain: {match.domain}
                    </div>
                  )}
                </motion.div>
              ))}
            </div>
          </div>
        )}
      </div>
      
      {/* Flow History Panel */}
      {flowHistory.length > 0 && (
        <div className="qdpi-flows-panel p-4 bg-gray-900 rounded-lg border">
          <h4 className="text-md font-semibold text-white mb-3">
            Flow History ({flowHistory.length})
          </h4>
          <div className="space-y-2 max-h-60 overflow-y-auto">
            <AnimatePresence>
              {flowHistory.slice(-10).reverse().map((flow, index) => (
                <motion.div
                  key={flowHistory.length - index}
                  className="p-3 bg-gray-800 rounded border border-gray-700"
                  initial={{ opacity: 0, y: -10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -10 }}
                  transition={{ duration: 0.3 }}
                >
                  <div className="flex justify-between items-center mb-1">
                    <span className="text-white text-sm font-medium">
                      {flow.flow}
                    </span>
                    <span className={`text-xs px-2 py-1 rounded ${
                      flow.status === 'executed' ? 'bg-green-600' : 
                      flow.status === 'error' ? 'bg-red-600' : 'bg-yellow-600'
                    }`}>
                      {flow.status}
                    </span>
                  </div>
                  <div className="text-gray-400 text-xs">
                    Type: {flow.flow_type}
                  </div>
                  {flow.action && (
                    <div className="text-blue-400 text-xs mt-1">
                      Action: {flow.action}
                    </div>
                  )}
                </motion.div>
              ))}
            </AnimatePresence>
          </div>
        </div>
      )}
      
      {/* Loading Overlay */}
      {isLoading && (
        <motion.div
          className="absolute inset-0 bg-black bg-opacity-50 flex items-center justify-center"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
        >
          <div className="flex items-center gap-2 text-white">
            <div className="animate-spin w-5 h-5 border-2 border-white border-t-transparent rounded-full" />
            Processing QDPI operation...
          </div>
        </motion.div>
      )}
    </div>
  );
};

export default QDPIInterface;