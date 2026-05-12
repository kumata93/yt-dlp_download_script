import subprocess
import argparse
import sys
import shutil

def check_dependencies():
    """依存コマンドの存在チェック"""
    if shutil.which("ffmpeg") is None:
        print("エラー: ffmpegがインストールされていないか、パスが通っていません。")
        print("動画の結合やMP3への変換、メタデータの付与にはffmpegが必要です。")
        print("インストールし、環境変数(PATH)を通してから再実行してください。")
        sys.exit(1)

def run_cmd(cmd):
    """コマンドを実行するヘルパー関数"""
    try:
        is_shell = isinstance(cmd, str)
        subprocess.run(cmd, shell=is_shell, check=True)
    except subprocess.CalledProcessError as e:
        print(f"\nコマンドの実行中にエラーが発生しました: {e}")
        sys.exit(1)

def main():
    # 実行前に依存ツールのチェック
    check_dependencies()

    parser = argparse.ArgumentParser(description="yt-dlp 自動更新＆ダウンロードツール")
    parser.add_argument("url", help="ダウンロードしたいURL")
    parser.add_argument("--mp3", action="store_true", help="MP3形式でダウンロードする場合に指定")
    parser.add_argument("-t", "--title", help="曲名（ファイル名、タイトル、アルバム名に設定されます）")
    parser.add_argument("-a", "--artist", help="アーティスト名（参加アーティスト、アルバムアーティストに設定されます）")
    
    args = parser.parse_args()

    # 1. インストール確認 ＆ アップデート
    print("yt-dlpの確認と更新を行っています...")
    # sys.executableを利用して、現在実行中のPython環境（仮想環境）にインストールする
    run_cmd([sys.executable, "-m", "pip", "install", "-U", "yt-dlp", "--quiet"])

    # 2. ダウンロード処理
    print("\n準備完了。ダウンロードを開始します。")
    if args.mp3:
        print(f"[{args.url}] を MP3 でダウンロード中...")
        
        cmd = ["yt-dlp", "-x", "--audio-format", "mp3"]
        
        if args.title:
            cmd.extend(["-o", f"{args.title}.%(ext)s"])
            
        pp_args = []
        if args.title:
            safe_title = args.title.replace('"', '')
            pp_args.append(f'-metadata title="{safe_title}"')
            pp_args.append(f'-metadata album="{safe_title}"')
            
        if args.artist:
            safe_artist = args.artist.replace('"', '')
            pp_args.append(f'-metadata artist="{safe_artist}"')
            pp_args.append(f'-metadata album_artist="{safe_artist}"')
            
        if pp_args:
            cmd.extend(["--postprocessor-args", " ".join(pp_args)])
            
        cmd.append(args.url)
        run_cmd(cmd)
        
    else:
        print(f"[{args.url}] を 動画 でダウンロード中...")
        run_cmd(["yt-dlp", args.url])

    print("\nダウンロードが完了しました。")

if __name__ == "__main__":
    main()