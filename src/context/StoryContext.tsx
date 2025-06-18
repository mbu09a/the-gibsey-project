import React, { createContext, useContext, useState, useEffect } from 'react';
import { StoryPage, SymbolRotation, Prompt, BranchNode, PromptType, PageType } from '../types/story';
import { corpusColors } from '../assets/colors';
import { BOOK_SECTIONS, getSectionByPageNumber, getAccessedSections } from '../types/sections';
import storyData from '../assets/texts.json';

interface StoryContextType {
  pages: StoryPage[];
  currentPageIndex: number;
  currentPage: StoryPage | null;
  currentSymbol: string | null;
  currentColor: string;
  currentRotation: SymbolRotation;
  furthestPageIndex: number;
  setCurrentPageIndex: (index: number) => void;
  navigateToSymbol: (symbolId: string) => void;
  nextPage: () => void;
  previousPage: () => void;
  getPagesBySymbol: (symbolId: string) => StoryPage[];
  getAllSymbols: () => { id: string; name: string; color: string; pageCount: number }[];
  
  // Section Navigation Functions
  navigateToSection: (sectionId: number) => void;
  getCurrentSection: () => any;
  getAccessibleSections: () => any[];
  
  // Mycelial Network Functions
  rotateSymbol: (rotation: SymbolRotation) => void;
  createBranch: (prompt: Prompt, content: string, authorType: 'user' | 'ai') => string;
  navigateToBranch: (branchId: string) => void;
  getBranchTree: (pageId?: string) => BranchNode[];
  getCurrentPrompts: () => Prompt[];
}

// Helper function to generate PRD-compliant prompts for each page
const generateDefaultPrompts = (page: StoryPage): Prompt[] => {
  const characterName = getCharacterName(page.symbolId);
  return [
    {
      id: `${page.id}-character-prompt`,
      type: 'character_prompt' as PromptType,
      text: `What does ${characterName} do next?`,
      targetRotation: 90 as SymbolRotation,
      description: "Character action prompt - drives the narrative forward"
    },
    {
      id: `${page.id}-user-prompt`,
      type: 'user_prompt' as PromptType,
      text: `Ask ${characterName} a question...`,
      targetRotation: 180 as SymbolRotation,
      description: "User query - direct interaction with character"
    },
    {
      id: `${page.id}-character-response`,
      type: 'character_response' as PromptType,
      text: `${characterName} responds to your inquiry`,
      targetRotation: 270 as SymbolRotation,
      description: "Character response - AI-driven dialogue"
    }
  ];
};

// Helper to get character name from symbolId
const getCharacterName = (symbolId: string): string => {
  const characterMap: Record<string, string> = {
    'an-author': 'The Author',
    'london-fox': 'London Fox',
    'glyph-marrow': 'Glyph Marrow',
    'phillip-bafflemint': 'Phillip Bafflemint',
    'jacklyn-variance': 'Jacklyn Variance',
    'oren-progresso': 'Oren Progresso',
    'natalie-weissman': 'Natalie Weissman',
    'princhetta': 'Princhetta',
    'copy-e-right': 'Copy-E-Right',
    'arieol-owlist': 'Arieol Owlist',
    'jack-parlance': 'Jack Parlance',
    'manny-valentinas': 'Manny Valentinas',
    'shamrock-stillman': 'Shamrock Stillman',
    'todd-fishbone': 'Todd Fishbone'
  };
  return characterMap[symbolId] || 'The Character';
};

const StoryContext = createContext<StoryContextType | undefined>(undefined);

