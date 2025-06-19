export interface StoryPage {
  id: string;
  symbol?: string;
  symbolId: string;
  title: string;
  text: string;
  content?: string;
  section?: number;
  pageIndex?: number;
  color?: string;
  createdAt?: Date;
  updatedAt?: Date;
  metadata?: Record<string, any>;
  rotation?: SymbolRotation;
  pageType?: string;
  author?: string;
  parentId?: string;
}

export enum SymbolRotation {
  ZERO = 0,
  NINETY = 90,
  ONE_EIGHTY = 180,
  TWO_SEVENTY = 270
}

export interface Prompt {
  id: string;
  type: PromptType;
  text: string;
  symbolId: string;
}

export enum PromptType {
  CHARACTER = "character",
  USER = "user", 
  SYSTEM = "system"
}

export interface StorySymbol {
  symbol: string;
  name: string;
  description?: string;
  color: string;
}