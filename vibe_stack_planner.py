#!/usr/bin/env python3
"""
Vibe Coder Stack Planner MCP Server

A Model Context Protocol server that helps non-technical builders ("vibe coders") 
plan the right tech stack for their ideas through progressive questioning using 
the MCP elicitation spec.

This server focuses on:
- Simple, jargon-free questions
- Platform-as-a-Service recommendations
- Practical deployment guidance
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

# Elicitation data structures
@dataclass
class ProjectVisionInput:
    """Input structure for project vision elicitation"""
    project_vision: str

@dataclass
class UserInfoInput:
    """Input structure for target users and interaction"""
    target_users: str
    user_interaction: str

@dataclass
class FeatureDataInput:
    """Input structure for features and data needs"""
    core_features: str
    data_needs: str

@dataclass
class ScaleTimelineInput:
    """Input structure for scale and timeline"""
    user_scale: Literal["personal", "small_community", "hundreds", "thousands_plus"]
    timeline: Literal["experimental", "few_weeks", "month_or_two", "urgent"]

@dataclass
class ResourcesInput:
    """Input structure for budget and technical comfort"""
    budget_level: Literal["free_only", "low_cost", "reasonable", "flexible"]
    technical_comfort: Literal["avoid_technical", "basic_setup", "some_technical", "enjoy_technical"]


# Initialize the MCP server
mcp = FastMCP("Vibe Coder Stack Planner")

# In-memory storage for active planning sessions
planning_sessions: Dict[str, ProjectRequirements] = {}


@mcp.tool()
async def start_project_planning(ctx: Context) -> str:
    """
    Start the project planning process by gathering basic information about what you want to build.
    
    This will ask you simple questions about your idea - no technical knowledge required!
    """
    # Create a unique session ID for this planning session
    session_id = f"planning_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    planning_sessions[session_id] = ProjectRequirements()
    
    await ctx.info("Starting project planning process...")
    
    # Begin elicitation flow - Step 1: Project Vision
    result = await ctx.elicit(
        message="""Let's start planning your project! First, tell me about your vision.

What problem are you trying to solve, or what idea do you want to build? 
Think about it like you're explaining to a friend - what would this thing do and why would people want to use it?""",
        response_type=ProjectVisionInput
    )
    
    if result.action == "accept":
        planning_sessions[session_id].project_vision = result.data.project_vision
        
        # Continue to step 2
        return await _ask_about_users(session_id, ctx)
    elif result.action == "decline":
        return "No problem! Feel free to start again when you're ready to plan your project."
    else:
        return "Planning cancelled. You can restart anytime with start_project_planning."


async def _ask_about_users(session_id: str, ctx: Context) -> str:
    """Step 2: Ask about target users and how they'll interact"""
    result = await ctx.elicit(
        message="""Great! Now let's talk about who will use this.

Who do you imagine using your project? Are they:
- People like you who have a specific problem to solve?
- Businesses that need this functionality?
- General consumers who would find this useful?
- A specific community or group?

Also, how do you picture them using it? Will they:
- Visit a website and use it occasionally?
- Use it regularly as part of their daily routine?
- Access it on their phone while on the go?
- Need to collaborate with others?""",
        response_type=UserInfoInput
    )
    
    if result.action == "accept":
        planning_sessions[session_id].target_users = result.data.target_users
        planning_sessions[session_id].user_interaction = result.data.user_interaction
        
        return await _ask_about_features(session_id, ctx)
    elif result.action == "decline":
        return "No worries! You can restart the planning process anytime."
    else:
        return "Planning cancelled. Feel free to start over when ready."


async def _ask_about_features(session_id: str, ctx: Context) -> str:
    """Step 3: Ask about core features and data needs"""
    result = await ctx.elicit(
        message="""Perfect! Now let's think about what your project actually needs to do.

What are the main things people will do with your project? For example:
- Will they create accounts and log in?
- Do they need to store or upload information?
- Will they search for things or browse content?
- Do they need to communicate with others?
- Will there be payments or transactions?
- Does it need to send notifications or emails?

Also, what kind of information will your project work with?
- User profiles and preferences?
- Documents, images, or files?
- Data from other websites or services?
- Real-time information that changes frequently?""",
        response_type=FeatureDataInput
    )
    
    if result.action == "accept":
        # Parse core features into a list
        features_text = result.data.core_features
        planning_sessions[session_id].core_features = [f.strip() for f in features_text.split(',') if f.strip()]
        planning_sessions[session_id].data_needs = result.data.data_needs
        
        return await _ask_about_scale(session_id, ctx)
    elif result.action == "decline":
        return "No problem! You can restart the planning process anytime."
    else:
        return "Planning cancelled. Feel free to start over when ready."


async def _ask_about_scale(session_id: str, ctx: Context) -> str:
    """Step 4: Ask about expected scale and timeline"""
    result = await ctx.elicit(
        message="""Great! Let's talk about your expectations for growth and timing.

How many people do you think might use this?
When do you want to have something working?""",
        response_type=ScaleTimelineInput
    )
    
    if result.action == "accept":
        planning_sessions[session_id].user_scale = result.data.user_scale
        planning_sessions[session_id].timeline = result.data.timeline
        
        return await _ask_about_resources(session_id, ctx)
    elif result.action == "decline":
        return "No problem! You can restart the planning process anytime."
    else:
        return "Planning cancelled. Feel free to start over when ready."


