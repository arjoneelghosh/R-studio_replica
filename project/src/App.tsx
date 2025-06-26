import React from 'react';
import Hero from './components/Hero';
import WhatItDoes from './components/WhatItDoes';
import ModelComparison from './components/ModelComparison';
import DatasetPreview from './components/DatasetPreview';
import HowItWorks from './components/HowItWorks';
import CallToAction from './components/CallToAction';
import Footer from './components/Footer';

function App() {
  return (
    <div className="font-inter">
      <Hero />
      <WhatItDoes />
      <ModelComparison />
      <DatasetPreview />
      <HowItWorks />
      <CallToAction />
      <Footer />
    </div>
  );
}

export default App;