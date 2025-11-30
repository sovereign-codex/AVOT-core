"""Runtime stubs for executing AVOTs."""

import logging
from typing import Any

from .registry import get_agent

logger = logging.getLogger(__name__)


def run_agent(agent_id: str, **kwargs: Any) -> None:
    """Simulate running an AVOT.

    Looks up the agent spec by id and logs what would be executed. This is a
    placeholder for future integration with dedicated AVOT repositories.
    """

    agent = get_agent(agent_id)
    if agent is None:
        raise ValueError(f"Agent '{agent_id}' is not registered.")

    message = (
        "[AVOT runtime] would execute %(agent)s via %(module)s.%(func)s with args %(kwargs)s"
    )
    logger.info(message, {
        "agent": agent.id,
        "module": agent.entrypoint.module,
        "func": agent.entrypoint.function,
        "kwargs": kwargs,
    })
    print(message % {
        "agent": agent.id,
        "module": agent.entrypoint.module,
        "func": agent.entrypoint.function,
        "kwargs": kwargs,
    })
