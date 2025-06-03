import React from 'react';
import CRTFrame from '../components/CRTFrame';
import PageViewer from '../components/PageViewer';
import SymbolIndex from '../components/SymbolIndex';
import SymbolTag from '../components/SymbolTag';
import { useStory } from '../context/StoryContext';

const HomePage: React.FC = () => {
  const { currentColor } = useStory();

  return (
    <CRTFrame>
      <div className="h-full flex flex-col"
           style={{
             '--scrollbar-track-color': `${currentColor}1A`,
             '--scrollbar-thumb-color': `${currentColor}66`,
             '--scrollbar-glow-color': `${currentColor}80`,
             '--scrollbar-thumb-hover-color': `${currentColor}99`
           } as React.CSSProperties}>
        <header className="mb-8 text-center">
          <h1 className="text-4xl font-bold mb-4 font-crt"
              style={{ 
                color: currentColor,
                textShadow: `0 0 20px ${currentColor}CC, 0 0 40px ${currentColor}66` 
              }}>
            THE GIBSEY PROJECT
          </h1>
          <SymbolTag />
        </header>

        <div className="flex-1 grid grid-cols-1 lg:grid-cols-4 gap-8 min-h-0">
          <aside className="lg:col-span-1 h-full overflow-hidden">
            <div className="h-full border border-opacity-30 rounded p-4"
                 style={{ 
                   borderColor: currentColor,
                   boxShadow: `inset 0 0 20px ${currentColor}1A` 
                 }}>
              <SymbolIndex />
            </div>
          </aside>

          <main className="lg:col-span-3 h-full overflow-hidden">
            <div className="h-full border border-opacity-30 rounded p-6"
                 style={{ 
                   borderColor: currentColor,
                   boxShadow: `inset 0 0 20px ${currentColor}1A` 
                 }}>
              <PageViewer />
            </div>
          </main>
        </div>
      </div>
    </CRTFrame>
  );
};

export default HomePage;