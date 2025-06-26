import React from 'react';
import { Upload, Settings, BarChart3 } from 'lucide-react';

const HowItWorks: React.FC = () => {
  const steps = [
    {
      icon: Upload,
      title: "Upload Historical Data",
      description: "Import your time-series data in CSV format with date and value columns. Our system automatically validates and preprocesses your data.",
      color: "blue"
    },
    {
      icon: Settings,
      title: "Configure Parameters",
      description: "Choose your forecast period, select additional variables, and let our AI determine the optimal model settings for your specific dataset.",
      color: "teal"
    },
    {
      icon: BarChart3,
      title: "Get Results",
      description: "Receive comprehensive forecast graphs, accuracy metrics, confidence intervals, and downloadable results ready for presentation.",
      color: "purple"
    }
  ];

  const getColorClasses = (color: string) => {
    switch (color) {
      case 'blue':
        return {
          bg: 'bg-blue-500/20',
          border: 'border-blue-400/30',
          icon: 'text-blue-400',
          number: 'text-blue-400',
          gradient: 'from-blue-500/10 to-blue-600/5'
        };
      case 'teal':
        return {
          bg: 'bg-teal-500/20',
          border: 'border-teal-400/30',
          icon: 'text-teal-400',
          number: 'text-teal-400',
          gradient: 'from-teal-500/10 to-teal-600/5'
        };
      case 'purple':
        return {
          bg: 'bg-purple-500/20',
          border: 'border-purple-400/30',
          icon: 'text-purple-400',
          number: 'text-purple-400',
          gradient: 'from-purple-500/10 to-purple-600/5'
        };
      default:
        return {
          bg: 'bg-blue-500/20',
          border: 'border-blue-400/30',
          icon: 'text-blue-400',
          number: 'text-blue-400',
          gradient: 'from-blue-500/10 to-blue-600/5'
        };
    }
  };

  return (
    <section id="how-it-works" className="py-20 bg-gradient-to-b from-slate-900 to-gray-900">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-3xl sm:text-4xl font-bold text-white mb-4">
            How It Works
          </h2>
          <p className="text-xl text-gray-300 max-w-2xl mx-auto">
            Get professional forecasts in three simple steps
          </p>
        </div>
        
        <div className="relative">
          {/* Desktop connector lines */}
          <div className="hidden lg:block absolute top-1/2 left-0 right-0 h-0.5 bg-gradient-to-r from-transparent via-gray-600 to-transparent transform -translate-y-1/2 z-0"></div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 lg:gap-12 relative z-10">
            {steps.map((step, index) => {
              const colors = getColorClasses(step.color);
              
              return (
                <div
                  key={index}
                  className="relative group"
                >
                  <div className={`relative bg-gradient-to-br ${colors.gradient} backdrop-blur-sm border border-slate-600/50 rounded-2xl p-8 hover:border-slate-500/50 transition-all duration-300 transform hover:-translate-y-2 hover:shadow-2xl hover:shadow-black/30`}>
                    {/* Step number */}
                    <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                      <div className={`w-8 h-8 ${colors.bg} ${colors.border} border-2 rounded-full flex items-center justify-center backdrop-blur-sm shadow-lg`}>
                        <span className={`text-sm font-bold ${colors.number}`}>
                          {index + 1}
                        </span>
                      </div>
                    </div>
                    
                    {/* Icon */}
                    <div className="flex justify-center mb-6 mt-4">
                      <div className={`p-4 ${colors.bg} rounded-full group-hover:scale-110 transition-transform duration-300 shadow-lg`}>
                        <step.icon className={`w-8 h-8 ${colors.icon}`} />
                      </div>
                    </div>
                    
                    {/* Content */}
                    <h3 className="text-xl font-semibold text-white mb-4 text-center">
                      {step.title}
                    </h3>
                    
                    <p className="text-gray-400 text-center leading-relaxed group-hover:text-gray-300 transition-colors duration-300">
                      {step.description}
                    </p>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
        
        {/* Bottom CTA */}
        <div className="text-center mt-16">
          <div className="inline-flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-slate-700/50 to-slate-600/50 rounded-full border border-slate-500/30">
            <span className="text-gray-300 text-sm">Ready to start?</span>
            <span className="text-blue-400 font-medium">Launch the tool above ↑</span>
          </div>
        </div>
      </div>
    </section>
  );
};

export default HowItWorks;