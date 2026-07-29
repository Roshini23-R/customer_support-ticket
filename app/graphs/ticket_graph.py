from typing import TypedDict
from langgraph.graph import StateGraph, START, END

from app.graphs.nodes import (
    classify_node,
    retrieve_node,
    resolve_node,
    escalate_node,
    route_after_classification,
    route_after_retrieval,
)



from .ticket_input import TicketInput

def build_ticket_graph():
    # Use TicketInput instead of plain dict so LangServe can infer the input schema.
    graph = StateGraph(TicketInput)

    # Nodes
    graph.add_node("classify", classify_node)
    graph.add_node("retrieve", retrieve_node)
    graph.add_node("resolve", resolve_node)
    graph.add_node("escalate", escalate_node)

    # Edges
    graph.add_edge(START, "classify")

    graph.add_conditional_edges(
        "classify",
        route_after_classification,
        {
            "retrieve": "retrieve",
            "escalate": "escalate",
        },
    )

    graph.add_conditional_edges(
        "retrieve",
        route_after_retrieval,
        {
            "resolve": "resolve",
            "escalate": "escalate",
        },
    )

    graph.add_edge("resolve", END)
    graph.add_edge("escalate", END)

    return graph.compile()


graph = build_ticket_graph()



