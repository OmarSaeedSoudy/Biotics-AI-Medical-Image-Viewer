import React from 'react';

import './App.css';
// import DwvComponent from './DwvComponent';
import DwvComponent from './Components/DicomWebView/DwvComponent';


import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';  // Replace Switch with Routes
import PatientsList from './Components/Patients/Patients';
import MedicalRecords from './Components/MedicalRecords/MedicalRecords';
import Login from './Components/Login/Login';
import AddPatient from './Components/Patients/AddPatient';
import MedicalRecordForm  from './Components/MedicalRecords/AddMedicalRecord'
import AuthenticatedLayout from './Components/AuthenticatedLayout/AuthenticatedLayout'
// import ImageViewer from './Components/DicomWebViewer/ImageViewer';

import useMediaQuery from '@mui/material/useMediaQuery';
import CssBaseline from '@mui/material/CssBaseline';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { indigo, pink } from '@mui/material/colors';

export default function App() {
    const prefersDarkMode = useMediaQuery('(prefers-color-scheme: dark)');
    const theme = createTheme({
      typography: {
        useNextVariants: true,
      },
      palette: {
        primary: {
          main: indigo[500]
        },
        secondary: {
          main: pink[500]
        },
        mode: prefersDarkMode ? 'dark' : 'light',
      }
    });

    return (
      <Router>
        <Routes>
          <Route path="/" element={<Login />} /> {/* Login route remains separate */}
          <Route path='/dwv_viewer' element={
            <ThemeProvider theme={theme}>
            <CssBaseline />
            <div className="App">
              <DwvComponent />
            </div>
          </ThemeProvider>
          }/>
          <Route element={<AuthenticatedLayout />}>
          <Route path="/patients" element={<PatientsList />} />
          <Route path="/medical_records/get/:patientId" element={<MedicalRecords />} />
          <Route path="/add_patient" element={<AddPatient />} />
          <Route path="/add_medical_record" element={<MedicalRecordForm />} />
          
          </Route>
        </Routes>
      </Router>
    );
}
