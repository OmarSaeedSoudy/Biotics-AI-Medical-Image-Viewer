import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';
import { Link } from 'react-router-dom';

const MedicalRecords = () => {
  const [medicalRecords, setMedicalRecords] = useState([]);
  const [selectedRecord, setSelectedRecord] = useState(null);
  const [modalVisible, setModalVisible] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');

  const { patientId } = useParams();

  useEffect(() => {
    const axiosInstance = axios.create({
      baseURL: 'http://localhost:5000',
      withCredentials: true,
    });

    const fetchMedicalRecords = async () => {
      try {
        const accessToken = localStorage.getItem('jwtToken');
        const response = await axiosInstance.get(`/medical_records/get/${patientId}`, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });
        setMedicalRecords(response.data.patient_medical_records);
      } catch (error) {
        console.error('Error fetching medical_records:', error);
      }
    };

    fetchMedicalRecords();
  }, [patientId]);

  const openModal = (record) => {
    setSelectedRecord(record);
    setModalVisible(true);
  };

  const closeModal = () => {
    setSelectedRecord(null);
    setModalVisible(false);
  };

  const filteredData = selectedRecord
    ? Object.entries(selectedRecord.dicom_details || {})
        .filter(([key]) => key.toLowerCase().includes(searchQuery.toLowerCase()))
        .reduce((acc, [key, value]) => ({ ...acc, [key]: value }), {})
    : {};

  return (
    <div className="medical-records-container">
      <h2>Medical Records</h2>
      {medicalRecords.map((record, index) => (
        <div className="medical-record-container" key={index}>
          <h3>Medical Record Number: {index + 1} </h3>
          <h3>Patient Name: {record.patient_name}</h3>
          <h3>Description: {record.description}</h3>
          <a href={record.dicom_url} target="_blank" rel="noopener noreferrer">Download DICOM File</a>
          <button className="view-dicom-button" onClick={() => openModal(record)}>View DICOM Details</button>
          <Link to={`/dwv_viewer`}>
            <button className="view-dicom-button">View DICOM File at DWV Viewer</button>
          </Link>
        </div>
      ))}

      {/* DICOM Details Modal */}
      {modalVisible && selectedRecord && (
        <div className="dicom-modal">
          <div className="dicom-modal-content">
            <span className="dicom-modal-close" onClick={closeModal}>&times;</span>
            <input
              type="text"
              placeholder="Search DICOM data..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
            <pre>{JSON.stringify(filteredData, null, 2)}</pre>
          </div>
        </div>
      )}
    </div>
  );
};

export default MedicalRecords;

// CSS (You can add this to your existing CSS or create a new CSS file)
