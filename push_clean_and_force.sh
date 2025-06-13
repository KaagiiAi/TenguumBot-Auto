#!/bin/bash

echo "🚨 GitHub push-д орсон нууц түлхүүрийг устгаж байна..."

# 1. Firebase key orson file-уудыг устгах
rm -f *.json *.txt memory.json memory.txt

# 2. Git history-с нууц key-г арилгах
git rm -rf --cached .
git add .
git commit -m "🔥 Remove secrets before force push"

# 3. Force push хийх
echo "🚀 Force push хийгдэж байна..."
git push --force origin main

echo "✅ Амжилттай push хийлээ!"