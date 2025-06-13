import os
from git import Repo

def push_to_github():
    repo_dir = os.getcwd()
    repo = Repo.init(repo_dir)

    github_token = os.getenv("GITHUB_TOKEN")
    github_repo = os.getenv("GITHUB_REPO")

    if not github_token or not github_repo:
        raise Exception("❌ .env файлд GITHUB_TOKEN эсвэл GITHUB_REPO алга байна!")

    origin_url = f"https://{github_token}@github.com/{github_repo}.git"

    if "origin" not in [remote.name for remote in repo.remotes]:
        repo.create_remote("origin", origin_url)
    else:
        repo.delete_remote("origin")
        repo.create_remote("origin", origin_url)

    repo.git.add(A=True)
    repo.index.commit("🤖 Auto-pushed from Replit via push_code.py")
    repo.git.push("origin", "main", force=True)
    print("✅ Код амжилттай GitHub руу push хийгдлээ!")

if __name__ == "__main__":
    push_to_github()