import React, { useState, useMemo } from 'react';
import { Search } from 'lucide-react';
import ViewToggle from './ViewToggle';
import TableView from './TableView';
import CardView from './CardView';
import StatsSection from './StatsSection';
import SortOptions from './SortOptions';
import { useRepoData } from './hooks/useRepoData';
import SearchBar from './SearchBar';

const SortableRepoTable = ({ initialData = [] }) => {
  const [isTableView, setIsTableView] = useState(true);
  const {
    filteredAndSortedData,
    paginatedData,
    searchTerm,
    setSearchTerm,
    sortConfig,
    handleSort,
    pagination,
    totalItems
  } = useRepoData(initialData);

  if (!Array.isArray(initialData) || initialData.length === 0) {
    return (
      <div className="w-full bg-white rounded-xl shadow-lg p-8">
        <div className="text-center text-gray-500">
          No repositories available
        </div>
      </div>
    );
  }

  return (
    <div className="w-full bg-white rounded-xl shadow-lg">
      {/* Header */}
      <div className="p-4 border-b">
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
          <div className="flex items-center gap-4">
            <h2 className="text-xl font-bold text-gray-900">Featured Repositories</h2>
            <ViewToggle isTableView={isTableView} onToggle={() => setIsTableView(!isTableView)} />
          </div>
          <SearchBar searchTerm={searchTerm} onSearch={setSearchTerm} />
        </div>
      </div>

      {/* Stats */}
      <StatsSection data={initialData} />

      {/* Sort Options */}
      <SortOptions sortConfig={sortConfig} onSort={handleSort} />

      {/* Main Content */}
      <div className="transition-all duration-300 ease-in-out">
        {isTableView ? (
          <TableView 
            data={paginatedData}
            sortConfig={sortConfig}
            onSort={handleSort}
            pagination={pagination}
          />
        ) : (
          <CardView data={paginatedData} />
        )}
      </div>

      {/* Empty State */}
      {filteredAndSortedData.length === 0 && (
        <div className="p-8 text-center text-gray-500">
          <div className="mx-auto w-24 h-24 mb-4">
            <Search className="w-full h-full text-gray-300" />
          </div>
          <h3 className="text-lg font-medium mb-2">No repositories found</h3>
          <p className="text-sm text-gray-400">
            Try adjusting your search or filter criteria
          </p>
        </div>
      )}

      {/* Footer */}
      <div className="p-4 border-t text-sm text-gray-500 text-center">
        Showing {paginatedData.length} of {totalItems} repositories
      </div>
    </div>
  );
};

export default SortableRepoTable;