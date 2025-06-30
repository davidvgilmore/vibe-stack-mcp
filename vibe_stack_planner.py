#!/usr/bin/env python3
"""
Vibe Coder Stack Planner MCP Server

A Model Context Protocol server that helps non-technical builders ("vibe coders") 
plan the right tech stack for their ideas through progressive questioning.

This server follows Vibe Coder Best Practices (2025):
- Web-first approach: 90% of projects work great as web apps (mobile browsers work excellently)
- Modern serverless architecture: Next.js + Neon/Supabase + Vercel
- Start small, scale up: Always assume starting with small user base initially
- Platform-as-a-Service focus: Avoid complex infrastructure setup
- AI-friendly tooling: Technologies with excellent AI assistant support

Key Principles:
- Simple, jargon-free questions
- Interactive process (user must provide answers, agent presents questions)
- Practical deployment guidance
- Cost-effective recommendations with generous free tiers
- Modern 2025 tech stack (includes newer features like Neon Auth beta)
"""

import json
import asyncio
from typing import Dict, Any, Optional, List, Literal
from dataclasses import dataclass, asdict
from datetime import datetime

from fastmcp import FastMCP, Context


# Data structures for project planning
@dataclass
class ProjectRequirements:
    """Stores gathered project requirements"""
    project_vision: str = ""
    target_users: str = ""
    user_interaction: str = ""
    core_features: List[str] = None
    data_needs: str = ""
    user_scale: str = ""
    timeline: str = ""
    budget_level: str = ""
    technical_comfort: str = ""
    gathered_at: str = ""
    
    def __post_init__(self):
        if self.core_features is None:
            self.core_features = []
        if self.gathered_at == "":
            self.gathered_at = datetime.now().isoformat()

# Using step-by-step tools instead of elicitation for now


# Initialize the MCP server
mcp = FastMCP("Vibe Coder Stack Planner")

# In-memory storage for active planning sessions
planning_sessions: Dict[str, ProjectRequirements] = {}


@mcp.tool()
async def start_project_planning(ctx: Context) -> str:
    """
    Start the project planning process by gathering basic information about what you want to build.
    
    This will guide you through a series of questions about your project idea - no technical knowledge required!
    Note: This version uses a guided approach since elicitation isn't available yet.
    """
    await ctx.info("Starting project planning process...")
    
    return """🚀 Let's plan your tech stack! I'll ask you a series of simple questions.

**IMPORTANT**: This is an interactive process. I will ask you questions and YOU need to provide the answers. Do not answer the questions yourself - wait for the user to respond to each step.

**Step 1: Tell me about your project vision**

Please describe what you want to build:
- What problem are you trying to solve?
- What would this app/website do?
- Why would people want to use it?

Just explain it like you're telling a friend about your idea! Once you provide this, I'll guide you through the next steps.

*Example: "I want to build a simple task management app for my small team. We're always forgetting who's supposed to do what and when things are due."*

After you tell me about your vision, I'll ask you about:
- Who will use it and how
- What features you need  
- Your timeline and budget
- Your technical comfort level

Then I'll recommend the perfect tech stack for your needs!"""


# Helper functions removed - using step-by-step tools instead of elicitation


