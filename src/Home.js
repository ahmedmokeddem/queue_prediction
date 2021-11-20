import React, { useEffect } from 'react';
import logo from './BlackLogo.svg';
import { useNavigate } from 'react-router-dom';

function Home() {
  let navigate = useNavigate();
  const DELAY = 5000;

  useEffect(() => {
    setTimeout(() => {
      navigate("/services", { replace: true });
    }, DELAY);

  });

  return (
    <div className="bg">
      <h4 className="app-name">Queue Predict</h4>

      <div className="logo-container">
        <img src={logo} alt="logo" />
        <div className="circle" style={{'--i': 0}}>
        </div>
        <div className="circle" style={{'--i': 1}}>
        </div>
        <div className="circle" style={{'--i': 2}}>
        </div>
      </div>

      <div className="text-container">
        <h1 className="essayer">Hey! it's QueueP</h1>
        <div className="text">Ayez une vision de l'avenir des files d'attente de vos services publics et ne perdez pas de temps, nous nous occupons de l'avenir.</div>
      </div>


    </div>
  );
}

export default Home;
