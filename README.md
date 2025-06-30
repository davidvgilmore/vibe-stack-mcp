# Vibe Coder Stack Planner 🚀

A Model Context Protocol (MCP) server that helps non-technical builders ("vibe coders") plan the right tech stack for their ideas through progressive questioning using the MCP elicitation specification.

## What it does

This MCP server helps people who have great ideas but don't know the technical jargon. Instead of asking "Do you need a REST API with PostgreSQL?" it asks "What kind of information will people store in your app?"

### Key Features

- **Jargon-free questioning**: Uses simple language anyone can understand
- **Progressive elicitation**: Gathers requirements step-by-step using MCP's elicitation spec
- **Platform-as-a-Service focus**: Recommends easy-to-use platforms like Vercel, Supabase, Netlify
- **Practical guidance**: Provides deployment guides and cost estimates
- **Beginner-friendly**: Focuses on tools that minimize technical complexity

## Installation

1. **Install dependencies:**
```bash
uv pip install fastmcp
```

2. **Run the server:**
```bash
python run_server.py
```

3. **Add to your MCP client configuration** (e.g., Claude Desktop):
```json
{
  "mcpServers": {
    "vibe-stack-planner": {
      "command": "python",
      "args": ["/path/to/vibe_coder_stack_planner/run_server.py"]
    }
  }
}
```

## Tools Available

### `start_project_planning()`
Initiates the interactive planning process through a series of simple questions:
- What are you trying to build?
- Who will use it and how?
- What features do you need?
- How many users do you expect?
- What's your budget and technical comfort level?

### `recommend_stack(session_requirements?)`
Provides tech stack recommendations based on gathered requirements. Can be used with or without the interactive process.

### `explain_recommendation(detail_level?)`
Explains why specific technologies were recommended, with "basic" or "detailed" explanations.

### `get_deployment_guide(platform?)`
Provides step-by-step deployment instructions tailored to your specific needs.

## Example Usage

```
User: I want to build something but I don't know where to start technically.

AI: Let me help you plan the right tech stack! I'll use the vibe coder stack planner to ask you some simple questions.

[Uses start_project_planning tool]

Server: Let's start planning your project! First, tell me about your vision.
What problem are you trying to solve, or what idea do you want to build?

[Progressive questioning continues...]

Server: 🎉 Perfect! Based on what you've told me, here's my recommendation:

**Recommended Tech Stack:**
• Frontend: Next.js (React framework) for a modern web app
• Backend: Supabase (handles database, auth, and API automatically)  
• Hosting: Vercel (free tier covers most small projects)
• Domain: Namecheap or Google Domains (~$12/year)

**Why this works for you:**
I chose beginner-friendly tools that handle most technical details automatically. These tools let you build and deploy quickly. This stack has generous free tiers to keep costs minimal.
```

## Architecture

The server uses:
- **FastMCP**: High-level Python framework for MCP servers
- **Elicitation Spec**: Latest MCP elicitation specification for interactive questioning
- **Rule-based recommendations**: Analyzes requirements to suggest appropriate technologies
- **Progressive disclosure**: Builds complexity gradually based on user comfort level

## Supported Platforms

The server focuses on Platform-as-a-Service solutions:
- **Frontend**: Vercel, Netlify, GitHub Pages
- **Backend**: Vercel Functions, Netlify Functions, Supabase
- **Database**: Supabase, PlanetScale, Firebase
- **Auth**: Supabase Auth, Auth0, Clerk
- **Hosting**: Vercel, Netlify, Render

## Development

To extend or modify the server:

1. **Add new question types**: Modify the elicitation flow in `_ask_about_*` functions
2. **Enhance recommendations**: Update the `_analyze_requirements` function
3. **Add new platforms**: Extend the recommendation logic and deployment guides
4. **Improve UI**: The elicitation spec supports rich form controls

## License

This project is open source. Feel free to fork, extend, and contribute!

---

*Built with ❤️ for the vibe coder community*