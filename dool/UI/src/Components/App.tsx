import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Listjob from './Listjob'; // Adjust the path as necessary
import Listjobview from './Listjobview'; // The component you want to navigate to
import "../App.css"

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Listjob/>} />
        <Route path="/ListView" element={<Listjobview />} />
      </Routes>
    </Router>
  );
}

export default App;
