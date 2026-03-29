import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Clock } from 'lucide-react';

export default function EventList() {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    fetch('http://localhost:8000/event-types/')
      .then((res) => res.json())
      .then((data) => {
        setEvents(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error('Error fetching events:', err);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <p className="text-center">Loading available events...</p>;
  }

  // Fallback state for local dev
  if (events.length === 0) {
    return (
      <div className="card" style={{padding:'2rem', textAlign:'center'}}>
        <h2>No Events Configured Base</h2>
        <p>Please use Swagger UI (http://localhost:8000/docs) to seed Event Types.</p>
      </div>
    );
  }

  return (
    <>
      <h1 style={{ textAlign: 'left', marginBottom: '1.5rem' }}>Select an Event</h1>
      <div className="event-grid">
        {events.map((event) => (
          <div 
            key={event.id} 
            className="card event-card"
            onClick={() => navigate(`/book/${event.id}`, { state: { eventType: event } })}
          >
            <h3 className="event-title">{event.name}</h3>
            <div className="flex-between mt-4">
              <span style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', color: 'var(--text-muted)' }}>
                <Clock size={16} color="var(--accent)" />
                {event.duration} minutes
              </span>
              <button className="btn">Book Now</button>
            </div>
          </div>
        ))}
      </div>
    </>
  );
}
