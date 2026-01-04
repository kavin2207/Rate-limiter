Write-Host "Starting FastAPI server..."

$server = Start-Process -NoNewWindow -PassThru `
    python `
    "-m uvicorn main:app --host 0.0.0.0 --port 8000"

Start-Sleep -Seconds 2

Write-Host "Sending requests..."

for ($i = 1; $i -le 20; $i++) {
    Write-Host "Request $i"
    $response = curl -Method POST http://localhost:8000/orders -Headers @{"X-User-Id"="123"} -UseBasicParsing -ErrorAction SilentlyContinue
    $response.Headers
    Start-Sleep -Milliseconds 500
}

Write-Host "Stopping server..."
Stop-Process -Id $server.Id
