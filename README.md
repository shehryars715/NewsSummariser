# DailyNews AI 🗞️🤖

A comprehensive AI-powered news platform that automatically scrapes, categorizes, and intelligently summarizes Pakistani news from Dawn.com. Built with modern web technologies and advanced AI capabilities to provide users with smart news consumption experiences.

## 📋 Project Overview

DailyNews AI is a full-stack application that combines automated news scraping, AI-powered categorization, vector-based search, and intelligent summarization into a seamless news consumption platform. The system continuously monitors Dawn.com, processes articles with machine learning models, and presents them through an intuitive web interface.

### 🎯 Problem Statement

Traditional news consumption is inefficient:
- Information overload with hundreds of articles daily
- Time-consuming manual browsing and filtering
- Difficulty finding relevant news on specific topics
- No intelligent analysis or context for complex stories
- Poor mobile experience on traditional news sites

### 💡 Solution

DailyNews AI addresses these challenges by:
- **Automated Content Curation**: Continuous scraping and processing
- **AI-Powered Organization**: Intelligent categorization and tagging
- **Semantic Search**: Vector-based similarity search for precise results
- **Intelligent Summarization**: AI-generated summaries for quick understanding
- **Modern UX**: Responsive, mobile-first interface designed for today's readers

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         DailyNews AI System                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐    ┌──────────────┐    ┌─────────────────┐    │
│  │   Dawn.com  │───▶│   Scraper    │───▶│   Supabase DB   │    │
│  │ (News Source│    │   Module     │    │   (Articles)    │    │
│  └─────────────┘    └──────────────┘    └─────────────────┘    │
│                             │                       │           │
│                             ▼                       ▼           │
│                    ┌──────────────┐    ┌─────────────────┐     │
│                    │ HuggingFace  │    │ Google Gemini   │     │
│                    │ BART Classifier    │ Embeddings     │     │
│                    └──────────────┘    └─────────────────┘     │
│                             │                       │           │
│                             ▼                       ▼           │
│                    ┌──────────────┐    ┌─────────────────┐     │
│                    │ Categories   │    │ FAISS Vector   │     │
│                    │ & Metadata   │    │ Search Index   │     │
│                    └──────────────┘    └─────────────────┘     │
│                                                   │           │
│                                                   ▼           │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                FastAPI Backend                          │   │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────────┐   │   │
│  │  │   Search    │ │    RAG      │ │  Summarization  │   │   │
│  │  │   Engine    │ │   System    │ │     Service     │   │   │
│  │  └─────────────┘ └─────────────┘ └─────────────────┘   │   │
│  └─────────────────────────────────────────────────────────┘   │
│                             │                                   │
│                             ▼                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              React Frontend                             │   │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────────┐   │   │
│  │  │   Search    │ │  Category   │ │   AI Summary    │   │   │
│  │  │ Interface   │ │  Browser    │ │   Generator     │   │   │
│  │  └─────────────┘ └─────────────┘ └─────────────────┘   │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 🚀 Key Features

### 🔄 **Automated News Pipeline**
- **Continuous Scraping**: Monitors Dawn.com every 2 hours for new content
- **Smart Extraction**: Extracts titles, excerpts, content, and metadata
- **Duplicate Detection**: Prevents duplicate articles in the database
- **Content Validation**: Ensures article quality and completeness
- **Automatic Cleanup**: Removes articles older than 24 hours

### 🤖 **AI-Powered Intelligence**
- **Content Categorization**: Uses Hugging Face BART-Large-MNLI for classification
- **Vector Embeddings**: Google Gemini generates semantic embeddings
- **Similarity Search**: FAISS-based vector search for relevant articles
- **Smart Summarization**: Context-aware AI summaries using Gemini 2.5 Flash
- **Relevance Scoring**: Quantified similarity scores for search results

### 🔍 **Advanced Search Capabilities**
- **Semantic Search**: Find articles by meaning, not just keywords
- **Category Filtering**: Browse by Sports, Technology, Business, National News
- **Intelligent Queries**: Ask natural language questions
- **Adjustable Parameters**: Control number of results and analysis depth
- **Real-time Results**: Sub-second search response times

### 🎨 **Modern User Experience**
- **Responsive Design**: Optimized for mobile, tablet, and desktop
- **Professional UI**: Clean, news-focused interface with smooth animations
- **Interactive Cards**: Rich article cards with summarization capabilities
- **Real-time Feedback**: Loading states, progress indicators, and notifications
- **Accessibility**: WCAG-compliant design with keyboard navigation support

## 🛠️ Technology Stack

### **Backend (Python)**
| Component | Technology | Purpose |
|-----------|------------|---------|
| **Framework** | FastAPI | High-performance async API framework |
| **Web Scraping** | BeautifulSoup + Requests | HTML parsing and HTTP requests |
| **Database** | Supabase (PostgreSQL) | Primary data storage with real-time features |
| **Vector Store** | FAISS | Fast similarity search and clustering |
| **AI Models** | Google Gemini AI | Embeddings and text generation |
| **Classification** | Hugging Face Transformers | Article categorization |
| **Task Scheduling** | Python time module | Periodic scraping automation |
| **Environment** | Python 3.8+ | Runtime environment |

### **Frontend (React)**
| Component | Technology | Purpose |
|-----------|------------|---------|
| **Framework** | React 18 + TypeScript | Modern UI development |
| **Build Tool** | Vite | Fast development and building |
| **Styling** | Tailwind CSS | Utility-first CSS framework |
| **UI Components** | shadcn/ui + Radix UI | Professional component library |
| **State Management** | TanStack Query | Server state management |
| **Routing** | React Router | Client-side navigation |
| **Icons** | Lucide React | Consistent iconography |
| **Notifications** | Sonner | Toast notifications |

### **Infrastructure & Services**
| Component | Technology | Purpose |
|-----------|------------|---------|
| **Database** | Supabase | PostgreSQL with real-time subscriptions |
| **Storage** | Supabase Storage | FAISS index and file storage |
| **AI Services** | Google Gemini API | Text generation and embeddings |
| **ML Models** | Hugging Face API | Classification and NLP tasks |
| **Monitoring** | Built-in health checks | System status monitoring |

### **User Experience**
- **Supported Devices**: Mobile, tablet, desktop
- **Browser Compatibility**: All modern browsers
- **Accessibility Score**: WCAG 2.1 AA compliant
- **Language Support**: English (Pakistan context)


## 🚀 Quick Start

### **Prerequisites**
- Python 3.8+
- Node.js 16+
- Supabase account
- Google Gemini API key
- Hugging Face API token

### **1. Environment Setup**
```bash
# Clone the repository
git clone https://github.com/shehryars715/NewsSummariser
cd dailynews-ai

# Backend setup
cd backend
pip install -r requirements.txt
cp .env.example .env
# Configure your .env file with API keys

# Frontend setup  
cd ../frontend
npm install
# Configure your environment variables
```

### **2. Database Setup**
```sql
-- Create Supabase table
CREATE TABLE news_articles (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    excerpt TEXT,
    content TEXT,
    url TEXT UNIQUE NOT NULL,
    category TEXT,
    publish_time TIMESTAMPTZ,
    scraped_at TIMESTAMPTZ DEFAULT NOW()
);
```

### **3. Run the Application**
```bash
# Terminal 1: Start backend
cd backend
python main.py  # Starts scraper + API server

# Terminal 2: Start frontend
cd frontend  
npm run dev     # Starts development server
```

### **4. Access the Application**
- **Frontend**: https://news-summariser-iota.vercel.app/
- **API**: https://newssummariser-5a49.onrender.com
- **Health Check**: https://newssummariser-5a49.onrender.com/

## 📈 Roadmap & Future Enhancements

### **Phase 1: Current Features** ✅
- [x] Automated news scraping from Dawn.com
- [x] AI-powered article categorization
- [x] Vector-based semantic search
- [x] Real-time AI summarization
- [x] Modern responsive web interface
- [x] FAISS-based similarity search

### **Phase 2: Enhanced Intelligence** 🚧
- [ ] Multi-source news aggregation (Express Tribune, The News)
- [ ] Sentiment analysis and trend detection
- [ ] Personalized recommendations
- [ ] Real-time breaking news alerts
- [ ] Advanced filtering and sorting options
- [ ] Export functionality (PDF, email)

### **Phase 3: Advanced Features** 📋
- [ ] User authentication and profiles
- [ ] Bookmarking and reading lists
- [ ] Social sharing integrations
- [ ] Mobile app development
- [ ] Multilingual support (Urdu)
- [ ] Analytics dashboard

### **Phase 4: Enterprise Features** 🔮
- [ ] API rate limiting and authentication
- [ ] Advanced analytics and insights
- [ ] Custom RSS feeds generation
- [ ] Webhook notifications
- [ ] Enterprise dashboard
- [ ] White-label solutions

## 🤝 Contributing

We welcome contributions from the community! Here's how you can help:

### **Ways to Contribute**
- 🐛 **Bug Reports**: Found an issue? Create a detailed bug report
- 💡 **Feature Requests**: Have an idea? Suggest new features
- 🔧 **Code Contributions**: Submit pull requests for improvements
- 📝 **Documentation**: Help improve our documentation
- 🧪 **Testing**: Help test new features and report feedback

### **Development Workflow**
1. Fork the repository
2. Create a feature branch: 
3. Make your changes and test thoroughly
4. Write or update tests as needed
5. Update documentation if required
6. Submit a pull request with a clear description

### **Coding Standards**
- **Backend**: Follow PEP 8 Python style guide
- **Frontend**: Use TypeScript and follow React best practices
- **Commits**: Use conventional commit messages
- **Testing**: Include tests for new features
- **Documentation**: Update README and code comments

## 📄 License

This project is licensed under the **MIT License** 


### **Community Guidelines**
- Be respectful and inclusive
- Provide constructive feedback
- Help others learn and grow
- Follow our code of conduct
- Share knowledge and experiences


**Project Links**:
- **Repository**: https://github.com/shehryars715/NewsSummariser
- **Live Demo**: https://news-summariser-iota.vercel.app/

---

## 🌟 Acknowledgments

Special thanks to:
- **Dawn News** for providing quality journalism
- **Google Gemini** for powerful AI capabilities
- **Hugging Face** for accessible machine learning models
- **Supabase** for robust backend infrastructure  
- **Open Source Community** for amazing tools and libraries

---

**Built with ❤️ for the Pakistani news community**

*Making news consumption intelligent, efficient, and enjoyable.*
