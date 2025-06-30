# Podcast Books Platform

A platform that automatically extracts and organizes book mentions from podcasts, helping users discover and purchase books mentioned in their favorite shows.

## 🎯 Problem Statement

As podcast listeners, we often hear about fascinating books mentioned in shows like Dwarkesh Podcast, World of DaaS, and 80,000 Hours. The problem is that we're usually listening while driving or commuting, and by the time we get home, we've forgotten what those books were. This platform solves that problem by automatically identifying, extracting, and organizing book mentions from podcast episodes.

## 👥 Target Users

- **Primary**: Intellectually curious knowledge workers, PMs, entrepreneurs who listen to business/intellectual podcasts
- **Future expansion**: Any podcast listeners (romance novels, true crime, etc.)

## ✨ Core Features

### Phase 1 (MVP)
- **YouTube Link Processing**: Accept YouTube podcast links and extract book mentions
- **Search Interface**: Search for books mentioned across podcasts
- **Browse by Podcast**: Filter and browse by specific shows
- **Purchase Links**: Direct links to Amazon and other book retailers
- **Cross-Reference Discovery**: See which books are mentioned across multiple episodes/shows

### Phase 2 (Future)
- **Reading Lists**: Save books for later
- **User Accounts**: Personal libraries and recommendations
- **Automated Processing**: Bulk process popular podcasts
- **Mobile App**: Native mobile experience

## 🏗 Technical Architecture

### Recommended Tech Stack (via Vibe Stack Planner)
- **Frontend**: Next.js 15 with App Router
- **Backend**: Next.js API routes 
- **Database**: Neon (serverless Postgres)
- **Authentication**: Clerk
- **Styling**: Tailwind CSS + shadcn/ui
- **Hosting**: Vercel
- **Domain**: Custom domain (~$12/year)

### Core Data Pipeline
```
YouTube Link → Audio Extraction → Transcription → Book Mention Detection → Entity Matching → Database Storage
```

### Key Components
1. **YouTube Processing MCP Server**: Handles video → audio → transcript → book extraction
2. **Book Database**: ISBN, titles, authors, purchase links
3. **Podcast Index**: Show metadata, episodes, hosts
4. **Entity Matching Engine**: Maps fuzzy book mentions to canonical book entries
5. **Web Interface**: Search, browse, discover UI

## 🛠 Implementation Plan

### Phase 1: Core Infrastructure (Week 1-2)
- [ ] Set up Next.js project with recommended stack
- [ ] Build YouTube processing MCP server
- [ ] Create basic database schema (podcasts, books, mentions)
- [ ] Implement book mention extraction (using LLM APIs)
- [ ] Basic web interface for testing

### Phase 2: User Interface (Week 3-4)
- [ ] Search functionality
- [ ] Browse by podcast interface
- [ ] Book detail pages with purchase links
- [ ] Responsive design
- [ ] Basic analytics

### Phase 3: Production Ready (Week 5-6)
- [ ] Error handling and edge cases
- [ ] Performance optimization
- [ ] SEO optimization
- [ ] Deployment to production
- [ ] Domain setup and launch

## 💰 Cost Estimate

**Monthly Operating Costs**: $0-20
- Neon Database: Free tier (generous limits)
- Vercel Hosting: Free tier 
- Transcription API: Pay-per-use (using existing Anthropic/Gemini credits)
- Domain: ~$1/month

## 🔄 Development Approach

This project is being built as a test case for:
- **Vibe Coding methodology**: Rapid prototyping and iteration
- **MCP Server architecture**: Modular, reusable components
- **AI-powered data extraction**: Using LLMs for unstructured data processing

## 📁 Repository Structure

```
/
├── README.md                    # This file
├── vibe_stack_planner.py       # MCP server for tech stack planning
├── PLANNING_SESSION.md         # Detailed planning session notes
├── next-app/                   # Next.js application (to be created)
├── mcp-servers/               # Custom MCP servers
│   └── youtube-book-extractor/ # YouTube → book extraction pipeline
└── docs/                      # Additional documentation
```

## 🚀 Getting Started

1. **Planning Complete**: ✅ Used Vibe Stack Planner MCP server
2. **Next**: Set up Next.js project with recommended stack
3. **Then**: Build YouTube processing MCP server
4. **Finally**: Implement core extraction pipeline

## 📊 Success Metrics

- Books successfully extracted per podcast episode
- User engagement with search/browse features
- Conversion rate to book purchases
- Cross-podcast book discovery rate

---

Built with [Memex](https://memex.tech) and the Vibe Stack Planner MCP server.