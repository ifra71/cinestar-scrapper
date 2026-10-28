from playwright.sync_api import sync_playwright
from urllib.parse import urljoin
from discord_poster import send_movie_list, send_showtimes

BASE_URL = "https://cinestar.pk"


def get_now_showing(page):
    page.goto(f"{BASE_URL}/Browsing/Movies/NowShowing")
    page.wait_for_selector(".list-item.movie")

    movies = []

    for card in page.locator(".list-item.movie").all():
        title = card.locator(".item-title").inner_text().strip()

        image = card.locator(".image-outer img").get_attribute("src")
        poster_url = urljoin(BASE_URL, image) if image else None

        date_element = card.locator(".movie-opening-date")
        release_date = date_element.inner_text().strip() if date_element.count() else "Not listed"

        link = card.locator(".item-details a").get_attribute("href")
        details_url = urljoin(BASE_URL, link) if link else None

        movies.append({
            "title": title,
            "release_date": release_date,
            "poster_url": poster_url,
            "details_url": details_url,
        })

    return movies


def get_coming_soon(page):
    page.goto(f"{BASE_URL}/Browsing/Movies/ComingSoon")
    page.wait_for_selector(".list-item.movie")

    movies = []

    for card in page.locator(".list-item.movie").all():
        title = card.locator(".item-title").inner_text().strip()

        image = card.locator(".image-outer img").get_attribute("src")
        poster_url = urljoin(BASE_URL, image) if image else None

        date_element = card.locator(".movie-opening-date")
        release_date = date_element.inner_text().strip() if date_element.count() else "Not listed"

        link = card.locator(".item-details a").get_attribute("href")
        details_url = urljoin(BASE_URL, link) if link else None

        movies.append({
            "title": title,
            "release_date": release_date,
            "poster_url": poster_url,
            "details_url": details_url,
        })

    return movies


def get_movie_showtimes(page, movie):
    if not movie["details_url"]:
        return []

    page.goto(movie["details_url"])
    page.wait_for_selector(".film-showtimes")

    cinemas = []

    for cinema in page.locator(".film-showtimes").all():
        cinema_name = cinema.locator(".film-title").inner_text().strip()
        sessions = []

        for session in cinema.locator(".session").all():
            show_date = session.locator(".session-date").inner_text().strip()
            showtimes = session.locator("time").all_inner_texts()

            sessions.append({
                "date": show_date,
                "times": [time.strip() for time in showtimes],
            })

        cinemas.append({
            "cinema": cinema_name,
            "sessions": sessions,
        })

    return cinemas


def main():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        page = browser.new_page()

        now_showing = get_now_showing(page)
        coming_soon = get_coming_soon(page)

        send_movie_list("NOW SHOWING — CineStar", now_showing)
        send_movie_list("COMING SOON — CineStar", coming_soon)

        print("NOW SHOWING MOVIES")
        print("=" * 40)

        for movie in now_showing:
            print("Movie:", movie["title"])
            print("Release Date:", movie["release_date"])
            print("Poster:", movie["poster_url"])
            print("Details:", movie["details_url"])
            print("-" * 40)

        print("\nCOMING SOON MOVIES")
        print("=" * 40)

        for movie in coming_soon:
            print("Movie:", movie["title"])
            print("Release Date:", movie["release_date"])
            print("Poster:", movie["poster_url"])
            print("Details:", movie["details_url"])
            print("-" * 40)

        print("\nMOVIE SHOWTIMES")
        print("=" * 40)

        for movie in now_showing:
            print("\nMovie:", movie["title"])

            try:
                cinemas = get_movie_showtimes(page, movie)

                send_showtimes(movie, cinemas)

                for cinema in cinemas:
                    print("Cinema:", cinema["cinema"])

                    for session in cinema["sessions"]:
                        print("Date:", session["date"])
                        print("Times:", ", ".join(session["times"]))

                    print("-" * 30)

            except Exception as error:
                print("Could not retrieve showtimes:", error)

        browser.close()


