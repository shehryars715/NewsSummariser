# News RAG Frontend

A modern React-based web application that provides an intelligent news browsing experience with AI-powered search and summarization. Built with TypeScript, Vite, and Tailwind CSS, featuring real-time news data from the backend API.

## 🚀 Features

- **AI-Powered Search**: Semantic search with intelligent article retrieval
- **Smart Summarization**: Generate AI summaries for individual articles or search queries
- **Category Browsing**: Browse news by categories (Sports, Technology, Business, National)
- **Responsive Design**: Mobile-first responsive design with modern UI components
- **Real-time Updates**: Live API health monitoring and real-time data fetching
- **Professional UI**: Clean, modern interface with smooth animations and transitions

## 🛠️ Tech Stack

### Core Framework
- **React 18.3.1** - Modern React with hooks and concurrent features
- **TypeScript** - Type-safe development
- **Vite 5.4.19** - Lightning-fast build tool and dev server

### UI & Styling
- **Tailwind CSS 3.4.17** - Utility-first CSS framework
- **shadcn/ui** - High-quality React UI components
- **Radix UI** - Accessible, unstyled UI primitives
- **Lucide React** - Beautiful & consistent icon library

### State Management & Data Fetching
- **TanStack Query** - Powerful data synchronization for React
- **Supabase Client** - Real-time database integration
- **React Hook Form** - Performant, flexible forms with easy validation

### Additional Libraries
- **React Router DOM** - Client-side routing
- **Recharts** - Responsive chart library
- **Sonner** - An opinionated toast component
- **Next Themes** - Perfect dark mode support
- **date-fns** - Modern JavaScript date utility library

## 📋 Prerequisites

- Node.js 16+ 
- npm or yarn package manager
- Running backend API (see backend README)

## 📦 Installation

1. **Clone and navigate to frontend**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   # or
   yarn install
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Configure your `.env` file:
   ```env
   # Supabase Configuration (for direct database access)
   VITE_SUPABASE_URL=your_supabase_project_url
   VITE_SUPABASE_ANON_KEY=your_supabase_anon_key
   
   # API Configuration (Backend URL)
   VITE_API_URL=http://localhost:8000
   ```

## 🚀 Development

### Start Development Server
```bash
npm run dev
# or
yarn dev
```

The application will be available at `http://localhost:8080`

### Build for Production
```bash
npm run build
# or
yarn build
```

### Preview Production Build
```bash
npm run preview
# or
yarn preview
```

### Linting
```bash
npm run lint
# or
yarn lint
```

## 🎨 Design System

### Color Palette
- **Primary**: Blue-based professional color scheme
- **Categories**: Color-coded news categories
  - Sports: Green (`--news-category-sports`)
  - Technology: Blue (`--news-category-tech`) 
  - Business: Orange (`--news-category-business`)
  - National: Red (`--news-category-national`)
  - Other: Purple (`--news-category-other`)

### Typography
- Modern, readable font stack with proper hierarchy
- Responsive typography scaling
- Consistent spacing and line heights

### Components
- Card-based layout with subtle shadows and gradients
- Smooth animations and hover effects
- Mobile-first responsive design
- Accessible color contrasts and focus states

## 🔌 API Integration

### Backend Endpoints Used

1. **Health Check**
   ```typescript
   GET http://localhost:8000/
   ```

2. **Search Articles**
   ```typescript
   POST http://localhost:8000/search
   {
     "query": string,
     "max_articles": number
   }
   ```

3. **AI Query & Summary**
   ```typescript
   POST http://localhost:8000/query  
   {
     "query": string,
     "max_articles": number
   }
   ```

4. **Summarize by URL**
   ```typescript
   POST http://localhost:8000/summarize-url
   {
     "url": string
   }
   ```

### API Response Types

```typescript
interface Article {
  id?: number;
  title: string;
  excerpt?: string;
  url: string;
  category?: string;
  relevance_score?: number;
  publish_time?: string;
  content?: string;
}

interface SearchResponse {
  articles: Article[];
}

interface QueryResponse {
  summary: string;
  articles_used: Article[];
}

interface SummarizeResponse {
  title: string;
  summary: string;
  category?: string;
  url: string;
}
```

