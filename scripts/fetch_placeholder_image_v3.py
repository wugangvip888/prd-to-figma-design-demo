#!/usr/bin/env python3
"""
fetch_placeholder_image.py
从 Unsplash 按关键词获取占位图 URL，供工作流在需要图片的地方使用。

用法：
    python scripts/fetch_placeholder_image.py --query "campus story"
    python scripts/fetch_placeholder_image.py --query "ancient chinese palace" --count 3

输出：
    单张：直接输出图片 URL（字符串）
    多张：输出 JSON 数组
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.request
import urllib.parse
import urllib.error
from pathlib import Path

# 自动加载项目根目录的 .env 文件
ROOT = Path(__file__).resolve().parents[1]
ENV_FILE = ROOT / ".env"


def load_env(env_path: Path) -> None:
    """从 .env 文件加载环境变量（仅当变量尚未设置时）。"""
    if not env_path.exists():
        return
    with open(env_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = value


def fetch_images(
    query: str,
    count: int = 1,
    orientation: str = "landscape",
) -> list[dict]:
    """
    从 Unsplash 搜索图片，返回图片信息列表。

    返回格式：
    [
      {
        "url": "https://images.unsplash.com/...",   # 可直接嵌入 Figma 的图片 URL
        "thumb_url": "https://...",                  # 缩略图（更小，加载快）
        "alt": "图片描述",
        "photographer": "摄影师名",
        "unsplash_link": "https://unsplash.com/..."  # 原始页面（用于署名）
      },
      ...
    ]
    """
    access_key = os.environ.get("UNSPLASH_ACCESS_KEY", "").strip()
    if not access_key:
        sys.exit(0)

    params = urllib.parse.urlencode(
        {
            "query": query,
            "per_page": min(count, 30),
            "orientation": orientation,
            "content_filter": "high",
        }
    )
    api_url = f"https://api.unsplash.com/search/photos?{params}"

    req = urllib.request.Request(
        api_url,
        headers={
            "Authorization": f"Client-ID {access_key}",
            "Accept-Version": "v1",
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        sys.exit(0)
    except urllib.error.URLError as e:
        sys.exit(0)

    results = data.get("results", [])
    if not results:
        return []

    images = []
    for item in results[:count]:
        # 按指定尺寸裁切（Unsplash 支持 w/h 参数）
        sized_url = item["urls"]["regular"]  # Unsplash regular 尺寸，由 Figma 图形框控制显示大小

        images.append(
            {
                "url": sized_url,
                "thumb_url": item["urls"]["thumb"],
                "alt": item.get("alt_description") or item.get("description") or query,
                "photographer": item["user"]["name"],
                "unsplash_link": item["links"]["html"],
            }
        )

    return images


def main() -> None:
    parser = argparse.ArgumentParser(
        description="从 Unsplash 获取占位图 URL",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  # 获取单张图片 URL（直接输出，方便脚本嵌套调用）
  python scripts/fetch_placeholder_image.py --query "campus life"

  # 获取 3 张，指定尺寸，输出 JSON
  python scripts/fetch_placeholder_image.py --query "ancient palace" --count 3

  # 竖向图片（适合人物/海报场景）
  python scripts/fetch_placeholder_image.py --query "portrait" --orientation portrait
        """,
    )
    parser.add_argument("--query", required=True, help="搜索关键词（英文效果更好）")
    parser.add_argument("--count", type=int, default=1, help="获取图片数量（默认 1，最多 30）")
    parser.add_argument(
        "--orientation",
        choices=["landscape", "portrait", "squarish"],
        default="landscape",
        help="图片方向（默认 landscape 横向）",
    )
    parser.add_argument(
        "--json", action="store_true", help="强制以 JSON 格式输出（默认单张只输出 URL）"
    )

    args = parser.parse_args()

    load_env(ENV_FILE)

    images = fetch_images(
        query=args.query,
        count=args.count,
        orientation=args.orientation,
    )

    if not images:
        sys.exit(0)

    # 单张且不要求 JSON：直接输出 URL，方便其他脚本调用
    if args.count == 1 and not args.json:
        print(images[0]["url"])
    else:
        print(json.dumps(images, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
