'use client';

import React, { useState, useEffect } from 'react';
import { Card } from '@/components/ui/Card';
import { Users, Activity, Wrench, DollarSign, BarChart2 } from 'lucide-react';
import { motion } from 'framer-motion';

export default function AdminDashboardPage() {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAnalytics();
  }, []);

  const fetchAnalytics = async () => {
    try {
      const token = localStorage.getItem('token');
      const res = await fetch(`http://localhost:8000/api/v1/admin/analytics`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (res.ok) {
        setData(await res.json());
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const MetricCard = ({ title, value, icon, delay, color }: any) => (
    <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay }}>
      <Card style={{ display: 'flex', alignItems: 'center', gap: '1.5rem', background: `linear-gradient(135deg, ${color}22 0%, rgba(0,0,0,0) 100%)`, border: `1px solid ${color}44` }}>
        <div style={{ background: `${color}33`, padding: '1rem', borderRadius: '12px', color: color }}>
          {icon}
        </div>
        <div>
          <p style={{ color: 'var(--color-text-muted)', fontSize: '0.875rem', marginBottom: '0.25rem' }}>{title}</p>
          <h2 style={{ fontSize: '2rem', color: 'white' }}>{value}</h2>
        </div>
      </Card>
    </motion.div>
  );

  return (
    <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
      <div style={{ marginBottom: '2rem' }}>
        <h1 style={{ fontSize: '2rem', marginBottom: '0.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <BarChart2 color="var(--color-primary)" /> Platform Analytics Overview
        </h1>
        <p style={{ color: 'var(--color-text-muted)' }}>God-mode view of all system operations, AI usage, and network health.</p>
      </div>

      {loading || !data ? (
        <p>Loading analytics...</p>
      ) : (
        <>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '1.5rem', marginBottom: '3rem' }}>
            <MetricCard 
              title="Total Registered Users" 
              value={data.metrics.total_users} 
              icon={<Users size={32} />} 
              delay={0}
              color="#0088ff"
            />
            <MetricCard 
              title="AI Inspections Processed" 
              value={data.metrics.total_inspections} 
              icon={<Activity size={32} />} 
              delay={0.1}
              color="#ff6b00"
            />
            <MetricCard 
              title="Total Garage Bookings" 
              value={data.metrics.total_bookings} 
              icon={<Wrench size={32} />} 
              delay={0.2}
              color="#00cc66"
            />
            <MetricCard 
              title="Avg. Repair Estimate" 
              value={`$${data.metrics.average_repair_estimate.toLocaleString()}`} 
              icon={<DollarSign size={32} />} 
              delay={0.3}
              color="#ffcc00"
            />
          </div>

          <h2 style={{ fontSize: '1.5rem', marginBottom: '1rem' }}>Recent AI Inferences</h2>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            {data.recent_inspections.length === 0 ? (
              <Card style={{ color: 'var(--color-text-muted)', textAlign: 'center' }}>No recent activity.</Card>
            ) : (
              data.recent_inspections.map((insp: any, idx: number) => (
                <motion.div key={insp.id} initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.4 + (idx * 0.1) }}>
                  <Card style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <div>
                      <h4 style={{ fontSize: '1.1rem' }}>Inspection #{insp.id}</h4>
                      <p style={{ color: 'var(--color-text-muted)', fontSize: '0.875rem' }}>Vehicle ID: {insp.vehicle_id}</p>
                    </div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '2rem' }}>
                      <span style={{ color: 'var(--color-text-muted)', fontSize: '0.875rem' }}>
                        {new Date(insp.created_at).toLocaleString()}
                      </span>
                      <span style={{ background: 'rgba(255,255,255,0.1)', padding: '4px 12px', borderRadius: '16px', fontSize: '0.875rem', color: insp.status === 'completed' ? '#00cc66' : '#ff9900' }}>
                        {insp.status.toUpperCase()}
                      </span>
                    </div>
                  </Card>
                </motion.div>
              ))
            )}
          </div>
        </>
      )}
    </div>
  );
}
