export interface Section {
  id: string;
  name: string;
  description: string;
  pages: string[];
  unlocked: boolean;
  order: number;
}

export interface SectionTree {
  sections: Section[];
  currentSection: string;
  furthestUnlocked: number;
}