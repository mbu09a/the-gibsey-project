import React, { useState } from 'react';
import CRTFrame from '../components/CRTFrame';
import PageViewer from '../components/PageViewer';
import { VaultIndex } from '../components/VaultIndex';
import SymbolTag from '../components/SymbolTag';
import ClusterSync from '../components/ClusterSync';
import { useStory } from '../context/StoryContext';

const HomePage: React.FC = () => {
  const { currentColor } = useStory();
  const [showTOC, setShowTOC] = useState(false);
  const [showClusterSync, setShowClusterSync] = useState(false);

  return (
    <CRTFrame>
      <div className="h-full flex flex-col"
           style={{
             '--scrollbar-track-color': `${currentColor}1A`,
             '--scrollbar-thumb-color': `${currentColor}66`,
             '--scrollbar-glow-color': `${currentColor}80`,
             '--scrollbar-thumb-hover-color': `${currentColor}99`
           } as React.CSSProperties}>
        
        {/* Header - responsive */}
        <header className="mb-4 sm:mb-6 lg:mb-8 text-center px-2">
          <h1 className="text-2xl sm:text-3xl lg:text-4xl font-bold mb-2 sm:mb-4 font-crt"
              style={{ 
                color: currentColor,
                textShadow: `0 0 20px ${currentColor}CC, 0 0 40px ${currentColor}66` 
              }}>
            THE GIBSEY PROJECT
          </h1>
          <SymbolTag />
          
          {/* Mobile TOC Toggle Button */}
          <button
            className="lg:hidden mt-4 px-4 py-2 border rounded font-crt text-sm transition-all"
            onClick={() => setShowTOC(!showTOC)}
            style={{
              color: currentColor,
              borderColor: currentColor,
              boxShadow: `0 0 10px ${currentColor}40`
            }}
          >
            {showTOC ? '← Back to Story' : 'Vault →'}
          </button>
        </header>

        {/* Main Content Area - responsive layout */}
        <div className="flex-1 min-h-0 px-2 lg:px-0">
          {/* Desktop Layout */}
          <div className="hidden lg:grid lg:grid-cols-4 gap-8 h-full">
            <aside className="col-span-1 h-full overflow-hidden">
              <div className="h-full border border-opacity-30 rounded p-4"
                   style={{ 
                     borderColor: currentColor,
                     boxShadow: `inset 0 0 20px ${currentColor}1A` 
                   }}>
                <VaultIndex />
              </div>
            </aside>

            <main className="col-span-3 h-full overflow-hidden">
              <div className="h-full border border-opacity-30 rounded p-6"
                   style={{ 
                     borderColor: currentColor,
                     boxShadow: `inset 0 0 20px ${currentColor}1A` 
                   }}>
                <PageViewer />
              </div>
            </main>
          </div>

          {/* Mobile Layout */}
          <div className="lg:hidden h-full">
            {showTOC ? (
              /* Mobile TOC View */
              <div className="h-full border border-opacity-30 rounded p-4"
                   style={{ 
                     borderColor: currentColor,
                     boxShadow: `inset 0 0 20px ${currentColor}1A` 
                   }}>
                <VaultIndex />
              </div>
            ) : (
              /* Mobile Story View */
              <div className="h-full border border-opacity-30 rounded p-4 sm:p-6"
                   style={{ 
                     borderColor: currentColor,
                     boxShadow: `inset 0 0 20px ${currentColor}1A` 
                   }}>
                <PageViewer />
              </div>
            )}
          </div>
        </div>
        
        {/* Mycelial Cluster Sync - Fixed Overlay */}
        <ClusterSync 
          isVisible={showClusterSync} 
          onToggle={() => setShowClusterSync(!showClusterSync)} 
        />
      </div>
    </CRTFrame>
  );
};

export default HomePage;