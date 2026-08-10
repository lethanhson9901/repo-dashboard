export const validateRepoData = (data) => {
    if (!Array.isArray(data)) {
      throw new Error('Repository data must be an array');
    }

    return data.map(repo => {
      if (!repo || typeof repo !== 'object') {
        throw new Error('Each repository must be an object');
      }

      const rawUrl = String(repo.url || '');
      const safeUrl = /^https?:\/\//i.test(rawUrl) ? rawUrl : '';

      const rawProfileUrl = repo.owner ? String(repo.owner.profile_url || '') : '';
      const safeProfileUrl = /^https?:\/\//i.test(rawProfileUrl) ? rawProfileUrl : '';

      const validatedRepo = {
        name: String(repo.name || ''),
        description: String(repo.description || ''),
        url: safeUrl,
        language: repo.language || null,
        stars: Number(repo.stars || 0),
        forks: Number(repo.forks || 0),
        last_updated: repo.last_updated || new Date().toISOString(),
        topics: Array.isArray(repo.topics) ? repo.topics : [],
        owner: repo.owner ? {
          username: String(repo.owner.username || ''),
          profile_url: safeProfileUrl
        } : null
      };

      return validatedRepo;
    });
  };