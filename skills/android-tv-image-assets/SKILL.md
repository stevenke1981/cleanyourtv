---
name: android-tv-image-assets
description: Generate CleanYourTV Android TV backgrounds and transparent icon masters with Codex built-in image_gen, prepare Android PNG/vector/adaptive icon and TV banner assets, and export optional multi-size Windows ICO files with provenance and visual checks. Use for wallpaper, launcher artwork, banners or icon/ico requests.
---

# Android TV image assets

Read `AGENTS.md` and [asset formats](references/asset-specs.md). Keep this separate from an App UI rewrite. Existing launcher UI glyphs are Android vector drawables; preserve editable sources rather than replacing an entire icon system with bitmaps.

## Generate with the built-in tool

Use Codex's built-in `image_gen` (`image_gen.imagegen` or its host-exposed equivalent) by default. In Claude Code, which has no built-in generator, call the Antigravity CLI instead: run `agy -p "<prompt>. Save it as a PNG named <name>.png in the current directory, then print its absolute path." --mode accept-edits --print-timeout 280s` from an empty folder, one asset per call. It uses the Google account signed in to `agy`, which should be the paid account set aside for agents. Treat its output like any generated image: check the real file exists, its dimensions and alpha, and view it before use. Do not use an API script, paid external service, or request an API key as a workaround. If the built-in tool is missing or fails, deliver the prompts/specifications and record generation `NOT_RUN` or `FAILED` with the actual reason. Do not fabricate an output or call a procedural placeholder a generated image. An explicit no-spend restriction rules out a paid fallback.

1. Inspect the target screen, existing theme and any reference images. Start with the project's dark navy/black, restrained teal/violet ambient light and pale mint accents. Match the actual reference rather than imposing this palette on every request.
2. Choose a [prompt example](references/prompts.md). Wallpapers need quiet dark space behind the clock, pills, hero title and dock. Do not bake UI labels into a wallpaper. Icon masters require actual alpha: request `transparent_background: true`, with ample mask-safe padding. An adaptive background is a separate opaque layer.
3. Generate one asset per built-in call. Use only parameters the available tool documents; do not invent size, output-path or model controls. For local image edits, inspect with `view_image` first, then use the built-in edit mechanism. For brand-new images omit edit references.
4. Save/copy the returned source into the project promptly. Some hosts save under `$CODEX_HOME/generated_images`; others return image data. Use the actual returned file/data, never assume a guessed path or leave a project dependency outside the workspace. Preserve raw output and record its real dimensions; a prompt requesting 1920x1080 does not guarantee them.
5. Use the local [asset helper](scripts/tv_assets.py) for explicit format conversion, resizing and ICO export only. This helper does not generate artwork or remove backgrounds. Never erase alpha by exporting the icon master as JPEG. Do not rename a PNG to `.ico`.
6. Inspect the final images with `view_image`: wallpaper with real text/pill surfaces and a focus indicator; icon over light/dark/checkerboard surfaces and at 16, 32, 48 and 160 px; banner at 320x180, with exact localized app name; adaptive masks at the target density. Record the measured contrast and any edge/halo defects. A metadata/alpha check alone cannot detect a painted checkerboard or certify readability.

Use [generation records and acceptance](references/records-and-acceptance.md) for naming, provenance and the evidence schema. Keep source art, export commands and SHA-256 hashes linked. Label mockups as mockups, never TV screenshots.

Deliver previews outside `themes/` and `launcher/` until their separate integration is requested. `themes/` requires a real-TV screenshot; generated examples must not bypass that requirement. `.ico` belongs in an optional desktop/export directory, never the Android resource tree. Do not change the manifest, permissions, Gradle dependencies, device settings or deploy assets merely to demonstrate this skill.

When Android resources are explicitly changed, keep PNG/vector/adaptive sources and validate Android references plus the required local build. Otherwise validate only the skill, helper and exported images; UI acceptance stays `NOT_RUN` without actual device operation.
