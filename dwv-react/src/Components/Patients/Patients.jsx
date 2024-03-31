import React, { useState, useEffect } from 'react';
import axios from 'axios';
import PatientsContainer from "./styles";
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const PatientsList = () => {
  const [patients, setPatients] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [filteredPatients, setFilteredPatients] = useState([]);

  useEffect(() => {
    const axiosInstance = axios.create({
      baseURL: 'http://localhost:5000',
      withCredentials: true
    });

    const fetchPatients = async () => {
      try {
        const accessToken = localStorage.getItem('jwtToken');
        const response = await axiosInstance.get('/patients/get_all', {
          headers: {
            Authorization: `Bearer ${accessToken}`
          }
        });
        if (response.data.patients) {
          toast.success('All Your Patients Have Been Fetched Successfully.');
        }
        else {
          toast.error("You Don't Have Any Patients Assigned To You");
        }
        setPatients(response.data.patients);
        setFilteredPatients(response.data.patients); // Initialize filteredPatients with all patients
      } catch (error) {
        if (error.response && error.response.status === 401) {
          setError('Unauthorized access. Please log in.');
          toast.error('Unauthorized access. Please log in.');
          
        } else {
          setError('Failed to register medical record');
          toast.error('Error Fetching Patients');
        }
      }
    };

    fetchPatients();
  }, []);

  const handleSearchChange = (e) => {
    setSearchQuery(e.target.value);
    const filtered = patients.filter(patient =>
      patient.patient_name.toLowerCase().includes(e.target.value.toLowerCase())
    );
    setFilteredPatients(filtered);
  };

  const viewMedicalRecords = async (patientId) => {
    window.location.href = `/medical_records/get/${patientId}`;
  };

  const handleAddPatient = () => {
    window.location.href = '/add_patient'; // Redirect to add patient page
  };

  const handleAddMedicalRecord = () => {
    window.location.href = '/add_medical_record'; // Redirect to add patient page
  };

  return (
    <div className="patient-container">
      <ToastContainer />
      <h2>My Patients</h2>
      
      {/* Search Bar */}
      <input
        type="text"
        placeholder="Search by Patient Name"
        value={searchQuery}
        onChange={handleSearchChange}
        style={{ marginBottom: '20px', padding: '10px', width: '300px' }}
      />

      {/* Add Patient Button */}
      <button 
        onClick={handleAddPatient}
        style={{ marginRight: '10px', padding: '10px 20px', backgroundColor: '#007BFF', color: '#fff', border: 'none', borderRadius: '5px', cursor: 'pointer' }}
      >
        Add Patient
      </button>
      <button 
        onClick={handleAddMedicalRecord}
        style={{ padding: '10px 20px', backgroundColor: '#007BFF', color: '#fff', border: 'none', borderRadius: '5px', cursor: 'pointer' }}
      >
        Add Medical Record
      </button>

      <ul>
        {filteredPatients.map((patient) => (
          <PatientsContainer key={patient.patient_id}>
            <p>Patient Name: {patient.patient_name}</p>
            <p>Patient Email: {patient.patient_email}</p>
            <button 
              onClick={() => viewMedicalRecords(patient.patient_id)}
              style={{ marginTop: '10px', padding: '10px 20px', backgroundColor: '#007BFF', color: '#fff', border: 'none', borderRadius: '5px', cursor: 'pointer' }}
            >
              View Medical Records
            </button>
          </PatientsContainer>
        ))}
      </ul>
    </div>
  );
};

export default PatientsList;
