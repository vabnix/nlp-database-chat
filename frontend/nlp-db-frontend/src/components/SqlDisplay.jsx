import { Database, Clock } from 'lucide-react';

export const SqlDisplay = ({ sql, executionTime }) => {
  return (
    <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
      <h2 className="text-lg font-semibold mb-2 flex items-center gap-2">
        <Database size={20} className="text-gray-500" />
        Generated SQL Query
      </h2>
      <pre className="bg-gray-50 p-4 rounded-md overflow-x-auto">
        {sql}
      </pre>
      <div className="mt-2 text-sm text-gray-500 flex items-center gap-1">
        <Clock size={16} />
        Execution time: {executionTime.toFixed(3)}s
      </div>
    </div>
  );
};