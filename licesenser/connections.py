import appdirs
import requests_cache

session = requests_cache.CachedSession(
    appdirs.user_cache_dir("licesenser", "bcx"),  # change with app name
    use_cache_dir=True,
    cache_control=True,
    expire_after=requests_cache.timedelta(days=7),
    allowable_codes=[200, 400],
    allowable_methods=["GET"],
    match_headers=["Accept-Language"],
    stale_if_error=True,
)
