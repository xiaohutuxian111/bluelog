"""
@FileName：utils.py
@Author：stone
@Time：2023/5/10 16:36
@Description:
"""

from urllib.parse import urlparse, urljoin
from flask import request, redirect, url_for


def is_safe_url(target):
    """验证用户的亲求地址是否被冲定向"""
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


def redirect_back(default='blog.index', **kwargs):
    """重定向到默认的路径"""
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(default, **kwargs))