## 📱 Key Features

### 1. Hero Section
- **Dual Search Interface**: Regular search + AI-powered queries
- **Quick Query Suggestions**: Pre-defined popular search terms
- **Real-time Results**: Instant search with loading states
- **Copy/Share Functionality**: Easy sharing of AI summaries

### 2. Category Sections
- **Dynamic Loading**: Load articles by category from Supabase
- **Load More/Less**: Expandable article lists
- **Real-time Updates**: Fresh content from database

### 3. Article Cards
- **Smart Categorization**: Color-coded category badges
- **Relevance Scoring**: Shows search relevance percentages
- **Individual Summaries**: AI summarization for each article
- **External Links**: Direct access to original articles

### 4. Search & AI Features
- **Semantic Search**: Vector-based similarity search
- **AI Summarization**: Context-aware content summaries
- **Adjustable Parameters**: Control number of articles analyzed
- **Sort & Filter**: Multiple sorting options

### 5. Responsive Design
- **Mobile-First**: Optimized for all screen sizes  
- **Touch-Friendly**: Proper spacing for mobile interactions
- **Progressive Enhancement**: Works well on all devices

## 🔧 Configuration

### Vite Configuration
- **Development Server**: Runs on port 8080 with hot reload
- **Path Aliases**: `@/` mapped to `src/` directory
- **React SWC**: Fast refresh and compilation
- **Component Tagging**: Development-mode component identification

### Tailwind Configuration
- **Custom Design System**: Extended color palette for news themes
- **Typography Plugin**: Enhanced text styling options
- **Animation Plugin**: Smooth micro-interactions
- **Container Queries**: Responsive design utilities

### TypeScript Configuration
- **Strict Mode**: Disabled for rapid development
- **Path Mapping**: Absolute imports with `@/` prefix
- **Modern ES Features**: ES2020 target with latest libraries

## 🚨 Error Handling

- **Toast Notifications**: User-friendly error messages
- **Loading States**: Clear feedback during API calls
- **Offline Handling**: Graceful degradation when API unavailable
- **404 Pages**: Proper error page routing
- **API Status Monitoring**: Real-time backend health checking

## 🎯 Performance Optimizations

- **Code Splitting**: Automatic route-based splitting
- **Lazy Loading**: Components loaded on demand
- **Image Optimization**: Responsive images with proper sizing
- **Bundle Analysis**: Optimized dependency bundling
- **Caching Strategy**: Efficient API response caching

## 🚀 Deployment

### Build Process
```bash
npm run build
```

### Deployment Options
- **Vercel**: Recommended for easy React deployment
- **Netlify**: Great for static site hosting
- **AWS S3 + CloudFront**: Enterprise-grade hosting
- **Docker**: Containerized deployment option

### Environment Variables for Production
```env
VITE_API_URL=https://your-backend-api.com
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your_production_anon_key
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-feature`
3. Make your changes following the coding standards
4. Test your changes thoroughly
5. Submit a pull request with a clear description

### Coding Standards
- Use TypeScript for all new components
- Follow existing naming conventions
- Write descriptive commit messages
- Ensure responsive design compatibility
- Add appropriate error handling

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support & Troubleshooting

### Common Issues

1. **API Connection Errors**
   - Verify backend is running on `http://localhost:8000`
   - Check network connectivity and CORS settings
   - Ensure environment variables are properly set

2. **Build Failures**
   - Clear node_modules and reinstall dependencies
   - Check TypeScript errors in terminal
   - Verify all imports and paths are correct

3. **Styling Issues**
   - Ensure Tailwind CSS is properly configured
   - Check for conflicting CSS rules
   - Verify responsive design breakpoints

### Performance Issues
- Use React DevTools for component profiling
- Check network tab for slow API calls
- Monitor bundle size with build analysis tools

For additional support, please create an issue in the repository with:
- Description of the problem
- Steps to reproduce
- Browser and system information
- Console error messages (if any)
