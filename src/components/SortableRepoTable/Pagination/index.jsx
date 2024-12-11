import React from 'react';
import { 
  ChevronLeft,
  ChevronRight,
  ChevronsLeft,
  ChevronsRight 
} from 'lucide-react';

const Pagination = ({ 
  currentPage, 
  totalPages, 
  setCurrentPage, 
  itemsPerPage, 
  setItemsPerPage,
  totalItems 
}) => {
  const handleItemsPerPageChange = (newValue) => {
    setItemsPerPage(Number(newValue));
    setCurrentPage(1);
  };

  const startItem = totalItems === 0 ? 0 : Math.min((currentPage - 1) * itemsPerPage + 1, totalItems);
  const endItem = Math.min(currentPage * itemsPerPage, totalItems);

  return (
    <div className="flex items-center justify-between px-4 py-3 border-t">
      <div className="flex items-center gap-2">
        <span className="text-sm text-gray-700">Show</span>
        <select
          value={itemsPerPage}
          onChange={(e) => handleItemsPerPageChange(e.target.value)}
          className="border rounded px-2 py-1 text-sm"
        >
          <option value={50}>50</option>
          <option value={100}>100</option>
          <option value={-1}>All</option>
        </select>
        <span className="text-sm text-gray-700">entries</span>
      </div>
      
      <div className="flex items-center gap-2">
        <span className="text-sm text-gray-700">
          {totalItems > 0 ? `Showing ${startItem} to ${endItem} of ${totalItems} entries` : 'No entries'}
        </span>
        
        <div className="flex gap-1">
          <button
            onClick={() => setCurrentPage(1)}
            disabled={currentPage === 1}
            className="p-1 rounded hover:bg-gray-100 disabled:opacity-50"
          >
            <ChevronsLeft className="h-4 w-4" />
          </button>
          <button
            onClick={() => setCurrentPage(currentPage - 1)}
            disabled={currentPage === 1}
            className="p-1 rounded hover:bg-gray-100 disabled:opacity-50"
          >
            <ChevronLeft className="h-4 w-4" />
          </button>
          <button
            onClick={() => setCurrentPage(currentPage + 1)}
            disabled={currentPage === totalPages}
            className="p-1 rounded hover:bg-gray-100 disabled:opacity-50"
          >
            <ChevronRight className="h-4 w-4" />
          </button>
          <button
            onClick={() => setCurrentPage(totalPages)}
            disabled={currentPage === totalPages}
            className="p-1 rounded hover:bg-gray-100 disabled:opacity-50"
          >
            <ChevronsRight className="h-4 w-4" />
          </button>
        </div>
      </div>
    </div>
  );
};

export default Pagination;