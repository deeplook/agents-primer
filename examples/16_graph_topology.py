"""Inspect SDK handoffs as graph edges before running any model."""

from _shared import demo_model
from agents import Agent, Handoff


def main() -> None:
    billing = Agent(name="Billing", model=demo_model())
    technical = Agent(name="Technical", model=demo_model())
    triage = Agent(name="Triage", model=demo_model(), handoffs=[billing, technical])
    agents = [triage, billing, technical]
    graph = {
        agent.name: [
            edge.agent_name if isinstance(edge, Handoff) else edge.name
            for edge in agent.handoffs
        ]
        for agent in agents
    }
    assert all(target in graph for edges in graph.values() for target in edges)
    print(f"OK: SDK handoff graph={graph}")


if __name__ == "__main__":
    main()
