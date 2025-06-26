import React from 'react';
import { Clock, Calendar, TrendingUp, Zap } from 'lucide-react';

const ModelComparison: React.FC = () => {
  return (
    <section className="py-20 bg-gradient-to-b from-slate-900 to-gray-900">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-3xl sm:text-4xl font-bold text-white mb-4">
            Model Comparison
          </h2>
          <p className="text-xl text-gray-300 max-w-2xl mx-auto">
            Choose the right forecasting approach for your specific business needs
          </p>
        </div>
        
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* ARIMA Panel */}
          <div className="bg-gradient-to-br from-blue-900/30 to-blue-800/20 backdrop-blur-sm border border-blue-500/30 rounded-2xl p-8 hover:border-blue-400/50 transition-all duration-300 transform hover:scale-105">
            <div className="flex items-center justify-center mb-6">
              <div className="p-4 bg-blue-500/20 rounded-full">
                <Clock className="w-10 h-10 text-blue-400" />
              </div>
            </div>
            
            <h3 className="text-2xl font-bold text-white mb-4 text-center">
              ARIMA Model
            </h3>
            
            <p className="text-blue-200 text-center mb-6 font-medium">
              Best for short-term, stationary trends
            </p>
            
            <ul className="space-y-3">
              <li className="flex items-start gap-3">
                <Zap className="w-5 h-5 text-blue-400 mt-0.5 flex-shrink-0" />
                <span className="text-gray-300">Excellent for linear trend analysis and short-term predictions</span>
              </li>
              <li className="flex items-start gap-3">
                <Zap className="w-5 h-5 text-blue-400 mt-0.5 flex-shrink-0" />
                <span className="text-gray-300">Fast computation with minimal data preprocessing requirements</span>
              </li>
              <li className="flex items-start gap-3">
                <Zap className="w-5 h-5 text-blue-400 mt-0.5 flex-shrink-0" />
                <span className="text-gray-300">Ideal for stationary time series with consistent patterns</span>
              </li>
            </ul>
          </div>
          
          {/* Prophet Panel */}
          <div className="bg-gradient-to-br from-teal-900/30 to-teal-800/20 backdrop-blur-sm border border-teal-500/30 rounded-2xl p-8 hover:border-teal-400/50 transition-all duration-300 transform hover:scale-105">
            <div className="flex items-center justify-center mb-6">
              <div className="p-4 bg-teal-500/20 rounded-full">
                <Calendar className="w-10 h-10 text-teal-400" />
              </div>
            </div>
            
            <h3 className="text-2xl font-bold text-white mb-4 text-center">
              Prophet Model
            </h3>
            
            <p className="text-teal-200 text-center mb-6 font-medium">
              Handles seasonal, holiday-impacted long-term trends
            </p>
            
            <ul className="space-y-3">
              <li className="flex items-start gap-3">
                <TrendingUp className="w-5 h-5 text-teal-400 mt-0.5 flex-shrink-0" />
                <span className="text-gray-300">Advanced seasonality detection with holiday effect modeling</span>
              </li>
              <li className="flex items-start gap-3">
                <TrendingUp className="w-5 h-5 text-teal-400 mt-0.5 flex-shrink-0" />
                <span className="text-gray-300">Robust handling of missing data and outliers</span>
              </li>
              <li className="flex items-start gap-3">
                <TrendingUp className="w-5 h-5 text-teal-400 mt-0.5 flex-shrink-0" />
                <span className="text-gray-300">Perfect for long-term forecasts with complex patterns</span>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </section>
  );
};

export default ModelComparison;