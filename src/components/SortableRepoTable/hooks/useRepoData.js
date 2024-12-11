import { useState, useMemo } from 'react';

export const useRepoData = (initialData) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [sortConfig, setSortConfig] = useState({ key: 'stars', direction: 'desc' });
  const [currentPage, setCurrentPage] = useState(1);
  const [itemsPerPage, setItemsPerPage] = useState(50);

  const filteredAndSortedData = useMemo(() => {
    let filtered = [...initialData];
    
    if (searchTerm) {
      filtered = filtered.filter(repo => {
        const searchFields = [
          repo.name,
          repo.description,
          repo.language,
          ...(repo.topics || []),
          repo.owner?.username
        ].filter(Boolean);

        return searchFields.some(field => 
          field.toLowerCase().includes(searchTerm.toLowerCase())
        );
      });
    }

    return filtered.sort((a, b) => {
      const { key, direction } = sortConfig;
      
      if (key === 'last_updated') {
        const dateA = new Date(a[key] || 0);
        const dateB = new Date(b[key] || 0);
        return direction === 'asc' ? dateA - dateB : dateB - dateA;
      }
      
      if (key === 'owner') {
        const valueA = a.owner?.username ?? '';
        const valueB = b.owner?.username ?? '';
        return direction === 'asc'
          ? valueA.localeCompare(valueB)
          : valueB.localeCompare(valueA);
      }
      
      const valueA = a[key] ?? 0;
      const valueB = b[key] ?? 0;
      
      if (typeof valueA === 'number' && typeof valueB === 'number') {
        return direction === 'asc' ? valueA - valueB : valueB - valueA;
      }
      
      const stringA = String(valueA).toLowerCase();
      const stringB = String(valueB).toLowerCase();
      return direction === 'asc'
        ? stringA.localeCompare(stringB)
        : stringB.localeCompare(stringA);
    });
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