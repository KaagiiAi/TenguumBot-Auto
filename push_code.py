import os
import subprocess
import datetime

def push_to_github():
    repo_url = f"https://{os.getenv('GITHUB_TOKEN')}@github.com/{os.getenv('GITHUB_REPO')}.git"
    commit_msg = f"🔄 Auto-pushed at {datetime.datetime.utcnow().isoformat()}"

    try:
        # Git тохиргоонууд
        subprocess.run(["git", "config", "--global", "user.email", "tenguun@bot.ai"], check=True)
        subprocess.run(["git", "config", "--global", "user.name", "TenguunBot"], check=True)

        # Git коммандууд
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "branch", "-M", "main"], check=True)
        subprocess.run(["git", "remote", "add", "origin", repo_url], check=True)
        subprocess.run(["git", "push", "-u", "origin", "main", "--force"], check=True)

        print("✅ Код амжилттай GitHub руу push хийгдлээ!")
    except subprocess.CalledProcessError as e:
        print("❌ Алдаа гарлаа:", e)

if __name__ == "__main__":
    push_to_github()