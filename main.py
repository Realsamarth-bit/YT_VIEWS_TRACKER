import requests
import time
import csv
from datetime import datetime

# ==========================
# CONFIGURATION
# ==========================
API_KEY = "AIzaSyCysIYbV9tMz4iDFYwH****************"   # Replace with your YouTube API key
CSV_LOGGING = True         # Set to True to save data in CSV
CSV_FILE = "youtube_views_log.csv"


def get_views(video_id):
    """
    Fetch total view count for a given YouTube video ID.
    Returns integer view count or None if failed.
    """
    url = "https://www.googleapis.com/youtube/v3/videos"
    params = {
        "part": "statistics",
        "id": video_id,
        "key": API_KEY
    }
    try:
        res = requests.get(url, params=params, timeout=10)
        res.raise_for_status()
        data = res.json()
        if not data["items"]:
            print(f"[ERROR] Invalid Video ID: {video_id}")
            return None
        return int(data["items"][0]["statistics"]["viewCount"])
    except Exception as e:
        print(f"[ERROR] Fetching views failed: {e}")
        return None


def log_to_csv(timestamp, views, live_views, note=""):
    """Append tracking data to CSV file."""
    if not CSV_LOGGING:
        return
    with open(CSV_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, views, live_views, note])


def track_video(video_id):
    """
    Track YouTube video views over intervals:
    - Initial
    - 1 min
    - 3 min
    - 5 min
    """
    print("=" * 60)
    print("       📊 YOUTUBE LIVE VIEWS TRACKER")
    print("=" * 60)

    # STEP 1: Initial Views
    initial_views = get_views(video_id)
    if initial_views is None:
        return
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] Initial Views: {initial_views}")
    log_to_csv(timestamp, initial_views, 0, "Initial")

    # STEP 2: After 1 Minute
    print("\n⏳ Waiting 1 minute...")
    time.sleep(60)
    views_1min = get_views(video_id)
    if views_1min is None:
        return
    live_1min = views_1min - initial_views
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] Views after 1 min: {views_1min} | Live 1 min views = {live_1min}")
    log_to_csv(timestamp, views_1min, live_1min, "1 min")

    # STEP 3: After 3 Minutes (2 more min)
    print("\n⏳ Waiting 2 more minutes (total 3)...")
    time.sleep(120)
    views_3min = get_views(video_id)
    if views_3min is None:
        return
    live_3min = views_3min - initial_views
    avg_per_min = live_3min / 3
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] Views after 3 min: {views_3min} | Live 3 min views = {live_3min}")
    print(f"📈 Average per 1 min views (till 3 min) = {avg_per_min:.2f}")
    log_to_csv(timestamp, views_3min, live_3min, "3 min avg")

    # STEP 4: After 5 Minutes (2 more min)
    print("\n⏳ Waiting 2 more minutes (total 5)...")
    time.sleep(120)
    views_5min = get_views(video_id)
    if views_5min is None:
        return
    live_5min = views_5min - initial_views
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] Views after 5 min: {views_5min} | Live 5 min views = {live_5min}")
    log_to_csv(timestamp, views_5min, live_5min, "5 min")

    print("\n✅ Tracking Finished Successfully.")
    print("=" * 60)


def init_csv():
    """Initialize CSV file with headers if enabled."""
    if CSV_LOGGING:
        with open(CSV_FILE, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Timestamp", "Total Views", "Live Views", "Note"])


if __name__ == "__main__":
    video_id = input("🎥 Enter YouTube Video ID: ").strip()
    init_csv()
    track_video(video_id)
    #

