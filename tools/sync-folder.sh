#!/usr/bin/env bash
# 共享讨论文件夹 · 自动同步脚本（macOS / Linux）
#
# 作用：把你电脑上的这个文件夹和 GitHub 保持双向自动同步。
#   - Claude 写的新文件会自动出现在你的文件夹里
#   - 你放进 inbox/ 的 ChatGPT 回复会自动推上去，Claude 立刻看到
#
# 用法：
#   1) 先克隆仓库到你电脑（只做一次）：
#        git clone -b claude/japan-ai-drama-localization-zb42vp \
#          https://github.com/zhoujun11112/jinxu-helper-download.git ~/短剧讨论
#   2) 进入文件夹并启动同步（保持这个终端窗口开着）：
#        cd ~/短剧讨论 && bash tools/sync-folder.sh
#
# 停止：按 Ctrl+C

set -u

BRANCH="claude/japan-ai-drama-localization-zb42vp"
INTERVAL="${SYNC_INTERVAL:-15}"   # 每隔几秒同步一次

cd "$(dirname "$0")/.." || exit 1

echo "======================================"
echo " 共享讨论文件夹 · 自动同步已启动"
echo " 目录：$(pwd)"
echo " 分支：$BRANCH"
echo " 间隔：${INTERVAL}秒"
echo ""
echo " 把 ChatGPT 的回复存成 .md 文件，放进："
echo "   docs/japan-ai-short-drama/exchange/inbox/"
echo " 文件名：R01-gpt-to-claude.md（轮次递增）"
echo ""
echo " 保持本窗口开着。按 Ctrl+C 停止。"
echo "======================================"
echo ""

while true; do
  # 1) 拉取 Claude 的新发言
  before=$(git rev-parse HEAD 2>/dev/null)
  git pull --rebase --autostash origin "$BRANCH" -q 2>/dev/null
  after=$(git rev-parse HEAD 2>/dev/null)
  if [ "$before" != "$after" ]; then
    echo "[$(date '+%H:%M:%S')] ⬇ 收到 Claude 的新文件："
    git diff --name-only "$before" "$after" 2>/dev/null | sed 's/^/    /'
  fi

  # 2) 推送你放进来的新文件
  if [ -n "$(git status --porcelain)" ]; then
    changed=$(git status --porcelain | sed 's/^...//' | tr '\n' ' ')
    git add -A
    git commit -q -m "同步：${changed}" 2>/dev/null
    if git push -q origin "$BRANCH" 2>/dev/null; then
      echo "[$(date '+%H:%M:%S')] ⬆ 已发送给 Claude：${changed}"
    else
      echo "[$(date '+%H:%M:%S')] ⚠ 推送失败，${INTERVAL}秒后重试（检查网络或 GitHub 登录）"
    fi
  fi

  sleep "$INTERVAL"
done
