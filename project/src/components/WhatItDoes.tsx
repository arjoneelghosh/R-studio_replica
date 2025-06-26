import React from 'react';
import { BarChart3, Target, Calendar, Download } from 'lucide-react';

const WhatItDoes: React.FC = () => {
  const features = [
    {
      icon: BarChart3,
      title: "Accurate Time-Series Forecasts",
      description: "Generate precise predictions using state-of-the-art ARIMA & Prophet algorithms with automated parameter optimization"
    },
    {
      icon: Target,
      title: "Auto-Model Selection",
      description: "Intelligent model selection based on AIC, RMSE, and cross-validation metrics to ensure optimal forecasting performance"
    },
    {
      icon: Calendar,
      title: "Advanced Pattern Recognition",
      description: "Automatically handles complex trends, seasonal patterns, holidays, and promotional impacts in your data"
    },
    {
      icon: Download,
      title: "Complete Output Package",
      description: "Get interactive forecast graphs, detailed error metrics, confidence intervals, and downloadable CSV results"
    }
  ];

  return (
    <section className="py-20 bg-gradient-to-b from-slate-800 to-slate-900">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-3xl sm:text-4xl font-bold text-white mb-4">
            What This Tool Does
          </h2>
          <p className="text-xl text-gray-300 max-w-2xl mx-auto">
            Professional-grade forecasting capabilities powered by advanced machine learning models
          </p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {features.map((feature, index) => (
            <div
              key={index}
              className="group bg-gradient-to-br from-slate-700/50 to-slate-800/50 backdrop-blur-sm border border-slate-600/50 rounded-2xl p-6 hover:border-blue-400/50 transition-all duration-300 transform hover:-translate-y-2 hover:shadow-xl hover:shadow-blue-500/10"
            >
              <div className="flex justify-center mb-4">
                <div className="p-3 bg-blue-500/20 rounded-full group-hover:bg-blue-500/30 transition-colors duration-300">
                  <feature.icon className="w-8 h-8 text-blue-400 group-hover:text-blue-300 transition-colors duration-300" />
                </div>
              </div>
              
              <h3 className="text-xl font-semibold text-white mb-3 text-center">
                {feature.title}
              </h3>
              
              <p className="text-gray-400 text-center leading-relaxed group-hover:text-gray-300 transition-colors duration-300">
                {feature.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default WhatItDoes;