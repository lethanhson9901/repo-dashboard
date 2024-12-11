import React from 'react';
import { ArrowUp, ArrowDown } from 'lucide-react';

const SortOptions = ({ sortConfig, onSort }) => {
  const sortButtons = [
    { key: 'stars', label: 'Stars' },
    { key: 'forks', label: 'Forks' },
    { key: 'name', label: 'Name' },
    { key: 'last_updated', label: 'Last Updated' }
  ];

  return (
    <div className="p-4 border-b bg-gray-50">
      <div className="flex flex-wrap gap-2 text-sm">
        <span className="text-gray-500">Sort by:</span>
        {sortButtons.map(({ key, label }) => (
          <button 
            key={key}
            onClick={() => onSort(key)}
            className={`px-2 py-1 rounded transition-colors ${
              sortConfig.key === key 
                ? 'bg-blue-100 text-blue-700' 
                : 'hover:bg-gray-200'
            }`}
          >
            <div className="flex items-center gap-1">
              {label}
              {sortConfig.key === key && (
                sortConfig.direction === 'asc' 
                  ? <ArrowUp className="h-3 w-3" />
                  : <ArrowDown className="h-3 w-3" />
              )}
            </div>
          </button>
        ))}
      </div>
    </div>
  );
};

export default SortOptions;