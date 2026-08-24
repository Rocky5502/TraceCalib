$ErrorActionPreference = "Continue"
Write-Host "=== TraceCalib-SE Windows preflight ==="
Get-Date -Format o

Write-Host "`n--- Windows / RAM / CPU ---"
Get-ComputerInfo | Select-Object WindowsProductName, WindowsVersion, OsBuildNumber, CsProcessors, CsTotalPhysicalMemory

Write-Host "`n--- NVIDIA GPU inventory ---"
nvidia-smi --query-gpu=index,name,memory.total,driver_version,compute_cap --format=csv,noheader,nounits

Write-Host "`n--- WSL ---"
wsl --version
wsl -l -v

Write-Host "`n--- Docker ---"
docker version

Write-Host "`n--- Git ---"
git --version

Write-Host "`nThis script intentionally does not print API keys or environment-variable values."
