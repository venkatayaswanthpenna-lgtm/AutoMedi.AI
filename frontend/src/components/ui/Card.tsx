'use client';

import React from 'react';
import { motion } from 'framer-motion';

interface CardProps {
  children: React.ReactNode;
  style?: React.CSSProperties;
  className?: string;
  interactive?: boolean;
}

export function Card({ children, style, className = '', interactive = false }: CardProps) {
  return (
    <motion.div
      className={`glass-panel ${className}`}
      whileHover={interactive ? { y: -5, boxShadow: '0 10px 30px rgba(0,0,0,0.5)' } : {}}
      transition={{ type: 'spring', stiffness: 300 }}
      style={{
        padding: '1.5rem',
        ...style
      }}
    >
      {children}
    </motion.div>
  );
}
