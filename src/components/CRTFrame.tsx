import React from 'react';

interface CRTFrameProps {
  children: React.ReactNode;
  className?: string;
}

const CRTFrame: React.FC<CRTFrameProps> = ({ children, className = '' }) => {
  return (
    <div className={`crt-container relative w-full h-screen bg-crt-bg overflow-hidden ${className}`}>
      <div className="crt-bezel absolute inset-0 bg-gradient-to-br from-gray-900 to-black rounded-none sm:rounded-lg p-2 sm:p-4 lg:p-8">
        <div className="crt-screen relative w-full h-full bg-black rounded-none sm:rounded overflow-hidden">
          <div className="crt-content relative z-10 w-full h-full p-3 sm:p-4 lg:p-8 overflow-hidden">
            {children}
          </div>
          
          {/* Scanlines - reduced on mobile */}
          <div className="crt-scanlines absolute inset-0 pointer-events-none opacity-3 sm:opacity-5">
            <div className="scanline animate-scanline"></div>
          </div>
          
          {/* Flicker effect - reduced on mobile */}
          <div className="crt-flicker absolute inset-0 pointer-events-none animate-flicker opacity-50 sm:opacity-100"></div>
          
          {/* Screen curvature effect - reduced on mobile */}
          <div className="crt-curve absolute inset-0 pointer-events-none"
               style={{
                 background: 'radial-gradient(ellipse at center, transparent 0%, rgba(0,0,0,0.1) 70%, rgba(0,0,0,0.2) 100%)',
               }}>
          </div>
          
          {/* Green phosphor glow - adjusted for mobile */}
          <div className="crt-glow absolute inset-0 pointer-events-none"
               style={{
                 boxShadow: 'inset 0 0 60px rgba(52, 255, 120, 0.05), inset 0 0 120px rgba(52, 255, 120, 0.1)',
               }}>
          </div>
          
          {/* Screen reflection - reduced on mobile */}
          <div className="crt-reflection absolute inset-0 pointer-events-none opacity-3 sm:opacity-5"
               style={{
                 background: 'linear-gradient(135deg, rgba(255,255,255,0.05) 0%, transparent 50%)',
               }}>
          </div>
        </div>
        
        {/* Outer bezel glow - adjusted for mobile */}
        <div className="absolute inset-0 rounded-none sm:rounded-lg pointer-events-none"
             style={{
               boxShadow: '0 0 40px rgba(52, 255, 120, 0.1), inset 0 0 20px rgba(0,0,0,0.6), 0 0 80px rgba(52, 255, 120, 0.2)',
             }}>
        </div>
      </div>
      
      {/* Ambient glow - reduced on mobile */}
      <div className="absolute inset-0 pointer-events-none"
           style={{
             background: 'radial-gradient(circle at center, rgba(52, 255, 120, 0.03) 0%, transparent 50%)',
           }}>
      </div>
    </div>
  );
};

export default CRTFrame;