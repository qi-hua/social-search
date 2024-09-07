import queue
import threading
import time
import random

class Headers:
    def get(self):
        return {
            "accept": "*/*",
            "accept-language": "zh-CN,zh;q=0.9",
            "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
            "content-type": "application/json",
            "priority": "u=1, i",
            "sec-ch-ua": "\"Chromium\";v=\"128\", \"Not;A=Brand\";v=\"24\", \"Google Chrome\";v=\"128\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Linux\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "x-client-transaction-id": "wb9ID4HsNBg/hqYJak9Yi2QK9UWfdeZS/u7Kfn5Fs/4KPXanQc7DXvdQsXSWdJ8LnBfgQ8MQFQ6NkUpSP38XpPjFoecbwg",
            "x-client-uuid": "2efd7197-a0b6-412f-a2b3-4838bc2d3512",
            "x-csrf-token": "68533ad99b9087cc627a7a6ae5a394617a0fad83b1c8a61f5a9265983eecaf9445d0b99167f2c2f939fd343df3382cd8c564eb923ec289a0b9555467440d176b689c531b4082a8ac76fa8777aa546a85",
            "x-twitter-active-user": "yes",
            "x-twitter-auth-type": "OAuth2Session",
            "x-twitter-client-language": "zh-cn",
            "cookie": "guest_id=v1%3A172492511036050844; night_mode=2; guest_id_marketing=v1%3A172492511036050844; guest_id_ads=v1%3A172492511036050844; kdt=lX5FwBt8kL9ncMRL8A1FSccCGZCeC9orYML6B9YW; auth_token=9e3ea18a93e041ff239fed24691fee32ef0c68ee; ct0=68533ad99b9087cc627a7a6ae5a394617a0fad83b1c8a61f5a9265983eecaf9445d0b99167f2c2f939fd343df3382cd8c564eb923ec289a0b9555467440d176b689c531b4082a8ac76fa8777aa546a85; twid=u%3D1827165974426218496; att=1-hVH9OzW0YXC06zrDMhThTIRVEQFm9SCTfs7hOGS2; lang=zh-cn; personalization_id=\"v1_q/7YVe1IHQ5uJwoaLgQRww==\"",
            "Referer": "https://x.com/search?q=TESLA%E8%82%A1%E7%A5%A8%E6%80%8E%E4%B9%88%E6%A0%B7&src=typed_query&f=live",
            "Referrer-Policy": "strict-origin-when-cross-origin"
        }

HEADERS = Headers()


class QueueHeaders:
    _headers: dict = {}
    token_bucket = queue.Queue()

    def get(self, timeout=None) -> tuple[str, dict]:
        """获取令牌"""
        try:
            token_id = self.token_bucket.get(timeout=timeout)
            if token_id in self._headers:
                return token_id, self._headers[token_id]
            else:
                # retry
                return self.get(timeout=timeout)
        except:
            return False, {}
        
    def put(self, token_id: str, headers: dict):
        """添加令牌"""
        self._headers[token_id] = headers
        self.token_bucket.put(token_id)

    def delete(self, token_id: str):
        """删除header"""
        if token_id in self._headers:
            del self._headers[token_id]

    def clear(self):
        """清空令牌桶"""
        self.token_bucket.queue.clear()
        self._headers.clear()

    def release(self, token_id: str):
        """释放令牌"""
        self.token_bucket.put(token_id)