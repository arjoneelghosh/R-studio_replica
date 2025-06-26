import React from 'react';
import { Rocket, ArrowRight } from 'lucide-react';

const CallToAction: React.FC = () => {
  return (
    <section className="py-20 bg-gradient-to-b from-gray-900 to-slate-900">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <div className="bg-gradient-to-br from-slate-800/50 to-slate-700/30 backdrop-blur-sm border border-slate-600/50 rounded-3xl p-12 relative overflow-hidden">
          {/* Background decorative elements */}
          <div className="absolute inset-0 overflow-hidden">
            <div className="absolute -top-20 -right-20 w-40 h-40 bg-blue-500/10 rounded-full blur-2xl"></div>
            <div className="absolute -bottom-20 -left-20 w-40 h-40 bg-teal-500/10 rounded-full blur-2xl"></div>
          </div>
          
          <div className="relative z-10">
            <div className="flex justify-center mb-8">
              <div className="p-4 bg-gradient-to-br from-blue-500/20 to-teal-500/20 rounded-full">
                <Rocket className="w-12 h-12 text-blue-400" />
              </div>
            </div>
            
            <h2 className="text-3xl sm:text-4xl font-bold text-white mb-6">
              Ready to Start Forecasting?
            </h2>
            
            <p className="text-xl text-gray-300 mb-8 max-w-2xl mx-auto leading-relaxed">
              Transform your historical data into actionable business insights with our advanced forecasting engine.
            </p>
            
            <button className="group bg-gradient-to-r from-blue-500 to-teal-500 hover:from-blue-600 hover:to-teal-600 text-white font-semibold px-8 py-4 rounded-full text-lg transition-all duration-300 transform hover:scale-105 hover:shadow-xl hover:shadow-blue-500/25 inline-flex items-center gap-3">
              Launch Forecast Tool
              <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform duration-300" />
            </button>
            
            <p className="text-sm text-gray-400 mt-6">
              No signup required • Process data securely • Get instant results
            </p>
          </div>
        </div>
      </div>
    </section>
  );
};

export default CallToAction;