export const StoryProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  // Enhanced pages with PRD-compliant branching support
  const [pages, setPages] = useState<StoryPage[]>(() => {
    const basePages = storyData as StoryPage[];
    // Initialize pages with PRD-compliant structure
    return basePages.map(page => ({
      ...page,
      rotation: 0 as SymbolRotation, // Primary story path = 0°
      pageType: 'primary' as PageType, // Original story pages are primary
      author: 'system', // Original story is system-authored
      prompts: generateDefaultPrompts(page),
      childIds: [],
      branches: []
    }));
  });
  
  const [currentPageIndex, setCurrentPageIndexState] = useState(() => {
    const savedIndex = localStorage.getItem('currentPageIndex');
    return savedIndex ? parseInt(savedIndex, 10) : 0;
  });
  const [furthestPageIndex, setFurthestPageIndex] = useState(() => {
    const savedFurthest = localStorage.getItem('furthestPageIndex');
    return savedFurthest ? parseInt(savedFurthest, 10) : 0;
  });
  const [currentRotation, setCurrentRotation] = useState<SymbolRotation>(0);
  const [branchPages, setBranchPages] = useState<Map<string, StoryPage>>(new Map());

  const currentPage = pages[currentPageIndex] || null;
  const currentSymbol = currentPage?.symbolId || null;
  const currentColor = currentSymbol ? corpusColors[currentSymbol] : '#34FF78';

  const setCurrentPageIndex = (index: number) => {
    setCurrentPageIndexState(index);
    localStorage.setItem('currentPageIndex', index.toString());
    
    if (index > furthestPageIndex) {
      setFurthestPageIndex(index);
      localStorage.setItem('furthestPageIndex', index.toString());
    }
  };

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
    
    if (firstPageIndex !== -1 && firstPageIndex <= furthestPageIndex) {
      // Smooth transition by immediately setting the page
      setCurrentPageIndex(firstPageIndex);
    }
  };

  const nextPage = () => {
    if (currentPageIndex < pages.length - 1 && currentPageIndex < furthestPageIndex) {
      setCurrentPageIndex(currentPageIndex + 1);
    } else if (currentPageIndex === furthestPageIndex && currentPageIndex < pages.length - 1) {
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

  // Mycelial Network Functions
  const rotateSymbol = (rotation: SymbolRotation) => {
    setCurrentRotation(rotation);
    if (currentPage) {
      setPages(prev => prev.map(page => 
        page.id === currentPage.id 
          ? { ...page, rotation } 
          : page
      ));
    }
  };

  const createBranch = (prompt: Prompt, content: string, authorType: 'user' | 'ai'): string => {
    if (!currentPage) return '';
    
    const branchId = `${currentPage.id}-branch-${Date.now()}`;
    
    // Determine page type based on prompt type and author
    let pageType: PageType;
    if (prompt.type === 'user_prompt') {
      pageType = authorType === 'user' ? 'user_query' : 'ai_response';
    } else {
      pageType = 'prompt'; // character_prompt or character_response
    }
    
    const newBranch: StoryPage = {
      ...currentPage,
      id: branchId,
      text: content,
      parentId: currentPage.id,
      childIds: [],
      branches: [],
      rotation: prompt.targetRotation,
      pageType,
      promptType: prompt.type,
      author: authorType === 'user' ? 'user' : getCharacterName(currentPage.symbolId),
      branchId: `branch-${currentPage.id}-${Date.now()}`,
      createdAt: new Date(),
      metadata: {
        ...currentPage.metadata,
        promptUsed: prompt.id,
        authorType,
        originalPageId: currentPage.id
      }
    };

    // Add branch to branch pages map
    setBranchPages(prev => new Map(prev.set(branchId, newBranch)));

    // Update parent page with new child
    setPages(prev => prev.map(page => 
      page.id === currentPage.id
        ? {
            ...page,
            childIds: [...page.childIds, branchId],
            branches: [...page.branches, {
              pageId: branchId,
              promptUsed: prompt.id,
              createdBy: authorType,
              timestamp: new Date()
            }]
          }
        : page
    ));

    return branchId;
  };

  const navigateToBranch = (branchId: string) => {
    const branchPage = branchPages.get(branchId);
    if (branchPage) {
      // For now, we'll simulate navigation by updating the current page text
      // In a full implementation, this would navigate to the branch page
      console.log(`Navigating to branch: ${branchId}`, branchPage);
    }
  };

  const getBranchTree = (pageId?: string): BranchNode[] => {
    const targetPageId = pageId || currentPage?.id;
    if (!targetPageId) return [];
    
    const page = pages.find(p => p.id === targetPageId);
    return page?.branches || [];
  };

  const getCurrentPrompts = (): Prompt[] => {
    return currentPage?.prompts || [];
  };

  // Section Navigation Functions
  const navigateToSection = (sectionId: number) => {
    const section = BOOK_SECTIONS.find(s => s.id === sectionId);
    if (!section) return;
    
    // Navigate to the first page of the section (convert 1-based to 0-based index)
    const targetPageIndex = section.startPage - 1;
    
    // Allow navigation to any section (remove restriction)
    setCurrentPageIndex(targetPageIndex);
    
    // Update furthest page if we're jumping ahead
    if (targetPageIndex > furthestPageIndex) {
      setFurthestPageIndex(targetPageIndex);
    }
  };

  const getCurrentSection = () => {
    if (!currentPage) return null;
    return getSectionByPageNumber(currentPageIndex + 1); // Convert 0-based to 1-based
  };

  const getAccessibleSections = () => {
    return BOOK_SECTIONS; // Return all sections - all are now accessible
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
        currentRotation,
        furthestPageIndex,
        setCurrentPageIndex,
        navigateToSymbol,
        nextPage,
        previousPage,
        getPagesBySymbol,
        getAllSymbols,
        
        // Section Navigation Functions
        navigateToSection,
        getCurrentSection,
        getAccessibleSections,
        
        // Mycelial Network Functions
        rotateSymbol,
        createBranch,
        navigateToBranch,
        getBranchTree,
        getCurrentPrompts
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