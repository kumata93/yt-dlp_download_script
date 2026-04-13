import subprocess
import argparse
import sys

def run_cmd(cmd):
    """コマンドを実行するヘルパー関数だよ"""
    try:
        # 実行中の出力（プログレスバーとか）もそのまま見れるようにしておくね
        subprocess.run(cmd, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"\nエラーが出ちゃったみたい... 確認してみてね: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="yt-dlp自動更新＆ダウンロードツール")
    parser.add_argument("url", help="ダウンロードしたいURL")
    parser.add_argument("--mp3", action="store_true", help="MP3形式でダウンロードする場合は指定してね")
    args = parser.parse_args()

    # 1. インストール確認 ＆ アップデート
    print("yt-dlpの確認と更新をしてるよ！ちょっと待っててね...")
    # pip経由でインストール・更新するのが一番手軽だからこれにしてるよ
    run_cmd("pip install -U yt-dlp")

    # 2. ダウンロード処理
    print("\n準備完了！ダウンロードを始めるね。")
    if args.mp3:
        # 音声のみ抽出してMP3に変換するコマンドだよ
        print(f"[{args.url}] を MP3 でダウンロード中...")
        run_cmd(f'yt-dlp -x --audio-format mp3 "{args.url}"')
    else:
        # デフォルトの高画質動画でダウンロードするコマンドだよ
        print(f"[{args.url}] を 動画 でダウンロード中...")
        run_cmd(f'yt-dlp "{args.url}"')

    print("\nお疲れ様！ダウンロード完了したよ♡")

if __name__ == "__main__":
    main()