import React, { useState, useEffect } from 'react';
import { getShipmentTracking } from '../../services/shipmentService';

const ShipmentTracking = ({ shipmentId }) => {
  const [trackingData, setTrackingData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchTrackingData = async () => {
      try {
        const data = await getShipmentTracking(shipmentId);
        setTrackingData(data);
      } catch (err) {
        setError('Failed to fetch tracking data.');
        console.error(`Error fetching tracking for shipment ${shipmentId}:`, err);
      }
    };

    fetchTrackingData();
  }, [shipmentId]);

  if (error) {
    return <div>{error}</div>;
  }

  if (!trackingData) {
    return <div>Loading tracking data...</div>;
  }

  return (
    <div>
      <h2>Shipment Tracking - ID: {shipmentId}</h2>
      <p>Status: {trackingData.status}</p>
      {/* Display other tracking details as needed */}
    </div>
  );
};

export default ShipmentTracking;