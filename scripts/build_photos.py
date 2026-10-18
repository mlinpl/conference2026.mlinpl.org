# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "pillow",
#   "pyyaml",
# ]
# ///
"""Builds the photo gallery from the original photos.

Reads the originals from _images/photos/<photographer-id>/ (directly or in subfolders),
assigns each photo to a day by its EXIF capture date, as configured in _data/photos-config.yml,
and writes:
- web-sized photos to images/photos/full/<photographer-id>/,
- thumbnails to images/photos/thumbnail/<photographer-id>/,
- the gallery data to _data/photos.yml.

It works incrementally: new photos are added to the gallery, already processed ones are skipped
(use --overwrite to redo them), and photos stay in the gallery when their originals are removed.
Deleted web-sized photos or thumbnails are regenerated from the originals. To remove a photo, delete its original
and its web-sized photo or thumbnail (the rest is removed then).
To start over, delete images/photos/ and _data/photos.yml.

Usage: uv run scripts/build_photos.py [--overwrite]
"""

import argparse
import sys
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import yaml
from PIL import Image, ImageOps

FULL_SIZE = 2400
# Thumbnails are shown in a 240px box, so they are twice that for high-DPI screens
THUMB_SIZE = 480
FULL_QUALITY = 85
THUMB_QUALITY = 80
EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".tif", ".tiff"}

EXIF_IFD = 0x8769
EXIF_DATETIME_ORIGINAL = 0x9003
EXIF_DATETIME = 0x0132
EXIF_GPS_IFD = 0x8825
EXIF_ORIENTATION = 0x0112


@dataclass
class Photo:
    path: Path
    photographer: str
    taken: datetime | None = None

    @property
    def filename(self):
        return self.path.name

    @property
    def output_name(self):
        return self.path.stem + ".webp"


def find_photos(photographer_dir):
    # Hidden files are skipped, e.g. macOS ._* metadata files that share the photos' extensions
    return [
        Photo(path, photographer_dir.name)
        for path in sorted(photographer_dir.rglob("*"))
        if path.is_file() and path.suffix.lower() in EXTENSIONS
        and not any(part.startswith(".") for part in path.relative_to(photographer_dir).parts)
    ]


def read_taken(photo):
    """Returns the capture time from EXIF (only the image header is read)."""
    with Image.open(photo.path) as img:
        exif = img.getexif()
        value = exif.get_ifd(EXIF_IFD).get(EXIF_DATETIME_ORIGINAL) or exif.get(EXIF_DATETIME)
    return datetime.strptime(value.strip("\x00 "), "%Y:%m:%d %H:%M:%S") if value else None


def published_exif(original):
    """Keeps all EXIF, except the orientation, which is already applied to the pixels."""
    exif = original.getexif()
    for ifd in (EXIF_IFD, EXIF_GPS_IFD):
        exif.get_ifd(ifd)  # loads the nested IFD, so that it is written back too
    exif.pop(EXIF_ORIENTATION, None)
    return exif.tobytes()


def save_resized(img, path, size, quality, exif):
    resized = img.copy()
    resized.thumbnail((size, size), Image.Resampling.LANCZOS)
    path.parent.mkdir(parents=True, exist_ok=True)
    resized.save(path, "WEBP", quality=quality, icc_profile=img.info.get("icc_profile"), exif=exif)


def process(photo, full_path, thumb_path, overwrite):
    if overwrite or not (full_path.exists() and thumb_path.exists()):
        with Image.open(photo.path) as original:
            img = ImageOps.exif_transpose(original).convert("RGB")
            img.info["icc_profile"] = original.info.get("icc_profile")
            exif = published_exif(original)
            save_resized(img, full_path, FULL_SIZE, FULL_QUALITY, exif)
            save_resized(img, thumb_path, THUMB_SIZE, THUMB_QUALITY, exif)
    with Image.open(full_path) as full, Image.open(thumb_path) as thumb:
        return full.size, thumb.size


class FlowDict(dict):
    pass


