import { StoryProvider } from './context/StoryContext';
import HomePage from './pages';
import { TokenizerDebug } from './components/TokenizerDebug';
import './styles/globals.css';

function App() {
  // Check if we're in debug mode
  const isDebugMode = new URLSearchParams(window.location.search).has('debug');
  
  if (isDebugMode) {
    return <TokenizerDebug />;
  }
  
  return (
    <StoryProvider>
      <HomePage />
    </StoryProvider>
  );
}

export default App;