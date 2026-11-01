---
name: apple-app-architecture
description: Design or migrate Apple apps using Dan's local Swift package architecture and API-owned Hono/Zod contracts. Use for new iOS app foundations, shared iPad/watch/Mac services, vertical feature boundaries, or an architecture migration; not routine UI edits.
---

# Apple App Architecture

Use Dan's preferred architecture: thin native app shells, local Swift Package
Manager modules, features that can grow independently, and an API that owns its
wire contract. Share business rules and services across Apple platforms without
making every platform use the same interface.

The pattern comes from KeepFresh's local packages and feature products, refined
in TripSplit for multiple Apple platforms, explicit offline sync and Hono/Zod
contracts. These are defaults for architecture work, not a reason to restructure
unrelated code during a small fix. Existing product requirements take precedence.

## Start with the application

Inspect the actual project, manifests, storage, API and release commands. Identify
whether this is a new app, a feature extension or a migration. Establish the first
shipping platform, offline needs, account/collaboration model, deployment target
and compatibility obligations. Ask only for decisions that cannot be inferred
from the brief or code; make the dependency graph and ownership decisions visible.

Use the relevant guides, rather than loading every guide for every task:

- [Swift packages](references/apple-packages.md): package boundaries, dependency
  direction, platform composition and adding a vertical feature.
- [API and contracts](references/api-contracts.md): Bun, Hono/Zod, Cloudflare,
  portable schemas, Swift consumers and optional server-backed sync.
- [New applications](references/new-app.md): establish the smallest working
  foundation and deliver the first real feature through it.
- [Migrations](references/migration.md): extract an existing app incrementally
  while preserving storage, sessions, behaviour and deployed clients.

## Preferred repository boundary

For a new multi-platform monorepo:

```text
apple/
  ios/                 iPhone/iPad shell, Xcode project, entitlements and assets
  Packages/            Local Swift packages and their resources/tests
  scripts/             Apple build and release entrypoints
api/
  src/schemas/         Canonical Zod request/response schemas
  src/routes/          Typed Hono route registration and HTTP handlers
  src/services/        Application operations and external integrations
  contracts/           Generated OpenAPI and cross-language fixtures
  docs/                Protocol semantics
docs/                  Cross-platform decisions and data provenance
scripts/               Tools genuinely shared across platforms
```

Add `apple/watchos/`, `apple/macos/` or root `web/` when those applications are
being built. iPad can share the adaptive iOS target. Do not create empty platform
shells or a backend for a local-only app. `apple/` describes all Apple work more
accurately than a top-level `ios/` containing Mac and Watch code; this is Dan's
repository convention, not an Apple requirement. Existing separate repositories
can use the same package/API boundaries without a forced monorepo migration.

## Decisions to preserve

- Put reusable rules and value types below networking, persistence, application
  coordination and feature UI. Declare each target's direct dependencies.
- Keep concrete app composition, navigation, entitlement configuration and
  platform-only interaction at the edge. Packages receive dependencies and
  configuration rather than discovering them through the app bundle or globals.
- Use feature products such as `SearchUI` or `TripsUI`; a package may contain
  multiple targets/products. Four packages, fixed names and one package per
  screen are not requirements.
- Let Zod own API shapes and derive TypeScript types. Generate portable OpenAPI
  from the actual Hono routes. Hono RPC shares TypeScript types; Swift needs its
  own transport adapter or a generated Swift client.
- Keep wire, domain and persisted models separate where their lifecycles differ.
  An API schema edit must not silently become a local database migration.
- Prefer Bun for API tooling and Hono with `@hono/zod-openapi`. For new hosted
  services, Cloudflare is Dan's preferred platform; choose its storage products
  for the workload. Bun tooling does not make Bun the Workers runtime.

## Validation and delivery

Run relevant tests locally on the source being delivered. Keep new CI minimal:
fast type/schema/data checks, with native builds and long test suites run locally
instead of duplicated remotely. Existing repository policy still applies; do not
rewrite its CI as a side effect of loading this skill. A hosted TestFlight job may
skip tests already verified locally for that revision, while retaining signing,
archive/export, upload and exact-build verification.

Document the resulting graph, contract-generation command, local checks and
extension path in the application repository. Report the source revision,
validation performed and any platform not actually compiled or exercised.
For TestFlight delivery, use the project's release entrypoint and the
`testflight-release` skill if available. Architecture work alone does not
authorise provisioning, deployment, a production data migration or a release.
