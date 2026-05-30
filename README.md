# crewai-ejentum

[CrewAI](https://crewai.com) tool for the Ejentum Reasoning Harness. Exposes a single `EjentumHarnessTool` class with a `mode` parameter covering eight values: four dynamic (`reasoning`, `code`, `anti-deception`, `memory`) and four adaptive (`adaptive-reasoning`, `adaptive-code`, `adaptive-anti-deception`, `adaptive-memory`).

Use the harness before the agent generates on complex, multi-step, or multi-constraint tasks where the model's default reasoning template would miss a constraint, take a shortcut, or drift across turns. Each call returns a *cognitive operation*: a structured procedure (numbered steps with a failure pattern to refuse and a falsification test) paired with an executable reasoning topology (a DAG of those steps with decision gates, parallel branches, bounded loops, and meta-cognitive exit nodes). The agent reads both layers before producing its response.

Dynamic modes return the top-1 abstract operation from the matching library; adaptive modes additionally run an adapter LLM that rewrites the operation with task-specific identifiers. Adaptive modes require the Go or Super tier.

## Install

```bash
pip install crewai-ejentum
```

## Configuration

```bash
export EJENTUM_API_KEY="ej_..."
```

`EJENTUM_API_KEY` is read from the environment at call time. Get a key at [ejentum.com/pricing](https://ejentum.com/pricing).

## Usage

```python
from crewai import Agent, Task, Crew
from crewai_ejentum import EjentumHarnessTool

harness = EjentumHarnessTool()

architect = Agent(
    role="Senior architect",
    goal="Evaluate technical decisions honestly",
    backstory="Pragmatic; pushes back on sunk-cost framings.",
    tools=[harness],
)

task = Task(
    description=(
        "We have spent three months on the GraphQL gateway. It's mostly done. "
        "Should we keep going or pivot to REST? "
        "Call the Ejentum harness with mode='anti-deception' first."
    ),
    agent=architect,
    expected_output="A recommendation that separates past spending from prospective evaluation.",
)

Crew(agents=[architect], tasks=[task]).kickoff()
```

## Modes

| Mode | Library size | Domain |
|---|---:|---|
| `reasoning` | 311 | abstraction, time, causality, simulation, spatial, metacognition |
| `code` | 128 | software-engineering layer |
| `anti-deception` | 139 | sycophancy, hallucination, deception, adversarial framing, judgment, executive control |
| `memory` | 101 | perception layer (filter-oriented; not for fact extraction) |
| `adaptive-reasoning` | 311 (same pool) | with adapter LLM rewriting procedure + topology for the specific task |
| `adaptive-code` | 128 | same as above for code |
| `adaptive-anti-deception` | 139 | same as above for anti-deception |
| `adaptive-memory` | 101 | same as above for memory |

## Inputs

`EjentumHarnessTool._run` accepts:

- `query` (string, required): a 1-2 sentence description of the task. For `mode="memory"` or `"adaptive-memory"`, use the format `"I noticed X. This might mean Y. Sharpen: Z."`.
- `mode` (string, required): one of the eight mode strings above.

Returns the injection as a string. Errors return as human-readable strings; the tool does not raise, so an agent step never crashes the run.

## API reference

```python
EjentumHarnessTool(
    api_url: str = "https://api.ejentum.com/harness/",
    timeout_seconds: float = 10.0,
)
```

| Field | Default | Description |
|---|---|---|
| `api_url` | `https://api.ejentum.com/harness/` | Override for self-hosted gateway. |
| `timeout_seconds` | `10.0` | Per-call HTTP timeout. |

## Wire contract

```
POST https://api.ejentum.com/harness/
Headers: Authorization: Bearer <key>, Content-Type: application/json
Body:    { "query": <string>, "mode": <one of 8 mode strings> }
Response (200): [ { "<mode>": "<injection string>" } ]
Response (401|403|429): { "error": "..." }
```

Full wire contract, field structure of an injection, DAG syntax, and a canonical dynamic-vs-adaptive comparison on the same query are documented in the [ejentum-mcp README](https://github.com/ejentum/ejentum-mcp#wire-contract).

## ejentum-mcp alternative

The same eight modes are exposed as MCP tools at `https://api.ejentum.com/mcp`. If you prefer that route, CrewAI's MCP support can consume the hosted endpoint with Bearer auth.

## Compatibility

- Python 3.10+
- `crewai>=0.40.0`
- `requests>=2.31.0`

## License

[MIT](./LICENSE)


## Measured effects

The Ejentum harness is benchmarked publicly under CC BY 4.0 at [github.com/ejentum/benchmarks](https://github.com/ejentum/benchmarks):

- **ELEPHANT** sycophancy: 5.8% composite on GPT-4o (40 real Reddit scenarios)
- **LiveCodeBench Hard**: 85.7% to 100% on Claude Opus (28 competitive programming tasks)
- **Memory retention**: 50% fewer stale facts served (20-turn implicit state changes)
- Plus per-harness numbers across BBH/CausalBench/MuSR, ARC-AGI-3, SciCode, and perception tasks

Methodology, scenarios, run scripts, and raw outputs are all in-repo.
