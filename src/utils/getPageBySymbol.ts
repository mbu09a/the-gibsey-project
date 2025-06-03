import { StoryPage } from '../types/story';

/**
 * Utility function to find a story page by its symbol
 * @param pages - Array of story pages
 * @param symbol - The symbol to search for
 * @returns The matching page or null if not found
 */
export const getPageBySymbol = (
  pages: StoryPage[], 
  symbol: string
): StoryPage | null => {
  return pages.find(page => 
    (page.symbol?.toLowerCase() === symbol.toLowerCase()) ||
    (page.symbolId?.toLowerCase() === symbol.toLowerCase())
  ) || null;
};

/**
 * Get all pages with a specific symbol
 * @param pages - Array of story pages
 * @param symbol - The symbol to filter by
 * @returns Array of matching pages
 */
export const getPagesBySymbol = (
  pages: StoryPage[], 
  symbol: string
): StoryPage[] => {
  return pages.filter(page => 
    (page.symbol?.toLowerCase() === symbol.toLowerCase()) ||
    (page.symbolId?.toLowerCase() === symbol.toLowerCase())
  );
};

/**
 * Get all unique symbols from pages
 * @param pages - Array of story pages
 * @returns Array of unique symbols
 */
export const getUniqueSymbols = (pages: StoryPage[]): string[] => {
  const symbols = pages.map(page => page.symbolId || page.symbol).filter((s): s is string => Boolean(s));
  return Array.from(new Set(symbols));
};

/**
 * Get page by symbol ID specifically
 * @param pages - Array of story pages
 * @param symbolId - The symbol ID to search for
 * @returns The matching page or null if not found
 */
export const getPageBySymbolId = (
  pages: StoryPage[], 
  symbolId: string
): StoryPage | null => {
  return pages.find(page => 
    page.symbolId?.toLowerCase() === symbolId.toLowerCase()
  ) || null;
};