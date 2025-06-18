export type SymbolRotation = 0 | 90 | 180 | 270;

export type PromptType = 'character_prompt' | 'user_prompt' | 'character_response';

export type PageType = 'primary' | 'prompt' | 'user_query' | 'ai_response';

export interface Prompt {
  id: string;
  type: PromptType;
  text: string;
  targetRotation: SymbolRotation;
  description: string;
}

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
  
  // PRD-Compliant Core Fields
  rotation: SymbolRotation;
  pageType: PageType;
  parentId?: string;
  promptType?: PromptType;
  author: string; // 'user', 'AI', 'system', character name
  branchId?: string;
  
  // Mycelial Network Extensions
  prompts: Prompt[];
  childIds: string[];
  branches: BranchNode[];
}

export interface BranchNode {
  pageId: string;
  promptUsed: string;
  createdBy: 'user' | 'ai';
  timestamp: Date;
}

export interface StorySymbol {
  symbol: string;
  name: string;
  description?: string;
  color: string;
}