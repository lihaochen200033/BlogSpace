import React, { Component, useState } from 'react'
import '../node_modules/bootstrap/dist/css/bootstrap.min.css'
import './App.css'
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom'
import Login from './components/login.component'
import SignUp from './components/signup.component'
import Homepage from './components/homepage'
import { AUTH_TOKEN } from './constants';

function App() {
  const [LoggedIn, setLoggedIn] = useState(false);

  const handle_logout = () => {
    localStorage.removeItem(AUTH_TOKEN);
    setLoggedIn(false);
  };

  return (
    <div className="App">
      <nav className="navbar navbar-expand-lg navbar-light fixed-top">
        <div className="container">
          <Link className="navbar-brand" to={'/sign-in'}>
            BlogSpace
          </Link>
          <div className="collapse navbar-collapse" id="navbarTogglerDemo02">
            <ul className="navbar-nav ml-auto">
              {!LoggedIn && (<li className="nav-item">
                <Link className="nav-link" to={'/sign-in'}>
                  Login
                </Link>
              </li>)}
              {!LoggedIn && (<li className="nav-item">
                <Link className="nav-link" to={'/sign-up'}>
                  Sign up
                </Link>
              </li>)}
              {LoggedIn && (<li className="nav-item">
                <Link className="nav-link" to={'/sign-in'} onClick={handle_logout}>
                  Logout
                </Link>
              </li>)}
            </ul>
          </div>
        </div>
      </nav>
      <div className="auth-wrapper">
        <div className="auth-inner">
          <Routes>
            <Route exact path="/" Component={(routeProps)=><Login {...routeProps} LoggedIn={LoggedIn} setLoggedIn={setLoggedIn}/>} />
            <Route path="/sign-in" Component={(routeProps)=><Login {...routeProps} LoggedIn={LoggedIn} setLoggedIn={setLoggedIn}/>} />
            <Route path="/sign-up" element={<SignUp />} />
            <Route path="/homepage" element={<Homepage />} />
          </Routes>
        </div>
      </div>
    </div>
  )
}
export default App