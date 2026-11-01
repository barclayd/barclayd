# Swift package architecture

## Why these boundaries exist

KeepFresh demonstrates local SPM packages and multiple feature products in a
`Features` package. TripSplit groups those concerns into domain, infrastructure,
application and feature packages, with separate products inside each where
useful. Retain the principle rather than copying every dependency: broad shared
dependency lists and sibling-feature imports make later extraction harder.

The intended benefits are reusable services for Watch/Mac, isolated tests,
explicit dependencies and features that can evolve without growing one app
target. Packages enforce module boundaries; folders alone do not. Extra modules
also add API and build maintenance, so introduce a boundary for a real consumer,
independent responsibility or platform constraint.

| Concern | Owns | Can depend on |
| --- | --- | --- |
| Domain | Value types, invariants, pure calculations, service protocols where useful | Foundation and focused platform-independent dependencies |
| Networking | HTTP transport, wire DTO mapping, error decoding, credential-provider integration | Domain; optional generated wire-client target |
| Persistence | Local storage, repositories, migrations, cached state | Domain and the chosen storage framework |
| Sync, if needed | Outbox, reconciliation, retry/conflict state | Domain, networking, persistence |
| Application | Use cases, observable coordination and feature-facing state | Domain and required service products |
| Design system / SharedUI | Visual tokens, controls and genuinely reusable presentation | Supported UI frameworks; small shared values where needed |
| Feature UI products | A feature's screens, presentation state and public entrypoint | Application/domain, design system and necessary adapters |
| App shell | Lifecycle, root navigation, dependency construction, entitlements | The products that this platform composes |

Dependencies flow down towards domain/services. Domain does not import SwiftUI,
UIKit, an app target or presentation routing. Infrastructure does not import
feature UI. Avoid routing between feature implementations directly; let the app
or a focused routing abstraction connect feature intents and stable identifiers.

## Local SPM mechanics

Use sibling local dependencies, for example
`.package(path: "../ProductDomain")`, and declare each target's required products
with `.product(name: "ProductDomain", package: "ProductDomain")`. A manifest's
package dependencies make products available; target dependencies determine the
module graph. Do not rely on transitive imports. Library products expose targets;
Swift `import` uses the module/target name, which can differ from the product name.

Organise `Sources/<Target>/` and `Tests/<Target>Tests/`. Expose only the types and
initialisers a consuming module needs; synthesised memberwise initialisers are
not automatically public. Prefer internal implementation details to making
everything public just to get the extraction to compile.

Declare package resources and access them with `Bundle.module` inside their
owning target. Keep app icons, entitlements and app lifecycle configuration with
the app shell. Inject base URLs, authentication providers and environment choices;
do not have a network package read `Bundle.main` or find a global app state.

Preserve the repository's project tooling. If it uses XcodeGen, update the source
configuration and regenerate its project instead of maintaining two divergent
definitions. Include local package references and products in each consuming app
target. Folder moves must also update scripts, CI, fixture paths and release
project discovery.

## Multiple Apple platforms

Set deployment targets from actual requirements and SDK availability. Do not copy
TripSplit's particular SDK versions into every project. A manifest listing
watchOS/macOS is not evidence that the package compiles on those platforms.

Compile reusable products for each claimed platform. Keep UIKit, unavailable
SwiftUI modifiers, MapKit presentation, biometric/sign-in presentation and haptics
in supported feature or adapter targets. macOS and watchOS compose their own
navigation and interaction around the same use cases; iPad may use adaptive
presentation in the iOS app. Share UI where it fits the platform, not as a
condition for sharing the network or domain layer.

Use explicit concurrency ownership: UI coordination generally belongs on the
main actor; mutable network/session and storage work needs its own appropriate
isolation. Move values across boundaries rather than leaking storage contexts or
mutable persisted objects. Respect SwiftData context/model isolation. Do not use
`@unchecked Sendable` or disable concurrency checking to disguise a boundary
problem. Cancellation and errors should survive through the transport/use-case
layers so features can stop obsolete work and present useful recovery.

## Add a vertical feature

For a new feature, identify its state and operations, then add only the domain
rules and service methods it needs. Give its UI a focused target/product and a
small public entrypoint accepting dependencies or a feature model. Connect that
entrypoint in the app shell. Feature presentation state lives with the feature;
shared account/session/sync coordination lives in application services.

For example, a future `PackingUI` can use a packing use case and repository while
a Watch target consumes that use case without importing `PackingUI`. Add a new
package only when a separate lifecycle or consumer justifies it; another target
inside `ProductFeatures` is often sufficient. Extract SharedUI after concrete
reuse appears, rather than creating a global container for unrelated helpers.

Test rules without UI, services with injected transport/storage, and feature
behaviour at the boundary that matters. Use previews with explicit sample state;
production startup must not silently seed demo data. An interface extraction
should preserve the existing design and interactions unless redesign is requested.

## Implementation references

- KeepFresh: `Packages/Features/Package.swift`, `Packages/Network/Package.swift`
  in `~/Documents/Coding/keepfresh-ios` when available.
- TripSplit: `apple/Packages/`, `apple/ios/project.yml` and
  `docs/architecture.md` in `~/Developer/tripspl.it` when available.
- [Apple: organising code with local packages](https://developer.apple.com/documentation/xcode/organizing-your-code-with-local-packages)
- [Swift PackageDescription reference](https://docs.swift.org/package-manager/PackageDescription/PackageDescription.html)

The local repositories are examples, not prerequisites for using this guide.
