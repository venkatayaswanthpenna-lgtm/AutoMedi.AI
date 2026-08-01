'use client';

import React, { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import { Card } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { motion } from 'framer-motion';
import { AlertTriangle, CheckCircle, Clock, Search, Download, DollarSign } from 'lucide-react';
import { ChatBot } from '@/components/ui/ChatBot';

export default function InspectionDetailPage() {
  const { id } = useParams();
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let interval: NodeJS.Timeout;
    
    const fetchResults = async () => {
      try {
        const token = localStorage.getItem('token');
        const res = await fetch(`http://localhost:8000/api/v1/inspections/${id}/results`, {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        if (res.ok) {
          const result = await res.json();
          setData(result);
          if (result.status === 'completed') {
            setLoading(false);
            if (interval) clearInterval(interval);
          }
        }
      } catch (err) {
        console.error(err);
      }
    };

    fetchResults();
    interval = setInterval(fetchResults, 3000); // Poll every 3 seconds
    
    return () => clearInterval(interval);
  }, [id]);

  const handleDownloadPDF = async () => {
    try {
      const token = localStorage.getItem('token');
      const res = await fetch(`http://localhost:8000/api/v1/reports/${id}/report/pdf`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (!res.ok) throw new Error('PDF Generation failed');
      
      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `AutoRepair_Report_${id}.pdf`;
      document.body.appendChild(a);
      a.click();
      a.remove();
    } catch (err) {
      console.error(err);
      alert('Failed to download PDF');
    }
  };

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'Critical': return '#ff4d4d';
      case 'High': return '#ff9900';
      case 'Medium': return '#ffcc00';
      case 'Low': return '#00cc66';
      default: return 'white';
    }
  };

  if (loading || !data) {
    return (
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', minHeight: '60vh', gap: '1rem' }}>
        <motion.div 
          animate={{ rotate: 360 }} 
          transition={{ repeat: Infinity, duration: 2, ease: "linear" }}
        >
          <Search size={48} color="var(--color-primary)" />
        </motion.div>
        <h2 style={{ color: 'var(--color-primary)' }}>AI is Analyzing Inspection #{id}...</h2>
        <p style={{ color: 'var(--color-text-muted)' }}>Detecting scratches, dents, and structural damages.</p>
      </div>
    );
  }

  return (
    <div style={{ maxWidth: '1000px', margin: '0 auto' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
        <div>
          <h1 style={{ fontSize: '2rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            Inspection #{id} Results
            {data.status === 'completed' && <CheckCircle color="var(--color-secondary)" />}
          </h1>
          <p style={{ color: 'var(--color-text-muted)' }}>AI Confidence Score is aggregated across detections.</p>
        </div>
        {data.status === 'completed' && (
          <Button variant="secondary" onClick={handleDownloadPDF} style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Download size={18} /> Generate PDF Report
          </Button>
        )}
      </div>

      {data.cost && (
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} style={{ marginBottom: '2rem' }}>
          <Card style={{ background: 'linear-gradient(135deg, rgba(255,107,0,0.1) 0%, rgba(0,0,0,0) 100%)', border: '1px solid rgba(255,107,0,0.3)' }}>
            <h2 style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1rem', color: 'var(--color-primary)' }}>
              <DollarSign /> Estimated Repair Cost
            </h2>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem' }}>
              <div>
                <p style={{ color: 'var(--color-text-muted)', fontSize: '0.875rem' }}>Parts Cost</p>
                <p style={{ fontSize: '1.25rem', fontWeight: 'bold' }}>${data.cost.parts_cost_min} - ${data.cost.parts_cost_max}</p>
              </div>
              <div>
                <p style={{ color: 'var(--color-text-muted)', fontSize: '0.875rem' }}>Labor Cost</p>
                <p style={{ fontSize: '1.25rem', fontWeight: 'bold' }}>${data.cost.labor_cost_min} - ${data.cost.labor_cost_max}</p>
              </div>
              <div>
                <p style={{ color: 'var(--color-text-muted)', fontSize: '0.875rem' }}>Paint & Supplies</p>
                <p style={{ fontSize: '1.25rem', fontWeight: 'bold' }}>${data.cost.paint_cost_min} - ${data.cost.paint_cost_max}</p>
              </div>
              <div style={{ borderLeft: '1px solid var(--color-border)', paddingLeft: '1rem' }}>
                <p style={{ color: 'var(--color-text-muted)', fontSize: '0.875rem' }}>Total Estimate</p>
                <p style={{ fontSize: '1.5rem', fontWeight: 'bold', color: 'white' }}>${data.cost.total_cost_min} - ${data.cost.total_cost_max}</p>
              </div>
            </div>
          </Card>
        </motion.div>
      )}

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: '1.5rem' }}>
        {data.damages && data.damages.length > 0 ? (
          data.damages.map((damage: any, idx: number) => (
            <motion.div 
              key={damage.id} 
              initial={{ opacity: 0, y: 20 }} 
              animate={{ opacity: 1, y: 0 }} 
              transition={{ delay: idx * 0.1 }}
            >
              <Card>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '1rem' }}>
                  <h3 style={{ fontSize: '1.25rem', color: 'var(--color-primary)' }}>{damage.part_name}</h3>
                  <span style={{ 
                    background: 'rgba(255,255,255,0.1)', 
                    padding: '4px 8px', 
                    borderRadius: '4px', 
                    fontSize: '0.75rem',
                    color: getSeverityColor(damage.severity)
                  }}>
                    {damage.severity}
                  </span>
                </div>
                
                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', marginBottom: '1.5rem' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                    <span style={{ color: 'var(--color-text-muted)' }}>Damage Type</span>
                    <span>{damage.damage_type}</span>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                    <span style={{ color: 'var(--color-text-muted)' }}>AI Confidence</span>
                    <span>{(damage.confidence_score * 100).toFixed(0)}%</span>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                    <span style={{ color: 'var(--color-text-muted)' }}>Action</span>
                    <span style={{ fontWeight: 'bold' }}>{damage.repairability}</span>
                  </div>
                </div>

                {damage.severity === 'Critical' && (
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#ff4d4d', fontSize: '0.875rem' }}>
                    <AlertTriangle size={16} /> Immediate Attention Required
                  </div>
                )}
              </Card>
            </motion.div>
          ))
        ) : (
          <Card style={{ gridColumn: '1 / -1', textAlign: 'center', padding: '3rem' }}>
            <CheckCircle size={48} color="var(--color-secondary)" style={{ margin: '0 auto 1rem auto' }} />
            <h3>No Damages Detected</h3>
            <p style={{ color: 'var(--color-text-muted)' }}>The AI could not identify any significant damage on this vehicle.</p>
          </Card>
        )}
      </div>

      {data.status === 'completed' && <ChatBot inspectionId={id as string} />}
    </div>
  );
}
