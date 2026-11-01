# API infrastructure and contracts

## Runtime and ownership

Use strict TypeScript, Bun's locked dependency installation and script workflow,
Hono routing and `@hono/zod-openapi`. Pin a compatible dependency/toolchain set in
the project; do not copy old version numbers from an example. Keep Node available
when the selected build/test/Cloudflare tools require it. Bun manages local work;
Cloudflare Workers executes the deployed service. Check dependencies against
Workers APIs rather than assuming arbitrary Bun or Node APIs are available.

Keep concerns under `api/`:

```text
src/
  app.ts                 HTTP composition and middleware
  index.ts               Worker exports / scheduled handlers, when needed
  routes/v1/             Route definitions and handlers
  schemas/               Request, response and shared validation shapes
  types/                 Schema-inferred aliases and Hono environment types
  services/              Use cases, auth and external-provider integration
  middleware/            Authentication, bounded parsing, error handling
  data/                  Canonical metadata, if shared with clients
  durable-objects/        Only when the workload needs them
contracts/
  openapi.json           Generated, deterministic portable wire contract
  fixtures/              Cross-language examples, not another schema definition
docs/protocol.md          Semantics that types cannot express
scripts/                 Contract generation/checks and API operations
```

Choose names and nesting to fit the product. Keep HTTP handlers small: validated
input enters a service; services enforce permissions and invariants and map
storage to explicit responses. Storage rows are not automatically public DTOs.

## One authoritative wire schema

1. Define named request/response schemas with the `z` export from
   `@hono/zod-openapi` where OpenAPI metadata is used.
2. Declare method, versioned path, parameters, bodies, response status/content
   schemas and security with `createRoute`; register on `OpenAPIHono`.
3. Read validated request values through `c.req.valid(...)`. Infer TypeScript
   aliases using `z.infer<typeof schema>`; use `z.input` versus `z.output` where
   coercion, defaults or transformations make those types differ. Import aliases
   type-only to avoid a runtime cycle between schemas and services.
4. Generate OpenAPI from the same registered app/routes, not a second hand-built
   route inventory. Give operations stable IDs. Keep generation deterministic
   and add a check that fails when the committed artifact is stale.
5. Verify representative request/response fixtures against Zod and the generated
   contract. Include errors and null/omitted fields as well as successful data.

The contract folder remains useful **inside the API** as generated output and
fixtures. Remove duplicated hand-written TypeScript interfaces and independent
root-level wire schemas once all consumers use the canonical source. Do not
delete accounting examples or protocol rules merely because Zod exists.

Hono route typing does not, by itself, validate every outgoing response at
runtime. Use a deliberate response-mapping/validation strategy and contract tests
for storage/provider output. Zod request validation also does not replace
resource-level authorisation, cross-entity rules or transactional constraints.

Choose and document wire representations for IDs, instants versus civil dates,
time zones, enums and exact numeric values. For money or values beyond safe JSON
integer precision, use exact decimal/integer strings with bounds and explicit
rounding rules. Match missing versus explicit null semantics in Swift encoding
and decoding; an optional Swift property alone may not model a three-state patch.

OpenAPI cannot express every refinement, transformation, permission check or
retry rule. Put these semantics in `docs/protocol.md` and cross-language fixtures.
When generating OpenAPI 3.1, validate it with a compatible schema validator and
the intended client generator. TripSplit exposed a nullable `$ref`/`allOf`
generation issue: check that null is accepted only where intended, required keys
remain required and primitive bounds survive generation. Treat this as a
regression case to verify against installed versions, not a permanent patch to
apply blindly. Generation need not expose a public documentation endpoint.

Check named schemas both at nullable use sites and as standalone non-null
components. Ride On found that making `User.pause` nullable widened the shared
`Pause` component too. Comparing Zod and generated-schema validation exposed the
leak; a local union with null preserved the intended non-null component. For this
case, check a valid object, explicit null, an omitted required property and an
invalid primitive at the property, then verify that the shared component still
rejects null. Apply only a demonstrated local correction; do not rewrite every
nullable schema or assume one generator workaround fits all references.

## Existing route boundaries

Before adding automatic route validation, classify the existing HTTP surface:

- App-owned JSON routes can adopt typed request/response schemas incrementally.
- Vendor/delegated handlers, such as an authentication library's wildcard
  routes, retain their owning library's parsing and protocol. Do not wrap them
  in a generic JSON validator just to make the OpenAPI inventory look complete.
- Raw uploads, multipart bodies, webhooks and streaming endpoints need their
  actual media types and body-handling semantics. Preserve raw bytes where
  signature verification or an existing decoder requires them.

Document which routes the generated contract covers, which remain delegated or
not yet described, and how affected clients consume them. Prefer an explicit
coverage boundary to an invented schema or a claim that a partial artifact
describes the whole service. Keep excluded routes covered by their relevant
protocol/integration checks.

