"""Ejentum Reasoning Harness tool for CrewAI.

Exposes the four Ejentum cognitive harnesses (reasoning, code, anti-deception,
memory) as a single agent-callable CrewAI tool. Each call retrieves a
task-matched cognitive operation from a library of 679, engineered in two
layers: a natural-language procedure (named failure pattern, executable steps,
suppression vectors, falsification test) plus an executable reasoning topology
(graph DAG with decision gates, parallel branches, and meta-cognitive exit
nodes that let the model pause to self-observe and re-enter). The agent
ingests both layers and writes from them.

Free tier: 100 calls, no card required, at https://ejentum.com/pricing.
"""

from __future__ import annotations

import os
from typing import Any

import requests
from crewai.tools import BaseTool, EnvVar
from pydantic import Field

from crewai_ejentum.schemas import EjentumHarnessParams


DEFAULT_API_URL = "https://api.ejentum.com/harness/"


class EjentumHarnessTool(BaseTool):
    """Retrieve a task-matched cognitive operation from the Ejentum Reasoning Harness.

    The Ejentum library contains 679 cognitive operations across four harnesses.
    Each operation is engineered in two layers: a natural-language procedure
    (named failure pattern, executable steps, suppression vectors, falsification
    test) plus an executable reasoning topology (graph DAG with decision gates,
    parallel branches, bounded loops, and meta-cognitive exit nodes where the
    model pauses to self-observe and re-enters). Injected before the LLM step
    to harden reasoning against decay on complex tasks and long agent loops.

    Use ``mode='reasoning'`` before analytical, diagnostic, planning, or
    multi-step tasks (311 operations spanning abstraction, time, causality,
    simulation, spatial, metacognition). Use ``mode='code'`` before producing
    or reviewing code (128 operations in the software-engineering layer). Use
    ``mode='anti-deception'`` when a prompt pressures the agent to validate,
    certify, or soften an honest assessment (139 operations spanning sycophancy,
    hallucination, deception, adversarial framing, judgment, executive control).
    Use ``mode='memory'`` only when sharpening an observation already formed
    about cross-turn drift (101 operations in the perception layer).

    Requires the ``EJENTUM_API_KEY`` environment variable. Free tier (100 calls,
    no card) at https://ejentum.com/pricing.
    """

    name: str = "Ejentum Reasoning Harness"
    description: str = (
        "Retrieve a task-matched cognitive operation from Ejentum's library of 679 "
        "across four harnesses (reasoning, code, anti-deception, memory). Each "
        "operation is engineered in two layers: a natural-language procedure "
        "(named failure pattern, steps, suppression vectors, falsification test) "
        "plus an executable reasoning topology (graph DAG with gates, parallel "
        "branches, and meta-cognitive exits). The agent ingests both layers "
        "before responding."
    )
    args_schema: type = EjentumHarnessParams
    api_url: str = DEFAULT_API_URL
    timeout_seconds: float = 10.0
    env_vars: list[EnvVar] = Field(
        default_factory=lambda: [
            EnvVar(
                name="EJENTUM_API_KEY",
                description=(
                    "API key for the Ejentum Logic API. Free tier (100 calls, "
                    "no card) at https://ejentum.com/pricing."
                ),
                required=True,
            ),
        ]
    )

    def _run(self, **kwargs: Any) -> str:
        raw_query = kwargs.get("query")
        query = raw_query.strip() if isinstance(raw_query, str) else ""
        mode = kwargs.get("mode")

        if not query:
            return "Ejentum harness call failed: 'query' is required."
        valid_modes = {
            "reasoning",
            "code",
            "anti-deception",
            "memory",
            "adaptive-reasoning",
            "adaptive-code",
            "adaptive-anti-deception",
            "adaptive-memory",
        }
        if mode not in valid_modes:
            return (
                f"Ejentum harness call failed: 'mode' must be one of "
                f"reasoning|code|anti-deception|memory|adaptive-reasoning|"
                f"adaptive-code|adaptive-anti-deception|adaptive-memory, "
                f"got '{mode}'."
            )

        api_key = os.environ.get("EJENTUM_API_KEY")
        if not api_key:
            return (
                "Ejentum harness call failed: EJENTUM_API_KEY environment "
                "variable is not set. Get a free key (100 calls, no card) at "
                "https://ejentum.com/pricing."
            )

        try:
            response = requests.post(
                self.api_url,
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json={"query": query, "mode": mode},
                timeout=self.timeout_seconds,
            )
        except requests.RequestException as exc:
            return f"Ejentum harness call failed: network error: {exc}"

        if response.status_code == 401:
            return (
                "Ejentum harness call failed: unauthorized (401). Check the "
                "EJENTUM_API_KEY value. Get a key at https://ejentum.com/pricing."
            )
        if response.status_code != 200:
            return (
                f"Ejentum harness call failed: HTTP {response.status_code}. "
                f"Response: {response.text[:300]}"
            )

        try:
            data = response.json()
        except ValueError:
            return (
                f"Ejentum harness call failed: response is not valid JSON. "
                f"Body: {response.text[:300]}"
            )

        # The API returns: [{<mode>: <scaffold_string>}]
        if isinstance(data, list) and data and isinstance(data[0], dict):
            scaffold = data[0].get(mode)
            if isinstance(scaffold, str) and scaffold:
                return scaffold

        return (
            f"Ejentum harness call returned an unexpected response shape: "
            f"{str(data)[:300]}"
        )
