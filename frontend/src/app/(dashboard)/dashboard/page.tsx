'use client';

import React, { useEffect, useState } from 'react';
import { Card } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { FilePlus, History, Settings } from 'lucide-react';
import { motion } from 'framer-motion';
import Link from 'next/link';

export default function DashboardPage() {
  const [user, setUser] = useState<any>(null);

  useEffect(() => {
    const stored = localStorage.getItem('user');
    if (stored) {
      setUser(JSON.parse(stored));
    }
  }, []);

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: { 
      opacity: 1,
      transition: { staggerChildren: 0.1 }
    }
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { opacity: 1, y: 0 }
  };

  return (
    <motion.div 
      initial="hidden" 
      animate="visible" 
      variants={containerVariants}
    >
      <motion.h1 variants={itemVariants} style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>
        Welcome back, {user?.full_name || 'Driver'}!
      </motion.h1>
      <motion.p variants={itemVariants} style={{ color: 'var(--color-text-muted)', marginBottom: '2rem' }}>
        Here is your vehicle repair overview.
      </motion.p>

      <motion.div variants={itemVariants} style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '1.5rem', marginBottom: '2rem' }}>
        <Card interactive>
          <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '1rem' }}>
            <div style={{ padding: '12px', background: 'rgba(255, 107, 0, 0.1)', borderRadius: '12px', color: 'var(--color-primary)' }}>
              <FilePlus size={24} />
            </div>
            <h3 style={{ fontSize: '1.25rem' }}>New Inspection</h3>
          </div>
          <p style={{ color: 'var(--color-text-muted)', marginBottom: '1.5rem' }}>
            Upload images or a video of your vehicle damage to get an instant AI repair estimate.
          </p>
          <Link href="/inspections/new">
            <Button variant="primary" style={{ width: '100%' }}>Start Inspection</Button>
          </Link>
        </Card>

        <Card interactive>
          <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '1rem' }}>
            <div style={{ padding: '12px', background: 'rgba(0, 136, 255, 0.1)', borderRadius: '12px', color: 'var(--color-secondary)' }}>
              <History size={24} />
            </div>
            <h3 style={{ fontSize: '1.25rem' }}>Past Reports</h3>
          </div>
          <p style={{ color: 'var(--color-text-muted)', marginBottom: '1.5rem' }}>
            View your previously generated AI damage reports and mechanic estimates.
          </p>
          <Link href="/inspections/new">
            <Button variant="outline" style={{ width: '100%' }}>View History</Button>
          </Link>
        </Card>

        <Card interactive>
          <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '1rem' }}>
            <div style={{ padding: '12px', background: 'rgba(156, 163, 175, 0.1)', borderRadius: '12px', color: 'var(--color-text-muted)' }}>
              <Settings size={24} />
            </div>
            <h3 style={{ fontSize: '1.25rem' }}>Garage Discovery</h3>
          </div>
          <p style={{ color: 'var(--color-text-muted)', marginBottom: '1.5rem' }}>
            Find the best rated local mechanics around you to schedule a repair.
          </p>
          <Link href="/garages">
            <Button variant="secondary" style={{ width: '100%' }}>Find Mechanics</Button>
          </Link>
        </Card>
      </motion.div>
    </motion.div>
  );
}