For JSON routes with an existing bounded parser, make sure it executes before
automatic JSON validation consumes the stream. Preserve middleware order,
content-type handling, fatal UTF-8 decoding, byte limits and application error
envelopes. Check the installed framework's body consumption/caching behaviour;
if an adapter shares the already parsed body with validation, verify that it
cannot trigger an unbounded second read or bypass the original checks. Keep any
framework-dependent adapter small and covered when upgrading dependencies.

Exercise malformed JSON, invalid UTF-8, unsupported media types, oversized bodies
(including streamed bodies without a trustworthy Content-Length), valid requests
and existing auth/error precedence. Assert the original statuses and envelopes,
including 400/413/415 where applicable. This preserves behaviour that a schema
alone cannot describe. Ride On's JSON API, vendor auth and raw GPX uploads
demonstrated why these route classes need separate treatment.

## Swift and web consumers

For TypeScript clients, Hono RPC can share the typed route tree with `hc<AppType>`.
Preserve inference when composing/chaining routes, and export types without
bundling server implementation or secrets into the client. RPC is not a Swift
contract and does not make old installed apps update when the server changes.

For Swift, choose between a small handwritten Codable transport adapter validated
against fixtures, or Apple's Swift OpenAPI Generator with its runtime and a
supported transport such as URLSession. Both consume the API-owned definition;
do not introduce a second hand-maintained authoritative schema. If a generator
needs an input file inside a package, copy it reproducibly from
`api/contracts/openapi.json` and check drift rather than editing both copies.
Separate repositories can publish a versioned artifact with a pinned consumer.

Keep generated DTOs in the networking boundary and map to domain values. Do not
replace persisted SwiftData entities with generated response models. Specify
encoding/decoding and API-version compatibility independently of package layout.
Backward-compatible fields and transitions matter because multiple client
versions remain installed. Handle authentication refresh, cancellation, bounded
retries and error decoding centrally. Retry writes only with defined idempotency.

## Choose Cloudflare resources for the workload

| Resource | Appropriate role |
| --- | --- |
| Workers | HTTP API, provider integration and bounded request orchestration |
| D1 | Relational account/discovery data or the primary store for a conventional app |
| Durable Objects with SQLite | Per-entity coordination, transactional state and live collaboration when needed |
| R2 | Binary assets/attachments when the product needs object storage |
| KV | Cache/configuration where eventual consistency is acceptable |
| Queues / scheduled work | Asynchronous work and retries when requirements justify them |

TripSplit uses one Durable Object per trip and D1 for accounts/discovery. This is
a collaboration/transaction boundary, not a requirement for every new app. A
simple application may use D1 alone. Keep authoritative ownership explicit;
transactions do not extend across D1 and multiple Durable Objects. Where a
projection spans stores, use durable retry/outbox semantics and never let a stale
discovery index grant access.

Use typed bindings and migrations, bounded bodies/batches and consistent error
envelopes. Keep credentials in secret bindings and separate environments/resource
IDs; never copy a reference project's account, domain, app ID or signing keys.
Use `cf` for an existing `cloudflare.config.ts`; preserve Wrangler in an existing
Wrangler project unless migration is requested. Retrieve current CLI docs and
follow the project's release commands before provisioning or deployment.

## Accounts, offline data and recovery

Sign in with Apple is Dan's preferred native account option where accounts are
needed. Separate Apple identity from the app's user ID and device sessions;
verify tokens/nonces server-side and centralise refresh/revocation. Account and
membership permissions belong on the server, not in a hidden UI control.

For an app with editable offline shared data, persist a local confirmed state and
durable pending operations. Give operations stable IDs, keep payloads immutable
once attempted, and have the server commit atomically with an idempotency receipt.
Reconcile using revisions; preserve local drafts on conflict instead of silently
overwriting them. Live notifications are refresh hints, not the only sync path.
Reconcile on foreground/reconnect and isolate cached state by account.

When the service owns cross-device and shared sync, do not also enable automatic
CloudKit sync for the same mutable store. Normal device backup eligibility is a
separate recovery feature, not a sync protocol. Preserve drafts/outbox in backups,
keep credentials in appropriate device-bound Keychain storage and reconcile
restored state. Server backups/restore and sync-epoch recovery need their own
design. A local-only or explicitly CloudKit-based product needs a different
decision; do not add a server outbox merely to match TripSplit.

## Sources and examples

- [Hono Zod/OpenAPI](https://hono.dev/examples/zod-openapi)
- [Hono RPC](https://hono.dev/docs/guides/rpc)
- [Swift OpenAPI Generator](https://github.com/apple/swift-openapi-generator)
- [Workers Node.js compatibility](https://developers.cloudflare.com/workers/runtime-apis/nodejs/)
- [Cloudflare storage options](https://developers.cloudflare.com/workers/platform/storage-options/)
- KeepFresh: `~/Documents/Coding/keepfresh-api/src/{routes,schemas}` shows the
  route/schema pattern; its Supabase/Bun-server setup is not the Cloudflare design.
- TripSplit: `~/Developer/tripspl.it/api/` demonstrates the Cloudflare form,
  `src/types/contract.ts`, `src/contracts/openapi.ts`, `scripts/verify-contract.ts`
  and `docs/protocol.md`. Use these if available; this guide is self-contained.
