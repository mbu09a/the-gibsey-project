import { useState, useCallback } from 'react';

export interface QDPIResponse {
  success: boolean;
  data?: any;
  error?: string;
}

export const useQDPI = () => {
  const [isLoading, setIsLoading] = useState(false);

  const encodeToQDPI = useCallback(async (content: string): Promise<QDPIResponse> => {
    setIsLoading(true);
    try {
      const response = await fetch('http://localhost:8000/api/qdpi/encode', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ content }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return { success: true, data };
    } catch (error) {
      console.error('QDPI encode error:', error);
      return { 
        success: false, 
        error: error instanceof Error ? error.message : 'Unknown error'
      };
    } finally {
      setIsLoading(false);
    }
  }, []);

  const decodeFromQDPI = useCallback(async (glyphSequence: string): Promise<QDPIResponse> => {
    setIsLoading(true);
    try {
      const response = await fetch('http://localhost:8000/api/qdpi/decode', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ glyph_sequence: glyphSequence }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return { success: true, data };
    } catch (error) {
      console.error('QDPI decode error:', error);
      return { 
        success: false, 
        error: error instanceof Error ? error.message : 'Unknown error'
      };
    } finally {
      setIsLoading(false);
    }
  }, []);

  const executeSymbolFlow = useCallback(async (symbolName: string): Promise<QDPIResponse> => {
    setIsLoading(true);
    try {
      const response = await fetch(`http://localhost:8000/api/qdpi/execute/${symbolName}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return { success: true, data };
    } catch (error) {
      console.error('QDPI execute error:', error);
      return { 
        success: false, 
        error: error instanceof Error ? error.message : 'Unknown error'
      };
    } finally {
      setIsLoading(false);
    }
  }, []);

  return {
    encodeToQDPI,
    decodeFromQDPI,
    executeSymbolFlow,
    isLoading
  };
};