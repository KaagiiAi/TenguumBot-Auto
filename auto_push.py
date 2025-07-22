import subprocess
import os

def auto_git_push():
    try:
        # Git config тохируулах (анх удаа тохируулаагүй бол)
        subprocess.run(["git", "config", "user.name", "TenguunBot"], check=True)
        subprocess.run(["git", "config", "user.email", "tenguunbot@example.com"], check=True)

        # Git add
        subprocess.run(["git", "add", "."], check=True)

        # Staged өөрчлөлт байгаа эсэхийг шалгах
        status = subprocess.run(["git", "diff", "--cached", "--quiet"])

        if status.returncode != 0:
            # Өөрчлөлт байгаа бол commit + push
            subprocess.run(["git", "commit", "-m", "🤖 Auto update from Telegram bot"], check=True)
            subprocess.run(["git", "push"], check=True)
            return "✅ Push амжилттай хийгдлээ!"
        else:
            return "ℹ️ Шинэ commit хийх өөрчлөлт олдсонгүй."

    except subprocess.CalledProcessError as e:
        return f"❌ Push амжилтгүй боллоо: {e}"