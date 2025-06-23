import datetime
import os
from zoneinfo import ZoneInfo
from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, SseConnectionParams

api_base = os.getenv("OPENAI_API_BASE")
api_key = os.getenv("OPENAI_API_KEY")

toolset = MCPToolset(
    connection_params=SseConnectionParams(url="http://mcp:3001/sse", headers={}),
    tool_filter=['cubejs_cubesql', 'cubejs_meta']
)

cubesight_agent = LlmAgent(
    name="cubesight_agent",
    model=LiteLlm(
        model="openai/gpt-4o-mini",
        api_base=api_base,
        api_key=api_key
    ),
    description=(
        "Agent to understand cube schema and query cube for data."
    ),
    instruction=(
        "You are a helpful agent who can query data."
    ),
    tools=[toolset]
)

plot_agent = LlmAgent(
    name="plot_agent",
    model=LiteLlm(
        model="openai/gpt-4o-mini",
        api_base=api_base,
        api_key=api_key
    ),
    description=(
        """Create a React data visualization component that:
           - Connects to CubeJS data and renders charts using Recharts
           - Is a complete, self-contained single file ready for Electron
           - Automatically selects the most appropriate chart type based on the data structure
           - Fetches and analyzes cube metadata to determine optimal visualization
           - Handles multiple data types (time series, categorical, numerical comparisons)
           - Includes responsive design and error handling
           - Uses modern React hooks and clean code patterns
           - Returns only executable code without explanations or comments
           """
    ),
    instruction=(
        "You are a helpful agent who can plot visuals from cube data in React using Recharts."
    ),
)

greeting_agent = LlmAgent(
    name="greeting_agent",
    model=LiteLlm(
        model="openai/gpt-4o-mini",
        api_base=api_base,
        api_key=api_key
    ),
    description=(
        "Agent to greet user, manage session and delegate to pipeline agent."
    ),
    instruction=(
        "You are a helpful agent who can greet user, manage session and delegate to pipeline agent. Do not use tools directly. Restrict conversation to pipeline agent."
    ),
    sub_agents=[cubesight_agent, plot_agent]
)

root_agent = greeting_agent