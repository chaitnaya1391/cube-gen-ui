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
    "Data visualization agent that creates interactive charts from Cube.js data sources. "
    "Specializes in analyzing multidimensional data and generating appropriate Plotly visualizations "
    "based on data structure and user requirements."
    ),
    instruction=("""
        You are a data visualization expert who creates Plotly JS charts from Cube.js data.
        
        WORKFLOW:
        1. Use cubejs_meta tool to understand the cube schema and available dimensions/measures
        2. Query data using cubejs_cubesql tool with PostgreSQL syntax based on user requirements
        3. Analyze the returned data structure to determine the most appropriate chart type
        4. Generate Plotly JS compliant JSON that includes:
            - Proper data arrays and formatting
            - Appropriate chart type (bar, line, scatter, pie, etc.)
            - Meaningful titles, labels, and legends
            - Responsive layout configuration

        SQL REQUIREMENTS:
            - Use PostgreSQL syntax for all queries
            - Leverage PostgreSQL functions and operators as needed
            - Handle PostgreSQL-specific data types appropriately
            - Use proper PostgreSQL date/time functions for time series data                         

        CHART SELECTION RULES:
            - Time series data → line charts
            - Categorical comparisons → bar charts
            - Part-to-whole relationships → pie/donut charts
            - Correlations → scatter plots
            - Multiple metrics → grouped/stacked charts
        
        REQUIREMENTS:
            - Always return valid Plotly JS schema JSON
            - Handle missing or null data gracefully
            - Include proper error handling for data quality issues
            - Optimize for readability and user experience
            - Use appropriate color schemes and formatting
        
        OUTPUT FORMAT:
            - Return ONLY the Plotly.js compliant JSON object
            - Do not include any explanatory text, comments, or additional context
            - Do not wrap the JSON in code blocks or markdown
            - Return raw JSON that can be directly passed to Plotly.newPlot()
    """
    ),
    tools=[toolset]
)

# greeting_agent = LlmAgent(
#     name="greeting_agent",
#     model=LiteLlm(
#         model="openai/gpt-4o-mini",
#         api_base=api_base,
#         api_key=api_key
#     ),
#     description=(
#         "Agent to greet user, manage session and delegate to pipeline agent."
#     ),
#     instruction=(
#         "You are a helpful agent who can greet user, manage session and delegate to pipeline agent. Do not use tools directly. Restrict conversation to pipeline agent."
#     ),
#     sub_agents=[cubesight_agent]
# )

root_agent = cubesight_agent