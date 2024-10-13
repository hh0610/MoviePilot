from typing import Any, Optional, Union

import requests
import urllib3
from requests import Response, Session
from urllib3.exceptions import InsecureRequestWarning

from app.log import logger

urllib3.disable_warnings(InsecureRequestWarning)


class RequestUtils:
    _headers: dict = None
    _cookies: Union[str, dict] = None
    _proxies: dict = None
    _timeout: int = 20
    _session: Session = None

    def __init__(self,
                 headers: dict = None,
                 ua: str = None,
                 cookies: Union[str, dict] = None,
                 proxies: dict = None,
                 session: Session = None,
                 timeout: int = None,
                 referer: str = None,
                 content_type: str = None,
                 accept_type: str = None):
        if not content_type:
            content_type = "application/x-www-form-urlencoded; charset=UTF-8"
        if headers:
            self._headers = headers
        else:
            self._headers = {
                "User-Agent": ua,
                "Content-Type": content_type,
                "Accept": accept_type,
                "referer": referer
            }
        if cookies:
            if isinstance(cookies, str):
                self._cookies = self.cookie_parse(cookies)
            else:
                self._cookies = cookies
        if proxies:
            self._proxies = proxies
        if session:
            self._session = session
        if timeout:
            self._timeout = timeout

    def request(self, method: str, url: str, raise_exception: bool = False, **kwargs) -> Optional[Response]:
        """
        发起HTTP请求
        :param method: HTTP方法，如 get, post, put 等
        :param url: 请求的URL
        :param raise_exception: 是否在发生异常时抛出异常，否则默认拦截异常返回None
        :param kwargs: 其他请求参数，如headers, cookies, proxies等
        :return: HTTP响应对象
        :raises: requests.exceptions.RequestException 仅raise_exception为True时会抛出
        """
        if self._session is None:
            req_method = requests.request
        else:
            req_method = self._session.request
        kwargs.setdefault("headers", self._headers)
        kwargs.setdefault("cookies", self._cookies)
        kwargs.setdefault("proxies", self._proxies)
        kwargs.setdefault("timeout", self._timeout)
        kwargs.setdefault("verify", False)
        kwargs.setdefault("stream", False)
        try:
            return req_method(method, url, **kwargs)
        except requests.exceptions.RequestException as e:
            logger.debug(f"请求失败: {e}")
            if raise_exception:
                raise
            return None

    def get(self, url: str, params: dict = None, **kwargs) -> Optional[str]:
        """
        发送GET请求
        :param url: 请求的URL
        :param params: 请求的参数
        :param kwargs: 其他请求参数，如headers, cookies, proxies等
        :return: 响应的内容，若发生RequestException则返回None
        """
        response = self.request(method="get", url=url, params=params, **kwargs)
        return str(response.content, "utf-8") if response else None

    def post(self, url: str, data: Any = None, json: dict = None, **kwargs) -> Optional[Response]:
        """
        发送POST请求
        :param url: 请求的URL
        :param data: 请求的数据
        :param json: 请求的JSON数据
        :param kwargs: 其他请求参数，如headers, cookies, proxies等
        :return: HTTP响应对象，若发生RequestException则返回None
        """
        if json is None:
            json = {}
        return self.request(method="post", url=url, data=data, json=json, **kwargs)

    def put(self, url: str, data: Any = None, **kwargs) -> Optional[Response]:
        """
        发送PUT请求
        :param url: 请求的URL
        :param data: 请求的数据
        :param kwargs: 其他请求参数，如headers, cookies, proxies等
        :return: HTTP响应对象，若发生RequestException则返回None
        """
        return self.request(method="put", url=url, data=data, **kwargs)

    def get_res(self,
                url: str,
                params: dict = None,
                data: Any = None,
                json: dict = None,
                allow_redirects: bool = True,
                raise_exception: bool = False,
                **kwargs) -> Optional[Response]:
        """
        发送GET请求并返回响应对象
        :param url: 请求的URL
        :param params: 请求的参数
        :param data: 请求的数据
        :param json: 请求的JSON数据
        :param allow_redirects: 是否允许重定向
        :param raise_exception: 是否在发生异常时抛出异常，否则默认拦截异常返回None
        :param kwargs: 其他请求参数，如headers, cookies, proxies等
        :return: HTTP响应对象，若发生RequestException则返回None
        :raises: requests.exceptions.RequestException 仅raise_exception为True时会抛出
        """
        return self.request(method="get",
                            url=url,
                            params=params,
                            data=data,
                            json=json,
                            allow_redirects=allow_redirects,
                            raise_exception=raise_exception,
                            **kwargs)

    def post_res(self,
                 url: str,
                 data: Any = None,
                 params: dict = None,
                 allow_redirects: bool = True,
                 files: Any = None,
                 json: dict = None,
                 raise_exception: bool = False,
                 **kwargs) -> Optional[Response]:
        """
        发送POST请求并返回响应对象
        :param url: 请求的URL
        :param data: 请求的数据
        :param params: 请求的参数
        :param allow_redirects: 是否允许重定向
        :param files: 请求的文件
        :param json: 请求的JSON数据
        :param kwargs: 其他请求参数，如headers, cookies, proxies等
        :param raise_exception: 是否在发生异常时抛出异常，否则默认拦截异常返回None
        :return: HTTP响应对象，若发生RequestException则返回None
        :raises: requests.exceptions.RequestException 仅raise_exception为True时会抛出
        """
        return self.request(method="post",
                            url=url,
                            data=data,
                            params=params,
                            allow_redirects=allow_redirects,
                            files=files,
                            json=json,
                            raise_exception=raise_exception,
                            **kwargs)

    def put_res(self,
                url: str,
                data: Any = None,
                params: dict = None,
                allow_redirects: bool = True,
                files: Any = None,
                json: dict = None,
                raise_exception: bool = False,
                **kwargs) -> Optional[Response]:
        """
        发送PUT请求并返回响应对象
        :param url: 请求的URL
        :param data: 请求的数据
        :param params: 请求的参数
        :param allow_redirects: 是否允许重定向
        :param files: 请求的文件
        :param json: 请求的JSON数据
        :param raise_exception: 是否在发生异常时抛出异常，否则默认拦截异常返回None
        :param kwargs: 其他请求参数，如headers, cookies, proxies等
        :return: HTTP响应对象，若发生RequestException则返回None
        :raises: requests.exceptions.RequestException 仅raise_exception为True时会抛出
        """
        return self.request(method="put",
                            url=url,
                            data=data,
                            params=params,
                            allow_redirects=allow_redirects,
                            files=files,
                            json=json,
                            raise_exception=raise_exception,
                            **kwargs)

    @staticmethod
    def cookie_parse(cookies_str: str, array: bool = False) -> Union[list, dict]:
        """
        解析cookie，转化为字典或者数组
        :param cookies_str: cookie字符串
        :param array: 是否转化为数组
        :return: 字典或者数组
        """
        if not cookies_str:
            return {}
        cookie_dict = {}
        cookies = cookies_str.split(";")
        for cookie in cookies:
            cstr = cookie.split("=")
            if len(cstr) > 1:
                cookie_dict[cstr[0].strip()] = cstr[1].strip()
        if array:
            return [{"name": k, "value": v} for k, v in cookie_dict.items()]
        return cookie_dict