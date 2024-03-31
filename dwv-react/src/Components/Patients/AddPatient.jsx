import React, { useState } from 'react';
import axios from 'axios';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const AddPatient = () => {
  const [patientName, setPatientName] = useState('');
  const [patientEmail, setPatientEmail] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();

    const axiosInstance = axios.create({
      baseURL: 'http://localhost:5000',
      withCredentials: true
    });

    try {
      const accessToken = localStorage.getItem('jwtToken');
      const response = await axiosInstance.post('/patient/register', {
        name: patientName,
        email: patientEmail
      }, {
        headers: {
          Authorization: `Bearer ${accessToken}`
        }
      });
      console.log(response)
      if (response.status === 201 || response.status === 200) {
        window.location.href = '/patients';
      } else {
        setError('Failed to add patient');
        toast.error('Failed to add patient');
      }
    } catch (error) {
      console.error('Error adding patient:', error);
      setError('Failed to add patient');
      toast.error('Failed to add patient');
    }
  };

  return (
    <div 
      className="medical-record-form-container" 
      style={{ 
        maxWidth: '600px', 
        margin: '0 auto', 
        padding: '20px', 
        border: '1px solid #ccc', 
        borderRadius: '5px' 
      }}
    >
      <ToastContainer />
      <h2>Add New Patient</h2>

      {error && <p className="error-message">{error}</p>}

      <form onSubmit={handleSubmit}>
        <div className="form-group" style={{ marginBottom: '20px' }}>
          <label htmlFor="patientName" style={{ display: 'block', marginBottom: '5px' }}>Patient Name:</label>
          <input
            type="text"
            id="patientName"
            value={patientName}
            onChange={(e) => setPatientName(e.target.value)}
            required
            style={{ width: '100%', padding: '10px', border: '1px solid #ccc', borderRadius: '5px', fontSize: '16px' }}
          />
        </div>

        <div className="form-group" style={{ marginBottom: '20px' }}>
          <label htmlFor="patientEmail" style={{ display: 'block', marginBottom: '5px' }}>Patient Email:</label>
          <input
            type="email"
            id="patientEmail"
            value={patientEmail}
            onChange={(e) => setPatientEmail(e.target.value)}
            required
            style={{ width: '100%', padding: '10px', border: '1px solid #ccc', borderRadius: '5px', fontSize: '16px' }}
          />
        </div>

        <button 
          type="submit" 
          style={{ 
            backgroundColor: '#007bff', 
            color: 'white', 
            padding: '12px 20px', 
            border: 'none', 
            borderRadius: '5px', 
            cursor: 'pointer', 
            fontSize: '16px', 
            transition: 'background-color 0.3s ease' 
          }}
        >
          Add Patient
        </button>
      </form>
    </div>
  );
};

export default AddPatient;
