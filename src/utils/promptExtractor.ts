import { Prompt, PromptType } from '../types/story';

export function extractPrompts(text: string, symbolId: string): Prompt[] {
  // Basic prompt extraction logic
  const prompts: Prompt[] = [];
  
  // Extract character prompts (placeholder implementation)
  const characterPromptRegex = /\[CHARACTER\](.*?)\[\/CHARACTER\]/g;
  let match;
  
  while ((match = characterPromptRegex.exec(text)) !== null) {
    prompts.push({
      id: `${symbolId}-${prompts.length}`,
      type: PromptType.CHARACTER,
      text: match[1].trim(),
      symbolId
    });
  }
  
  return prompts;
}

export function createPrompt(text: string, type: PromptType, symbolId: string): Prompt {
  return {
    id: `${symbolId}-${Date.now()}`,
    type,
    text,
    symbolId
  };
}