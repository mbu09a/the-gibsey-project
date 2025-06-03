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
}

export interface StorySymbol {
  symbol: string;
  name: string;
  description?: string;
  color: string;
}