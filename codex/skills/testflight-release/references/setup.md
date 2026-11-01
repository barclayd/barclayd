# Authentication and signing

Install the shared command and skill with `./codex/install-testflight.sh` from
`~/Developer/barclayd`. Install ASC with Homebrew (`brew install asc`) if absent.
`asc install-skills` installs its pinned, reviewed upstream skill pack. Keep the
CLI version aligned with `codex/testflight-toolchain.json` when upgrading.

## App Store Connect

Inspect `asc auth status` first. Validate access with `testflight check` for the
actual app and internal group. A saved profile alone proves nothing about live
permissions. Prefer the official API over `asc web` session commands.

For a new team API key, the Account Holder enables API access in App Store
Connect > Users and Access > Integrations. An Account Holder or Admin can create
a team key. App Manager supports TestFlight management; provisioning operations
may need different permissions. Team keys apply across the team's apps. An
individual key inherits the user's app access but does not support provisioning
endpoints. Choose access for the actual operations, not maximum privileges.

Keep the one-time `.p8` download outside Git in a private directory (0700) with
file mode 0600. Do not paste private key material into chat. Register it:

```sh
asc auth login --name PROFILE --key-id KEY_ID --issuer-id ISSUER_ID \
  --private-key /private/path/AuthKey_KEY_ID.p8 --network
```

Keychain-backed ASC authentication and Xcode's authentication are separate.
Xcode's CLI accepts `-authenticationKeyPath`, `-authenticationKeyID` and
`-authenticationKeyIssuerID` with `-allowProvisioningUpdates`. Keep the original
protected key file if using these Xcode arguments. A headless CI job can provide
`ASC_KEY_ID`, `ASC_ISSUER_ID`, `ASC_PRIVATE_KEY_PATH` and
`ASC_BYPASS_KEYCHAIN=1` from its secret store. Never log their values or enable
shell tracing around credentials.

## Signing

Inspect local identities with `security find-identity -v -p codesigning` and the
app's actual entitlements/profiles. A development identity is not a distribution
identity. An API key cannot recover an existing certificate's private key.

For a prepared Mac, use existing signing assets and API-authenticated automatic
provisioning. Xcode may use managed cloud signing on export; verify this with an
actual export before claiming unattended signing works.

For a fresh CI runner, provision an exportable distribution identity and profiles
for every target, store them in CI secrets or an encrypted signing store, and
import them into a temporary keychain. The upstream `asc-signing-setup` skill
covers `asc signing fetch`, `asc signing keychain` and signing sync. Inspect the
team's existing certificates first. Do not revoke or replace working identities
as a repair attempt. Keep creation/rotation within the authorised setup task.

## TripSplit

The first integration uses app `6829340844`, bundle `it.tripspl.TripSplit`, team
`R2GGK3VN2C`, and internal group `69183108-1726-4905-82c5-e3e6ecae0251` (Dan).
These are nonsecret identifiers; revalidate them at release time. The local ASC
profile is `codex-testflight`. App-specific build instructions live alongside the
TripSplit iOS shell (`apple/ios/README.md`, or `ios/README.md` in the older layout).

Sources checked 1 November 2026:
- [Apple API keys](https://developer.apple.com/help/app-store-connect/get-started/app-store-connect-api/)
- [ASC signing](https://github.com/rorkai/App-Store-Connect-CLI/blob/5.17.1/guides/code-signing.mdx)
- [Fastlane API permissions](https://docs.fastlane.tools/app-store-connect-api/)
