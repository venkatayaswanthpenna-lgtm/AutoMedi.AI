'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { motion, AnimatePresence } from 'framer-motion';
import { Card } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Upload, Car, CheckCircle } from 'lucide-react';

const ANGLES = ['Front View', 'Rear View', 'Left Side', 'Right Side', '45° Front'];

export default function NewInspectionPage() {
  const [step, setStep] = useState(1);
  const [vehicleData, setVehicleData] = useState({
    company: '', model: '', year: '', vehicle_type: '', fuel_type: '', transmission: '', color: '', mileage: '', vin: ''
  });
  const [files, setFiles] = useState<{ [key: string]: File | null }>({});
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handleVehicleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setVehicleData({ ...vehicleData, [e.target.name]: e.target.value });
  };

  const handleFileChange = (angle: string, e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFiles({ ...files, [angle]: e.target.files[0] });
    }
  };

  const handleSubmit = async () => {
    setLoading(true);
    try {
      const formData = new FormData();
      Object.entries(vehicleData).forEach(([key, value]) => {
        if (value) formData.append(key, value);
      });

      ANGLES.forEach((angle) => {
        if (files[angle]) {
          formData.append('angles', angle);
          formData.append('files', files[angle] as File);
        }
      });

      const token = localStorage.getItem('token');
      const res = await fetch('http://localhost:8000/api/v1/vehicles/inspections', {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` },
        body: formData,
      });

      if (!res.ok) throw new Error('Upload failed');
      const data = await res.json();
      router.push(`/inspections/${data.id}`);
    } catch (error) {
      console.error(error);
      alert('Failed to upload inspection');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: '800px', margin: '0 auto' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '2rem' }}>
        <div style={{ flex: 1, height: '4px', background: step >= 1 ? 'var(--color-primary)' : 'var(--color-border)', borderRadius: '2px' }} />
        <div style={{ flex: 1, height: '4px', background: step >= 2 ? 'var(--color-primary)' : 'var(--color-border)', borderRadius: '2px' }} />
      </div>

      <AnimatePresence mode="wait">
        {step === 1 && (
          <motion.div key="step1" initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: 20 }}>
            <Card>
              <h2 style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1.5rem', color: 'var(--color-primary)' }}>
                <Car /> Vehicle Information
              </h2>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
                <div>
                  <label style={{ display: 'block', marginBottom: '0.5rem', color: 'var(--color-text-muted)' }}>Make/Company *</label>
                  <input name="company" required value={vehicleData.company} onChange={handleVehicleChange} style={{ width: '100%', padding: '12px', borderRadius: '8px', background: 'var(--color-background)', border: '1px solid var(--color-border)', color: 'white' }} />
                </div>
                <div>
                  <label style={{ display: 'block', marginBottom: '0.5rem', color: 'var(--color-text-muted)' }}>Model *</label>
                  <input name="model" required value={vehicleData.model} onChange={handleVehicleChange} style={{ width: '100%', padding: '12px', borderRadius: '8px', background: 'var(--color-background)', border: '1px solid var(--color-border)', color: 'white' }} />
                </div>
                <div>
                  <label style={{ display: 'block', marginBottom: '0.5rem', color: 'var(--color-text-muted)' }}>Year *</label>
                  <input type="number" name="year" required value={vehicleData.year} onChange={handleVehicleChange} style={{ width: '100%', padding: '12px', borderRadius: '8px', background: 'var(--color-background)', border: '1px solid var(--color-border)', color: 'white' }} />
                </div>
                <div>
                  <label style={{ display: 'block', marginBottom: '0.5rem', color: 'var(--color-text-muted)' }}>Vehicle Type *</label>
                  <select name="vehicle_type" value={vehicleData.vehicle_type} onChange={handleVehicleChange} style={{ width: '100%', padding: '12px', borderRadius: '8px', background: 'var(--color-background)', border: '1px solid var(--color-border)', color: 'white' }}>
                    <option value="">Select Type</option>
                    <option value="Sedan">Sedan</option>
                    <option value="SUV">SUV</option>
                    <option value="Truck">Truck</option>
                  </select>
                </div>
              </div>
              <div style={{ marginTop: '2rem', display: 'flex', justifyContent: 'flex-end' }}>
                <Button onClick={() => setStep(2)} disabled={!vehicleData.company || !vehicleData.model || !vehicleData.year || !vehicleData.vehicle_type}>
                  Next: Upload Media
                </Button>
              </div>
            </Card>
          </motion.div>
        )}

        {step === 2 && (
          <motion.div key="step2" initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: 20 }}>
            <Card>
              <h2 style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem', color: 'var(--color-primary)' }}>
                <Upload /> Multi-Angle Inspection Capture
              </h2>
              <p style={{ color: 'var(--color-text-muted)', marginBottom: '1.5rem' }}>
                Please upload clear photos of your vehicle. You can upload just one image, but multiple angles help provide a more accurate AI damage assessment.
              </p>
              
              <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                {ANGLES.map(angle => (
                  <div key={angle} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '1rem', background: 'var(--color-background)', borderRadius: '8px', border: '1px solid var(--color-border)' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                      <span style={{ fontWeight: '500' }}>{angle}</span>
                      {files[angle] && <CheckCircle size={16} color="var(--color-primary)" />}
                    </div>
                    <label style={{ cursor: 'pointer', padding: '8px 16px', background: 'var(--color-surface)', borderRadius: '4px', border: '1px solid var(--color-border)', color: 'white', transition: 'all 0.2s' }}>
                      {files[angle] ? 'Change File' : 'Upload'}
                      <input type="file" accept="image/*,video/*" hidden onChange={(e) => handleFileChange(angle, e)} />
                    </label>
                  </div>
                ))}
              </div>

              <div style={{ marginTop: '2rem', display: 'flex', justifyContent: 'space-between' }}>
                <Button variant="outline" onClick={() => setStep(1)}>Back</Button>
                <Button onClick={handleSubmit} disabled={loading || Object.keys(files).length === 0}>
                  {loading ? 'Analyzing...' : 'Submit for AI Analysis'}
                </Button>
              </div>
            </Card>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
