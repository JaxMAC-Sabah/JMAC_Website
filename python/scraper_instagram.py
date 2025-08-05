import instaloader

L = instaloader.Instaloader()

L.load_session_from_file("piranisabah")  # .session filename but without the .session extension

# Get posts from a public account
profile = instaloader.Profile.from_username(L.context, "jaxpsn")

for post in profile.get_posts():
    print("📅", post.date)
    print("📝", post.caption[:200])  # print first 200 chars of caption
    print("🔗", f"https://www.instagram.com/p/{post.shortcode}/")
    print("------")
    break
