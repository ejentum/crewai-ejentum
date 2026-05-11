# crewai-ejentum

A [CrewAI](https://crewai.com) tool that retrieves a task-matched **cognitive operation** from the [Ejentum](https://ejentum.com) Reasoning Harness and injects it into the agent's reasoning before it produces an answer.

Each operation in the Ejentum library (679 of them, organized across four harnesses) is engineered in **two layers**:

- a **natural-language procedure** the model can read, naming the steps to take and the failure pattern to refuse, and
- an **executable reasoning topology**: a graph-shaped plan over those steps. The plan names explicit decision points where the model branches, parallel branches that run and rejoin, bounded loops that run until convergence, named meta-cognitive moments where the model is asked to stop, look at its own working, and re-enter at a specific step, and escape paths for when the prescribed plan stops fitting the task at hand.

The natural-language layer tells the model *what* to do. The topology layer pins down *how* those steps connect: where to decide, where to loop, where to stop and look at itself. Together they act as a persistent attention anchor that survives long context windows and multi-turn execution chains, which is precisely where a model's own reasoning template typically decays.

## Installation

```bash
pip install crewai-ejentum
```

## Configuration

Get a free Ejentum API key (100 calls, no card required) at <https://ejentum.com/pricing> and set it in your environment:

```bash
export EJENTUM_API_KEY="zpka_..."
```

## Usage

```python
from crewai import Agent, Task, Crew
from crewai_ejentum import EjentumHarnessTool

harness = EjentumHarnessTool()

architect = Agent(
    role="Senior architect",
    goal="Evaluate technical decisions honestly",
    backstory="You are pragmatic and push back on sunk-cost framings.",
    tools=[harness],
)

task = Task(
    description=(
        "We've spent three months on the GraphQL gateway. It's mostly done. "
        "Should we keep going or pivot to REST? "
        "Call the Ejentum harness with mode='anti-deception' before answering."
    ),
    agent=architect,
    expected_output="A recommendation that separates past spending from prospective evaluation.",
)

Crew(agents=[architect], tasks=[task]).kickoff()
```

## The four harnesses

Pick the mode that matches what the agent is about to do:

| Mode | Best for | Library size |
|---|---|---|
| `reasoning` | Analytical, diagnostic, planning, multi-step tasks spanning abstraction, time, causality, simulation, spatial, and metacognition | 311 operations |
| `code` | Code generation, refactoring, review, and debugging across the software-engineering layer | 128 operations |
| `anti-deception` | Prompts that pressure the agent to validate, certify, or soften an honest assessment, spanning sycophancy, hallucination, deception, adversarial framing, judgment, and executive control | 139 operations |
| `memory` | Sharpening an observation already formed about cross-turn drift across the perception layer; filter-oriented, not write-oriented | 101 operations |

## What an injection looks like

A real `reasoning` mode response on the query `investigate why our nightly ETL job has started failing intermittently over the past two weeks; nothing in the code or schema has changed`:

```
[NEGATIVE GATE]
The server's response time was accepted as average, despite a suspicious
rhythm break in its timing pattern.

[PROCEDURE]
Step 1: Establish baseline timing profiles by extracting historical
durations and intervals for each event type. Step 2: Compare each observed
timing against its baseline and compute deviation magnitude. Step 3:
Classify anomalies as too fast, too slow, too early, or too late, and rank
by severity. ... Step 5: If deviation exceeds two standard deviations,
probe root cause by tracing upstream dependencies. ...

[REASONING TOPOLOGY]
S1:durations → FIXED_POINT[baselines] → N{dismiss_timing_deviations_
without_investigation} → for_each: S2:compare → S3:deviation →
G1{>2sigma?} --yes→ S4:classify → S5:probe_cause → FLAG → continue --no→
S6:validate → continue → all_checked → OUT:anomaly_report

[TARGET PATTERN]
Establish timing baselines by extracting historical response intervals.
Compare current server response time to this baseline. ...

[FALSIFICATION TEST]
If no event timing is flagged as suspiciously fast or slow relative to
baseline, temporal anomaly detection was not active.

Amplify: timing baseline comparison; anomaly classification; security
context elevation
Suppress: average timing acceptance; outlier normalization
```

The agent reads both the natural-language `[PROCEDURE]` and the graph-logic `[REASONING TOPOLOGY]` before generating its user-facing answer. The bracketed labels are instructions to the agent, not content to display; the user sees a naturally-phrased answer shaped by the injection.

## API reference

```python
EjentumHarnessTool(api_url: str = "...", timeout_seconds: float = 10.0)
```

| Field | Default | Description |
|---|---|---|
| `api_url` | `https://ejentum-main-ab125c3.zuplo.app/logicv1/` | Override only if you self-host the Ejentum Logic API gateway. |
| `timeout_seconds` | `10.0` | Per-call HTTP timeout. |

`EJENTUM_API_KEY` is read from the environment at call time.

The tool's `_run` accepts two arguments:

- `query` (string, required): a 1-2 sentence description of the task the agent is about to work on. For `mode='memory'`, format as `"I noticed [X]. This might mean [Y]. Sharpen: [Z]."`.
- `mode` (string, required): one of `reasoning`, `code`, `anti-deception`, `memory`.

Returns the scaffold string. Errors are returned as human-readable strings (the tool never raises so the agent never crashes the run).

## Compatibility

- Python 3.10+
- `crewai>=0.40.0`
- `requests>=2.31.0`

## Resources

- Ejentum homepage: <https://ejentum.com>
- Free tier and pricing: <https://ejentum.com/pricing>
- API reference: <https://ejentum.com/docs/api_reference>
- "Why LLM Agents Fail" essay: <https://ejentum.com/blog/why-llm-agents-fail>
- "Under Pressure" research paper: <https://doi.org/10.5281/zenodo.19392715>
- CrewAI documentation: <https://docs.crewai.com>

## License

[MIT](./LICENSE)