async def _analyze_requirements(requirements: ProjectRequirements) -> Dict[str, str]:
    """
    Analyze requirements and generate recommendations following Vibe Coder best practices:
    - Web-first approach (mobile browsers work great)
    - Modern PaaS platforms with generous free tiers
    - Serverless-first architecture
    - Focus on speed to value
    """
    
    recommendations = {
        "stack_summary": "",
        "reasoning": "",
        "cost_estimate": "",
        "complexity_level": ""
    }
    
    # Analyze data needs and features to determine architecture
    needs_database = any(keyword in requirements.data_needs.lower() + ' '.join(requirements.core_features).lower() 
                        for keyword in ['store', 'save', 'profile', 'user', 'account', 'data', 'records'])
    
    needs_auth = any(keyword in ' '.join(requirements.core_features).lower() 
                    for keyword in ['login', 'account', 'user', 'profile', 'auth', 'signup'])
    
    needs_real_time = any(keyword in requirements.data_needs.lower() + ' '.join(requirements.core_features).lower()
                         for keyword in ['chat', 'message', 'notification', 'real-time', 'live', 'collaborative'])

    # VIBE CODER PRINCIPLE: Web apps work everywhere
    # 90% of projects don't need native mobile apps - modern web apps work great on mobile browsers
    frontend_rec = "Next.js 15 with App Router"
    
    # Determine backend and database based on 2025 best practices
    if needs_database and needs_auth:
        # Use modern serverless Postgres with built-in auth
        if requirements.technical_comfort in ['avoid_technical', 'basic_setup']:
            backend_rec = "Next.js API routes with Supabase (includes auth + database)"
        else:
            backend_rec = "Next.js API routes with Neon (serverless Postgres) + Clerk auth"
    elif needs_database:
        # Database but no auth
        backend_rec = "Next.js API routes with Neon (serverless Postgres)"
    elif needs_auth:
        # Auth but no persistent database  
        backend_rec = "Next.js API routes with Clerk auth"
    else:
        # Static or minimal backend needs
        backend_rec = "Next.js API routes (for any server functionality)"
    
    # Always recommend Vercel for Next.js (made by same team)
    hosting_rec = "Vercel"
    
    # Build recommendation using 2025 Vibe Coder Stack
    recommendations["stack_summary"] = f"""
• Frontend: {frontend_rec}
• Backend: {backend_rec} 
• Styling: Tailwind CSS + shadcn/ui components
• Hosting: {hosting_rec}
• Domain: Namecheap (~$12/year)
"""
    
    # Build reasoning based on vibe coder principles
    reasoning_parts = [
        "This is the proven 2025 'Vibe Stack' - optimized for speed and simplicity"
    ]
    
    if requirements.technical_comfort in ['avoid_technical', 'basic_setup']:
        reasoning_parts.append("These tools have excellent documentation and AI assistant support")
    
    reasoning_parts.append("Everything scales automatically as you grow")
    reasoning_parts.append("Web app works perfectly on desktop and mobile browsers")
    
    recommendations["reasoning"] = ". ".join(reasoning_parts) + "."
    
    # Cost estimate based on realistic 2025 pricing
    if requirements.budget_level == 'free_only':
        recommendations["cost_estimate"] = "$0-20/month (generous free tiers + domain)"
    elif requirements.budget_level == 'low_cost':
        recommendations["cost_estimate"] = "$20-50/month"
    else:
        recommendations["cost_estimate"] = "$50-150/month with room to scale"
    
    # Complexity assessment
    if requirements.technical_comfort in ['avoid_technical', 'basic_setup']:
        recommendations["complexity_level"] = "Low - guided setup with excellent AI coding assistant support"
    elif requirements.technical_comfort == 'some_technical':
        recommendations["complexity_level"] = "Medium - straightforward setup, some coding required"
    else:
        recommendations["complexity_level"] = "Medium - full control with modern tooling"
    
    return recommendations


@mcp.tool()
async def collect_project_vision(ctx: Context, project_vision: str) -> str:
    """
    Collect your project vision and move to the next step of planning.
    
    Args:
        project_vision: Describe what you want to build and what problem it solves
    """
    # Create a new session
    session_id = f"planning_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    planning_sessions[session_id] = ProjectRequirements()
    planning_sessions[session_id].project_vision = project_vision
    
    await ctx.info(f"Recorded project vision for session {session_id}")
    
    return f"""Great! I understand you want to build: "{project_vision}"

**Step 2: Tell me about your users and how they'll interact**

Please tell me:
- **Who will use this?** (e.g., "My team of 8 people", "Small business owners", "Anyone who needs to track tasks")
- **How will they use it?** (e.g., "Check it daily", "Use occasionally", "On mobile while traveling")

Use the `collect_user_info` tool with this information to continue!"""


@mcp.tool()
async def collect_user_info(ctx: Context, target_users: str, user_interaction: str, session_id: Optional[str] = None) -> str:
    """
    Collect information about who will use your project and how.
    
    Args:
        target_users: Describe who will use your project
        user_interaction: Describe how often and in what context people will use this
        session_id: Optional session ID (will use most recent if not provided)
    """
    if not session_id:
        if not planning_sessions:
            return "No active planning session. Please start with `start_project_planning` first."
        session_id = max(planning_sessions.keys())
    
    if session_id not in planning_sessions:
        return f"Session {session_id} not found. Please start a new planning session."
    
    planning_sessions[session_id].target_users = target_users
    planning_sessions[session_id].user_interaction = user_interaction
    
    await ctx.info(f"Updated user info for session {session_id}")
    
    return f"""Perfect! So your users are: "{target_users}" and they'll use it: "{user_interaction}"

**Step 3: Features and data needs**

Please tell me:
- **What will people do with it?** (e.g., "Create tasks, assign to people, mark complete, see progress")
- **What information will it handle?** (e.g., "Task details, user profiles, due dates, completion status")

Use the `collect_features_data` tool to continue!"""


