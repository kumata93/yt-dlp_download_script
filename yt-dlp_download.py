import subprocess
import argparse
import sys

def run_cmd(cmd):
    """コマンドを実行するヘルパー関数"""
    try:
        # リスト形式で渡すことで、OSごとのエスケープ処理をsubprocessに任せる
        is_shell = isinstance(cmd, str)
        subprocess.run(cmd, shell=is_shell, check=True)
    except subprocess.CalledProcessError as e:
        print(f"\nコマンドの実行中にエラーが発生しました: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="yt-dlp 自動更新＆ダウンロードツール")
    parser.add_argument("url", help="ダウンロードしたいURL")
    parser.add_argument("--mp3", action="store_true", help="MP3形式でダウンロードする場合に指定")
    
    # 追加した引数
    parser.add_argument("-t", "--title", help="曲名（ファイル名、タイトル、アルバム名に設定されます）")
    parser.add_argument("-a", "--artist", help="アーティスト名（参加アーティスト、アルバムアーティストに設定されます）")
    
    args = parser.parse_args()

    # 1. インストール確認 ＆ アップデート
    print("yt-dlpの確認と更新を行っています...")
    run_cmd(["pip", "install", "-U", "yt-dlp"])

    # 2. ダウンロード処理
    print("\n準備完了。ダウンロードを開始します。")
    if args.mp3:
        print(f"[{args.url}] を MP3 でダウンロード中...")
        
        # コマンドをリストで組み立てる
        cmd = ["yt-dlp", "-x", "--audio-format", "mp3"]
        
        # ファイル名の指定
        if args.title:
            cmd.extend(["-o", f"{args.title}.%(ext)s"])
            
        # メタデータの指定 (ffmpegに渡す引数を構築)
        pp_args = []
        if args.title:
            # ダブルクォーテーションが含まれる場合の構文エラー防止
            safe_title = args.title.replace('"', '')
            pp_args.append(f'-metadata title="{safe_title}"')
            pp_args.append(f'-metadata album="{safe_title}"')
            
        if args.artist:
            safe_artist = args.artist.replace('"', '')
            pp_args.append(f'-metadata artist="{safe_artist}"')
            pp_args.append(f'-metadata album_artist="{safe_artist}"')
            
        if pp_args:
            # yt-dlpの仕様に合わせて、postprocessor-argsは一つの文字列として渡す
            cmd.extend(["--postprocessor-args", " ".join(pp_args)])
            
        cmd.append(args.url)
        run_cmd(cmd)
        
    else:
        print(f"[{args.url}] を 動画 でダウンロード中...")
        run_cmd(["yt-dlp", args.url])

    print("\nダウンロードが完了しました。")

if __name__ == "__main__":
    main()