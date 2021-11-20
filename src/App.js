import React from 'react';
import Home from './Home';
import Map from './Map';
import Services from './Services';
import {BrowserRouter, Routes, Route } from 'react-router-dom';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route exact path="/" element={<Home />} />
        <Route exact path="/app" element={<Map />} />
        <Route exact path="/services" element={<Services />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
