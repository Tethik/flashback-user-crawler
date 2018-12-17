# Flashback User Posts Crawler

![cat](https://66.media.tumblr.com/5face01e81b48d0a4403fee24a09e838/tumblr_o14899nCAX1v56zzqo5_500.jpg)

A simple crawler that fetches all of a users posts in their raw html form from the flashback.org website.

⚠ Only fetches the last 1000 posts, due to a limitation on how many posts are listed on a user's profile.

You will need:

1. python3 and pipenv
2. a throwaway flashback.org account. https://www.throwawaymail.com/ worked great for me to create an account with.
3. a VPN or proxy. I used https://mullvad.net

# Install / Setup

Use `pipenv install` to install all dependencies.

Addd your throwaway username and password in a `.env` file inside the project root, like the following.

```
FLASHBACK_USERNAME=username
FLASHBACK_PASSWORD=password
```

Next run `pipenv shell` to activate the environment.

# Example Usage

The following command will start a crawl and save all posts in their original html into the `downloaded_data` folder.
It requires a target userid, which you can find in the url by navigating to the target user's profile page
in your browser.

```
scrapy crawl user-posts -a userid=221078
```

If you'd like the entire threads, i.e. with all the pages, you can run the command with the `-a fetch_full_thread=True` flag.
Note that this will likely take a lot longer.

# Other helpful stuff

To verify how many posts were downloaded, I counted downloaded files via `ls -1q downloaded_data/221078/posts/ | wc -l`
then compared against the number given on the profile.