@mcp.tool()
async def collect_features_data(ctx: Context, core_features: str, data_needs: str, session_id: Optional[str] = None) -> str:
    """
    Collect information about features and data requirements.
    
    Args:
        core_features: Describe the main features or actions users will take
        data_needs: Describe what kind of data or information your project will work with
        session_id: Optional session ID (will use most recent if not provided)
    """
    if not session_id:
        if not planning_sessions:
            return "No active planning session. Please start with `start_project_planning` first."
        session_id = max(planning_sessions.keys())
    
    if session_id not in planning_sessions:
        return f"Session {session_id} not found. Please start a new planning session."
    
    # Parse core features into a list
    planning_sessions[session_id].core_features = [f.strip() for f in core_features.split(',') if f.strip()]
    planning_sessions[session_id].data_needs = data_needs
    
    await ctx.info(f"Updated features and data info for session {session_id}")
    
    return f"""Excellent! Features: "{core_features}" and data needs: "{data_needs}"

**Step 4: Timeline and budget (final step!)**

Please tell me:
- **When do you need this?** Choose one:
  - "experimental" (just experimenting, no rush)
  - "few_weeks" (within a few weeks for a basic version)  
  - "month_or_two" (need something in a month or two)
  - "urgent" (this is urgent, need it ASAP)

- **Budget level?** Choose one:
  - "free_only" (free or very low cost only)
  - "low_cost" (can spend a little bit ~$10-50/month)
  - "reasonable" (reasonable budget for a good solution ~$50-200/month)
  - "flexible" (budget is not a major constraint)

- **Technical comfort?** Choose one:
  - "avoid_technical" (I avoid technical things when possible)
  - "basic_setup" (I can handle basic setup with good instructions)
  - "some_technical" (I'm comfortable with some technical work)
  - "enjoy_technical" (I enjoy diving into technical details)

Use the `finalize_planning` tool to get your recommendations!"""


@mcp.tool()
async def collect_scale_timeline(ctx: Context, user_scale: str, timeline: str, session_id: Optional[str] = None) -> str:
    """
    Collect information about expected scale and timeline.
    
    Args:
        user_scale: Expected number of users (personal, small_community, hundreds, thousands_plus)
        timeline: When you need this (experimental, few_weeks, month_or_two, urgent)
        session_id: Optional session ID (will use most recent if not provided)
    """
    if not session_id:
        if not planning_sessions:
            return "No active planning session. Please start with `start_project_planning` first."
        session_id = max(planning_sessions.keys())
    
    if session_id not in planning_sessions:
        return f"Session {session_id} not found. Please start a new planning session."
    
    # Validate inputs
    valid_scales = ["personal", "small_community", "hundreds", "thousands_plus"]
    valid_timelines = ["experimental", "few_weeks", "month_or_two", "urgent"]
    
    if user_scale not in valid_scales:
        return f"Invalid user_scale. Please choose one of: {', '.join(valid_scales)}"
    
    if timeline not in valid_timelines:
        return f"Invalid timeline. Please choose one of: {', '.join(valid_timelines)}"
    
    # Set defaults for vibe coder principles (assume starting small)
    planning_sessions[session_id].user_scale = "small_start"  # Always assume starting small
    planning_sessions[session_id].timeline = timeline
    
    await ctx.info(f"Updated timeline for session {session_id} (assuming small start per vibe coder principles)")
    
    return f"""Great! Timeline: "{timeline}"

**Step 5: Budget and technical comfort (final step!)**

Please tell me:
- **Budget level?** Choose one:
  - "free_only" (free or very low cost only)
  - "low_cost" (can spend a little bit ~$10-50/month)
  - "reasonable" (reasonable budget for a good solution ~$50-200/month)
  - "flexible" (budget is not a major constraint)

- **Technical comfort?** Choose one:
  - "avoid_technical" (I avoid technical things when possible)
  - "basic_setup" (I can handle basic setup with good instructions)
  - "some_technical" (I'm comfortable with some technical work)
  - "enjoy_technical" (I enjoy diving into technical details)

Use the `finalize_planning` tool to get your recommendations!"""


