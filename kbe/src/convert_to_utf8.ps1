# 设置要处理的目录，默认当前目录
$TargetDir = $PSScriptRoot

# 获取所有 .cpp / .h 文件（递归子目录）
$files = Get-ChildItem -Path $TargetDir -Recurse -Include *.cpp,*.h,*.inl

function IsUtf8([string]$filePath) {
    $bytes = [System.IO.File]::ReadAllBytes($filePath)
    $utf8 = New-Object System.Text.UTF8Encoding($false, $true) # throwOnInvalidBytes = true
    try {
        $utf8.GetString($bytes) | Out-Null
        return $true
    } catch {
        return $false
    }
}

foreach ($file in $files) {
    Write-Host "[CHECK] $($file.FullName)"

    $bytes = [System.IO.File]::ReadAllBytes($file.FullName)
    # 检测 BOM
    if ($bytes.Length -ge 3 -and $bytes[0] -eq 0xEF -and $bytes[1] -eq 0xBB -and $bytes[2] -eq 0xBF) {
        Write-Host "[SKIP] 已是 UTF-8 BOM: $($file.FullName)"
        continue
    }

    if (IsUtf8 $file.FullName) {
        Write-Host "[SKIP] 已是 UTF-8 (无 BOM): $($file.FullName)"
        continue
    }

    Write-Host "[CONVERT] 转换为 UTF-8 无 BOM: $($file.FullName)"
    $content = Get-Content -Path $file.FullName -Encoding Default
    $utf8NoBOM = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllLines($file.FullName, $content, $utf8NoBOM)
}

Write-Host "[DONE] 全部处理完成"