yaml.SafeDumper.add_representer(
    FlowDict, lambda dumper, data: dumper.represent_mapping("tag:yaml.org,2002:map", data, flow_style=True)
)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--overwrite", action="store_true", help="reprocess photos that were already processed")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent, help=argparse.SUPPRESS)
    args = parser.parse_args()

    root = args.root
    sources_dir = root / "_images" / "photos"
    output_dir = root / "images" / "photos"
    config = yaml.safe_load((root / "_data" / "photos-config.yml").read_text())
    days = {str(day["date"]): day for day in config["days"]}
    photographers = config["photographers"]
    data_path = root / "_data" / "photos.yml"

    # Gallery entries by (photographer, output file), starting from the previous build
    entries = {}
    if data_path.exists():
        for day in yaml.safe_load(data_path.read_text()) or []:
            for photographer in day["photographers"]:
                for photo in photographer["photos"]:
                    entries[(photographer["id"], photo["file"])] = FlowDict(photo)
    errors = []
    photos = []
    for photographer_dir in sorted(p for p in sources_dir.glob("*") if p.is_dir()):
        if photographer_dir.name not in photographers:
            errors.append(f"{photographer_dir.name}/: not in photographers")
            continue
        found = find_photos(photographer_dir)
        print(f"Found {len(found)} photos in {photographer_dir.relative_to(root)}/")
        photos += found

    # Photos with a deleted output are regenerated from their originals, or removed when there are none
    # (before the checks below, so that removing photos can fix them)
    originals = {(photo.photographer, photo.output_name) for photo in photos}
    removed = [
        key for key in entries
        if key not in originals
        and not all((output_dir / subdir / key[0] / key[1]).exists() for subdir in ("full", "thumbnail"))
    ]
    for key in removed:
        del entries[key]

    for (photographer_id, file), entry in entries.items():
        if photographer_id not in photographers:
            errors.append(f"{file}: already in the gallery, but its photographer {photographer_id} is not in photographers")
        elif entry["taken"][:10] not in days:
            errors.append(f"{file}: already in the gallery, but its day {entry['taken'][:10]} is not a configured day")

    for photo in photos:
        photo.taken = read_taken(photo)
        if photo.taken is None:
            errors.append(f"{photo.filename}: no capture date in EXIF")
        elif str(photo.taken.date()) not in days:
            errors.append(f"{photo.filename}: taken on {photo.taken.date()}, which is not a configured day")

    outputs = {}
    for photo in photos:
        key = (photo.photographer, photo.output_name)
        if key in outputs:
            errors.append(f"{photo.path.relative_to(root)}: duplicate of {outputs[key].path.relative_to(root)}")
        outputs[key] = photo
        # A different photo with the same name (e.g. from another camera) that is in the gallery from an earlier batch
        taken = photo.taken and photo.taken.isoformat(sep=" ")
        if key in entries and taken and entries[key]["taken"] != taken and not args.overwrite:
            errors.append(
                f"{photo.path.relative_to(root)}: {photo.photographer}/{photo.output_name} is already in the gallery"
                f" from a different photo (taken {entries[key]['taken']}, this one {taken}),"
                " rename this original (or use --overwrite to replace the photo in the gallery)"
            )

    if errors:
        print(f"\n{len(errors)} problem(s):")
        print("\n".join(f"  {error}" for error in errors))
        sys.exit(1)

    paths = {
        id(photo): (
            output_dir / "full" / photo.photographer / photo.output_name,
            output_dir / "thumbnail" / photo.photographer / photo.output_name,
        )
        for photo in photos
    }
    with ProcessPoolExecutor() as pool:
        futures = [pool.submit(process, photo, *paths[id(photo)], args.overwrite) for photo in photos]
        sizes = {}
        for i, (photo, future) in enumerate(zip(photos, futures), start=1):
            sizes[id(photo)] = future.result()
            print(f"\rProcessed {i}/{len(photos)}", end="", flush=True)
    print()

    new_count = sum((photo.photographer, photo.output_name) not in entries for photo in photos)
    for photo in photos:
        (width, height), (thumb_width, thumb_height) = sizes[id(photo)]
        entries[(photo.photographer, photo.output_name)] = FlowDict(
            file=photo.output_name, taken=photo.taken.isoformat(sep=" "), width=width, height=height,
            thumb_width=thumb_width, thumb_height=thumb_height,
        )
    print(f"Added {new_count} new photos")

    for photographer_id, file in removed:
        print(f"Removed {photographer_id}/{file} (its photo or thumbnail was deleted, and there is no original)")
        for subdir in ("full", "thumbnail"):
            (output_dir / subdir / photographer_id / file).unlink(missing_ok=True)

    gallery = []
    for day_number, (date, day) in enumerate(sorted(days.items()), start=1):
        day_photographers = []
        for photographer_id, photographer in photographers.items():
            day_photos = sorted(
                (entry for (entry_photographer, _), entry in entries.items()
                 if entry_photographer == photographer_id and entry["taken"][:10] == date),
                key=lambda entry: (entry["taken"], entry["file"]),
            )
            if not day_photos:
                continue
            entry = {"id": photographer_id, "name": photographer.get("name")}
            if photographer.get("url"):
                entry["url"] = photographer["url"]
            entry["photos"] = day_photos
            day_photographers.append(entry)
        if day_photographers:
            gallery.append({"id": f"day-{day_number}", "label": day["label"], "photographers": day_photographers})

    # Written to a temporary file first, so an interrupted run does not lose the gallery
    temp_path = data_path.with_suffix(".yml.tmp")
    with open(temp_path, "w") as f:
        f.write("# Generated by scripts/build_photos.py from _data/photos-config.yml - do not edit by hand.\n")
        yaml.dump(gallery, f, Dumper=yaml.SafeDumper, sort_keys=False, allow_unicode=True, width=200)
    temp_path.replace(data_path)
    print(f"Wrote {data_path.relative_to(root)}: " + ", ".join(
        f"{day['id']}: " + " + ".join(str(len(p["photos"])) for p in day["photographers"]) for day in gallery
    ))


if __name__ == "__main__":
    main()