async def _ask_about_resources(session_id: str, ctx: Context) -> str:
    """Step 5: Ask about budget and technical comfort level"""
    result = await ctx.elicit(
        message="""Almost done! Last questions about resources and comfort level.

What's your budget situation for this project?
How comfortable are you with technical stuff?""",
        response_type=ResourcesInput
    )
    
    if result.action == "accept":
        planning_sessions[session_id].budget_level = result.data.budget_level
        planning_sessions[session_id].technical_comfort = result.data.technical_comfort
        
        # Generate recommendations
        return await _generate_recommendations(session_id, ctx)
    elif result.action == "decline":
        return "No problem! You can restart the planning process anytime."
    else:
        return "Planning cancelled. Feel free to start over when ready."


async def _generate_recommendations(session_id: str, ctx: Context) -> str:
    """Generate final tech stack recommendations based on gathered requirements"""
    requirements = planning_sessions.get(session_id)
    if not requirements:
        return "Error: Planning session not found. Please start over."
    
    await ctx.info("Analyzing your requirements and generating recommendations...")
    
    # This is where we'd call the recommendation engine
    recommendations = await _analyze_requirements(requirements)
    
    return f"""🎉 Perfect! Based on what you've told me, here's my recommendation:

**Recommended Tech Stack:**
{recommendations['stack_summary']}

**Why this works for you:**
{recommendations['reasoning']}

**Estimated monthly cost:** {recommendations['cost_estimate']}
**Setup complexity:** {recommendations['complexity_level']}

Use the `get_deployment_guide` tool to get step-by-step instructions for setting this up!

You can also use `explain_recommendation` if you want more details about why I suggested this approach."""


async def _analyze_requirements(requirements: ProjectRequirements) -> Dict[str, str]:
    """Analyze requirements and generate recommendations using system prompt"""
    
    # This is our recommendation engine - could be enhanced with LLM calls
    # For now, using rule-based logic
    
    recommendations = {
        "stack_summary": "",
        "reasoning": "",
        "cost_estimate": "",
        "complexity_level": ""
    }
    
    # Analyze data needs and features to determine architecture
    needs_database = any(keyword in requirements.data_needs.lower() + ' '.join(requirements.core_features).lower() 
                        for keyword in ['store', 'save', 'profile', 'user', 'account', 'data'])
    
    needs_auth = any(keyword in ' '.join(requirements.core_features).lower() 
                    for keyword in ['login', 'account', 'user', 'profile'])
    
    needs_real_time = any(keyword in requirements.data_needs.lower() + ' '.join(requirements.core_features).lower()
                         for keyword in ['chat', 'message', 'notification', 'real-time', 'live'])
    
    # Determine frontend approach
    if requirements.user_interaction.lower().find('phone') != -1 or requirements.user_interaction.lower().find('mobile') != -1:
        frontend_rec = "React Native with Expo (works on both iPhone and Android)"
    else:
        frontend_rec = "Next.js (React framework) for a modern web app"
    
    # Determine backend and database
    if requirements.technical_comfort in ['avoid_technical', 'basic_setup']:
        if needs_database:
            backend_rec = "Supabase (handles database, auth, and API automatically)"
        else:
            backend_rec = "Vercel Functions (serverless, no server management)"
    else:
        if needs_database:
            backend_rec = "Next.js API routes with PlanetScale MySQL database"
        else:
            backend_rec = "Vercel or Netlify Functions"
    
    # Determine hosting
    if requirements.budget_level == 'free_only':
        hosting_rec = "Vercel (free tier covers most small projects)"
    elif requirements.budget_level == 'low_cost':
        hosting_rec = "Vercel Pro or Netlify Pro ($20/month)"
    else:
        hosting_rec = "Vercel Pro with premium add-ons as needed"
    
    # Build recommendation
    recommendations["stack_summary"] = f"""
• Frontend: {frontend_rec}
• Backend: {backend_rec}
• Hosting: {hosting_rec}
• Domain: Namecheap or Google Domains (~$12/year)
"""
    
    # Build reasoning
    reasoning_parts = []
    if requirements.technical_comfort in ['avoid_technical', 'basic_setup']:
        reasoning_parts.append("I chose beginner-friendly tools that handle most technical details automatically")
    
    if requirements.timeline in ['urgent', 'few_weeks']:
        reasoning_parts.append("These tools let you build and deploy quickly")
    
    if requirements.budget_level == 'free_only':
        reasoning_parts.append("This stack has generous free tiers to keep costs minimal")
    
    if requirements.user_scale in ['thousands_plus', 'hundreds']:
        reasoning_parts.append("These platforms scale automatically as you grow")
    
    recommendations["reasoning"] = ". ".join(reasoning_parts) + "."
    
    # Cost estimate
    if requirements.budget_level == 'free_only':
        recommendations["cost_estimate"] = "$0-15/month (domain + potential overages)"
    elif requirements.budget_level == 'low_cost':
        recommendations["cost_estimate"] = "$20-40/month"
    else:
        recommendations["cost_estimate"] = "$50-150/month with room to scale"
    
    # Complexity
    if requirements.technical_comfort in ['avoid_technical', 'basic_setup']:
        recommendations["complexity_level"] = "Low - mostly drag-and-drop with good documentation"
    else:
        recommendations["complexity_level"] = "Medium - some coding required but well-supported"
    
    return recommendations


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
   - Supabase automatically provides PostgreSQL database
   - Use their visual table editor to create your data structure
   - No SQL knowledge required!
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