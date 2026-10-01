<#
    re/fetch-re.ps1
    视光之家 6.9 前端契约重新抓取脚本（可复现）

    用途：
      重新拉取生产前端静态资源，离线生成 routes.csv / endpoints.csv，
      并与 frontend-manifest.json 中的 SHA256 对比，判断生产是否升版。

    安全性说明：
      - 仅对 https://<PROD_HOST>/pc/ 下的**静态公开资源**发 GET 请求
      - 不携带任何 Cookie / Token / 凭据
      - 不调用任何 /admin/*.json 或 /auth/*.json 业务端点
      - 不产生任何生产数据写入
      - 原始 bundle 落在系统临时目录，**不写入项目工作区**

    用法：
      powershell -ExecutionPolicy Bypass -File re\fetch-re.ps1
      powershell -ExecutionPolicy Bypass -File re\fetch-re.ps1 -CheckOnly
#>
[CmdletBinding()]
param(
    [switch]$CheckOnly
)

$ErrorActionPreference = 'Stop'
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

$Base      = if ($env:SGVJ_PROD_HOST) { $env:SGVJ_PROD_HOST.TrimEnd('/') + '/pc/' } else { 'https://<PROD_HOST>/pc/' }
$WorkDir   = Join-Path $env:TEMP 'sgzj-re'
$RepoRe    = Split-Path -Parent $MyInvocation.MyCommand.Path
$Manifest  = Join-Path $RepoRe 'frontend-manifest.json'

# 静态资源清单：文件名 -> URL
$Assets = [ordered]@{
    'controller.js' = 'js/controller/controller-76f1134453.js'
    'directive.js'  = 'js/directive/directive-1699b90cad.js'
    'main.js'       = 'js/main/main-0283a75ded.js'
    'factory.js'    = 'js/factory/factory-c7cec33f4b.js'
    'service.js'    = 'js/service/service-a8283608aa.js'
    'index.html'    = 'index.html'
}

function Get-Sha256([string]$Path) {
    (Get-FileHash $Path -Algorithm SHA256).Hash.ToLower()
}

# ---------------------------------------------------------------- 0 号闸门
Write-Host '== 0 号闸门校验 ==' -ForegroundColor Cyan
$Gate = @('controller.js', 'deliveryList.html', 'machineOrderCompleted.html', 'machineOrderList.html')
foreach ($g in $Gate) {
    $hit = Get-ChildItem -Path (Split-Path -Parent $RepoRe) -Recurse -Filter $g -File -ErrorAction SilentlyContinue |
           Select-Object -First 1
    if ($hit) { Write-Host ("  {0}  {1}" -f (Get-Sha256 $hit.FullName).Substring(0, 16), $g) }
    else      { Write-Warning "  未找到 $g" }
}

# ---------------------------------------------------------------- 抓取
if (-not $CheckOnly) {
    New-Item -ItemType Directory -Force -Path $WorkDir | Out-Null
    Write-Host "`n== 抓取静态资源 ==" -ForegroundColor Cyan
    foreach ($k in $Assets.Keys) {
        $url = $Base + $Assets[$k]
        $out = Join-Path $WorkDir $k
        try {
            Invoke-WebRequest -Uri $url -OutFile $out -UseBasicParsing -TimeoutSec 60
            Write-Host ("  {0,-14} {1,10:N0} B  {2}" -f $k, (Get-Item $out).Length, (Get-Sha256 $out).Substring(0, 16))
        }
        catch {
            Write-Warning "  $k 抓取失败：$($_.Exception.Message)"
        }
    }
}

# ---------------------------------------------------------------- 升版比对
if (Test-Path $Manifest) {
    Write-Host "`n== 与已归档基线比对 ==" -ForegroundColor Cyan
    $man = Get-Content $Manifest -Raw -Encoding UTF8 | ConvertFrom-Json
    Write-Host ("  基线版本：{0}    观测时间：{1}" -f $man.version, $man.observedAt)
    $changed = 0
    foreach ($a in $man.artifacts) {
        $p = Join-Path $WorkDir $a.name
        if (-not (Test-Path $p)) { Write-Host ("  {0,-14} 缺失，无法比对" -f $a.name); continue }
        $now = Get-Sha256 $p
        $same = ($now -eq $a.sha256)
        if (-not $same) { $changed++ }
        if ($same) {
            Write-Host ("  {0,-14} 一致" -f $a.name)
        }
        else {
            Write-Host ("  {0,-14} ** 已变更 **" -f $a.name)
            Write-Host ("      baseline {0}" -f $a.sha256.Substring(0, 16))
            Write-Host ("      current  {0}" -f $now.Substring(0, 16))
        }
    }
    if ($changed -gt 0) {
        Write-Warning "生产前端已升版（$changed 个文件变更）。需重新核验 R1 基线后再开发。"
    }
    else {
        Write-Host '  与基线一致，可继续按 R1/R2/R3 开发。' -ForegroundColor Green
    }
}
else {
    Write-Warning "未找到 $Manifest，无法比对基线。"
}

# ---------------------------------------------------------------- 契约抽取
if (-not $CheckOnly) {
    Write-Host "`n== 抽取路由与端点 ==" -ForegroundColor Cyan

    $mainText = [IO.File]::ReadAllText((Join-Path $WorkDir 'main.js'), [Text.Encoding]::UTF8)
    $states = [regex]::Matches($mainText, '\.state\(\s*"(?<s>[^"]+)"\s*,\s*\{(?<body>(?:(?!\.state\().)*)', 'Singleline')
    $routeRows = foreach ($m in $states) {
        $b = $m.Groups['body'].Value
        [pscustomobject]@{
            State = $m.Groups['s'].Value
            Url   = $(if ($b -match 'url\s*:\s*"([^"]*)"')           { $Matches[1] } else { '' })
            Ctrl  = $(if ($b -match 'controller\s*:\s*"([^"]*)"')   { $Matches[1] } else { '' })
            Tpl   = $(if ($b -match 'templateUrl\s*:\s*"([^"]*)"')  { $Matches[1] } else { '' })
        }
    }
    $routeRows | Where-Object { $_.Tpl -like 'views/*' } |
        Export-Csv (Join-Path $RepoRe 'routes.csv') -NoTypeInformation -Encoding UTF8

    $ctrlText = [IO.File]::ReadAllText((Join-Path $WorkDir 'controller.js'), [Text.Encoding]::UTF8)
    $eps = [regex]::Matches($ctrlText, '["''](?<u>/(?:admin|auth|api|pay|open|stat|upload|file)[A-Za-z0-9_\-/\.]*\.json)["'']') |
           ForEach-Object { $_.Groups['u'].Value } | Sort-Object -Unique
    $eps | Export-Csv (Join-Path $RepoRe 'endpoints.csv') -NoTypeInformation -Encoding UTF8

    Write-Host ("  路由 {0} 条 / 端点 {1} 个 -> re\routes.csv, re\endpoints.csv" -f
        @($routeRows | Where-Object { $_.Tpl -like 'views/*' }).Count, $eps.Count)
    Write-Host '  完成。' -ForegroundColor Green
}
