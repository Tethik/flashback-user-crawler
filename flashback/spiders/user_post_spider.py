import os
import hashlib
import scrapy
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor


class UserPostSpider(scrapy.Spider):
    name = "user-posts"
    allowed_domains = ["www.flashback.org", "flashback.org"]
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"

    def __init__(self, userid, fetch_full_thread=False, *args, **kwargs):
        super(UserPostSpider, self).__init__(*args, **kwargs)
        self.userid = userid
        self.fetch_full_thread = fetch_full_thread

        self.start_urls = [
            f"https://www.flashback.org/find_posts_by_user.php?userid={userid}"
        ]

    # This is where the spider will start.
    def start_requests(self):
        password_hash = hashlib.md5(
            os.environ["FLASHBACK_PASSWORD"].encode("utf-8")
        ).hexdigest()
        formdata = {
            "do": "login",
            "vb_login_md5password": password_hash,
            "vb_login_md5password_utf": password_hash,
            "vb_login_username": os.environ["FLASHBACK_USERNAME"],
            "vb_login_password": "",
            "cookieuser": "1",
        }

        yield scrapy.FormRequest(
            "https://www.flashback.org/login.php",
            formdata=formdata,
            callback=self.parse_logged_in,
        )

    def parse_posts_list(self, response: scrapy.http.Response):
        # Fetch the posts
        for href in response.css("#posts a::attr(href)"):
            if href.get().startswith("/p"):
                yield response.follow(href, self.parse_thread)

        # Fetch all pages
        for href in response.css(".pagination a::attr(href)"):
            yield response.follow(href, self.parse_posts_list)

    def parse_logged_in(self, response: scrapy.http.Response):
        # Now that we are logged in, fetch the target user post list
        for req in self.start_urls:
            yield scrapy.Request(req, self.parse_posts_list)

    def parse_thread(self, response: scrapy.http.Response):
        page = response.url.split("/")[3]  # http://blbla.com/< 3
        folder = os.path.join(os.getcwd(), "downloaded_data", self.userid, "posts")
        os.makedirs(folder, exist_ok=True)
        filename = f"{folder}/{page}.html"
        with open(filename, "wb") as f:
            f.write(response.body)
        self.log("Saved file %s" % filename)

        # Fetch other pages of the same thread
        if self.fetch_full_thread:
            for href in response.css(".pagination a::attr(href)"):
                yield response.follow(href, self.parse_thread)

