"""crewai-ejentum: CrewAI tool for the Ejentum Reasoning Harness.

Exposes :class:`EjentumHarnessTool` as an agent-callable CrewAI tool. Each call
retrieves a task-matched cognitive operation from a library of 679, engineered in
two layers: a natural-language procedure plus an executable reasoning topology
(graph DAG with gates, parallel branches, and meta-cognitive exit nodes). The
calling LLM ingests both layers before writing.

Free tier: 100 calls, no card required, at https://ejentum.com/pricing.
"""

from crewai_ejentum.tool import EjentumHarnessTool
from crewai_ejentum.schemas import EjentumHarnessParams, HarnessMode

__all__ = ["EjentumHarnessTool", "EjentumHarnessParams", "HarnessMode"]
__version__ = "0.1.0"
