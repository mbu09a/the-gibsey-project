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
  // New methods for recovered components
  getCurrentPrompts: () => any[];
  createBranch: (prompt: any) => void;
  rotateSymbol: (symbolId: string, rotation: number) => void;
  getBranchTree: () => any;
  navigateToBranch: (branchId: string) => void;
  furthestPageIndex: number;
  navigateToSection: (sectionId: string) => void;
  getCurrentSection: () => any;
  getAccessibleSections: () => any[];
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
    } 
    // Handle chapter-specific navigation for Phillip Bafflemint
    else if (tocId.startsWith('phillip-bafflemint-chapter-')) {
      // Extract chapter from the tocId (e.g., "phillip-bafflemint-chapter-1" -> "Chapter 1")
      const chapterNum = tocId.replace('phillip-bafflemint-chapter-', '');
      const chapterName = `Chapter ${chapterNum}`;
      firstPageIndex = pages.findIndex(page => 
        page.symbolId === 'phillip-bafflemint' && 
        (page as any).chapter === chapterName
      );
    }
    // Handle part-specific navigation for Jacklyn Variance
    else if (tocId.startsWith('jacklyn-variance-part-')) {
      // Extract part from the tocId (e.g., "jacklyn-variance-part-1" -> "Part 1")
      const partNum = tocId.replace('jacklyn-variance-part-', '');
      const partName = `Part ${partNum}`;
      firstPageIndex = pages.findIndex(page => 
        page.symbolId === 'jacklyn-variance' && 
        (page as any).chapter === partName
      );
    }
    // Handle part-specific navigation for Arieol Owlist
    else if (tocId.startsWith('arieol-owlist-part-')) {
      // Extract part from the tocId (e.g., "arieol-owlist-part-1" -> "Part 1")
      const partNum = tocId.replace('arieol-owlist-part-', '');
      const partName = `Part ${partNum}`;
      firstPageIndex = pages.findIndex(page => 
        page.symbolId === 'arieol-owlist' && 
        (page as any).chapter === partName
      );
    }
    // Handle chapter-specific navigation for Manny Valentinas
    else if (tocId.startsWith('manny-valentinas-chapter-')) {
      // Extract chapter from the tocId (e.g., "manny-valentinas-chapter-4" -> "Chapter 4")
      const chapterNum = tocId.replace('manny-valentinas-chapter-', '');
      const chapterName = `Chapter ${chapterNum}`;
      firstPageIndex = pages.findIndex(page => 
        page.symbolId === 'manny-valentinas' && 
        (page as any).chapter === chapterName
      );
    }
    // Handle chapter-specific navigation for Shamrock Stillman
    else if (tocId.startsWith('shamrock-stillman-chapter-')) {
      // Extract chapter from the tocId (e.g., "shamrock-stillman-chapter-7" -> "Chapter 7")
      const chapterNum = tocId.replace('shamrock-stillman-chapter-', '');
      const chapterName = `Chapter ${chapterNum}`;
      firstPageIndex = pages.findIndex(page => 
        page.symbolId === 'shamrock-stillman' && 
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
      // For Glyph Marrow, Phillip Bafflemint, Jacklyn Variance, Arieol Owlist, Manny Valentinas, and Shamrock Stillman, use symbolId + chapter/part, for others just use symbolId
      let tocId = page.symbolId;
      if ((page.symbolId === 'glyph-marrow' || page.symbolId === 'phillip-bafflemint' || page.symbolId === 'jacklyn-variance' || page.symbolId === 'arieol-owlist' || page.symbolId === 'manny-valentinas' || page.symbolId === 'shamrock-stillman') && (page as any).chapter) {
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

  // Stub implementations for recovered component compatibility
  const getCurrentPrompts = () => [];
  const createBranch = (prompt: any) => {};
  const rotateSymbol = (symbolId: string, rotation: number) => {};
  const getBranchTree = () => ({ branches: [], currentBranch: null });
  const navigateToBranch = (branchId: string) => {};
  const navigateToSection = (sectionId: string) => {};
  const getCurrentSection = () => ({ id: 'main', name: 'Main Story' });
  const getAccessibleSections = () => [{ id: 'main', name: 'Main Story' }];

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
        getAllSymbols,
        getCurrentPrompts,
        createBranch,
        rotateSymbol,
        getBranchTree,
        navigateToBranch,
        furthestPageIndex: pages.length - 1,
        navigateToSection,
        getCurrentSection,
        getAccessibleSections
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