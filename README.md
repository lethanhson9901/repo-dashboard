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

## Quick Start

```bash
# Clone the repository
git clone https://github.com/username/repo-dashboard.git
cd repo-dashboard

# Install Python dependencies
pip install -r requirements.txt

# Install Node.js dependencies
npm install

# Configure environment
cp .env.example .env

# Fetch repository data
python scripts/pull_star_repos.py

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
   pip install -r requirements.txt
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
   GITHUB_USERNAME=your_username
   GITHUB_TOKEN=your_token
   OUTPUT_FILE=src/data/repos.json
   ```

4. **Data Synchronization**

   Run the repository fetch script:
   ```bash
   python scripts/pull_star_repos.py
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


### Dependencies

**Python Packages**
| Package | Version | Description |
|---------|---------|-------------|
| requests | 2.31.0 | HTTP requests library |
| python-dotenv | 1.0.0 | Environment variable management |
| tqdm | 4.66.1 | Progress bars for data fetching |
| python-dateutil | 2.8.2 | Date parsing utilities |

### Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| `GITHUB_USERNAME` | Your GitHub username | - |
| `GITHUB_TOKEN` | Personal access token | - |
| `OUTPUT_FILE` | Data output location | `src/data/repos.json` |

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

```bash
# Create a branch
git checkout -b feature/amazing-feature

# Commit changes
git commit -m 'Add amazing feature'

# Push to branch
git push origin feature/amazing-feature
```

## License

Released under the MIT License. See [LICENSE](LICENSE) for details.

## Support

- 📫 [Open an issue](https://github.com/username/repo-dashboard/issues)
- 🌟 Star the project
- 🐦 Follow on [Twitter](https://twitter.com/username)

---

<div align="center">

**[Website](https://your-website.com)** • **[Documentation](docs)** • **[Report Bug](issues)** • **[Request Feature](issues)**

Made with ❤️ by [Your Name](https://github.com/username)

</div>