if __name__ == "__main__":
    main()















# from playwright.sync_api import sync_playwright
# from urllib.parse import urljoin


# def main():
#     with sync_playwright() as playwright:
#         browser = playwright.chromium.launch(headless=False)
#         page = browser.new_page()

#         page.goto("https://cinestar.pk/Browsing/Movies/ComingSoon")
#         page.wait_for_selector(".list-item.movie")

#         movie_cards = page.locator(".list-item.movie")

#         print("COMING SOON MOVIES")
#         print("=" * 40)

#         for card in movie_cards.all():
#             title = card.locator(".item-title").inner_text().strip()

#             image = card.locator(".image-outer img").get_attribute("src")
#             poster_url = urljoin("https://cinestar.pk", image) if image else None

#             release_date = card.locator(".movie-opening-date").inner_text().strip()

#             link = card.locator(".item-details a").get_attribute("href")
#             details_url = urljoin("https://cinestar.pk", link) if link else None

#             print("Movie:", title)
#             print("Release Date:", release_date)
#             print("Poster:", poster_url)
#             print("Details:", details_url)
#             print("-" * 40)

#         browser.close()


# if __name__ == "__main__":
#     main()




# from playwright.sync_api import sync_playwright


# def main():
#     with sync_playwright() as playwright:
#         browser = playwright.chromium.launch(headless=False)
#         page = browser.new_page()

#         page.goto("https://cinestar.pk/Browsing/Movies/ComingSoon")
#         page.wait_for_load_state("domcontentloaded")

#         print("Page title:", page.title())
#         print("Page headings:")
#         print(page.locator("h2, h3").all_inner_texts())

#         browser.close()


# if __name__ == "__main__":
#     main()





# from playwright.sync_api import sync_playwright
# from urllib.parse import urljoin


# def main():
#     with sync_playwright() as playwright:
#         browser = playwright.chromium.launch(headless=False)
#         page = browser.new_page()

#         movie_url = "https://cinestar.pk/Browsing/Movies/Details/h-HO00001169"
#         page.goto(movie_url)
#         page.wait_for_selector(".film-showtimes")

#         cinemas = page.locator(".film-showtimes")

#         for cinema in cinemas.all():
#             cinema_name = cinema.locator(".film-title").inner_text().strip()

#             print("Cinema:", cinema_name)

#             sessions = cinema.locator(".session").all()

#             for session in sessions:
#                 show_date = session.locator(".session-date").inner_text().strip()
#                 showtimes = session.locator("time").all_inner_texts()

#                 print("Date:", show_date)

#                 for showtime in showtimes:
#                     print("Time:", showtime.strip())

#             print("-" * 40)

#         browser.close()


# if __name__ == "__main__":
#     main()









# from playwright.sync_api import sync_playwright
# from urllib.parse import urljoin


# def main():
#     with sync_playwright() as playwright:
#         browser = playwright.chromium.launch(headless=False)
#         page = browser.new_page()

#         page.goto("https://cinestar.pk/Browsing/Movies/NowShowing")

#         page.wait_for_selector("article#movies-list .list-item.movie")

#         movie_cards = page.locator("article#movies-list .list-item.movie")

#         print("Now Showing Movies")
#         print("=" * 40)

#         for card in movie_cards.all():
#             title = card.locator(".item-title").inner_text().strip()

#             image = card.locator(".image-outer img").get_attribute("src")
#             image_url = urljoin("https://cinestar.pk", image) if image else None

#             link = card.locator(".item-details a").get_attribute("href")
#             details_url = urljoin("https://cinestar.pk", link) if link else None

#             print("Movie:", title)
#             print("Poster:", image_url)
#             print("Details:", details_url)
#             print("-" * 40)

#         browser.close()


# if __name__ == "__main__":
#     main()
