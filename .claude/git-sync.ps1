$projectPath = "c:\Users\ClaraCristineSouzaRo\OneDrive - Starian\AI OPS\Claude code"
Set-Location $projectPath

$status = git status --porcelain 2>&1
if ($status) {
    git add -A
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm"
    git commit -m "auto: sync $timestamp"
    git push origin main 2>&1 | Out-Null
}
