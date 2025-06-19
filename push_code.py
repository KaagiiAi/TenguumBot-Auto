import os
from git import Repo

# Төслийн үндсэн зам
project_path = os.path.dirname(os.path.abspath(__file__))

# Git тохиргоо
github_repo_url = "https://github.com/KaagiiAi/TenguunBot-Auto.git"
github_token = os.getenv("GITHUB_TOKEN")
remote_with_token = github_repo_url.replace("https://", f"https://{github_token}@")

# Git repo холбох, push хийх
if not os.path.exists(os.path.join(project_path, ".git")):
    repo = Repo.init(project_path)
    origin = repo.create_remote("origin", remote_with_token)
else:
    repo = Repo(project_path)
    origin = repo.remote("origin")

repo.git.add(all=True)
repo.index.commit("🔄 Auto sync: push from Replit TenguunBotClean")
origin.push(force=True)
print("✅ GitHub push амжилттай. Auto sync бүрэн идэвхжсэн.")