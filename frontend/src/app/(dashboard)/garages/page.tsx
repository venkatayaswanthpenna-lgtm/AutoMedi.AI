'use client';

import React, { useState, useEffect } from 'react';
import { Card } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { MapPin, Star, Phone, Calendar } from 'lucide-react';
import { motion } from 'framer-motion';
import dynamic from 'next/dynamic';

// Dynamically import Map component with SSR disabled because Leaflet uses window
const DynamicMap = dynamic(() => import('@/components/Map'), { 
  ssr: false,
  loading: () => <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%' }}>Loading Map...</div>
});

export default function GarageDiscoveryPage() {
  const [garages, setGarages] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedGarage, setSelectedGarage] = useState<any>(null);

  useEffect(() => {
    fetchGarages();
  }, []);

  const fetchGarages = async () => {
    try {
      const token = localStorage.getItem('token');
      // Using mock coordinates for San Francisco
      const res = await fetch(`http://localhost:8000/api/v1/garages/?lat=37.7749&lng=-122.4194`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (res.ok) {
        setGarages(await res.json());
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleBook = async (garage: any) => {
    try {
      const token = localStorage.getItem('token');
      const payload = {
        garage_id: garage.id,
        appointment_time: new Date(Date.now() + 86400000).toISOString(), // Tomorrow
      };
      const res = await fetch(`http://localhost:8000/api/v1/garages/bookings`, {
        method: 'POST',
        headers: { 
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
      });
      
      if (res.ok) {
        alert('Booking Confirmed for Tomorrow!');
      } else {
        alert('Failed to book appointment');
      }
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
      <div style={{ marginBottom: '2rem' }}>
        <h1 style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>Garage Discovery</h1>
        <p style={{ color: 'var(--color-text-muted)' }}>Find and book top-rated mechanics near you based on your location.</p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 2fr', gap: '2rem' }}>
        
        {/* List of Garages */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', height: '70vh', overflowY: 'auto', paddingRight: '1rem' }}>
          {loading ? (
            <p>Loading nearby garages...</p>
          ) : (
            garages.map((g, idx) => (
              <motion.div 
                key={g.id} 
                initial={{ opacity: 0, x: -20 }} 
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: idx * 0.1 }}
                onClick={() => setSelectedGarage(g)}
              >
                <Card interactive style={{ 
                  cursor: 'pointer', 
                  border: selectedGarage?.id === g.id ? '2px solid var(--color-primary)' : '1px solid var(--color-border)' 
                }}>
                  <h3 style={{ fontSize: '1.25rem', marginBottom: '0.5rem' }}>{g.name}</h3>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--color-text-muted)', fontSize: '0.875rem', marginBottom: '0.25rem' }}>
                    <MapPin size={16} /> {g.address}
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '1rem' }}>
                    <span style={{ display: 'flex', alignItems: 'center', gap: '0.25rem', color: '#ffcc00' }}>
                      <Star size={16} fill="#ffcc00" /> {g.rating}
                    </span>
                    <Button variant="outline" onClick={(e) => { e.stopPropagation(); handleBook(g); }}>
                      <Calendar size={16} style={{ marginRight: '0.5rem' }}/> Book Now
                    </Button>
                  </div>
                </Card>
              </motion.div>
            ))
          )}
        </div>

        {/* Interactive Map Area */}
        <div style={{ 
          background: 'var(--color-surface)', 
          borderRadius: '16px', 
          border: '1px solid var(--color-border)', 
          position: 'relative',
          overflow: 'hidden',
          minHeight: '500px'
        }}>
          <DynamicMap 
            garages={garages}
            selectedGarage={selectedGarage}
            onGarageSelect={setSelectedGarage}
          />
          
          {/* Overlay for quick action when garage is selected via map click */}
          {selectedGarage && (
            <div style={{
              position: 'absolute',
              bottom: '20px',
              left: '50%',
              transform: 'translateX(-50%)',
              background: 'var(--color-surface)',
              padding: '1rem',
              borderRadius: '8px',
              border: '1px solid var(--color-border)',
              zIndex: 1000,
              display: 'flex',
              alignItems: 'center',
              gap: '1rem',
              boxShadow: '0 4px 6px rgba(0,0,0,0.3)'
            }}>
              <div>
                <h4 style={{ margin: '0 0 0.25rem 0' }}>{selectedGarage.name}</h4>
                <div style={{ fontSize: '0.875rem', color: 'var(--color-text-muted)' }}><Phone size={12} style={{ verticalAlign: 'middle' }}/> {selectedGarage.phone}</div>
              </div>
              <Button size="sm" onClick={() => handleBook(selectedGarage)}>Book Now</Button>
            </div>
          )}
        </div>

      </div>
    </div>
  );
}
