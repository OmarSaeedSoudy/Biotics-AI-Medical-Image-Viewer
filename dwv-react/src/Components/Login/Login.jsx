import React, { useState } from 'react';
import axios from 'axios';
import * as Components from './LoginStyles.js';
import { useNavigate } from 'react-router-dom';
import { useDispatch } from 'react-redux';
import { setUser } from '../../Redux/Slices/UserSlice';

const Login = () => {
    const [signIn, toggle] = React.useState(true);
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');

    const navigate = useNavigate()

    const dispatch = useDispatch()

    const handleSignIn = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('http://localhost:5000/user/login', {
                username,
                password,
            });
            console.log("Login response", response);
            // Store token in local storage or cookies
            localStorage.setItem('jwtToken', response.data.access_token);
            dispatch(setUser({name:username, role:"doctor"}))
        // Navigate to patients list
            navigate('/patients');
        } catch (error) {
            console.error('Error signing in:', error);
            setError('Invalid username or password');
        }
    };
    
    return (
      <Components.Container>  
        <Components.SignInContainer>
          <Components.Form onSubmit={handleSignIn}>
            <Components.Title>Sign in</Components.Title>
            <Components.Input
              type='text'
              placeholder='Username'
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
            <Components.Input
              type='password'
              placeholder='Password'
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
            <Components.Anchor href='#'>Forgot your password?</Components.Anchor>
            {error && <Components.Error>{error}</Components.Error>}
            <Components.Button>Sign In</Components.Button>
          </Components.Form>
        </Components.SignInContainer>
      </Components.Container>
    );
}


export default Login
