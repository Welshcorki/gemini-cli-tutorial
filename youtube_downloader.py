

import yt_dlp

def download_youtube_video(url):
    """
    주어진 YouTube URL에서 동영상을 다운로드합니다.
    """
    ydl_opts = {
        'format': 'best',
        'outtmpl': '%(title)s.%(ext)s',
        'noplaylist': True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print(f"\n성공적으로 다운로드했습니다: {url}")
    except Exception as e:
        print(f"\n다운로드 중 오류가 발생했습니다: {e}")

if __name__ == "__main__":
    print("YouTube 동영상 다운로더")
    video_url = input("다운로드할 YouTube 동영상 URL을 입력하세요: ")
    if video_url:
        download_youtube_video(video_url)
    else:
        print("URL이 입력되지 않았습니다. 프로그램을 종료합니다.")

