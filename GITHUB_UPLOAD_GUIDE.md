# 📤 GitHub Upload Instructions

Follow these steps to upload your project to GitHub:

## Step 1: Initialize Git Repository

Open your terminal in the project directory and run:

```bash
cd "d:\6 Semester Subjects\Data Science\Assignment_01"
git init
```

## Step 2: Add Remote Repository

```bash
git remote add origin https://github.com/AbdurRafayBaig/NYC-Toll-Compliance-Audit-2025.git
```

## Step 3: Stage All Files

```bash
git add .
```

This will add all files except those listed in `.gitignore`

## Step 4: Create Initial Commit

```bash
git commit -m "Initial commit: NYC Toll Compliance Audit 2025 - Complete data pipeline, analytics, and interactive dashboard"
```

## Step 5: Push to GitHub

```bash
git branch -M main
git push -u origin main
```

## 🔐 Authentication

If prompted for credentials:
- **Username**: AbdurRafayBaig
- **Password**: Use a Personal Access Token (PAT), not your GitHub password

### How to create a Personal Access Token:
1. Go to GitHub.com → Settings → Developer settings → Personal access tokens
2. Click "Generate new token (classic)"
3. Give it a name like "NYC Audit Project"
4. Select scopes: `repo` (full control of private repositories)
5. Click "Generate token"
6. Copy the token and use it as your password

## ✅ Verify Upload

After pushing, visit:
https://github.com/AbdurRafayBaig/NYC-Toll-Compliance-Audit-2025

You should see all your files uploaded!

## 📝 Files That Will Be Uploaded

✅ pipeline.py
✅ dashboard.py
✅ requirements.txt
✅ README.md
✅ audit_report.md
✅ src/ (all Python modules)
✅ .gitignore

❌ .venv/ (excluded by .gitignore)
❌ data/*.parquet (excluded - too large)
❌ output/*.csv (excluded - generated files)

## 🆘 Troubleshooting

**Error: "remote origin already exists"**
```bash
git remote remove origin
git remote add origin https://github.com/AbdurRafayBaig/NYC-Toll-Compliance-Audit-2025.git
```

**Error: "failed to push some refs"**
```bash
git pull origin main --allow-unrelated-histories
git push -u origin main
```
