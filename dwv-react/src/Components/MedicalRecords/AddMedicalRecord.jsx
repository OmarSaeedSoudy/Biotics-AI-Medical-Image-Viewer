import React, { useState, useEffect } from 'react';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './MedicalRecords.css';

const MedicalRecordForm = () => {
  const [formData, setFormData] = useState({
    patient_id: '',
    dicom_file: null,
    description: ''
  });
  const [patients, setPatients] = useState([]);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [isDragOver, setIsDragOver] = useState(false);
  const navigate = useNavigate()

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
        setPatients(response.data.patients);
      } catch (error) {
        toast.error('Unauthorized access. Please log in.');
        
      }
    };

    fetchPatients();
  }, []);

  const handleChange = (e) => {
    const { name, value, files } = e.target;
    setFormData({
      ...formData,
      [name]: name === 'dicom_file' ? files[0] : value
    });
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragOver(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragOver(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    setFormData({
      ...formData,
      dicom_file: file
    });
    setIsDragOver(false);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const axiosInstance = axios.create({
      baseURL: 'http://localhost:5000',
      withCredentials: true
    });

    const accessToken = localStorage.getItem('jwtToken');

    const formDataToSend = new FormData();
    formDataToSend.append('patient_id', formData.patient_id);
    formDataToSend.append('dicom_file', formData.dicom_file);
    formDataToSend.append('description', formData.description);

    try {
      const response = await axiosInstance.post('/medical_records/register', formDataToSend, {
        headers: {
          'Authorization': `Bearer ${accessToken}`,
          'Content-Type': 'multipart/form-data'
        }
      });

      if (response.status === 201) {
        setSuccess('Medical record registered successfully');
        toast.success("Medical Record Added Successfully");
      } else if (response.status === 401) {
        setError('Unauthorized access. Please log in.');
        toast.error('Unauthorized access. Please log in.');
        
      } else {
        setError('Failed to register medical record');
        toast.error('Failed to register medical record');
      }
    } catch (error) {
      if (error.response && error.response.status === 401) {
        setError('Unauthorized access. Please log in.');
        toast.error('Unauthorized access. Please log in.');
        
      } else {
        setError('Failed to register medical record');
        toast.error('Failed to register medical record');
      }
    }
  };

  return (
    <div className="medical-record-form-container">
      <ToastContainer />
      <h2>Register Medical Record</h2>

      {error && <p className="error-message">{error}</p>}
      {success && <p className="success-message">{success}</p>}

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="patient_id">Patient Name:</label>
          <select
            id="patient_id"
            name="patient_id"
            value={formData.patient_id}
            onChange={handleChange}
            required
          >
            <option value="" disabled>Select Patient</option>
            {patients.map((patient) => (
              <option key={patient.patient_id} value={patient.patient_id}>
                {patient.patient_name}
              </option>
            ))}
          </select>
        </div>

        <div className={`form-group dropzone ${isDragOver ? 'dragover' : ''}`}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
        >
          <label htmlFor="dicom_file" className="dropzone-label">
            Clieck Here To Browse Files
            <input
              type="file"
              id="dicom_file"
              name="dicom_file"
              onChange={handleChange}
              required
            />
          </label>
          <p>Drag & Drop or Click to Upload</p>
        </div>

        <div className="form-group">
          <label htmlFor="description">Description:</label>
          <textarea
            id="description"
            name="description"
            value={formData.description}
            onChange={handleChange}
            required
          ></textarea>
        </div>

        <button type="submit">Register Medical Record</button>
      </form>
    </div>
  );
};

export default MedicalRecordForm;