@mcp.tool()
async def finalize_planning(ctx: Context, timeline: str, budget_level: str, technical_comfort: str, session_id: Optional[str] = None) -> str:
    """
    Finalize the planning process and get tech stack recommendations.
    
    Args:
        timeline: When you need this (experimental, few_weeks, month_or_two, urgent)
        budget_level: Budget level (free_only, low_cost, reasonable, flexible)
        technical_comfort: Technical comfort level (avoid_technical, basic_setup, some_technical, enjoy_technical)
        session_id: Optional session ID (will use most recent if not provided)
    """
    if not session_id:
        if not planning_sessions:
            return "No active planning session. Please start with `start_project_planning` first."
        session_id = max(planning_sessions.keys())
    
    if session_id not in planning_sessions:
        return f"Session {session_id} not found. Please start a new planning session."
    
    # Validate inputs
    valid_timelines = ["experimental", "few_weeks", "month_or_two", "urgent"]
    valid_budgets = ["free_only", "low_cost", "reasonable", "flexible"]
    valid_comfort = ["avoid_technical", "basic_setup", "some_technical", "enjoy_technical"]
    
    if timeline not in valid_timelines:
        return f"Invalid timeline. Please choose one of: {', '.join(valid_timelines)}"
    
    if budget_level not in valid_budgets:
        return f"Invalid budget_level. Please choose one of: {', '.join(valid_budgets)}"
    
    if technical_comfort not in valid_comfort:
        return f"Invalid technical_comfort. Please choose one of: {', '.join(valid_comfort)}"
    
    planning_sessions[session_id].timeline = timeline
    planning_sessions[session_id].budget_level = budget_level
    planning_sessions[session_id].technical_comfort = technical_comfort
    # Always assume starting small (vibe coder principle)
    planning_sessions[session_id].user_scale = "small_start"
    
    await ctx.info(f"Finalizing recommendations for session {session_id}")
    
    # Generate recommendations
    requirements = planning_sessions[session_id]
    recommendations = await _analyze_requirements(requirements)
    
    return f"""🎉 Perfect! Based on everything you've told me, here's my recommendation:

**Your Project Summary:**
- Vision: {requirements.project_vision}
- Users: {requirements.target_users}
- Timeline: {requirements.timeline}
- Budget: {requirements.budget_level}, Technical comfort: {requirements.technical_comfort}
- Approach: Starting small and scaling up (vibe coder best practice)

**Recommended Tech Stack:**
{recommendations['stack_summary']}

**Why this works for you:**
{recommendations['reasoning']}

**Estimated monthly cost:** {recommendations['cost_estimate']}
**Setup complexity:** {recommendations['complexity_level']}

Use the `get_deployment_guide` tool to get step-by-step instructions for setting this up!

You can also use `explain_recommendation` if you want more details about why I suggested this approach."""


@mcp.tool()
async def recommend_stack(session_requirements: Optional[str] = None) -> str:
    """
    Get tech stack recommendations. If you haven't completed the planning process,
    this will start it for you.
    
    Args:
        session_requirements: Optional JSON string of requirements if you want to skip the interactive process
    """
    
    if session_requirements:
        # Direct recommendation from provided requirements
        try:
            req_data = json.loads(session_requirements)
            requirements = ProjectRequirements(**req_data)
            recommendations = await _analyze_requirements(requirements)
            
            return f"""**Tech Stack Recommendation:**

{recommendations['stack_summary']}

**Reasoning:** {recommendations['reasoning']}
**Estimated Cost:** {recommendations['cost_estimate']}
**Setup Complexity:** {recommendations['complexity_level']}"""
            
        except (json.JSONDecodeError, TypeError) as e:
            return f"Error parsing requirements: {e}. Please use start_project_planning instead."
    
    else:
        # No session provided, start the interactive process
        return await start_project_planning()


@mcp.tool()
async def explain_recommendation(detail_level: str = "detailed") -> str:
    """
    Get a detailed explanation of why specific technologies were recommended.
    
    Args:
        detail_level: "basic" for simple explanation or "detailed" for technical details
    """
    
    if not planning_sessions:
        return "No active planning sessions. Please run start_project_planning first."
    
    # Get the most recent session
    latest_session = max(planning_sessions.keys())
    requirements = planning_sessions[latest_session]
    
    if detail_level == "basic":
        return f"""**Why I recommended this stack for your project:**

Based on your vision: "{requirements.project_vision[:100]}..."

• **Easy to start:** The tools I suggested are designed for people who want to focus on their idea, not wrestle with technical setup
• **Grows with you:** These platforms automatically handle more users without you having to rebuild everything
• **Budget-friendly:** Fits your {requirements.budget_level.replace('_', ' ')} budget with predictable costs
• **Timeline-appropriate:** You can get a working version deployed in {requirements.timeline.replace('_', ' ')}

The combination of these tools means you spend time building features users want, not managing servers or databases."""
    
    else:
        # Detailed technical explanation
        return f"""**Detailed Technical Reasoning:**

**Project Analysis:**
- Vision: {requirements.project_vision}
- Users: {requirements.target_users}
- Scale: {requirements.user_scale} users expected
- Timeline: {requirements.timeline}
- Budget: {requirements.budget_level}
- Technical comfort: {requirements.technical_comfort}

**Architecture Decisions:**

1. **Frontend Choice:** Modern React-based approach because:
   - Large community and excellent documentation
   - Component-based architecture scales well
   - Great tooling and development experience
   
2. **Backend Strategy:** Platform-as-a-Service approach because:
   - Reduces operational overhead (no server management)
   - Built-in scaling and security features
   - Pay-as-you-grow pricing model
   
3. **Database Selection:** Based on your data needs:
   - Managed databases reduce maintenance burden
   - Built-in backup and security features
   - Automatic scaling capabilities
   
4. **Hosting Platform:** Cloud-native deployment because:
   - Global CDN for fast performance
   - Automatic HTTPS and security
   - Integrated CI/CD pipelines

This stack follows modern "Jamstack" principles: JavaScript frontend, APIs, and Markup pre-built where possible."""


