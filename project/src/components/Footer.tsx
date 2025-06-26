import React from 'react';
import { Github, Mail} from 'lucide-react';

const Footer: React.FC = () => {
  return (
    <footer className="bg-slate-900 border-t border-slate-700/50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="text-center">
          <div className="flex justify-center items-center gap-6 mb-6">
            <button className="p-2 text-gray-400 hover:text-white transition-colors duration-300 hover:bg-slate-800 rounded-full">
              <Github className="w-5 h-5" />
            </button>
            <button className="p-2 text-gray-400 hover:text-white transition-colors duration-300 hover:bg-slate-800 rounded-full">
              <Mail className="w-5 h-5" />
            </button>
          </div>
          
          <div className="flex items-center justify-center gap-2 text-gray-400 mb-4">
            <span>Built by</span>
            <span className="text-white font-medium">Arjoneel Ghosh</span>
          </div>
          
          <p className="text-gray-500 text-sm">
            Powered by Python, ARIMA & Prophet
          </p>
          
          <div className="mt-8 pt-8 border-t border-slate-800">
            <p className="text-xs text-gray-500">
              © 2024 Sales Forecasting Engine. Made by Arjoneel Ghosh. 
            </p>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;