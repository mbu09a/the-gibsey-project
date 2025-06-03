import { useState, useEffect } from 'react';

interface UseTypewriterOptions {
  speed?: number;
  delay?: number;
  onComplete?: () => void;
}

export const useTypewriter = (
  text: string,
  options: UseTypewriterOptions = {}
) => {
  const { speed = 30, delay = 0, onComplete } = options;
  const [displayedText, setDisplayedText] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [isComplete, setIsComplete] = useState(false);

  useEffect(() => {
    // Immediately reset state for smooth transitions
    setDisplayedText('');
    setIsTyping(false);
    setIsComplete(false);

    let timeoutId: NodeJS.Timeout;
    let intervalId: NodeJS.Timeout;

    const startTimer = setTimeout(() => {
      setIsTyping(true);
      let currentIndex = 0;

      const typeInterval = setInterval(() => {
        if (currentIndex < text.length) {
          setDisplayedText(text.slice(0, currentIndex + 1));
          currentIndex++;
        } else {
          clearInterval(typeInterval);
          setIsTyping(false);
          setIsComplete(true);
          onComplete?.();
        }
      }, speed);

      intervalId = typeInterval;
    }, delay);

    timeoutId = startTimer;

    // Cleanup function to prevent memory leaks and smooth transitions
    return () => {
      clearTimeout(timeoutId);
      clearInterval(intervalId);
    };
  }, [text, speed, delay, onComplete]);

  return { displayedText, isTyping, isComplete };
};