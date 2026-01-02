# Skill Obsolescence Predictor - Frontend

React + Vite frontend for the Future Skill & Tech-Stack Obsolescence Predictor.

## Features

- 📊 Interactive dashboard with skill overview
- 🔍 Browse all skills with filtering and search
- ⚠️ High-risk skills monitoring
- ✨ Emerging skills discovery
- 👥 Role trends and required skills
- 📈 Data visualizations with Recharts
- 🎨 Modern, responsive UI

## Setup

### Prerequisites

- Node.js 18+
- npm or yarn

### Installation

```bash
cd frontend
npm install
```

### Development

```bash
npm run dev
```

The app will be available at `http://localhost:5173`

### Build

```bash
npm run build
```

### Environment Variables

Create a `.env` file in the frontend directory:

```env
VITE_API_URL=http://localhost:8000
```

## Project Structure

```
frontend/
├── src/
│   ├── components/      # Reusable components
│   │   ├── Card.jsx
│   │   ├── SkillCard.jsx
│   │   ├── Layout.jsx
│   │   ├── Loading.jsx
│   │   └── Error.jsx
│   ├── pages/          # Page components
│   │   ├── Dashboard.jsx
│   │   ├── Skills.jsx
│   │   ├── SkillDetail.jsx
│   │   ├── HighRiskSkills.jsx
│   │   ├── EmergingSkills.jsx
│   │   └── RoleTrends.jsx
│   ├── services/       # API services
│   │   └── api.js
│   ├── App.jsx         # Main app component
│   └── main.jsx        # Entry point
├── index.html
└── vite.config.js
```

## Technologies

- **React 18** - UI library
- **Vite** - Build tool
- **React Router** - Routing
- **Axios** - HTTP client
- **Recharts** - Chart library
- **CSS3** - Styling

## API Integration

The frontend communicates with the FastAPI backend through the API service layer (`src/services/api.js`). All API calls are centralized here for easy maintenance.

## Components

### Layout
Main navigation and page structure.

### Dashboard
Overview page with statistics, charts, and featured skills.

### Skills
Browse all skills with search and filtering capabilities.

### SkillDetail
Detailed view of a single skill with metrics and trends.

### HighRiskSkills
List of skills with high obsolescence risk.

### EmergingSkills
List of emerging skills with growth potential.

### RoleTrends
Technology roles and their required skill sets.

