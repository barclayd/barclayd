# Start a new application

## Establish the first useful slice

Identify the core user action and the first shipping platform. Record whether it
needs local persistence, accounts, remote data or shared editing. List future
platforms as intended consumers, without building their shells yet. Agree the
initial dependency graph and data ownership in a short architecture note.

Create the `apple/` boundary and an iOS shell. Start with the package targets
needed by the first feature: domain, application logic and feature UI, adding
networking/persistence only when the flow needs them. They may be products in a
small number of packages. Avoid scaffolding a sync engine, account system,
generic router or repository protocol with no consumer.

Use existing design assets and native platform patterns. The architecture should
make the intended interface easier to deliver; it does not supply a replacement
design system or license a redesign.

## Build through the boundaries

For a server-backed feature, define its Zod input/output, route, errors and access
rules alongside the domain use case. Generate the OpenAPI artifact, then add the
Swift transport mapping or generated-client adapter. Implement one operation
through API service/storage, network adapter, application state and feature UI.
Inject dependencies from the app shell and provide explicit preview fixtures.

A useful first slice proves launch, loading, a real read or mutation, failure and
retry behaviour, plus relaunch if local state matters. If offline writes are a
requirement, also prove disconnected creation, durable pending state and
reconnection without duplicate records. If collaboration is required, verify
membership enforcement and a competing edit; a single happy-path device is not
enough evidence for a shared-data architecture.

Keep platform adapters at the edge and compile the shared service targets for
the future platforms actually claimed as supported. Add a second feature to the
same dependency pattern; extract common UI or services only where the two
consumers demonstrate reuse.

## Leave an operable foundation

Provide the project's locked install, contract generation/check, local tests,
app build and release commands. Keep generated contracts deterministic, document
which schema owns them and distinguish app domain/storage types from wire types.
Use relevant local tests and small fast CI checks; do not add long duplicate
build matrices by default. Preserve any existing delivery policy.

The handoff should identify the package graph, how to add a feature/platform,
where configuration enters the app, server/storage ownership, offline/recovery
rules if applicable, and the source revision verified. Link useful docs rather
than copying this entire skill into the app repository.

Provisioning accounts, configuring production identity, deploying a backend and
publishing a beta are separate actions governed by the user's existing scope.
Use project-specific credentials and identifiers; examples are not configuration.
