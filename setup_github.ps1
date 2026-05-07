#!/usr/bin/env pwsh
<#
.SYNOPSIS
    setup_github.ps1 — Configura GitHub + secretos FTP para auto-deploy autónomo.
    Ejecutar UNA sola vez después de crear el repo en github.com

.DESCRIPTION
    1. Instala GitHub CLI (gh) si no está
    2. Conecta el repo local con GitHub
    3. Sube el código
    4. Configura los 4 secretos FTP como GitHub Secrets

.USO
    powershell -ExecutionPolicy Bypass -File setup_github.ps1
#>

$ErrorActionPreference = 'Stop'
$REPO_DIR = $PSScriptRoot

Write-Host ""
Write-Host "╔══════════════════════════════════════════════════════╗"
Write-Host "║  Liga Hypertensiones - Setup GitHub Actions          ║"
Write-Host "╚══════════════════════════════════════════════════════╝"
Write-Host ""

# ── Paso 1: Verificar / instalar gh CLI ──────────────────────────────────────
Write-Host "── [1/5] Verificando GitHub CLI..." -ForegroundColor Cyan
if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    Write-Host "  gh CLI no encontrado. Instalando via winget..." -ForegroundColor Yellow
    winget install --id GitHub.cli -e --source winget
    # Recargar PATH
    $env:PATH = [System.Environment]::GetEnvironmentVariable('PATH','Machine') + ';' + [System.Environment]::GetEnvironmentVariable('PATH','User')
    if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
        Write-Host "  ✗ No se pudo instalar gh CLI automáticamente." -ForegroundColor Red
        Write-Host "    Descárgalo de: https://cli.github.com/" -ForegroundColor Yellow
        Write-Host "    Luego vuelve a ejecutar este script." -ForegroundColor Yellow
        exit 1
    }
}
Write-Host "  ✓ gh CLI disponible: $(gh --version | Select-Object -First 1)" -ForegroundColor Green

# ── Paso 2: Autenticación en GitHub ─────────────────────────────────────────
Write-Host ""
Write-Host "── [2/5] Autenticación GitHub..." -ForegroundColor Cyan
$authStatus = gh auth status 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "  Abriendo login de GitHub en el navegador..." -ForegroundColor Yellow
    gh auth login --web --hostname github.com --git-protocol https
} else {
    Write-Host "  ✓ Ya autenticado" -ForegroundColor Green
}

# ── Paso 3: Crear repo en GitHub y enlazar ───────────────────────────────────
Write-Host ""
Write-Host "── [3/5] Repositorio GitHub..." -ForegroundColor Cyan

Set-Location $REPO_DIR

$remoteUrl = git remote get-url origin 2>&1
if ($LASTEXITCODE -ne 0) {
    # No tiene remote → crear repo y enlazar
    Write-Host "  Creando repositorio público en GitHub..." -ForegroundColor Yellow
    Write-Host "  (Público = GitHub Actions gratuito ilimitado)" -ForegroundColor DarkGray

    gh repo create liga-hypertensiones --public --source . --push --description "Liga Hypertensiones 25/26 - Dashboard LaLiga Hypermotion"
    Write-Host "  ✓ Repo creado y código subido" -ForegroundColor Green
} else {
    # Ya tiene remote → solo hacer push
    Write-Host "  Remote ya configurado: $remoteUrl" -ForegroundColor DarkGray
    git push -u origin master 2>&1
    Write-Host "  ✓ Código subido" -ForegroundColor Green
}

# Obtener el nombre del repo para los secrets
$repoFullName = gh repo view --json nameWithOwner -q '.nameWithOwner' 2>&1
Write-Host "  Repo: $repoFullName" -ForegroundColor DarkGray

# ── Paso 4: Configurar secretos FTP ─────────────────────────────────────────
Write-Host ""
Write-Host "── [4/5] Configurando secretos FTP de IONOS..." -ForegroundColor Cyan
Write-Host "  (Se guardan cifrados en GitHub - nunca visibles en logs)" -ForegroundColor DarkGray
Write-Host ""

Write-Host "  Necesito los datos FTP de IONOS." -ForegroundColor Yellow
Write-Host "  Los encuentras en: panel.ionos.es → Hosting → FTP" -ForegroundColor DarkGray
Write-Host ""

$ftpServer   = Read-Host "  Host FTP (ej: homepageXXXXX.1and1.es o ftp.alejandrobeltran.es)"
$ftpUser     = Read-Host "  Usuario FTP"
$ftpPassword = Read-Host "  Contraseña FTP" -AsSecureString
$ftpPath     = Read-Host "  Ruta en servidor (ej: /hypertensiones.alejandrobeltran.es/ o /)"

# Convertir SecureString a plain text solo para gh secret set
$ftpPasswordPlain = [Runtime.InteropServices.Marshal]::PtrToStringAuto(
    [Runtime.InteropServices.Marshal]::SecureStringToBSTR($ftpPassword)
)

Write-Host ""
Write-Host "  Creando secretos en GitHub..." -ForegroundColor DarkGray

$ftpServer      | gh secret set FTP_SERVER   --repo $repoFullName
$ftpUser        | gh secret set FTP_USERNAME --repo $repoFullName
$ftpPasswordPlain | gh secret set FTP_PASSWORD --repo $repoFullName
$ftpPath        | gh secret set FTP_PATH     --repo $repoFullName

# Limpiar contraseña de memoria
$ftpPasswordPlain = $null
[GC]::Collect()

Write-Host "  ✓ 4 secretos configurados (FTP_SERVER, FTP_USERNAME, FTP_PASSWORD, FTP_PATH)" -ForegroundColor Green

# ── Paso 5: Lanzar primer workflow ───────────────────────────────────────────
Write-Host ""
Write-Host "── [5/5] Lanzando primera ejecución..." -ForegroundColor Cyan
gh workflow run update.yml --repo $repoFullName
Start-Sleep -Seconds 3
Write-Host ""
Write-Host "  Abriendo GitHub Actions para ver el progreso..." -ForegroundColor DarkGray
gh repo view $repoFullName --web

# ── Resultado ────────────────────────────────────────────────────────────────
Write-Host ""
Write-Host "╔══════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║  ✓ SISTEMA COMPLETAMENTE AUTÓNOMO                    ║" -ForegroundColor Green
Write-Host "╠══════════════════════════════════════════════════════╣" -ForegroundColor Green
Write-Host "║  • Cada 10 min (13:00-23:59): actualización en vivo  ║" -ForegroundColor Green
Write-Host "║  • Cada hora (resto del día): actualización normal   ║" -ForegroundColor Green
Write-Host "║  • La web se recarga sola al detectar datos nuevos   ║" -ForegroundColor Green
Write-Host "║  • No requiere que el PC esté encendido              ║" -ForegroundColor Green
Write-Host "╠══════════════════════════════════════════════════════╣" -ForegroundColor Green
Write-Host "║  Para update manual: gh workflow run update.yml      ║" -ForegroundColor DarkGray
Write-Host "╚══════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""
