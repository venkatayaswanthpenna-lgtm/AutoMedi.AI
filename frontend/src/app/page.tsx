import Link from 'next/link';

export default function Home() {
  return (
    <main style={{ padding: '4rem', display: 'flex', flexDirection: 'column', alignItems: 'center', minHeight: '100vh' }}>
      <div className="glass-panel" style={{ padding: '3rem', maxWidth: '600px', textAlign: 'center' }}>
        <h1 style={{ color: 'var(--color-primary)', fontSize: '2.5rem', marginBottom: '1rem' }}>
          AutoMedi.AI
        </h1>
        <p style={{ color: 'var(--color-text-muted)', marginBottom: '2rem' }}>
          Production-Ready Vehicle Damage Assessment Platform
        </p>
        <Link href="/login" style={{ 
          background: 'var(--color-secondary)', 
          color: 'white', 
          border: 'none', 
          padding: '12px 24px', 
          borderRadius: '8px',
          cursor: 'pointer',
          fontWeight: 'bold',
          textDecoration: 'none',
          display: 'inline-block'
        }}>
          Get Started
        </Link>
      </div>
    </main>
  );
}
