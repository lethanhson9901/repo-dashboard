<div align="center">

# GitHub Repository Dashboard

[Features](#features) • [Quick Start](#quick-start) • [Documentation](#documentation) • [Contributing](#contributing)

A beautifully crafted dashboard for exploring and analyzing GitHub repositories with powerful search and visualization capabilities.

[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Made with React](https://img.shields.io/badge/Made%20with-React-61dafb.svg)](https://reactjs.org/)
[![Powered by GitHub API](https://img.shields.io/badge/Powered%20by-GitHub%20API-333.svg)](https://docs.github.com/en/rest)

![Dashboard Preview](docs/assets/preview.png)

</div>

---

## Features

- **Real-Time Search**
  - Instantly find repositories as you type
  - Filter by language, stars, and more

- **Rich Analytics**
  - Visualize repository statistics
  - Track language distribution
  - Monitor star history

- **Modern Design**
  - Clean, intuitive interface
  - Responsive across all devices
  - Dark mode support

- **Automated Updates**
  - Daily repository data synchronization
  - GitHub Actions workflow integration
  - Manual update triggers

## Quick Start

```bash
# Clone the repository
git clone https://github.com/lethanhson9901/repo-dashboard.git
cd repo-dashboard

# Install Python dependencies
pip install requests python-dotenv

# Install Node.js dependencies
npm install

# Configure environment
cp .env.example .env

# Fetch repository data
python backend/pull_your_star_repos.py

# Start development server
npm run dev
```

## Documentation

### Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn
- GitHub account

### Installation

1. **Python Setup**

   Create and activate a virtual environment (recommended):
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

   Install Python dependencies:
   ```bash
   pip install requests python-dotenv
   ```

2. **Node.js Setup**

   Install Node.js dependencies:
   ```bash
   npm install
   ```

3. **Environment Configuration**

   Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

   Configure your environment:
   ```env
   GH_USERNAME=your_username
   GH_PAT=your_personal_access_token
   OUTPUT_FILE=src/data/repos.json
   GITHUB_API_VERSION=2022-11-28
   ITEMS_PER_PAGE=100
   ```

4. **Data Synchronization**

   Run the repository fetch script:
   ```bash
   python backend/pull_your_star_repos.py
   ```

   Or commit with the update trigger:
   ```bash
   git commit -m "[update-repos] Updating repository data"
   git push
   ```

5. **Development**

   ```bash
   # Start development server
   npm run dev

   # Build for production
   npm run build

   # Start production server
   npm run start
   ```

### Automated Updates

The repository includes a GitHub Actions workflow that automatically updates the repository data:

1. **Daily Updates**
   - Runs automatically at 00:00 UTC
   - Fetches fresh repository data
   - Deploys updated dashboard

2. **Manual Updates**
   ```bash
   # Trigger update with commit
   git commit -m "[update-repos] Your commit message"
   git push

   # Regular commit (no update)
   git commit -m "Your commit message"
   git push
   ```

3. **Manual Trigger**
   - Go to Actions tab on GitHub
   - Select "Update and Deploy to GitHub Pages"
   - Click "Run workflow"

### Dependencies

**Python Packages**
| Package | Version | Description |
|---------|---------|-------------|
| requests | latest | HTTP requests library |
| python-dotenv | latest | Environment variable management |

### Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| `GH_USERNAME` | Your GitHub username | - |
| `GH_PAT` | GitHub Personal Access Token | - |
| `OUTPUT_FILE` | Data output location | `src/data/repos.json` |
| `GITHUB_API_VERSION` | GitHub API version | `2022-11-28` |
| `ITEMS_PER_PAGE` | Items per API request | `100` |

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

```bash
# Create a branch
git checkout -b feature/amazing-feature

# Commit changes with update
git commit -m '[update-repos] Add amazing feature'

# Commit changes without update
git commit -m 'Update documentation'

# Push to branch
git push origin feature/amazing-feature
```

## License

Released under the MIT License. See [LICENSE](LICENSE) for details.

## Support

- 📫 [Open an issue](https://github.com/lethanhson9901/repo-dashboard/issues)
- 🌟 Star the project
- 🐦 Follow on [Twitter](https://twitter.com/lethanhson9901)

---

<div align="center">

**[Website](https://your-website.com)** • **[Documentation](docs)** • **[Report Bug](issues)** • **[Request Feature](issues)**


Made with ❤️ by [Le Thanh Son](https://github.com/lethanhson9901)

</div>