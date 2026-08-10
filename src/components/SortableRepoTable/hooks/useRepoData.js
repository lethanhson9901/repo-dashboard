import { useState, useMemo } from 'react';
import { filterData, sortData } from '../utils/dataUtils';

export const useRepoData = (initialData) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [sortConfig, setSortConfig] = useState({ key: null, direction: 'asc' });
  const [currentPage, setCurrentPage] = useState(1);
  const [itemsPerPage, setItemsPerPage] = useState(50);

  const filteredAndSortedData = useMemo(() => {
    const filtered = filterData(initialData, searchTerm);
    if (!sortConfig.key) return filtered;
    return sortData(filtered, sortConfig);
  }, [initialData, searchTerm, sortConfig]);

  const paginatedData = useMemo(() => {
    if (itemsPerPage === -1) return filteredAndSortedData;
    const startIndex = (currentPage - 1) * itemsPerPage;
    return filteredAndSortedData.slice(startIndex, startIndex + itemsPerPage);
  }, [filteredAndSortedData, currentPage, itemsPerPage]);

  const handleSort = (key) => {
    setSortConfig(prevConfig => ({
      key,
      direction: prevConfig.key === key && prevConfig.direction === 'asc' ? 'desc' : 'asc'
    }));
  };

  const pagination = {
    currentPage,
    totalPages: itemsPerPage === -1 ? 1 : Math.ceil(filteredAndSortedData.length / itemsPerPage),
    itemsPerPage,
    setCurrentPage,
    setItemsPerPage
  };

  return {
    filteredAndSortedData,
    paginatedData,
    searchTerm,
    setSearchTerm,
    sortConfig,
    handleSort,
    pagination,
    totalItems: filteredAndSortedData.length
  };
};