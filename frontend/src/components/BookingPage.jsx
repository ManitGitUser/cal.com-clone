import { useState, useEffect } from 'react';
import { useParams, useLocation, useNavigate } from 'react-router-dom';
import { 
  format, startOfMonth, endOfMonth, eachDayOfInterval, 
  isSameMonth, isSameDay, addMonths, subMonths, isToday, isBefore, startOfDay 
} from 'date-fns';
import { Calendar as CalIcon, Clock, ChevronLeft, ChevronRight, Globe, CheckCircle } from 'lucide-react';

export default function BookingPage() {
  const { id } = useParams();
  const { state } = useLocation();
  const navigate = useNavigate();
  const [eventDef, setEventDef] = useState(state?.eventType || { id, name: "Loading...", duration: "-" });

  const [currentMonth, setCurrentMonth] = useState(new Date());
  const [selectedDate, setSelectedDate] = useState(null);
  const [slots, setSlots] = useState([]);
  const [loadingSlots, setLoadingSlots] = useState(false);
  const [selectedSlot, setSelectedSlot] = useState(null);
  
  // Form State
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [bookingSuccess, setBookingSuccess] = useState(false);
  const [error, setError] = useState(null);

  // Fallback fetch if navigated directly without state
  useEffect(() => {
    if (!state?.eventType) {
      fetch(`http://localhost:8000/event-types/${id}`)
        .then(res => res.json())
        .then(data => setEventDef(data))
        .catch(console.error);
    }
  }, [id, state]);

  // Fetch slots
  useEffect(() => {
    if (selectedDate) {
      setLoadingSlots(true);
      setSlots([]);
      setSelectedSlot(null);
      
      const formattedDate = format(selectedDate, 'yyyy-MM-dd');
      
      fetch(`http://localhost:8000/event-types/${id}/slots?target_date=${formattedDate}`)
        .then(res => res.json())
        .then(data => {
          setSlots(data);
          setLoadingSlots(false);
        })
        .catch(err => {
          console.error(err);
          setError("Failed to fetch slots.");
          setLoadingSlots(false);
        });
    }
  }, [selectedDate, id]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!selectedSlot || !email || !name) return;

    try {
      const res = await fetch('http://localhost:8000/bookings/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          start_time: selectedSlot.start_time,
          end_time: selectedSlot.end_time,
          attendee_email: email,
          event_type_id: parseInt(id)
        })
      });

      if (res.ok) {
        setBookingSuccess(true);
      } else {
        const d = await res.json();
        setError(d.detail || "Error creating booking");
      }
    } catch (err) {
       setError("Network error.");
    }
  };

  // Calendar Logic
  const monthStart = startOfMonth(currentMonth);
  const monthEnd = endOfMonth(monthStart);
  
  // Pad beginning of month
  const startDate = new Date(monthStart);
  startDate.setDate(startDate.getDate() - startDate.getDay());
  
  // Pad end of month
  const endDate = new Date(monthEnd);
  if (endDate.getDay() !== 6) {
    endDate.setDate(endDate.getDate() + (6 - endDate.getDay()));
  }

  const dateRange = eachDayOfInterval({ start: startDate, end: endDate });
  const weekDays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];

  if (bookingSuccess) {
    return (
      <div className="card text-center" style={{ padding: '4rem 2rem' }}>
        <CheckCircle size={64} color="var(--success)" style={{ margin: '0 auto 1.5rem auto' }} />
        <h1 style={{ marginBottom: '1rem'}}>Booking Confirmed</h1>
        <p>A calendar invitation has been sent to {email}.</p>
        <button className="btn mt-4" style={{width: 'auto'}} onClick={() => navigate('/')}>Return Home</button>
      </div>
    );
  }

  return (
    <div className="card booking-layout">
      {/* LEFT: Info */}
      <div className="booking-sidebar">
        <p className="text-muted" style={{textTransform: 'uppercase', fontSize: '0.8rem', fontWeight: 600, letterSpacing: '1px', marginBottom: '1rem'}}>Flux Capacitor</p>
        <h1 className="event-title" style={{marginBottom: '1.5rem'}}>{eventDef.name}</h1>
        
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', color: 'var(--text-muted)', fontSize: '0.95rem' }}>
          <span style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Clock size={18} /> {eventDef.duration} min
          </span>
          <span style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Globe size={18} /> UTC
          </span>
        </div>
      </div>

      {/* MIDDLE: Calendar */}
      <div className="booking-main">
        <h2 style={{ marginBottom: '1.5rem' }}>Select a Date & Time</h2>
        
        <div className="flex-between">
          <button 
            type="button" 
            style={{background:'none', border:'none', color:'var(--text-main)', cursor:'pointer'}}
            onClick={() => setCurrentMonth(subMonths(currentMonth, 1))}
          >
            <ChevronLeft size={20}/>
          </button>
          <span style={{fontWeight: 500}}>{format(currentMonth, 'MMMM yyyy')}</span>
          <button 
            type="button" 
            style={{background:'none', border:'none', color:'var(--text-main)', cursor:'pointer'}}
            onClick={() => setCurrentMonth(addMonths(currentMonth, 1))}
          >
            <ChevronRight size={20}/>
          </button>
        </div>

        <div className="calendar-grid">
          {weekDays.map(d => <div key={d} className="cal-header">{d}</div>)}
          {dateRange.map((day, i) => {
            const isSelectable = isSameMonth(day, monthStart) && !isBefore(day, startOfDay(new Date()));
            return (
              <div 
                key={i} 
                className={`cal-day 
                  ${!isSameMonth(day, monthStart) ? 'empty' : ''} 
                  ${isSelectable ? '' : 'disabled'}
                  ${selectedDate && isSameDay(day, selectedDate) ? 'selected' : ''}
                `}
                onClick={() => isSelectable ? setSelectedDate(day) : null}
              >
                {isSameMonth(day, monthStart) ? format(day, 'd') : ''}
              </div>
            )
          })}
        </div>
      </div>

      {/* RIGHT: Slots & Form */}
      {(selectedDate || selectedSlot) && (
        <div className="booking-slots">
          {!selectedSlot ? (
            <>
              <p style={{fontWeight: 500, marginBottom: '1rem'}}>
                {format(selectedDate, 'EEEE, MMMM d')}
              </p>
              
              {loadingSlots ? (
                Array.from({length: 4}).map((_,i) => <div key={i} className="skeleton" style={{height:'45px', width:'100%', marginBottom:'0.5rem'}}></div>)
              ) : slots.length === 0 ? (
                <div style={{color:'var(--text-muted)'}}>No slots available.</div>
              ) : (
                slots.map((s, i) => (
                  <button
                    key={i}
                    className="slot-btn"
                    onClick={() => setSelectedSlot(s)}
                  >
                    {format(new Date(s.start_time), 'h:mm a')}
                  </button>
                ))
              )}
            </>
          ) : (
            <>
              <div style={{display:'flex', alignItems:'center', gap:'0.5rem', marginBottom:'1.5rem'}}>
                <button type="button" onClick={() => setSelectedSlot(null)} style={{background:'none', border:'none', color:'var(--text-muted)', cursor:'pointer'}}><ChevronLeft size={20}/></button>
                <div style={{fontWeight: 600}}>
                  {format(new Date(selectedSlot.start_time), 'HH:mm')} - {format(new Date(selectedSlot.end_time), 'HH:mm')}
                </div>
              </div>
            
              <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', height: '100%', paddingBottom: '1rem'}}>
                
                {error && <div style={{ color: 'var(--danger)', marginBottom: '1rem', padding: '0.75rem', background: 'rgba(239, 68, 68, 0.1)', borderRadius: '6px', fontSize: '0.9rem' }}>{error}</div>}

                <label>Name</label>
                <input type="text" className="input-field" required value={name} onChange={e => setName(e.target.value)} />

                <label>Email</label>
                <input type="email" className="input-field" required value={email} onChange={e => setEmail(e.target.value)} />

                <div style={{flexGrow: 1}}></div>
                <button type="submit" className="btn">Confirm</button>
              </form>
            </>
          )}
        </div>
      )}
    </div>
  );
}
