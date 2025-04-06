git remote add upstream https://github.com/AI-Brokers/AIBrokers
git fetch upstream
git checkout main
git merge upstream/main
git commit -m "Merged changes from upstream"
git push origin main
