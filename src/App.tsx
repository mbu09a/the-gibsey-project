import { StoryProvider } from './context/StoryContext';
import HomePage from './pages';
import { TokenizerDebug } from './components/TokenizerDebug';
import QDPIDemo from './components/QDPIDemo';
import './styles/globals.css';

function App() {
  // Check URL path for routing
  const path = window.location.pathname;
  const isDebugMode = new URLSearchParams(window.location.search).has('debug');
  
  if (isDebugMode) {
    return <TokenizerDebug />;
  }
  
  if (path === '/qdpi') {
    return <QDPIDemo />;
  }
  
  return (
    <StoryProvider>
      <HomePage />
    </StoryProvider>
  );
}

export default App;