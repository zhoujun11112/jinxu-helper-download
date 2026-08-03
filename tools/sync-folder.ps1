# 共享讨论文件夹 · 自动同步脚本（Windows PowerShell）
#
# 作用：把你电脑上的这个文件夹和 GitHub 保持双向自动同步。
#   - Claude 写的新文件会自动出现在你的文件夹里
#   - 你放进 inbox\ 的 ChatGPT 回复会自动推上去，Claude 立刻看到
#
# 用法：
#   1) 先克隆仓库到你电脑（只做一次），在 PowerShell 里执行：
#        git clone -b claude/japan-ai-drama-localization-zb42vp https://github.com/zhoujun11112/jinxu-helper-download.git $HOME\短剧讨论
#   2) 启动同步（保持这个窗口开着）：
#        cd $HOME\短剧讨论 ; powershell -ExecutionPolicy Bypass -File tools\sync-folder.ps1
#
# 停止：按 Ctrl+C

$Branch   = "claude/japan-ai-drama-localization-zb42vp"
$Interval = 15   # 每隔几秒同步一次

Set-Location (Join-Path $PSScriptRoot "..")

Write-Host "======================================"
Write-Host " 共享讨论文件夹 · 自动同步已启动"
Write-Host " 目录：$(Get-Location)"
Write-Host " 分支：$Branch"
Write-Host " 间隔：$Interval 秒"
Write-Host ""
Write-Host " 把 ChatGPT 的回复存成 .md 文件，放进："
Write-Host "   docs\japan-ai-short-drama\exchange\inbox\"
Write-Host " 文件名：R01-gpt-to-claude.md（轮次递增）"
Write-Host ""
Write-Host " 保持本窗口开着。按 Ctrl+C 停止。"
Write-Host "======================================"
Write-Host ""

while ($true) {
    # 1) 拉取 Claude 的新发言
    $before = (git rev-parse HEAD 2>$null)
    git pull --rebase --autostash origin $Branch -q 2>$null
    $after = (git rev-parse HEAD 2>$null)
    if ($before -ne $after) {
        Write-Host "[$(Get-Date -Format HH:mm:ss)] 收到 Claude 的新文件：" -ForegroundColor Green
        git diff --name-only $before $after 2>$null | ForEach-Object { Write-Host "    $_" }
    }

    # 2) 推送你放进来的新文件
    $status = git status --porcelain
    if ($status) {
        $changed = ($status | ForEach-Object { $_.Substring(3) }) -join " "
        git add -A
        git commit -q -m "同步：$changed" 2>$null
        git push -q origin $Branch 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "[$(Get-Date -Format HH:mm:ss)] 已发送给 Claude：$changed" -ForegroundColor Cyan
        } else {
            Write-Host "[$(Get-Date -Format HH:mm:ss)] 推送失败，$Interval 秒后重试（检查网络或 GitHub 登录）" -ForegroundColor Yellow
        }
    }

    Start-Sleep -Seconds $Interval
}
