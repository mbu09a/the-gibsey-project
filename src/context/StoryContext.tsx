import React, { createContext, useContext, useState, useEffect } from 'react';
import { StoryPage } from '../types/story';
import { corpusColors } from '../assets/colors';
import storyData from '../assets/texts.json';

interface StoryContextType {
  pages: StoryPage[];
  currentPageIndex: number;
  currentPage: StoryPage | null;
  currentSymbol: string | null;
  currentColor: string;
  setCurrentPageIndex: (index: number) => void;
  navigateToSymbol: (symbolId: string) => void;
  nextPage: () => void;
  previousPage: () => void;
  getPagesBySymbol: (symbolId: string) => StoryPage[];
  getAllSymbols: () => { id: string; name: string; color: string; pageCount: number }[];
}

const StoryContext = createContext<StoryContextType | undefined>(undefined);

export const StoryProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [pages] = useState<StoryPage[]>(storyData as StoryPage[]);
  const [currentPageIndex, setCurrentPageIndex] = useState(0);

  const currentPage = pages[currentPageIndex] || null;
  const currentSymbol = currentPage?.symbolId || null;
  const currentColor = currentSymbol ? corpusColors[currentSymbol] : '#34FF78';

  const navigateToSymbol = (tocId: string) => {
    let firstPageIndex = -1;
    
    // Handle chapter-specific navigation for Glyph Marrow
    if (tocId.startsWith('glyph-marrow-chapter-')) {
      // Extract chapter from the tocId (e.g., "glyph-marrow-chapter-1" -> "Chapter 1")
      const chapterNum = tocId.replace('glyph-marrow-chapter-', '');
      const chapterName = `Chapter ${chapterNum}`;
      firstPageIndex = pages.findIndex(page => 
        page.symbolId === 'glyph-marrow' && 
        (page as any).chapter === chapterName
      );
    } else {
      // For other symbols, find by symbolId
      firstPageIndex = pages.findIndex(page => page.symbolId === tocId);
    }
    
    if (firstPageIndex !== -1) {
      // Smooth transition by immediately setting the page
      setCurrentPageIndex(firstPageIndex);
    }
  };

  const nextPage = () => {
    if (currentPageIndex < pages.length - 1) {
      setCurrentPageIndex(currentPageIndex + 1);
    }
  };

  const previousPage = () => {
    if (currentPageIndex > 0) {
      setCurrentPageIndex(currentPageIndex - 1);
    }
  };

  const getPagesBySymbol = (symbolId: string) => {
    return pages.filter(page => page.symbolId === symbolId);
  };

  const getAllSymbols = () => {
    const symbolMap = new Map<string, { name: string; color: string; pageCount: number }>();
    
    pages.forEach(page => {
      // Create unique identifier for table of contents
      // For Glyph Marrow, use symbolId + chapter, for others just use symbolId
      let tocId = page.symbolId;
      if (page.symbolId === 'glyph-marrow' && (page as any).chapter) {
        tocId = `${page.symbolId}-${(page as any).chapter.toLowerCase().replace(/\s+/g, '-')}`;
      }
      
      if (!symbolMap.has(tocId)) {
        symbolMap.set(tocId, {
          name: page.title,
          color: corpusColors[page.symbolId] || '#34FF78',
          pageCount: 0
        });
      }
      const symbol = symbolMap.get(tocId)!;
      symbol.pageCount++;
    });

    return Array.from(symbolMap.entries()).map(([id, data]) => ({
      id,
      ...data
    }));
  };

  useEffect(() => {
    const handleKeyPress = (e: KeyboardEvent) => {
      if (e.key === 'ArrowRight') nextPage();
      if (e.key === 'ArrowLeft') previousPage();
    };

    window.addEventListener('keydown', handleKeyPress);
    return () => window.removeEventListener('keydown', handleKeyPress);
  }, [currentPageIndex]);

  return (
    <StoryContext.Provider
      value={{
        pages,
        currentPageIndex,
        currentPage,
        currentSymbol,
        currentColor,
        setCurrentPageIndex,
        navigateToSymbol,
        nextPage,
        previousPage,
        getPagesBySymbol,
        getAllSymbols
      }}
    >
      {children}
    </StoryContext.Provider>
  );
};

export const useStory = () => {
  const context = useContext(StoryContext);
  if (context === undefined) {
    throw new Error('useStory must be used within a StoryProvider');
  }
  return context;
};