# Archive and export

Use a clean, committed app checkout and its documented project-generation/test
steps. These examples are for an automatically signed iOS project. Inspect
`xcodebuild -help` when the installed Xcode differs. Workspace and multi-target
projects should retain their existing build/signing configuration.

Record `git rev-parse HEAD`. Resolve a build number immediately before archiving:

```sh
asc builds next-build-number --app APP_ID --platform IOS --output json
```

Use `nextBuildNumber`; this is a lookup, not a global reservation. Serialise
releases for the app across agents, local machines and CI.

```sh
xcodebuild -project ios/TripSplit.xcodeproj -scheme TripSplit \
  -configuration Release -destination 'generic/platform=iOS' \
  -archivePath /private/path/TripSplit.xcarchive \
  -allowProvisioningUpdates \
  -authenticationKeyPath /private/path/AuthKey_KEY_ID.p8 \
  -authenticationKeyID KEY_ID -authenticationKeyIssuerID ISSUER_ID \
  CURRENT_PROJECT_VERSION=BUILD_NUMBER archive
```

Create a private `ExportOptions.plist` with these keys, preserving any necessary
project-specific options:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
  <key>method</key><string>app-store-connect</string>
  <key>destination</key><string>export</string>
  <key>signingStyle</key><string>automatic</string>
  <key>teamID</key><string>TEAM_ID</string>
  <key>testFlightInternalTestingOnly</key><true/>
  <key>manageAppVersionAndBuildNumber</key><false/>
  <key>uploadSymbols</key><true/>
</dict></plist>
```

```sh
xcodebuild -exportArchive -archivePath /private/path/TripSplit.xcarchive \
  -exportPath /private/path/export -exportOptionsPlist /private/path/ExportOptions.plist \
  -allowProvisioningUpdates \
  -authenticationKeyPath /private/path/AuthKey_KEY_ID.p8 \
  -authenticationKeyID KEY_ID -authenticationKeyIssuerID ISSUER_ID
```

Keep signing settings/profiles for all extensions. Do not pass a single profile
override to every target in a multi-target project. Verify the exported app's
bundle ID, version and build number before upload; the helper also checks these.
Keep raw signing/export logs private. The shared helper only uploads an existing
IPA; it never silently builds, signs or changes project settings.

## Manual signing when cloud signing is unavailable

For TripSplit, the dedicated local distribution identity and profile are under
`~/.config/testflight/signing/tripsplit`. Keep those files private. The dedicated
keychain is `codex-testflight.keychain-db`; `identity-password` and
`keychain-password` are protected password files. Inspect the installed profile
and certificate when renewing, rather than copying expired identifiers.

If the dedicated keychain has locked, unlock it without a UI prompt or a password
in the process arguments:

```sh
asc signing keychain unlock \
  --keychain ~/.config/testflight/signing/tripsplit/codex-testflight.keychain-db \
  --keychain-password-file ~/.config/testflight/signing/tripsplit/keychain-password \
  --timeout 3600
```

The validated export changes `signingStyle` to `manual`, sets
`signingCertificate` to the distribution certificate's SHA-1 fingerprint, and
adds `provisioningProfiles` mapping the app bundle ID to the installed App Store
profile UUID. This requires neither API authentication arguments nor a signed-in
Xcode account at export time. Keep `testFlightInternalTestingOnly=true`.

For a single-target manually signed archive, pass `CODE_SIGN_STYLE=Manual`,
`CODE_SIGN_IDENTITY=Apple Distribution`, `DEVELOPMENT_TEAM=TEAM_ID` and
`PROVISIONING_PROFILE_SPECIFIER=PROFILE_UUID` alongside the build-number
override. Do not apply this single-profile recipe to extension targets.

If archive/export fails, diagnose that stage before uploading. Do not switch to
an unsigned/simulator build or ad-hoc package. Exporting and uploading are
separate actions, so an export retry cannot upload a duplicate build.
