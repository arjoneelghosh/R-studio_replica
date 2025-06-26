import React from 'react';
import { FileText, Download } from 'lucide-react';

const DatasetPreview: React.FC = () => {
  const sampleData = [
    { year: '2002', month: 'JAN', new: '31,106', used: '49,927' },
    { year: '2002', month: 'FEB', new: '27,520', used: '50,982' },
    { year: '2002', month: 'MAR', new: '34,225', used: '58,794' },
    { year: '...', month: '...', new: '...', used: '...' },
    { year: '2024', month: 'SEP', new: '23,738', used: '45,657' },
    { year: '2024', month: 'OCT', new: '24,190', used: '47,760' }
  ];

  const handleDownload = () => {
    // Create a link to download the CSV file from the public folder
    const link = document.createElement('a');
    link.href = '/MVA_Vehicle_Sales_Counts_by_Month_for_Calendar_Year_2002_through_October_2024.csv';
    link.download = 'sample_vehicle_sales_data.csv';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <section className="py-20 bg-gradient-to-b from-gray-900 to-slate-900">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <div className="flex justify-center mb-6">
            <div className="p-3 bg-teal-500/20 rounded-full">
              <FileText className="w-8 h-8 text-teal-400" />
            </div>
          </div>
          
          <h2 className="text-3xl sm:text-4xl font-bold text-white mb-4">
            Sample Dataset
          </h2>
          <p className="text-xl text-gray-300 max-w-2xl mx-auto mb-8">
            See how your historical data should be structured for optimal forecasting results
          </p>
        </div>
        
        <div className="bg-gradient-to-br from-slate-800/50 to-slate-700/30 backdrop-blur-sm border border-slate-600/50 rounded-2xl overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-slate-700/50">
                <tr>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-blue-400 uppercase tracking-wider">
                    Year
                  </th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-teal-400 uppercase tracking-wider">
                    Month
                  </th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-purple-400 uppercase tracking-wider">
                    New Sales
                  </th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-orange-400 uppercase tracking-wider">
                    Used Sales
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-600/50">
                {sampleData.map((row, index) => (
                  <tr
                    key={index}
                    className={`hover:bg-slate-700/30 transition-colors duration-200 ${
                      row.year === '...' ? 'text-gray-500' : 'text-white'
                    }`}
                  >
                    <td className="px-6 py-4 text-sm font-medium">
                      {row.year}
                    </td>
                    <td className="px-6 py-4 text-sm">
                      {row.month}
                    </td>
                    <td className="px-6 py-4 text-sm">
                      {row.new}
                    </td>
                    <td className="px-6 py-4 text-sm">
                      {row.used}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          
          <div className="px-6 py-4 bg-slate-800/30 border-t border-slate-600/50">
            <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
              <p className="text-sm text-gray-400 italic">
                * Complete dataset: Monthly vehicle sales from 2002 to 2024 (276 records)
              </p>
              
              <button
                onClick={handleDownload}
                className="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-teal-500 to-blue-500 hover:from-teal-600 hover:to-blue-600 text-white rounded-lg font-medium transition-all duration-300 transform hover:scale-105 hover:shadow-lg"
              >
                <Download className="w-4 h-4" />
                Download Sample CSV
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default DatasetPreview;