@mcp.tool()
async def get_deployment_guide(platform: str = "recommended") -> str:
    """
    Get step-by-step deployment instructions for your recommended stack.
    
    Args:
        platform: "recommended", "vercel", "netlify", "supabase", or "all"
    """
    
    if not planning_sessions:
        return """No active planning session found. Here's a general deployment guide for beginners:

**Quick Start Deployment (Recommended Stack):**

1. **Set up your development environment:**
   ```bash
   # Install Node.js from nodejs.org
   # Install VS Code as your editor
   ```

2. **Create your project:**
   ```bash
   npx create-next-app@latest my-project
   cd my-project
   ```

3. **Deploy to Vercel (easiest option):**
   - Sign up at vercel.com with your GitHub account
   - Connect your GitHub repository
   - Click "Deploy" - it handles everything automatically!

4. **Add a custom domain:**
   - Buy domain from Namecheap or Google Domains
   - Add it in Vercel dashboard under "Domains"

**Total setup time:** 15-30 minutes for a basic site!"""
    
    # Get most recent session
    latest_session = max(planning_sessions.keys())
    requirements = planning_sessions[latest_session]
    
    guide = f"""**Deployment Guide for Your Project**

Based on your requirements, here's your step-by-step deployment plan:

**Phase 1: Setup (Day 1)**
1. **Install development tools:**
   - Download VS Code (free code editor): code.visualstudio.com
   - Install Node.js (JavaScript runtime): nodejs.org
   - Create GitHub account if you don't have one

2. **Create your project:**
   ```bash
   npx create-next-app@latest {requirements.project_vision.lower().replace(' ', '-')[:20]}
   cd {requirements.project_vision.lower().replace(' ', '-')[:20]}
   ```

**Phase 2: Basic Deployment (Day 1-2)**
1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Initial project setup"
   git push origin main
   ```

2. **Deploy to Vercel:**
   - Go to vercel.com and sign up with GitHub
   - Click "New Project" and import your repository
   - Click "Deploy" - done!
   - Your site will be live at: your-project.vercel.app

**Phase 3: Add Features (Days 3-7)**
"""
    
    # Add specific features based on their requirements
    if any('auth' in feature.lower() or 'login' in feature.lower() for feature in requirements.core_features):
        if 'neon' in guide.lower():
            guide += """
3. **Add user authentication with Neon Auth (beta):**
   ```bash
   npm install @neondatabase/serverless @auth/core
   ```
   - Sign up at neon.tech (generous free tier)
   - Enable Neon Auth in beta features
   - Built-in authentication with your database
   - OR use Clerk for more features: npm install @clerk/nextjs
"""
        else:
            guide += """
3. **Add user authentication:**
   ```bash
   npm install @supabase/supabase-js
   ```
   - Sign up at supabase.com (free)
   - Create new project
   - Copy your project URL and API key
   - Add to your environment variables in Vercel
"""
    
    if any('database' in req.lower() or 'store' in req.lower() for req in [requirements.data_needs]):
        guide += """
4. **Set up database:**
   - Modern serverless PostgreSQL with automatic scaling
   - Use visual table editor to create your data structure
   - No SQL knowledge required to get started!
   - Branching and point-in-time recovery included
"""
    
    guide += f"""
**Phase 4: Custom Domain (Optional)**
- Buy domain from Namecheap (~$12/year)
- Add in Vercel dashboard under "Domains"
- Automatic HTTPS included!

**Expected Timeline:** {requirements.timeline.replace('_', ' ')}
**Budget:** Starts free, scales with usage

**Need help?** Each platform has excellent documentation and community support!"""
    
    return guide


if __name__ == "__main__":
    mcp.run()