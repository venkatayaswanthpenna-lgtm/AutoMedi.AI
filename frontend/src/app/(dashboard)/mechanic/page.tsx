'use client';

import React, { useState, useEffect } from 'react';
import { Card } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Wrench, Clock, CheckCircle, Calendar } from 'lucide-react';
import { motion } from 'framer-motion';

export default function MechanicDashboardPage() {
  const [bookings, setBookings] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchBookings();
  }, []);

  const fetchBookings = async () => {
    try {
      const token = localStorage.getItem('token');
      const res = await fetch(`http://localhost:8000/api/v1/mechanics/bookings`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (res.ok) {
        setBookings(await res.json());
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const updateStatus = async (id: number, status: string) => {
    try {
      const token = localStorage.getItem('token');
      const res = await fetch(`http://localhost:8000/api/v1/mechanics/bookings/${id}/status?status=${status}`, {
        method: 'PUT',
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (res.ok) {
        fetchBookings();
      }
    } catch (err) {
      console.error(err);
    }
  };

  const pendingBookings = bookings.filter(b => b.status === 'pending');
  const confirmedBookings = bookings.filter(b => b.status === 'confirmed');
  const completedBookings = bookings.filter(b => b.status === 'completed');

  const KanbanColumn = ({ title, icon, color, data, actionLabel, onAction }: any) => (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
      <h3 style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: color, fontSize: '1.25rem', marginBottom: '0.5rem' }}>
        {icon} {title} ({data.length})
      </h3>
      {data.length === 0 ? (
        <Card style={{ textAlign: 'center', color: 'var(--color-text-muted)' }}>No records</Card>
      ) : (
        data.map((b: any, idx: number) => (
          <motion.div key={b.id} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: idx * 0.1 }}>
            <Card>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '1rem' }}>
                <div>
                  <h4 style={{ fontSize: '1.1rem', marginBottom: '0.25rem' }}>Booking #{b.id}</h4>
                  <p style={{ color: 'var(--color-text-muted)', fontSize: '0.875rem' }}>User ID: {b.user_id}</p>
                </div>
                <span style={{ background: 'rgba(255,255,255,0.1)', padding: '4px 8px', borderRadius: '4px', fontSize: '0.75rem', color: color }}>
                  {b.status.toUpperCase()}
                </span>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--color-text-muted)', fontSize: '0.875rem', marginBottom: '1.5rem' }}>
                <Calendar size={16} /> {new Date(b.appointment_time).toLocaleString()}
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                {b.inspection_id && (
                  <Button variant="outline" onClick={() => window.open(`/inspections/${b.inspection_id}`, '_blank')} style={{ padding: '0.5rem 1rem' }}>
                    View AI Report
                  </Button>
                )}
                {actionLabel && (
                  <Button variant="primary" onClick={() => onAction(b.id)} style={{ padding: '0.5rem 1rem' }}>
                    {actionLabel}
                  </Button>
                )}
              </div>
            </Card>
          </motion.div>
        ))
      )}
    </div>
  );

  return (
    <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
      <div style={{ marginBottom: '2rem' }}>
        <h1 style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>Mechanic Dashboard</h1>
        <p style={{ color: 'var(--color-text-muted)' }}>Manage incoming repair requests and view AI Damage Reports before the car arrives.</p>
      </div>

      {loading ? (
        <p>Loading bookings...</p>
      ) : (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '2rem' }}>
          
          <KanbanColumn 
            title="Pending Requests" 
            icon={<Clock />} 
            color="#ff9900" 
            data={pendingBookings} 
            actionLabel="Confirm Appointment"
            onAction={(id: number) => updateStatus(id, 'confirmed')}
          />
          
          <KanbanColumn 
            title="Confirmed / In Shop" 
            icon={<Wrench />} 
            color="var(--color-secondary)" 
            data={confirmedBookings} 
            actionLabel="Mark Completed"
            onAction={(id: number) => updateStatus(id, 'completed')}
          />

          <KanbanColumn 
            title="Completed" 
            icon={<CheckCircle />} 
            color="#00cc66" 
            data={completedBookings} 
            actionLabel={null}
            onAction={null}
          />
          
        </div>
      )}
    </div>
  );
}
