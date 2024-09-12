import os
import json
import asyncio
import threading
from datetime import datetime

import httpx

from app.utils.headers_manager import QueueHeaders  
from app.search_engines.base import BaseSearchEngine


SOCIALDATA_API_KEY = os.getenv('SOCIALDATA_API_KEY')

X_HOST = 'https://x.com'

class XSearch(BaseSearchEngine):

    # headers_manager = QueueHeaders()

    # async def _get_headers(self):
    #     self.headers_manager.get(timeout=5)

    # async def search(self, query: str, limit:int = 10, timeout:int=5, **kwargs) -> list:
    #     product_type = kwargs.get("product_type", "Latest")
    #     # 如果长时间未获取到headers，则会
    #     ok,headers = await self._get_headers()
    #     url = X_HOST + '/i/api/graphql/UN1i3zUiCWa-6r-Uaho4fw/SearchTimeline'
    #     params_data = {k: json.dumps(v, indent=None, separators=(',', ':')) for k, v in {
    #         "variables": {"rawQuery":query,"count":20,"querySource":"typed_query","product":product_type},
    #         "features": {"rweb_tipjar_consumption_enabled":True,"responsive_web_graphql_exclude_directive_enabled":True,"verified_phone_label_enabled":False,"creator_subscriptions_tweet_preview_api_enabled":True,"responsive_web_graphql_timeline_navigation_enabled":True,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":False,"communities_web_enable_tweet_community_results_fetch":True,"c9s_tweet_anatomy_moderator_badge_enabled":True,"articles_preview_enabled":True,"responsive_web_edit_tweet_api_enabled":True,"graphql_is_translatable_rweb_tweet_is_translatable_enabled":True,"view_counts_everywhere_api_enabled":True,"longform_notetweets_consumption_enabled":True,"responsive_web_twitter_article_tweet_consumption_enabled":True,"tweet_awards_web_tipping_enabled":False,"creator_subscriptions_quote_tweet_preview_enabled":False,"freedom_of_speech_not_reach_fetch_enabled":True,"standardized_nudges_misinfo":True,"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":True,"rweb_video_timestamps_enabled":True,"longform_notetweets_rich_text_read_enabled":True,"longform_notetweets_inline_media_enabled":True,"responsive_web_enhance_cards_enabled":False}
    #     }.items()}
    #     filters = {
    #         "Latest": "live",
    #         "Top": "top",
    #         "People": "user",
    #         "Media": "media",
    #         "Lists": "lists"
    #     }
    #     headers["Referer"] = f"{X_HOST}/search?q={query}&src=typed_query&f={filters[product_type]}"

    #     async with httpx.AsyncClient(headers=headers) as client:
    #         response = await client.get(url, headers=headers, params=params_data, **kwargs)
    #         # 校验状态码
    #         # TODO: 错误处理，当前请求失败，则重新请求
    #         return response.json()
        
        # async def get_results():
        #     await asyncio.sleep(timeout-1)
        #     return [{
        #         'link': 'https://www.x.com',
        #         'title': 'X',
        #         'host': 'x.com',
        #         'content': 'X is a social media platform'
        #         }]
        # results = await get_results()
        # return results

    def format_tweet(id,tweet):
        is_retweet = 'RT ' if tweet.get('isRetweet', False) else ''
        author = tweet.get('author', {}).get('userName', 'username')
        created_at = tweet.get('createdAt', '')
        created_at = datetime.fromisoformat(created_at.replace("Z", "+00:00")).strftime('%Y-%m-%d %H:%M:%S')
        
        text = tweet.get('text', '')  # Ensure text is not undefined
        formatted_text = '\n> '.join(text.split('\n'))
        
        # return f"""**{id}:{is_retweet}@{author} - {created_at}**\n\n> {formatted_text}\n\n*retweets: {tweet.get('retweetCount', 0)}, replies: {tweet.get('replyCount', 0)}, likes: {tweet.get('likeCount', 0)}, quotes: {tweet.get('quoteCount', 0)}, views: {tweet.get('viewCount', 0)}*\n"""
        return f"""**{id}:{is_retweet}@{author} - {created_at}**\n\n> {formatted_text}\n"""
    
    def transform_data(self, tweet):
        return {
            "id": tweet["id_str"],
            "link": f"{X_HOST}/{tweet['user'].get('screen_name', '')}/status/{tweet['id_str']}",
            "title": f"{tweet['user'].get('name', '')} on X",
            "host": X_HOST,
            "content": "RT:" if tweet.get("retweeted_status") else "" + tweet.get("full_text", tweet.get("text", ""))[:200],
            # "createdAt": tweet["tweet_created_at"],
            "createdAt": datetime.fromisoformat(tweet["tweet_created_at"].replace("Z", "+00:00")).strftime('%Y-%m-%d %H:%M:%S'),
            "author": tweet["user"].get("name", ""),
            "author_avatar":tweet["user"].get("profile_image_url_https", ""),
            
            "source": "X",
            # "isRetweet": True if tweet.get("retweeted_status") else False,
            # "author": {"userName": tweet["user"].get("screen_name", ""), "profile_image_url_https":tweet["user"].get("profile_image_url_https", "")},
            # "text": tweet.get("full_text", tweet.get("text", "")),

            # "retweetCount": tweet["retweet_count"],
            # "replyCount": tweet["reply_count"],
            # "likeCount": tweet["favorite_count"],
            # "quoteCount": tweet["quote_count"],
            # "viewCount": tweet.get("views_count", 0)
        }

    async def search(self, query: str, limit:int = 10, timeout:int=5, **kwargs) -> list:
        url = 'https://api.socialdata.tools/twitter/search'
        params = {
            'query': query.strip()+' -filter:retweets',
            'type': 'Latest'
        }
        headers = {
            'Authorization': 'Bearer ' + SOCIALDATA_API_KEY
        }
        # res = requests.get(url, params=params, headers=headers)
        async with httpx.AsyncClient(proxy=self.proxy) as client:
            res = await client.get(url, params=params, headers=headers)
        status_code = res.status_code
        if status_code == 200:
            tweets = [self.transform_data(tweet) for tweet in res.json()['tweets'][:limit]]
            return tweets
        else:
            print(res.__dict__)
            return []


