import React, { useState, useRef, useEffect } from 'react';
import { useStory } from '../context/StoryContext';

interface ChatMessage {
  id: string;
  type: 'user' | 'jacklyn';
  content: string;
  timestamp: Date;
  reportNumber?: string;
}

interface ChatInterfaceProps {
  isOpen: boolean;
  onClose: () => void;
}

const ChatInterface: React.FC<ChatInterfaceProps> = ({ isOpen, onClose }) => {
  const { currentPage, currentColor } = useStory();
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Initialize with Jacklyn's greeting
  useEffect(() => {
    if (isOpen && messages.length === 0) {
      const greeting: ChatMessage = {
        id: 'greeting',
        type: 'jacklyn',
        content: `D.A.D.D.Y.S-H.A.R.D #${Math.floor(Math.random() * 100) + 1} — Initial Contact
Subject: User Interface Detected

Terminal interface established. Current location: ${currentPage?.symbolId || 'unknown'}. Analysis mode active. State your query for surveillance review. All interactions are monitored and recorded for institutional purposes.

—JV`,
        timestamp: new Date(),
        reportNumber: '#' + (Math.floor(Math.random() * 100) + 1)
      };
      setMessages([greeting]);
    }
  }, [isOpen, currentPage?.symbolId]);

  const generateJacklynResponse = async (userInput: string): Promise<string> => {
    // Simulate AI processing delay
    await new Promise(resolve => setTimeout(resolve, 1500 + Math.random() * 1000));
    
    const reportNumber = Math.floor(Math.random() * 100) + 50;
    
    // Context-aware responses based on current page and user input
    const responses = {
      greeting: `D.A.D.D.Y.S-H.A.R.D #${reportNumber} — Response Protocol
Subject: User Query Processing

Query received and catalogued. Pattern recognition algorithms engaged. Your interest in the ${currentPage?.symbolId} sector has been noted. Recommend proceeding with caution—surveillance data indicates recursive anomalies in this narrative quadrant.

—JV`,
      
      about: `D.A.D.D.Y.S-H.A.R.D #${reportNumber} — Personnel File
Subject: Agent Identification

Jacklyn Variance, Anomaly Detection and Designation specialist. Current assignment: monitoring Gibsey World narrative infrastructure for systematic dysfunction. Years of service: classified. Personal feelings about this assignment: irrelevant. The work continues regardless of individual preference.

—JV`,
      
      mystery: `D.A.D.D.Y.S-H.A.R.D #${reportNumber} — Pattern Analysis
Subject: Systemic Ambiguity Assessment

Your observation regarding "${userInput}" aligns with institutional findings. The park's operational preference for ambiguity appears intentional—classic misdirection protocol. Recommend accepting uncertainty as baseline operational parameter. Truth, as always, remains institutionally inconvenient.

—JV`,
      
      help: `D.A.D.D.Y.S-H.A.R.D #${reportNumber} — Guidance Protocol
Subject: User Assistance Request

Analysis indicates you require navigation assistance. The mycelial network responds to symbolic rotation and prompt interaction. Current page rotation: ${currentPage?.rotation || 0}°. Branch creation available through narrative intervention. All paths monitored. Choose wisely.

—JV`,
      
      default: `D.A.D.D.Y.S-H.A.R.D #${reportNumber} — Query Analysis
Subject: "${userInput.slice(0, 30)}${userInput.length > 30 ? '...' : ''}"

Data reviewed. Pattern analysis inconclusive. The query reflects standard visitor confusion regarding park operations. Recommend re-phrasing with greater specificity. Note: all interactions are recorded for quality assurance and surveillance optimization purposes.

—JV`
    };
    
    const inputLower = userInput.toLowerCase();
    
    if (inputLower.includes('hello') || inputLower.includes('hi') || inputLower.includes('hey')) {
      return responses.greeting;
    } else if (inputLower.includes('who are you') || inputLower.includes('about you') || inputLower.includes('jacklyn')) {
      return responses.about;
    } else if (inputLower.includes('help') || inputLower.includes('how') || inputLower.includes('what can')) {
      return responses.help;
    } else if (inputLower.includes('mystery') || inputLower.includes('strange') || inputLower.includes('weird') || inputLower.includes('author')) {
      return responses.mystery;
    } else {
      return responses.default;
    }
  };

  const handleSendMessage = async () => {
    if (!inputValue.trim() || isProcessing) return;

    const userMessage: ChatMessage = {
      id: `user-${Date.now()}`,
      type: 'user',
      content: inputValue,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsProcessing(true);

    try {
      const jacklynResponse = await generateJacklynResponse(inputValue);
      
      const responseMessage: ChatMessage = {
        id: `jacklyn-${Date.now()}`,
        type: 'jacklyn',
        content: jacklynResponse,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, responseMessage]);
    } catch (error) {
      console.error('Error generating response:', error);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div 
        className="w-full max-w-2xl h-[80vh] border-2 rounded-sm flex flex-col"
        style={{ 
          borderColor: currentColor,
          backgroundColor: '#0a0a0a',
          boxShadow: `0 0 30px ${currentColor}40`
        }}
      >
        {/* Header */}
        <div 
          className="p-4 border-b flex items-center justify-between"
          style={{ borderColor: currentColor }}
        >
          <div className="flex items-center gap-3">
            <div 
              className="w-8 h-8 rounded-full flex items-center justify-center"
              style={{ 
                backgroundColor: currentColor,
                color: '#0a0a0a'
              }}
            >
              JV
            </div>
            <div>
              <div className="font-crt text-sm" style={{ color: currentColor }}>
                D.A.D.D.Y.S-H.A.R.D Terminal
              </div>
              <div className="font-crt text-xs opacity-50" style={{ color: currentColor }}>
                Jacklyn Variance • Active Monitoring
              </div>
            </div>
          </div>
          
          <button
            onClick={onClose}
            className="px-3 py-1 border font-crt text-sm transition-all hover:bg-opacity-20"
            style={{
              borderColor: currentColor,
              color: currentColor
            }}
          >
            [CLOSE]
          </button>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4 custom-scrollbar">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[80%] p-3 rounded-sm ${
                  message.type === 'user' 
                    ? 'border-l-4' 
                    : 'border-r-4'
                }`}
                style={{
                  borderColor: currentColor,
                  backgroundColor: message.type === 'user' 
                    ? `${currentColor}10` 
                    : `${currentColor}08`,
                  borderLeftColor: message.type === 'user' ? currentColor : 'transparent',
                  borderRightColor: message.type === 'jacklyn' ? currentColor : 'transparent'
                }}
              >
                <div className="font-crt text-sm whitespace-pre-wrap" style={{ color: currentColor }}>
                  {message.content}
                </div>
                <div className="font-crt text-xs opacity-50 mt-2" style={{ color: currentColor }}>
                  {message.timestamp.toLocaleTimeString()}
                </div>
              </div>
            </div>
          ))}
          
          {isProcessing && (
            <div className="flex justify-start">
              <div
                className="max-w-[80%] p-3 border-r-4 rounded-sm"
                style={{
                  borderColor: currentColor,
                  backgroundColor: `${currentColor}08`
                }}
              >
                <div className="font-crt text-sm flex items-center gap-2" style={{ color: currentColor }}>
                  <span>Generating analysis</span>
                  <div className="flex gap-1">
                    <div className="w-1 h-1 bg-current rounded-full animate-pulse" style={{ animationDelay: '0ms' }} />
                    <div className="w-1 h-1 bg-current rounded-full animate-pulse" style={{ animationDelay: '200ms' }} />
                    <div className="w-1 h-1 bg-current rounded-full animate-pulse" style={{ animationDelay: '400ms' }} />
                  </div>
                </div>
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>

        {/* Input */}
        <div 
          className="p-4 border-t"
          style={{ borderColor: currentColor }}
        >
          <div className="flex gap-2">
            <textarea
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder={`Ask ${currentPage?.symbolId === 'jacklyn-variance' ? 'Jacklyn Variance' : 'the character'} a question...`}
              disabled={isProcessing}
              className="flex-1 p-3 bg-transparent border font-crt text-sm resize-none h-20
                         focus:outline-none focus:ring-2 disabled:opacity-50"
              style={{
                borderColor: currentColor,
                color: currentColor,
                backgroundColor: `${currentColor}05`
              }}
            />
            <button
              onClick={handleSendMessage}
              disabled={isProcessing || !inputValue.trim()}
              className="px-4 py-2 border font-crt text-sm transition-all self-end
                         disabled:opacity-50 disabled:cursor-not-allowed"
              style={{
                borderColor: currentColor,
                color: currentColor,
                backgroundColor: inputValue.trim() ? `${currentColor}20` : 'transparent'
              }}
            >
              SEND
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;