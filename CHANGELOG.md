# Changelog

All notable changes to `crewai-ejentum` are documented here. This project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-05-11

### Added

- Initial release.
- `EjentumHarnessTool` CrewAI tool wrapping the Ejentum Logic API. Single tool, four modes (`reasoning`, `code`, `anti-deception`, `memory`) selected per call via the `mode` argument.
- `EjentumHarnessParams` pydantic schema declares `query` (required, non-empty) and `mode` (required, one of four).
- Live API credential test happens implicitly on first call: a 401 surfaces an actionable error pointing the operator at <https://ejentum.com/pricing>.
- Eight unit tests cover the failure surface: missing API key, invalid mode, missing query, whitespace-only query (the path that previously could leak a paid request), success-path response parsing, 401 path, unexpected response shape, non-string scaffold value, and network error.
- Published to PyPI with OIDC trusted-publisher provenance attestation via GitHub Actions.

### Background

This package is the standalone-PyPI replacement for the closed [crewAIInc/crewAI#5768](https://github.com/crewAIInc/crewAI/pull/5768) PR. Per CrewAI's [tool-publishing guide](https://docs.crewai.com/en/guides/tools/publish-custom-tools), third-party tools live in their own PyPI packages with the `crewai-` prefix rather than in the CrewAI monorepo.
