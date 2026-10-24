# Asset naming, provenance and acceptance

## Names and locations

Use stable semantic names with a version when keeping alternatives:

| Purpose | Example |
|---|---|
| Raw generated wallpaper | `cyt_wallpaper_aurora_dark_16x9_v01.source.png` |
| Prepared wallpaper | `cyt_wallpaper_aurora_dark_1920x1080_v01.jpg` |
| Raw alpha icon | `cyt_icon_clean_tv_square_v01.source.png` |
| Approved icon master | `cyt_icon_clean_tv_square_v01.png` |
| Desktop export | `exports/desktop/cyt_icon.ico` |
| Future Android resource | `mipmap-xhdpi/ic_launcher.png`, `drawable-xhdpi/tv_banner.png` |
| Language banner | `drawable-zh-rTW-xhdpi/tv_banner.png` (use the actual supported locale) |

Keep raw sources and machine-readable provenance with documentation examples; use ignored `work/` for scratch exports. When integrating a real theme, its runtime filename remains `wallpaper.jpg`, and its screenshot is independently captured from a real TV. A generated screenshot or procedural test fixture must never be used as that screenshot.

## Record one generation and its derivatives

Record only facts available from the tool. Do not invent a model version, seed, license guarantee, tool run ID or reproducible randomness. A hash establishes which bytes were inspected, not ownership or model reproducibility. Do not put credentials, device identifiers, usernames from screenshots or private reference paths in the record.

```json
{
  "asset_id": "cyt_icon_clean_tv_square_v01",
  "status": "NOT_RUN",
  "tool": "Codex built-in image_gen",
  "generated_at_utc": null,
  "tool_run_id": null,
  "model": null,
  "prompt": "Exact submitted prompt goes here when run",
  "transparent_background": true,
  "references": [],
  "rights_note": "Original requested concept; verify any supplied reference rights",
  "source": null,
  "derivatives": [],
  "visual_inspection": {"status": "NOT_RUN", "notes": []},
  "device_ui_acceptance": {"status": "NOT_RUN", "reason": "No TV or emulator operated"}
}
```

For a completed generation use `GENERATED` and include `source.path`, `source.sha256`, dimensions, colour mode/alpha, actual tool identifier and date. Each derivative records its path, SHA-256, export command, crop/resize/upscale, compression quality and result. Preserve `null` for unavailable tool metadata. When the tool is unavailable set `NOT_RUN` with a reason and leave the source absent; a failed call is `FAILED`. If a call returned an image but saving was interrupted, record that exact incomplete outcome rather than claiming a deliverable exists.

## Acceptance checklist

| Check | Evidence needed |
|---|---|
| Provenance | Raw image bytes saved, exact prompt and tool recorded, references identified and rights considered, hashes match. |
| Icon alpha | PNG decodes, square, nonempty alpha, genuinely transparent outside mark; not a painted checkerboard. |
| Icon appearance | Inspect light/dark/checkerboard surfaces, 16/32/48/160 px, edges and halos; no clipping under circle/squircle/adaptive masks. |
| Platform export | Android PNG/vector/adaptive sources retained; manifest uses a supported resource. ICO is separately exported and never required for Android. |
| ICO | Container header and all 16/24/32/48/64/128/256 entries reopen, decode with alpha and have readable silhouettes. |
| Wallpaper | Actual export 1920x1080, 16:9, opaque, around/below 300 KB for a theme; crop/upscale documented. No baked-in UI text. |
| Text readability | Inspect composited clock, pills, title and focused dock over the actual artwork; record actual ratios/sample locations, including worst bright regions. |
| Banner | 16:9 density variants, 320x180 xhdpi, exact app name, per-locale text, no clipped logo or accidental marketing copy. |
| App limits | No new launcher dependencies, permissions, runtime networking, giant master images or changed defaults. |
| UI evidence | Real TV/emulator and remote checks recorded separately. Without operation, UI acceptance is NOT_RUN. |

Helper results prove file properties only. Semantic checks (spelling, recognizability, halos, text and focus readability) need visual inspection. Record defects and pending work instead of turning a format PASS into full visual/UI acceptance.
