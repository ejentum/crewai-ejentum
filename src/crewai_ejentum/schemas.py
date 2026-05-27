"""Pydantic schemas for :class:`crewai_ejentum.EjentumHarnessTool`."""

from typing import Literal

from pydantic import BaseModel, Field


HarnessMode = Literal[
    "reasoning",
    "code",
    "anti-deception",
    "memory",
    "adaptive-reasoning",
    "adaptive-code",
    "adaptive-anti-deception",
    "adaptive-memory",
]


class EjentumHarnessParams(BaseModel):
    """Arguments for a single Ejentum harness call."""

    query: str = Field(
        ...,
        description=(
            "A 1-2 sentence description of the task the agent is about to work on. "
            "For mode='memory' or 'adaptive-memory', format as: \"I noticed [X]. "
            "This might mean [Y]. Sharpen: [Z].\""
        ),
        min_length=1,
    )
    mode: HarnessMode = Field(
        ...,
        description=(
            "Which cognitive harness to retrieve an injection from. Four dynamic "
            "modes (single retrieval, all tiers): 'reasoning' for analytical, "
            "diagnostic, planning, multi-step tasks. 'code' for code generation, "
            "refactoring, review, debugging. 'anti-deception' when the prompt "
            "pressures the agent to validate, certify, or soften an honest "
            "assessment. 'memory' only when sharpening an observation already "
            "formed about cross-turn drift. Four adaptive modes (top-k retrieval "
            "+ LLM adapter rewrites the operation to fit the specific task; "
            "Go or Super tier required): 'adaptive-reasoning', 'adaptive-code', "
            "'adaptive-anti-deception', 'adaptive-memory'. Use adaptive when the "
            "dynamic mode is too generic for the task at hand, or for high-stakes "
            "work where every step should already be mapped to the specifics."
        ),
    )
