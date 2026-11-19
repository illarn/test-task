import sys
import time
import urllib.error
import urllib.request


REQUEST_COUNT = 10
CHUNK_SIZE = 64 * 1024
MIB = 1024 * 1024


def measure(url: str, opener=urllib.request.urlopen, timer=time.perf_counter):
    total_bytes = 0
    durations = []

    for _ in range(REQUEST_COUNT):
        started_at = timer()
        request = urllib.request.Request(
            url, headers={"User-Agent": "download-speed/1.0"}
        )
        with opener(request) as response:
            while chunk := response.read(CHUNK_SIZE):
                total_bytes += len(chunk)
        durations.append(timer() - started_at)

    total_time = sum(durations)
    speed = total_bytes / total_time if total_time else float("inf")
    return sum(durations) / REQUEST_COUNT, total_bytes, speed


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 1:
        print(
            'Usage: uv run python download_speed.py "ссылка на изображение"',
            file=sys.stderr,
        )
        return 2

    try:
        average_time, total_bytes, speed = measure(argv[0])
    except (urllib.error.URLError, ValueError, OSError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    print(f"Average request time: {average_time:.3f} s")
    print(f"Downloaded: {total_bytes / MIB:.3f} MiB")
    print(f"Download speed: {speed / MIB:.3f} MiB/s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
