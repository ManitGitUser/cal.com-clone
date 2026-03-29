import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import EventList from './components/EventList.jsx';
import BookingPage from './components/BookingPage.jsx';
import { Calendar } from 'lucide-react';

function App() {
  return (
    <Router>
      <header className="app-header">
        <Link to="/" style={{ textDecoration: 'none' }}>
          <div className="brand-title">
            <span style={{background:'var(--accent)', color:'var(--text-inverse)', padding:'4px', borderRadius:'4px', display:'flex', alignItems:'center'}}>
              <Calendar size={20} />
            </span>
            Booking Platform
          </div>
        </Link>
      </header>

      <main>
        <Routes>
          <Route path="/" element={<EventList />} />
          <Route path="/book/:id" element={<BookingPage />} />
        </Routes>
      </main>
    </Router>
  );
}

export default App;
