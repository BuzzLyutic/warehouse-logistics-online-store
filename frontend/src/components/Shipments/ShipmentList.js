// src/components/Shipment/ShipmentList.js
import React, { useState, useEffect } from 'react';
import { getAllShipments } from '../../utils/api';
import '../../styles/ShipmentList.css';

const ShipmentList = () => {
    const [shipments, setShipments] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchShipments = async () => {
            try {
                const response = await getAllShipments();
                setShipments(response.data);
            } catch (err) {
                setError(err);
            } finally {
                setIsLoading(false);
            }
        };

        fetchShipments();
    }, []);

    if (isLoading) {
        return <div>Loading shipments...</div>;
    }

    if (error) {
        return <div>Error loading shipments: {error.message}</div>;
    }

    return (
        <div className="shipment-list-container">
            <h2>Shipments</h2>
            <table className="shipment-table">
                <thead>
                    <tr>
                        <th>Shipment ID</th>
                        <th>Order ID</th>
                        <th>Carrier</th>
                        <th>Tracking Number</th>
                        <th>Status</th>
                        <th>Created At</th>
                        <th>Updated At</th>
                        <th>Logs</th>
                    </tr>
                </thead>
                <tbody>
                    {shipments.map((shipment) => (
                        <tr key={shipment.shipment_id}>
                            <td>{shipment.shipment_id}</td>
                            <td>{shipment.order_id}</td>
                            <td>{shipment.carrier_name}</td>
                            <td>{shipment.tracking_number || 'N/A'}</td>
                            <td>{shipment.status}</td>
                            <td>{new Date(shipment.created_at).toLocaleString()}</td>
                            <td>{new Date(shipment.updated_at).toLocaleString()}</td>
                            <td>
                                {shipment.logs.length > 0 ? (
                                    <ul className="log-list">
                                        {shipment.logs.map((log, index) => (
                                            <li key={index}>
                                                {new Date(log.timestamp).toLocaleString()} - {log.location} - {log.status}
                                            </li>
                                        ))}
                                    </ul>
                                ) : (
                                    'No logs available'
                                )}
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default ShipmentList;