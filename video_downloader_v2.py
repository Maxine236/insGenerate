# -*- coding: utf-8 -*-
"""
Instagram 视频批量下载脚本（修复版 v2，带诊断功能）
用法：py video_downloader.py
会自动读取同文件夹下的 links.txt，下载到 videos 文件夹
"""
import re
import os
import time
import random
import yt_dlp

LINKS_FILE = "links.txt"
OUTPUT_DIR = "videos"
COOKIES_FILE = "cookies.txt"


def get_random_delay():
    return random.uniform(3, 6)


def read_file_any_encoding(file_path):
    """兼容记事本可能保存的各种编码（UTF-8/UTF-16/ANSI）"""
    for enc in ("utf-8-sig", "utf-16", "gbk", "latin-1"):
        try:
            with open(file_path, "r", encoding=enc) as f:
                content = f.read()
            # 简单校验：内容里应当出现 instagram 或 http 字样才算读对了
            if "http" in content or "instagram" in content:
                return content, enc
        except (UnicodeError, UnicodeDecodeError):
            continue
    # 都失败就用最宽容的方式读出来，供诊断
    with open(file_path, "r", encoding="latin-1", errors="replace") as f:
        return f.read(), "latin-1(强制)"


def extract_instagram_links(file_path):
    if not os.path.isfile(file_path):
        print(f"[诊断] 找不到文件: {os.path.abspath(file_path)}")
        print("[诊断] 当前文件夹里的文件有:")
        for name in os.listdir("."):
            print(f"   - {name}")
        return []

    content, enc = read_file_any_encoding(file_path)
    print(f"[诊断] 成功读取 {file_path}（编码: {enc}），内容共 {len(content)} 个字符")

    pattern = r"https?://(?:www\.)?instagram\.com/(?:[A-Za-z0-9_.]+/)?(reel|reels|p|tv)/([A-Za-z0-9_-]+)"
    matches = re.findall(pattern, content)

    links = []
    seen = set()
    for kind, code in matches:
        kind = "reel" if kind == "reels" else kind
        url = f"https://www.instagram.com/{kind}/{code}/"
        if code not in seen:
            seen.add(code)
            links.append(url)

    if links:
        print(f"找到 {len(links)} 个链接:")
        for link in links:
            print(f"- {link}")
    else:
        print("[诊断] 没有匹配到链接。下面是程序实际读到的文件内容（前500字符），")
        print("[诊断] 请把这段完整发给帮你的人查看：")
        print("-" * 40)
        print(repr(content[:500]))
        print("-" * 40)

    return links


def download_videos(links, output_path):
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    ydl_opts = {
        "format": "best",
        "outtmpl": os.path.join(output_path, "%(upload_date)s_%(id)s.%(ext)s"),
        "ignoreerrors": True,
        "quiet": False,
        "no_warnings": True,
    }

    if os.path.isfile(COOKIES_FILE):
        ydl_opts["cookiefile"] = COOKIES_FILE
        print(f"已加载 {COOKIES_FILE}")
    else:
        print("提示：未找到 cookies.txt，先尝试不登录下载。"
              "如果失败提示需要登录，请用浏览器扩展导出 cookies.txt 放到本文件夹。")

    success, failed = 0, []
    for i, link in enumerate(links, 1):
        print(f"\n[{i}/{len(links)}] 正在下载: {link}")
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                result = ydl.download([link])
            if result == 0:
                success += 1
            else:
                failed.append(link)
        except Exception as e:
            print(f"下载失败: {e}")
            failed.append(link)

        if i < len(links):
            delay = get_random_delay()
            print(f"等待 {delay:.1f} 秒后继续...")
            time.sleep(delay)

    print("\n" + "=" * 40)
    print(f"下载完成！成功 {success} 个，失败 {len(failed)} 个")
    if failed:
        print("以下链接下载失败，可以稍后重试：")
        for link in failed:
            print(f"- {link}")
    print(f"视频保存在: {os.path.abspath(output_path)}")


if __name__ == "__main__":
    print("开始提取链接...")
    links = extract_instagram_links(LINKS_FILE)

    if not links:
        print("未找到任何 Instagram 链接，请把上面的[诊断]信息发给帮你的人")
        raise SystemExit

    print(f"\n共 {len(links)} 个视频，开始下载...")
    download_videos(links, OUTPUT_DIR)
