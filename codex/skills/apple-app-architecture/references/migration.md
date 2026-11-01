# Migrate an existing application

## Capture compatibility before moving code

Inspect app targets, package manifests, direct/implicit imports, navigation,
resource loading, singleton dependencies and generated project files. Record the
existing build/test/release commands. Establish a working baseline and a small
set of meaningful behaviour checks before changing the layout.

Identify the compatibility surfaces that a folder/module move can break:

- Stored entity/type identities, schema versions, store URLs, document keys and
  Codable representations; module moves may change persisted type identity.
- Keychain service/access-group identifiers, bundle IDs, entitlements, sessions
  and device/install identity.
- Pending operations, operation IDs/payloads, sync cursors, account ownership and
  the way restored backups are reconciled.
- API paths, status/error envelopes, null/optional/default semantics, date/money
  representations and existing installed client versions.
- Server resource bindings, storage identity, migrations and live connections.

Create a synthetic fixture with the old app's real storage stack where possible,
or a controlled local copy of existing data. Include records, drafts and pending
operations. Do not commit personal data or secrets as migration fixtures. Keep a
recoverable baseline and separate structural extraction from behaviour changes.

## Extract in compilable increments

1. Document the intended graph and map existing responsibilities into it. Preserve
   names when a cosmetic rename would also change persistence or transport.
2. Extract pure domain values/rules. Add deliberate public APIs and prove a
   consumer can use them without importing the app target.
3. Extract networking and persistence behind explicit configuration/dependencies.
   Keep session refresh, storage paths, errors and encoding stable. Avoid moving
   persisted entities until their old-store compatibility has been demonstrated;
   use an explicit schema/data migration or keep compatibility types in place if
   required. Never delete and recreate a store to make the migration pass.
4. Extract sync and application coordination if they exist. Preserve operation
   identity, conflict handling and account isolation. Remove app-global access
   only as its replacement is wired and checked.
5. Extract one feature product at a time, retaining view identity, navigation and
   the current design. Move shared presentation/resources to their owning targets
   and replace app-bundle assumptions with package resource access.
6. Reduce the app to composition and platform adapters. Then group app/packages
   under `apple/` when adopting the monorepo layout. Update Xcode/project inputs,
   release paths, scripts, fixtures and documentation in the same change.

Adapt the sequence to the current graph; a temporary facade is preferable to a
large unbuildable rewrite. Do not widen every API, silence concurrency errors or
introduce circular dependencies to finish a move. Leave unrelated feature work
and broad formatting changes outside the migration.

## Move API contracts without changing the protocol accidentally

First capture real request/response fixtures and identify consumers of the old
contract. Derive TypeScript types from Zod and generate portable OpenAPI from the
actual Hono registry. Update each consumer or artifact publication path before
removing duplicated interfaces/root contracts. Preserve semantic fixtures under
`api/contracts/fixtures` and protocol documentation under `api/docs`.

Classify app-owned JSON, vendor/delegated handlers and non-JSON uploads before
changing registration. Follow [existing route boundaries](api-contracts.md#existing-route-boundaries)
to preserve parsing and validation order and document the generated contract's
actual coverage. A staged adoption can leave vendor-owned routes delegated.

Compare generated validation to runtime behaviour: required versus omitted keys,
explicit null, defaults/coercions, unions, numeric bounds, auth and error statuses.
Hono middleware order, body-size limits and error hooks can affect an existing
API even if a route's business code is unchanged. Test these boundaries. Keep
schema helpers below services to avoid schema-to-service runtime import cycles.

Renaming a backend directory does not require changing its runtime or database.
If adopting Bun/Hono/Cloudflare is also requested, stage those changes with
compatibility checks and retain resource identities. Do not combine a storage
replacement, destructive data migration or public API redesign with a package
extraction unless it is explicitly part of the task.

## Evidence for completion

Use checks proportional to the changed boundaries:

- Build the consuming app and relevant packages; compile any additional
  platforms claimed as supported. A macOS `swift test` is not a watchOS build.
- Open the old-store fixture with the new architecture and compare records,
  drafts and pending-operation identity. Exercise an in-place app update when
  storage/session continuity is involved; fresh installs do not prove it.
- Check wire fixtures and semantic invariants on both sides, plus current API
  runtime tests when handlers/validation/storage were touched.
- Run the release entrypoint's preflight/dry run after path changes. A successful
  simulator build is not evidence that signing/upload discovery still works.

Keep the full verification local and record its source revision. Repeat only
checks affected by subsequent changes. Report preserved behaviour, intentional
changes and any unverified real-device/production flow accurately. Shipping the
source through a PR does not, by itself, verify an installed beta or authorise a
production data migration.
