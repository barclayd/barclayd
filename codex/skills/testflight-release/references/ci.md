# macOS CI

The reusable workflow is `.github/workflows/testflight.yml` in `barclayd/barclayd`.
It tests a committed Xcode project, imports temporary manual signing, archives,
exports an internal-only IPA, uploads once and follows the exact build. Its
single profile supports one iOS app target; adapt signing explicitly for apps
with extensions. Keep an existing Fastlane pipeline where it already works.

Create a manual `workflow_dispatch` caller in the app repository. Pin `uses` and
`tooling-ref` to the same reviewed full commit of this repository. Supply the app,
bundle, team and internal group IDs, repository-relative project path (or `auto`
to discover a unique scheme-named project), scheme,
runner label, Xcode path and explicit simulator test destination. Do not use PR
events to give untrusted fork code signing credentials.

`run-tests` defaults to `true`. A caller may set `run-tests: false` to avoid
duplicating full local tests in CI. Before releasing with this opt-out, run the
app's required checks locally against the exact committed revision being
released and record the source SHA and results in the release handoff. Repeat
affected checks if the source changes. This skips only the `Test app` step;
archive, signing, upload and receipt verification still run.

Store these secrets in the **app repository's** `testflight` environment:

| Secret | Value |
| --- | --- |
| `ASC_KEY_ID` | App Store Connect key ID |
| `ASC_ISSUER_ID` | Team key issuer UUID |
| `ASC_PRIVATE_KEY_B64` | Base64 of the ASC `.p8` file |
| `DISTRIBUTION_P12_B64` | Base64 of the exportable distribution identity |
| `DISTRIBUTION_P12_PASSWORD` | Its password |
| `APP_STORE_PROFILE_B64` | Base64 of the matching App Store profile |

Base64 is transport encoding, not encryption. Use GitHub's secret store, never
repository variables or source files. Pass secret values to `gh secret set`
through stdin. Keep an independent protected copy of the identity and password;
Apple cannot return its private key later. Renewal is a deliberate setup action,
not something each release silently attempts.

The job validates app/group identity and signing profile/team/expiry before
upload. Only the small source/build/hash/status receipt is uploaded as a GitHub
artifact, not signing files, IPAs or raw diagnostics. Temporary signing cleanup
runs on failure as well as success. Use a dedicated/ephemeral runner.

Release concurrency is scoped to the app within its repository. Coordinate any
local release with that workflow: Apple's next-build-number query is not a
distributed reservation. The exported app's actual version/build are recorded.

Trigger an authorised release with `gh workflow run testflight.yml --ref BRANCH`
and inspect the returned run. The workflow must first exist on the repository's
default branch. A new PR can be checked and locally exercised before merging,
but do not report a hosted CI deployment as tested until an actual run succeeds.
Merging remains Dan's decision.

After an upload/processing failure, download that run's receipt and use
`testflight status` or `testflight resume`. Re-running the entire workflow creates
another build; do not use it as a processing retry. CI waits are bounded and can
finish with pending status while Apple is still processing.

## Initial validation

On 1 November 2026, TripSplit's App Manager API key authenticated successfully but
could not use cloud-managed signing. Xcode CLI also reported No Accounts even
though Organizer worked. A dedicated distribution certificate and App Store
profile, created using the same key role, enabled manual CLI export without a
browser or keychain prompt. Keep this distinction when diagnosing a new machine.

TripSplit build 7 then completed archive, manual export, API upload and helper
resume/status entirely from the CLI. Apple reported VALID, IN_BETA_TESTING and
access for the existing Dan group. The source was
`353939ce57a6f92a560e4f4745903531f601a857`; physical installation is a separate
check. The reusable CI signing prepare/cleanup sequence was also exercised
locally with the actual identity, preserving the pre-existing profile. Hosted
CI execution still needs the app's caller workflow merged and dispatched.

ASC 5.17.1 `signing fetch` hit a missing managed profile before creating files;
explicit `certificates create` and `profiles create` worked. Inspect partial
state before retrying bootstrap. OpenSSL 4's default PKCS#12 export failed macOS
import; a password-protected PKCS#12 using `-keypbe PBE-SHA1-3DES -certpbe
PBE-SHA1-3DES -macalg sha1` imported successfully. This is a compatibility option
for the import container, not a change to the Apple signing key or signature.
