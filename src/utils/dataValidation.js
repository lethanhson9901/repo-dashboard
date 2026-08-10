const sanitizeUrl = (raw) => /^https?:\/\//i.test(raw) ? raw : '';

export const validateRepoData = (data) => {
    if (!Array.isArray(data)) {
      throw new Error('Repository data must be an array');
    }

    return data.map(repo => {
      if (!repo || typeof repo !== 'object') {
        throw new Error('Each repository must be an object');
      }

      const validatedRepo = {
        name: String(repo.name || ''),
        description: String(repo.description || ''),
        url: sanitizeUrl(String(repo.url || '')),
        language: repo.language || null,
        stars: Number(repo.stars || 0),
        forks: Number(repo.forks || 0),
        last_updated: repo.last_updated || new Date().toISOString(),
        topics: Array.isArray(repo.topics) ? repo.topics : [],
        owner: repo.owner ? {
          username: String(repo.owner.username || ''),
          profile_url: sanitizeUrl(String(repo.owner.profile_url || ''))
        } : null
      };

      return validatedRepo;
    });
  };