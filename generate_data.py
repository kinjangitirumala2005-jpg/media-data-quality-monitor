
import pandas as pd
import numpy as np

np.random.seed(42)

n = 500

df = pd.DataFrame({
    "event_id": range(1, n + 1),
    "user_id": np.random.randint(1000, 2000, n),
    "event_type": np.random.choice(
        ["play", "pause", "login", "subscription"], n
    ),
    "watch_duration": np.random.randint(1, 600, n),
    "device": np.random.choice(
        ["mobile", "desktop", "smart_tv", "tablet"], n
    ),
    "timestamp": pd.date_range(
        "2026-11-01", periods=n, freq="min"
    )
})

# Introduce intentional data quality issues
df.loc[5, "user_id"] = np.nan
df.loc[12, "watch_duration"] = -10
df.loc[20, "event_type"] = "invalid_event"
df.loc[30, "event_id"] = 10

df.to_csv("streaming_events.csv", index=False)

print("Streaming event dataset generated successfully!")
print("Total records:", len(df))
