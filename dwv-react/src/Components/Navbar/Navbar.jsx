import React, { useState } from "react";
import { Link, useMatch, useResolvedPath } from "react-router-dom";
import { useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import './Navbar.css';
import axios from "axios";

export default function Navbar() {
  const [showSettings, setShowSettings] = useState(false);
  const userName = useSelector(state => state.User.name);
  console.log("Nav Bar User Name: ", userName)
  const user = {
    name: userName, // Replace with actual user name
  };

  const navigate = useNavigate()

  const toggleSettings = () => {
    setShowSettings(!showSettings);
  };

  const handleSignOut = () => {
    console.log("Signing Out..")
    const axiosInstance = axios.create({
      baseURL: 'http://localhost:5000',
      withCredentials: true
    });

    const fetchLogout = async () => {
      try {
        const accessToken = localStorage.getItem('jwtToken');
        const response = await axiosInstance.post('/user/logout', {
          headers: {
            Authorization: `Bearer ${accessToken}`
          }
          
        });
        navigate('/');
      } catch (error) {
        navigate('/');
        console.log("error signing out: ", error)
      }
    };

    fetchLogout();
  };
  return (
    <nav className="nav">
      <Link to="/" className="site-title">
        Biotics-AI Medical Image Viewer
      </Link>
      <ul className="nav-links">
          <button className="nav-button" onClick={() => navigate("/")}>Login</button>
          <button className="nav-button" onClick={() => navigate("/dwv_viewer")}>Dicom Web Viewer</button>
          <button className="nav-button" onClick={() => navigate("/patients")}>Patients</button>
          <button className="nav-button" onClick={() => navigate("/add_medical_record")}>Add Medical Record</button>
      </ul>
      <div className="user-settings">
        <button className="user-button" onClick={toggleSettings}>
          Signed in as : {user.name}
          <i className="fas fa-angle-down"></i>
        </button>
        {showSettings && (
          <div className="settings-dropdown">
            <button onClick={handleSignOut}>Sign Out</button>
          </div>
        )}
      </div>
    </nav>
  );
}

function CustomLink({ to, children, ...props }) {
  const resolvedPath = useResolvedPath(to);
  const isActive = useMatch({ path: resolvedPath.pathname, end: true });

  return (
    <li className={isActive ? "active" : ""}>
      <Link to={to} {...props}>
        {children}
      </Link>
    </li>
  );
}
