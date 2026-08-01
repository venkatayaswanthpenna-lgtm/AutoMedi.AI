'use client';

import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import { Star, Phone, Clock } from 'lucide-react';

// Fix for default marker icon in Next.js
// By deleting the default _getIconUrl, it forces Leaflet to use the configured iconUrls
delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
});

// Custom Icon for AutoMedi AI (Orange Marker)
const customIcon = new L.Icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-orange.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

// Helper component to auto-pan the map when a garage is selected
function MapController({ selectedGarage }: { selectedGarage: any }) {
  const map = useMap();
  
  useEffect(() => {
    if (selectedGarage && selectedGarage.latitude && selectedGarage.longitude) {
      map.flyTo([selectedGarage.latitude, selectedGarage.longitude], 15, {
        duration: 1.5
      });
    }
  }, [selectedGarage, map]);

  return null;
}

interface MapProps {
  garages: any[];
  selectedGarage: any;
  onGarageSelect: (garage: any) => void;
}

export default function GarageMap({ garages, selectedGarage, onGarageSelect }: MapProps) {
  // Default to San Francisco
  const defaultCenter: [number, number] = [37.7749, -122.4194];

  // Prevent SSR issues
  const [isMounted, setIsMounted] = useState(false);
  useEffect(() => setIsMounted(true), []);
  if (!isMounted) return null;

  return (
    <MapContainer 
      center={defaultCenter} 
      zoom={13} 
      style={{ height: '100%', width: '100%', minHeight: '500px', borderRadius: '16px', zIndex: 1 }}
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png" // Dark theme tile layer
      />
      
      {garages.map((garage) => (
        garage.latitude && garage.longitude && (
          <Marker 
            key={garage.id}
            position={[garage.latitude, garage.longitude]}
            icon={selectedGarage?.id === garage.id ? customIcon : new L.Icon.Default()}
            eventHandlers={{
              click: () => onGarageSelect(garage),
            }}
          >
            <Popup>
              <div style={{ padding: '0.25rem', color: '#1a1a1a' }}>
                <h4 style={{ margin: '0 0 0.5rem 0', fontSize: '1rem', fontWeight: 'bold' }}>{garage.name}</h4>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.25rem', marginBottom: '0.25rem' }}>
                  <Star size={14} color="#ffcc00" fill="#ffcc00" />
                  <span>{garage.rating} / 5.0</span>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.25rem', marginBottom: '0.5rem', fontSize: '0.875rem' }}>
                  <Phone size={14} /> {garage.phone}
                </div>
                <button 
                  onClick={() => alert(`Navigating to ${garage.name}...`)}
                  style={{
                    width: '100%',
                    padding: '0.5rem',
                    background: '#ff6600',
                    color: 'white',
                    border: 'none',
                    borderRadius: '4px',
                    cursor: 'pointer',
                    fontWeight: 'bold'
                  }}
                >
                  Get Directions
                </button>
              </div>
            </Popup>
          </Marker>
        )
      ))}

      <MapController selectedGarage={selectedGarage} />
    </MapContainer>
  );
}
