# Contributing to conference2026.mlinpl.org

## Project structure

This repository contains the source code for the 2026 edition of the ML in PL Conference website.
The site is built using Jekyll, and the generated output is placed in the `_site/` directory.

Do not edit generated files in `_site/` directly.

### Relationship with the main website

This repository is typically linked as a Git submodule in the main multi-year conference website repository.
When changes are merged into the `main` branch of this repository, it should trigger a GitHub Actions workflow (in the main repository) to update the submodule pointer and rebuild the unified site.

## Local setup

**Option 1: Using Docker**

1. Clone the repository.
2. Run with the existing `Dockerfile`.

**Option 2: Local Ruby environment**

1. Clone the repository.
2. Setup Ruby (refer to the README at https://github.com/mlinpl/mlinpl-jekyll-theme).
3. Install Ruby dependencies:

```bash
bundle install
```

4. Run the local build and preview server:

```bash
bash run_locally.sh
```

(or `npm run dev`)

This script:
- builds the Jekyll site into `_site/`,
- starts a local Jekyll server at `http://localhost:4000`.

## Contribution workflow

1. Create a branch from `main`:

```bash
git switch -c feature/short-description
```

2. Make your changes. 
   - Content and data can be found in `_data/`, `pages/`, `_includes/` and `_layouts/`.
3. Verify your changes locally by checking `http://localhost:4000` (ensure `bash run_locally.sh` is running).
4. Commit with a clear and concise message.
5. Open a pull request against this repository.

Suggested branch prefixes:
- `feature/...`
- `fix/...`
- `chore/...`

**When adding images use optimized versions.**
Add the original files first under `_images/<group>/` (e.g. `_images/sponsors/`), run `bash scripts/optimize_images.sh` (or `npm run images:optimize`), and refer to optimized versions from `images/optimized/` in the website content. `_images/` is not published; SVGs are copied to `images/optimized/` as they are.

**Adding conference photos.**
1. Put the originals of each photographer in their own folder `_images/photos/photographer-<n>/` (git-ignored), directly or in subfolders.
2. Map each folder to the photographer's name (and optional link) and list the conference days in `_data/photos-config.yml`. Folder names end up in the published image paths, so keep them neutral.
3. Run `uv run scripts/build_photos.py` (or `npm run photos:build`). It assigns photos to days by their EXIF capture date, writes web-sized photos and thumbnails (rotated, keeping the EXIF metadata) to `images/photos/`, and generates `_data/photos.yml`. It works incrementally: re-run it after each new batch, and only new photos are processed. Removing originals later (or not having them at all, e.g. in a fresh clone) keeps their photos in the gallery. Deleted outputs are regenerated from the originals. To remove a photo, delete its original and its files in `images/photos/`. To start over, delete `images/photos/` and `_data/photos.yml`.
4. Commit `images/photos/` and the two data files.

## Data conventions

- **Affiliations** (`author-title` and similar): separate multiple institutions with ` / ` (space-slash-space), e.g. `University of Warsaw / ML in PL`.
- **Co-authors**: list as a single comma-separated string, e.g. `Jane Doe, John Smith`.
- **Missing images**: when no photo is available, use `images/empty.png`.
- **Dates and times**: format dates as `Weekday / DD Month` (e.g. `Saturday / 10 October`) and times as `HH:MM - HH:MM` (e.g. `12:15 - 13:45`).
- **IDs**: each poster/talk `id` is a unique integer; when adding entries, continue the existing numbering and update any count ranges referenced elsewhere (e.g. session subtitles in `_data/agenda.yml`).

## Troubleshooting

- If changes to `_config.yml` or files in `_data/` are not reflected, restart the Jekyll server by stopping `run_locally.sh` and running it again.
- If the output looks stale, stop the server and run `bash run_locally.sh` again.
