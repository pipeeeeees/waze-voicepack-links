import glob
import os
import shutil


def _candidate_bins_from_env():
    candidates = []

    ffmpeg_home = os.environ.get("FFMPEG_HOME") or os.environ.get("FFMPEG_PATH")
    if ffmpeg_home:
        candidates.append(ffmpeg_home)
        candidates.append(os.path.join(ffmpeg_home, "bin"))

    for entry in os.environ.get("PATH", "").split(os.pathsep):
        if entry:
            candidates.append(entry)

    return candidates


def _windows_common_bins():
    if os.name != "nt":
        return []

    local_app_data = os.environ.get("LOCALAPPDATA", "")
    winget_pattern = os.path.join(
        local_app_data,
        "Microsoft",
        "WinGet",
        "Packages",
        "Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe",
        "ffmpeg-*",
        "bin",
    )

    user_profile = os.environ.get("USERPROFILE", "")

    return [
        r"C:\\ffmpeg\\bin",
        r"C:\\ffmpeg\\",
        r"C:\\tools\\ffmpeg\\bin",
        r"C:\\Program Files\\ffmpeg\\bin",
        r"C:\\Program Files (x86)\\ffmpeg\\bin",
        r"C:\\ProgramData\\chocolatey\\bin",
        os.path.join(user_profile, "scoop", "apps", "ffmpeg", "current", "bin"),
        *glob.glob(winget_pattern),
    ]


def _resolve_binary(binary_name):
    direct_override = os.environ.get("FFMPEG_BINARY")
    if direct_override and os.path.isfile(direct_override):
        return direct_override

    if binary_name.startswith("ffprobe"):
        direct_probe_override = os.environ.get("FFPROBE_BINARY")
        if direct_probe_override and os.path.isfile(direct_probe_override):
            return direct_probe_override

    from_path = shutil.which(binary_name)
    if from_path:
        return from_path

    for bin_dir in [*_candidate_bins_from_env(), *_windows_common_bins()]:
        candidate = os.path.join(bin_dir, binary_name)
        if os.path.isfile(candidate):
            return candidate

    return None


def _prepend_to_path(bin_dirs):
    existing = os.environ.get("PATH", "")
    existing_parts = [p for p in existing.split(os.pathsep) if p]

    normalized_existing = {os.path.normcase(os.path.normpath(p)) for p in existing_parts}

    ordered_new = []
    for path in bin_dirs:
        if not path:
            continue
        normalized = os.path.normcase(os.path.normpath(path))
        if normalized in normalized_existing:
            continue
        ordered_new.append(path)
        normalized_existing.add(normalized)

    if ordered_new:
        os.environ["PATH"] = os.pathsep.join([*ordered_new, *existing_parts])


def configure_ffmpeg_for_pydub(strict=True):
    ffmpeg_bin = _resolve_binary("ffmpeg.exe" if os.name == "nt" else "ffmpeg")
    ffprobe_bin = _resolve_binary("ffprobe.exe" if os.name == "nt" else "ffprobe")

    if ffmpeg_bin and not ffprobe_bin:
        sibling_ffprobe = os.path.join(os.path.dirname(ffmpeg_bin), "ffprobe.exe" if os.name == "nt" else "ffprobe")
        if os.path.isfile(sibling_ffprobe):
            ffprobe_bin = sibling_ffprobe

    # pydub launches ffmpeg/ffprobe via subprocess and some versions ignore
    # class attributes for probing. Keep the discovered bin directories on PATH.
    ffmpeg_dir = os.path.dirname(ffmpeg_bin) if ffmpeg_bin else None
    ffprobe_dir = os.path.dirname(ffprobe_bin) if ffprobe_bin else None
    _prepend_to_path([ffmpeg_dir, ffprobe_dir])

    from pydub import AudioSegment

    if ffmpeg_bin:
        AudioSegment.converter = ffmpeg_bin
        AudioSegment.ffmpeg = ffmpeg_bin
        os.environ["FFMPEG_BINARY"] = ffmpeg_bin
    if ffprobe_bin:
        AudioSegment.ffprobe = ffprobe_bin
        os.environ["FFPROBE_BINARY"] = ffprobe_bin

    if strict and (not ffmpeg_bin or not ffprobe_bin):
        candidate_paths = [*_candidate_bins_from_env(), *_windows_common_bins()]
        checked_paths = "\n - ".join(candidate_paths[:12])
        raise RuntimeError(
            "FFmpeg binaries were not found. Install FFmpeg and ensure both "
            "ffmpeg and ffprobe are available in PATH. You can also set "
            "FFMPEG_HOME/FFMPEG_PATH (folder) or FFMPEG_BINARY/FFPROBE_BINARY "
            "(full .exe paths). Checked locations:\n - "
            f"{checked_paths}"
        )

    return ffmpeg_bin, ffprobe_bin
