$jobs = @()

for ($i = 1; $i -le 20; $i++) {
    $jobs += Start-Job {
        curl -X POST http://localhost:8000/orders `
            -H "X-User-Id: 123" `
            -H "Connection: close" `
            -s -o NUL
    }
}

$jobs | Wait-Job
$jobs | Receive-Job
