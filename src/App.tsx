import { StoryProvider } from './context/StoryContext';
import HomePage from './pages';
import './styles/globals.css';

function App() {
  return (
    <StoryProvider>
      <HomePage />
    </StoryProvider>
  );
}

export default App;