export const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit'
    });
  };
  
  export const getLanguageColor = (language) => {
    const colors = {
      'JavaScript': 'bg-yellow-100 text-yellow-800 border-yellow-300',
      'Python': 'bg-blue-100 text-blue-800 border-blue-300',
      'TypeScript': 'bg-blue-100 text-blue-800 border-blue-300',
      'Java': 'bg-red-100 text-red-800 border-red-300',
      'Go': 'bg-cyan-100 text-cyan-800 border-cyan-300',
      'Rust': 'bg-orange-100 text-orange-800 border-orange-300',
      'Ruby': 'bg-red-100 text-red-800 border-red-300',
      'C++': 'bg-purple-100 text-purple-800 border-purple-300',
      'PHP': 'bg-indigo-100 text-indigo-800 border-indigo-300'
    };
    return colors[language] || 'bg-gray-100 text-gray-800 border-gray-300';
  };
  
  export const filterData = (data, searchTerm) => {
    if (!searchTerm) return data;
    
    return data.filter(repo => {
      if (!repo) return false;
      
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
  };
  
  export const sortData = (data, { key, direction }) => {
    return [...data].sort((a, b) => {
      if (!a || !b) return 0;
      
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
  };