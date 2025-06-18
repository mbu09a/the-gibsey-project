// Section structure for The Wonderful Worlds of Gibsey
export interface BookSection {
  id: number;
  title: string;
  character: string;
  symbolId: string;
  startPage: number;
  endPage: number;
  totalPages: number;
  chapters?: BookChapter[];
}

export interface BookChapter {
  id: string;
  title: string;
  startPage: number;
  endPage: number;
  totalPages: number;
}

export const BOOK_SECTIONS: BookSection[] = [
  {
    id: 1,
    title: "An Author's Preface",
    character: "An Author",
    symbolId: "an-author",
    startPage: 1,
    endPage: 8,
    totalPages: 8
  },
  {
    id: 2,
    title: "London Fox Who Vertically Disintegrates",
    character: "London Fox",
    symbolId: "london-fox",
    startPage: 9,
    endPage: 24,
    totalPages: 16
  },
  {
    id: 3,
    title: "An Unexpected Disappearance: A Glyph Marrow Mystery",
    character: "Glyph Marrow",
    symbolId: "glyph-marrow",
    startPage: 25,
    endPage: 203,
    totalPages: 179,
    chapters: [
      { id: "3-1", title: "Chapter 1: The Queue and Station", startPage: 25, endPage: 57, totalPages: 33 },
      { id: "3-2", title: "Chapter 2: The Tunnel", startPage: 58, endPage: 74, totalPages: 17 },
      { id: "3-3", title: "Chapter 3: The First Ascent", startPage: 75, endPage: 109, totalPages: 35 },
      { id: "3-4", title: "Chapter 4: The Flooded Town", startPage: 110, endPage: 141, totalPages: 32 },
      { id: "3-5", title: "Chapter 5: The Waterfall", startPage: 142, endPage: 176, totalPages: 35 },
      { id: "3-6", title: "Chapter 6: The Tunneled Vision", startPage: 177, endPage: 203, totalPages: 27 }
    ]
  },
  {
    id: 4,
    title: "An Expected Appearance: A Phillip Bafflemint Noir",
    character: "Phillip Bafflemint",
    symbolId: "phillip-bafflemint",
    startPage: 204,
    endPage: 235,
    totalPages: 32,
    chapters: [
      { id: "4-1", title: "Chapter 1: The Tunneled Vision", startPage: 204, endPage: 217, totalPages: 14 },
      { id: "4-2", title: "Chapter 2: The Flooded House", startPage: 218, endPage: 228, totalPages: 11 },
      { id: "4-3", title: "Chapter 3: The First Descent", startPage: 229, endPage: 235, totalPages: 7 }
    ]
  },
  {
    id: 5,
    title: "Jacklyn Variance, The Watcher, is Watched",
    character: "Jacklyn Variance",
    symbolId: "jacklyn-variance",
    startPage: 236,
    endPage: 307,
    totalPages: 72,
    chapters: [
      { id: "5-1", title: "Part 1", startPage: 236, endPage: 242, totalPages: 7 },
      { id: "5-2", title: "Part 2", startPage: 243, endPage: 271, totalPages: 29 },
      { id: "5-3", title: "Part 3", startPage: 272, endPage: 273, totalPages: 2 },
      { id: "5-4", title: "Part 4", startPage: 274, endPage: 307, totalPages: 34 }
    ]
  },
  {
    id: 6,
    title: "The Last Auteur",
    character: "Oren Progresso",
    symbolId: "oren-progresso",
    startPage: 308,
    endPage: 354,
    totalPages: 47
  },
  {
    id: 7,
    title: "Gibseyan Mysticism and its Symbolism",
    character: "Old Natalie Weissman",
    symbolId: "old-natalie",
    startPage: 355,
    endPage: 380,
    totalPages: 26
  },
  {
    id: 8,
    title: "Princhetta Who Thinks Herself Alive",
    character: "Princhetta",
    symbolId: "princhetta",
    startPage: 381,
    endPage: 385,
    totalPages: 5
  },
  {
    id: 9,
    title: "Petition for Bankruptcy- Chapter 11, by Perdition Books, a Subsidiary of Skingraft Publishing",
    character: "Cop-E-Right",
    symbolId: "cop-e-right",
    startPage: 386,
    endPage: 411,
    totalPages: 26
  },
  {
    id: 10,
    title: "The Tempestuous Storm",
    character: "New Natalie Weissman",
    symbolId: "new-natalie",
    startPage: 412,
    endPage: 432,
    totalPages: 21
  },
  {
    id: 11,
    title: "Arieol Owlist Who Wants to Achieve Agency",
    character: "Arieol Owlist",
    symbolId: "arieol-owlist",
    startPage: 433,
    endPage: 487,
    totalPages: 55,
    chapters: [
      { id: "11-1", title: "Part 1", startPage: 433, endPage: 444, totalPages: 12 },
      { id: "11-2", title: "Part 2", startPage: 445, endPage: 461, totalPages: 17 },
      { id: "11-3", title: "Part 3", startPage: 462, endPage: 487, totalPages: 26 }
    ]
  },
  {
    id: 12,
    title: "The Biggest Shit of All Time",
    character: "Jack Parlance",
    symbolId: "jack-parlance",
    startPage: 488,
    endPage: 500,
    totalPages: 13
  },
  {
    id: 13,
    title: "An Expected Appearance: A Phillip Bafflemint Noir - Chapters 4-6",
    character: "Manny Valentinas",
    symbolId: "manny-valentinas",
    startPage: 501,
    endPage: 564,
    totalPages: 64,
    chapters: [
      { id: "13-1", title: "Chapter 4: The Slip and The Mistake", startPage: 501, endPage: 526, totalPages: 26 },
      { id: "13-2", title: "Chapter 5: The Stations", startPage: 527, endPage: 545, totalPages: 19 },
      { id: "13-3", title: "Chapter 6: The Second Descent", startPage: 546, endPage: 564, totalPages: 19 }
    ]
  },
  {
    id: 14,
    title: "An Unexpected Disappearance: A Glyph Marrow Mystery - Chapters 7-11",
    character: "Shamrock Stillman",
    symbolId: "shamrock-stillman",
    startPage: 565,
    endPage: 641,
    totalPages: 77,
    chapters: [
      { id: "14-1", title: "Chapter 7: The Rainbows", startPage: 565, endPage: 584, totalPages: 20 },
      { id: "14-2", title: "Chapter 8: The Caves", startPage: 585, endPage: 603, totalPages: 19 },
      { id: "14-3", title: "Chapter 9: The Third Ascent", startPage: 604, endPage: 611, totalPages: 8 },
      { id: "14-4", title: "Chapter 10: The Geyser", startPage: 612, endPage: 623, totalPages: 12 },
      { id: "14-5", title: "Chapter 11: The Return to the Station", startPage: 624, endPage: 641, totalPages: 18 }
    ]
  },
  {
    id: 15,
    title: "Todd Fishbone Who Dreams of Synchronistic Extraction",
    character: "Todd Fishbone",
    symbolId: "todd-fishbone",
    startPage: 642,
    endPage: 677,
    totalPages: 36
  },
  {
    id: 16,
    title: "The Author's Preface",
    character: "The Author",
    symbolId: "the-author",
    startPage: 678,
    endPage: 710,
    totalPages: 33
  }
];

// Helper functions
export function getSectionByPageNumber(pageNumber: number): BookSection | null {
  return BOOK_SECTIONS.find(section => 
    pageNumber >= section.startPage && pageNumber <= section.endPage
  ) || null;
}

export function getAccessedSections(furthestPageReached: number): BookSection[] {
  return BOOK_SECTIONS.filter(section => furthestPageReached >= section.startPage);
}

export function getTotalPagesInAccessedSections(furthestPageReached: number): number {
  const accessedSections = getAccessedSections(furthestPageReached);
  return accessedSections.reduce((total, section) => {
    const pagesInSection = Math.min(furthestPageReached, section.endPage) - section.startPage + 1;
    return total + Math.max(0, pagesInSection);
  }, 0);
}

export function getGlobalPageIndex(sectionId: number, localPageIndex: number): number {
  const section = BOOK_SECTIONS.find(s => s.id === sectionId);
  if (!section) return 0;
  return section.startPage - 1 + localPageIndex; // Convert to 0-based index
}