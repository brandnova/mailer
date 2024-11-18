import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import DeveloperSubscription from './components/DeveloperSubscription';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<DeveloperSubscription />} />
      </Routes>
    </Router>
  );
}

export default App;
