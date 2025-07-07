import React, { useState, useEffect, useRef } from 'react';
import { motion } from 'framer-motion';
import QDPIInterface from './QDPIInterface';

interface QDPIDemoProps {
  className?: string;
}

const DEMO_EXAMPLES = [
  {
    title: "Search for Wisdom",
    description: "Search for symbols related to wisdom and knowledge",
    action: "search",
    data: "wisdom and understanding"
  },
  {
    title: "Encode a Message", 
    description: "Transform text into QDPI symbolic representation",
    action: "encode",
    data: "Hello Gibsey! How are you today?"
  },
  {
    title: "Ask Mode Query",
    description: "Switch to Ask mode and search for help",
    action: "mode_and_search",
    data: { mode: "ask", query: "help me understand" }
  },
  {
    title: "Index New Content",
    description: "Switch to Index mode and create something new", 
    action: "mode_and_encode",
    data: { mode: "index", content: "Creating new narrative branch" }
  },
  {
    title: "Symbol Flow Execution",
    description: "Execute flows for specific character symbols",
    action: "execute",
    data: "london_fox"
  }
];

export const QDPIDemo: React.FC<QDPIDemoProps> = ({ className = '' }) => {
  const [sessionId] = useState(() => `demo-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`);
  const [websocket, setWebsocket] = useState<WebSocket | null>(null);
  const [connectionStatus, setConnectionStatus] = useState<'connecting' | 'connected' | 'disconnected'>('connecting');
  const [currentState, setCurrentState] = useState<any>(null);
  const [activeSymbol, setActiveSymbol] = useState<any>(null);
  const [demoStep, setDemoStep] = useState(0);
  const [autoDemo, setAutoDemo] = useState(false);
  const [logs, setLogs] = useState<string[]>([]);
  
  const wsRef = useRef<WebSocket | null>(null);
  const qdpiRef = useRef<any>(null);
  
  // Add log entry
  const addLog = (message: string) => {
    setLogs(prev => [...prev.slice(-20), `${new Date().toLocaleTimeString()}: ${message}`]);
  };
  
  // Initialize WebSocket connection
  useEffect(() => {
    const connectWebSocket = () => {
      try {
        const ws = new WebSocket(`ws://localhost:8000/ws/qdpi/${sessionId}`);
        wsRef.current = ws;
        
        ws.onopen = () => {
          setConnectionStatus('connected');
          setWebsocket(ws);
          addLog('✅ Connected to Gibsey WebSocket');
          
          // Subscribe to QDPI events
          ws.send(JSON.stringify({
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
        };
        
        ws.onmessage = (event) => {
          try {
            const message = JSON.parse(event.data);
            
            switch (message.type) {
              case 'qdpi_subscription_confirmed':
                addLog('🔔 Subscribed to QDPI events');
                break;
                
              case 'qdpi_mode_changed':
                addLog(`🔄 Mode changed: ${message.data.old_mode} → ${message.data.new_mode}`);
                break;
                
              case 'qdpi_orientation_flipped':
                addLog(`🔄 Orientation flipped: ${message.data.old_orientation} → ${message.data.new_orientation}`);
                break;
                
              case 'qdpi_symbol_activated':
                addLog(`✨ Symbol activated: ${message.data.symbol.name}`);
                break;
                
              case 'qdpi_flow_executed':
                addLog(`⚡ Flows executed for: ${message.data.symbol_name}`);
                break;
                
              case 'qdpi_search_results':
                addLog(`🔍 Search completed: "${message.data.query}" (${message.data.results.count} results)`);
                break;
                
              default:
                if (message.type.startsWith('qdpi_')) {
                  addLog(`📡 QDPI event: ${message.type}`);
                }
                break;
            }
          } catch (error) {
            console.error('Error parsing WebSocket message:', error);
          }
        };
        
        ws.onclose = () => {
          setConnectionStatus('disconnected');
          setWebsocket(null);
          addLog('❌ WebSocket disconnected');
          
          // Attempt to reconnect after 3 seconds
          setTimeout(connectWebSocket, 3000);
        };
        
        ws.onerror = (error) => {
          console.error('WebSocket error:', error);
          addLog('❌ WebSocket error occurred');
        };
        
      } catch (error) {
        console.error('Failed to create WebSocket:', error);
        setConnectionStatus('disconnected');
        setTimeout(connectWebSocket, 3000);
      }
    };
    
    connectWebSocket();
    
    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, [sessionId]);
  
  // Auto-demo functionality
  useEffect(() => {
    if (!autoDemo) return;
    
    const interval = setInterval(() => {
      setDemoStep(prev => (prev + 1) % DEMO_EXAMPLES.length);
    }, 5000);
    
    return () => clearInterval(interval);
  }, [autoDemo]);
  
  // Execute demo example
  const executeDemo = async (example: typeof DEMO_EXAMPLES[0]) => {
    addLog(`🎬 Executing demo: ${example.title}`);
    
    // Here you would trigger the appropriate action based on example.action
    // For now, we'll just log it
    switch (example.action) {
      case 'search':
        // Trigger search in QDPI interface
        addLog(`🔍 Searching for: "${example.data}"`);
        break;
        
      case 'encode':
        // Trigger encoding in QDPI interface  
        addLog(`📝 Encoding: "${example.data}"`);
        break;
        
      case 'mode_and_search':
        const modeSearchData = example.data as { mode: string; query: string };
        addLog(`🔄 Switching to ${modeSearchData.mode} mode and searching for "${modeSearchData.query}"`);
        break;
        
      case 'mode_and_encode':
        const modeEncodeData = example.data as { mode: string; content: string };
        addLog(`🔄 Switching to ${modeEncodeData.mode} mode and encoding "${modeEncodeData.content}"`);
        break;
        
      case 'execute':
        addLog(`⚡ Executing flows for symbol: ${example.data}`);
        break;
    }
  };
  
  return (
    <div className={`qdpi-demo min-h-screen bg-gradient-to-br from-gray-900 to-black p-6 ${className}`}>
      {/* Header */}
      <div className="max-w-7xl mx-auto mb-8">
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-8"
        >
          <h1 className="text-4xl font-bold text-white mb-4">
            QDPI-256 Live Demo
          </h1>
          <p className="text-gray-400 text-lg mb-6">
            Quaternary Data Protocol Interface - Symbolic Machine Language for Gibsey
          </p>
          
          {/* Connection Status */}
          <div className="flex items-center justify-center gap-4 mb-6">
            <div className="flex items-center gap-2">
              <div 
                className={`w-3 h-3 rounded-full ${
                  connectionStatus === 'connected' ? 'bg-green-500' : 
                  connectionStatus === 'connecting' ? 'bg-yellow-500' : 'bg-red-500'
                }`}
              />
              <span className="text-white text-sm">
                WebSocket: {connectionStatus}
              </span>
            </div>
            
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-blue-500" />
              <span className="text-white text-sm">
                Session: {sessionId.slice(-8)}
              </span>
            </div>
          </div>
          
          {/* Demo Controls */}
          <div className="flex items-center justify-center gap-4 mb-6">
            <button
              onClick={() => setAutoDemo(!autoDemo)}
              className={`px-4 py-2 rounded font-medium transition-colors ${
                autoDemo 
                  ? 'bg-red-600 hover:bg-red-700 text-white' 
                  : 'bg-green-600 hover:bg-green-700 text-white'
              }`}
            >
              {autoDemo ? 'Stop Auto Demo' : 'Start Auto Demo'}
            </button>
            
            <select
              value={demoStep}
              onChange={(e) => setDemoStep(parseInt(e.target.value))}
              className="px-3 py-2 bg-gray-800 text-white rounded border border-gray-700"
            >
              {DEMO_EXAMPLES.map((example, index) => (
                <option key={index} value={index}>
                  {example.title}
                </option>
              ))}
            </select>
            
            <button
              onClick={() => executeDemo(DEMO_EXAMPLES[demoStep])}
              className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded font-medium"
            >
              Execute Demo
            </button>
          </div>
        </motion.div>
        
        {/* Current Demo Example */}
        {autoDemo && (
          <motion.div
            key={demoStep}
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="bg-gray-800 rounded-lg p-4 mb-6 border border-gray-700"
          >
            <h3 className="text-white font-semibold mb-2">
              Demo Step {demoStep + 1}: {DEMO_EXAMPLES[demoStep].title}
            </h3>
            <p className="text-gray-400 text-sm">
              {DEMO_EXAMPLES[demoStep].description}
            </p>
          </motion.div>
        )}
        
        {/* Main Interface */}
        <div className="grid lg:grid-cols-3 gap-6">
          {/* QDPI Interface */}
          <div className="lg:col-span-2">
            <QDPIInterface
              sessionId={sessionId}
              websocket={websocket}
              onStateChange={setCurrentState}
              onSymbolActivated={setActiveSymbol}
              className="relative"
            />
          </div>
          
          {/* Status Panel */}
          <div className="space-y-6">
            {/* Current State */}
            {currentState && (
              <motion.div
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                className="bg-gray-900 rounded-lg p-4 border border-gray-700"
              >
                <h4 className="text-white font-semibold mb-3">Current State</h4>
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-gray-400">Mode:</span>
                    <span className="text-white font-mono uppercase">{currentState.mode}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-400">Orientation:</span>
                    <span className="text-white">{currentState.orientation === 'n' ? 'Normal' : 'Upside'}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-400">Updated:</span>
                    <span className="text-white text-xs">
                      {new Date(currentState.timestamp).toLocaleTimeString()}
                    </span>
                  </div>
                </div>
              </motion.div>
            )}
            
            {/* Active Symbol */}
            {activeSymbol && (
              <motion.div
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                className="bg-gray-900 rounded-lg p-4 border border-gray-700"
              >
                <h4 className="text-white font-semibold mb-3">Active Symbol</h4>
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-gray-400">Name:</span>
                    <span className="text-white">{activeSymbol.name}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-400">Glyph ID:</span>
                    <span className="text-white font-mono">{activeSymbol.glyph_id}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-400">Rotation:</span>
                    <span className="text-white">{activeSymbol.rotation}°</span>
                  </div>
                </div>
              </motion.div>
            )}
            
            {/* Activity Log */}
            <div className="bg-gray-900 rounded-lg p-4 border border-gray-700">
              <h4 className="text-white font-semibold mb-3">Activity Log</h4>
              <div className="space-y-1 max-h-60 overflow-y-auto">
                {logs.slice(-10).map((log, index) => (
                  <motion.div
                    key={logs.length - index}
                    initial={{ opacity: 0, y: -10 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="text-xs text-gray-400 font-mono"
                  >
                    {log}
                  </motion.div>
                ))}
                {logs.length === 0 && (
                  <div className="text-xs text-gray-500 italic">
                    Activity will appear here...
                  </div>
                )}
              </div>
            </div>
            
            {/* Demo Examples */}
            <div className="bg-gray-900 rounded-lg p-4 border border-gray-700">
              <h4 className="text-white font-semibold mb-3">Demo Examples</h4>
              <div className="space-y-2">
                {DEMO_EXAMPLES.map((example, index) => (
                  <button
                    key={index}
                    onClick={() => {
                      setDemoStep(index);
                      executeDemo(example);
                    }}
                    className={`w-full text-left p-2 rounded text-sm transition-colors ${
                      index === demoStep 
                        ? 'bg-blue-600 text-white' 
                        : 'bg-gray-800 text-gray-300 hover:bg-gray-700'
                    }`}
                  >
                    <div className="font-medium">{example.title}</div>
                    <div className="text-xs opacity-80">{example.description}</div>
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default QDPIDemo;