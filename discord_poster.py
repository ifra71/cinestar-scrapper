import os

import requests
from dotenv import load_dotenv

load_dotenv()

WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")


def send_discord_message(content):
    if not WEBHOOK_URL:
        raise ValueError("DISCORD_WEBHOOK_URL was not found in .env")

    response = requests.post(
        WEBHOOK_URL,
        json={"content": content},
        timeout=15,
    )

    response.raise_for_status()
    print("Discord message sent successfully.")



def send_movie_list(heading, movies):
    if not WEBHOOK_URL:
        raise ValueError("DISCORD_WEBHOOK_URL was not found in .env")

    for start in range(0, len(movies), 10):
        batch = movies[start:start + 10]
        embeds = []

        for movie in batch:
            embed = {
                "title": movie["title"],
                "url": movie.get("details_url"),
                "description": f'Release date: {movie["release_date"]}',
            }

            if movie.get("poster_url"):
                embed["image"] = {"url": movie["poster_url"]}

            embeds.append(embed)

        response = requests.post(
            WEBHOOK_URL,
            json={
                "content": heading if start == 0 else f"{heading} (continued)",
                "embeds": embeds,
            },
            timeout=30,
        )

        response.raise_for_status()

    print(f"{heading}: sent {len(movies)} movies to Discord.")



def send_showtimes(movie, cinemas):
    if not WEBHOOK_URL:
        raise ValueError("DISCORD_WEBHOOK_URL was not found in .env")

    description = ""

    for cinema in cinemas:
        description += f'\n**{cinema["cinema"]}**\n'

        for session in cinema["sessions"]:
            times = ", ".join(session["times"]) or "No times listed"
            description += f'**{session["date"]}** — {times}\n'

    if not description:
        description = "No showtimes currently listed."

    embed = {
        "title": movie["title"],
        "description": description[:4000],
    }

    if movie.get("poster_url"):
        embed["thumbnail"] = {"url": movie["poster_url"]}

    if movie.get("details_url"):
        embed["url"] = movie["details_url"]

    response = requests.post(
        WEBHOOK_URL,
        json={
            "content": f'Showtimes — {movie["title"]}',
            "embeds": [embed],
        },
        timeout=30,
    )

    response.raise_for_status()
    print(f'Showtimes sent for {movie["title"]}.')
