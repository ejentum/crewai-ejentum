"""crewai-ejentum: CrewAI tool for the Ejentum Reasoning Harness.

Exposes :class:`EjentumHarnessTool` as an agent-callable CrewAI tool with a
``mode`` parameter covering eight modes: four dynamic (``reasoning``, ``code``,
``anti-deception``, ``memory``) and four adaptive (``adaptive-reasoning``,
``adaptive-code``, ``adaptive-anti-deception``, ``adaptive-memory``) that
pre-fit the cognitive operation to the caller's task via an adapter LLM.
Adaptive modes require the Go or Super tier.

Each call retrieves a task-matched cognitive operation from a library of 679,
engineered in two layers: a natural-language procedure plus an executable
reasoning topology (graph DAG with gates, parallel branches, and
meta-cognitive exit nodes). The calling LLM ingests both layers before writing.

Pricing at https://ejentum.com/pricing.
"""

from crewai_ejentum.tool import EjentumHarnessTool
from crewai_ejentum.schemas import EjentumHarnessParams, HarnessMode

__all__ = ["EjentumHarnessTool", "EjentumHarnessParams", "HarnessMode"]
__version__ = "0.2.0"
