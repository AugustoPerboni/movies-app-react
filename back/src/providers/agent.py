from agno.agent import Agent
from agno.models.openai import OpenAIResponses
from src.providers.settings_provider import settings
from agno.os import AgentOS
from agno.os.interfaces.agui import AGUI


def get_agno_assist():
    agno_assist = Agent(
        name="Agno Assist",
        model=OpenAIResponses(id="gpt-5.4-nano",api_key=settings.openai_api_key,),
        # tools=[MCPTools(url="https://docs.agno.com/mcp")],  # Agno docs via MCP
        add_datetime_to_context=True,
        add_history_to_context=True,     # include past runs
        num_history_runs=3,              # last 3 conversations
        markdown=True,
        followups=True,
    )
    return agno_assist



def create_app(base_app):
    agno_assist = get_agno_assist()
    agent_os = AgentOS(
        agents=[agno_assist], 
        interfaces=[AGUI(agent=agno_assist)], 
        tracing=True,
        base_app=base_app,
        )
    return agent_os.get_app()
