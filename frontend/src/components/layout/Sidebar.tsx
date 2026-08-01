'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { LayoutDashboard, Car, FileText, Map, Settings } from 'lucide-react';

export function Sidebar() {
  const pathname = usePathname();
  
  const navItems = [
    { name: 'Dashboard', path: '/dashboard', icon: <LayoutDashboard size={20} /> },
    { name: 'New Inspection', path: '/inspections/new', icon: <FileText size={20} /> },
    { name: 'Garage Map', path: '/garages', icon: <Map size={20} /> },
    { name: 'Mechanic Portal', path: '/mechanic', icon: <Car size={20} /> },
  ];

  return (
    <aside style={{
      width: '250px',
      background: 'rgba(26, 29, 36, 0.5)',
      borderRight: '1px solid var(--color-border)',
      padding: '2rem 1rem',
      display: 'flex',
      flexDirection: 'column',
      gap: '0.5rem',
      minHeight: 'calc(100vh - 72px)'
    }}>
      {navItems.map((item) => {
        const isActive = pathname === item.path;
        return (
          <Link href={item.path} key={item.path} style={{ textDecoration: 'none' }}>
            <div style={{
              display: 'flex',
              alignItems: 'center',
              gap: '1rem',
              padding: '12px 16px',
              borderRadius: '8px',
              background: isActive ? 'var(--color-primary)' : 'transparent',
              color: isActive ? '#fff' : 'var(--color-text-muted)',
              transition: 'all 0.2s',
              cursor: 'pointer'
            }}>
              {item.icon}
              <span style={{ fontWeight: isActive ? '600' : '400' }}>{item.name}</span>
            </div>
          </Link>
        );
      })}
    </aside>
  );
}
