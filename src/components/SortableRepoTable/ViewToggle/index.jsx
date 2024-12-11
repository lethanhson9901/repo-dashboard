import React from 'react';
import { LayoutGrid, LayoutList } from 'lucide-react';

const ViewToggle = ({ isTableView, onToggle }) => (
  <button
    onClick={onToggle}
    className="flex items-center gap-2 px-3 py-2 bg-white border rounded-lg hover:bg-gray-50 transition-colors"
  >
    {isTableView ? (
      <>
        <LayoutGrid className="h-4 w-4" />
        <span>Card View</span>
      </>
    ) : (
      <>
        <LayoutList className="h-4 w-4" />
        <span>Table View</span>
      </>
    )}
  </button>
);

export default ViewToggle;