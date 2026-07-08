# submit-indexnow.ps1
# Submit all live article URLs to IndexNow (Bing, Yandex, Seznam, Naver)
# Run: powershell -ExecutionPolicy Bypass -File submit-indexnow.ps1
#
# URLs verified 2026-06-24 against real Hugo permalinks:
#   - posts WITH `slug:` in front matter -> /posts/{slug}/
#   - posts WITHOUT slug                 -> /posts/{filename-without-.md}/  (date-prefixed)
# Deprecated duplicates (draft:true, excluded): old 2026-06-12 notion / murf / jasper.

$key  = "c1483141308e40cfaaee0f889553afa4"
$siteHost = "aiprofreelancer.com"

$urls = @(
    "https://aiprofreelancer.com/posts/ultahost-vps-review/",
    "https://aiprofreelancer.com/posts/pay-for-vps-with-crypto-bitcoin-2026/",
    "https://aiprofreelancer.com/posts/ultahost-vs-contabo-2026/",
    "https://aiprofreelancer.com/posts/ultahost-vs-hostinger-vps-2026/",
    "https://aiprofreelancer.com/posts/what-is-offshore-hosting-2026/",
    "https://aiprofreelancer.com/posts/hostinger-ai-review-2026/",
    "https://aiprofreelancer.com/posts/elevenlabs-ai-review-2026/",
    "https://aiprofreelancer.com/posts/best-ai-voice-generator-2026/",
    "https://aiprofreelancer.com/posts/best-ai-writing-tools-2026/",
    "https://aiprofreelancer.com/posts/best-vps-for-freelancers-2026/",
    "https://aiprofreelancer.com/posts/cheapest-vps-crypto-payment-2026/",
    "https://aiprofreelancer.com/posts/copy-ai-review-2026/",
    "https://aiprofreelancer.com/posts/copy-ai-vs-jasper-2026/",
    "https://aiprofreelancer.com/posts/elevenlabs-vs-murf-ai-2026/",
    "https://aiprofreelancer.com/posts/semrush-review-2026/",
    "https://aiprofreelancer.com/posts/surfer-seo-review-2026/",
    "https://aiprofreelancer.com/posts/writesonic-review-2026/",
    "https://aiprofreelancer.com/posts/best-cheap-dedicated-server-2026/",
    "https://aiprofreelancer.com/posts/best-unlimited-bandwidth-vps-2026/",
    "https://aiprofreelancer.com/posts/best-vps-for-wordpress-2026/",
    "https://aiprofreelancer.com/posts/best-vps-under-10-dollars-2026/",
    "https://aiprofreelancer.com/posts/best-windows-vps-hosting-2026/",
    "https://aiprofreelancer.com/posts/hostinger-vps-review-2026/",
    "https://aiprofreelancer.com/posts/managed-wordpress-vps-hosting-2026/",
    "https://aiprofreelancer.com/posts/vps-vs-shared-hosting-2026/",
    "https://aiprofreelancer.com/posts/systeme-io-review-2026/",
    "https://aiprofreelancer.com/posts/best-vpn-for-freelancers-2026/",
    "https://aiprofreelancer.com/posts/nordvpn-review-2026/",
    "https://aiprofreelancer.com/posts/nordvpn-vs-expressvpn-2026/",
    "https://aiprofreelancer.com/posts/nordvpn-vs-surfshark-2026/",
    "https://aiprofreelancer.com/posts/systeme-io-vs-clickfunnels-2026/",
    "https://aiprofreelancer.com/posts/nordvpn-vs-protonvpn-2026/",
    "https://aiprofreelancer.com/posts/ahrefs-vs-semrush-2026/",
    "https://aiprofreelancer.com/posts/2026-06-18-grammarly-review-2026/",
    "https://aiprofreelancer.com/posts/2026-06-19-writesonic-vs-copyai-2026/",
    "https://aiprofreelancer.com/posts/2026-06-20-notion-ai-review-2026/",
    "https://aiprofreelancer.com/posts/2026-06-21-murf-ai-review-2026/",
    "https://aiprofreelancer.com/posts/2026-06-23-descript-review-2026/",
    "https://aiprofreelancer.com/posts/canva-review-2026/",
    "https://aiprofreelancer.com/posts/otter-ai-review-2026/",
    "https://aiprofreelancer.com/posts/activecampaign-review-2026/",
    "https://aiprofreelancer.com/posts/getresponse-vs-mailchimp-2026/",
    "https://aiprofreelancer.com/posts/monday-com-review-2026/",
    "https://aiprofreelancer.com/posts/loom-review-2026/",
    "https://aiprofreelancer.com/posts/beautiful-ai-review-2026/",
    "https://aiprofreelancer.com/posts/kit-review-2026/",
    "https://aiprofreelancer.com/posts/figma-review-2026/",
    "https://aiprofreelancer.com/posts/zapier-review-2026/",
    "https://aiprofreelancer.com/posts/hubspot-review-2026/",
    "https://aiprofreelancer.com/posts/jasper-ai-review-2026/",
    "https://aiprofreelancer.com/posts/typeform-review-2026/",
    "https://aiprofreelancer.com/posts/ahrefs-review-2026/",
    "https://aiprofreelancer.com/posts/notion-vs-obsidian-2026/",
    "https://aiprofreelancer.com/posts/midjourney-review-2026/",
    "https://aiprofreelancer.com/posts/clickup-review-2026/",
    "https://aiprofreelancer.com/posts/webflow-review-2026/",
    "https://aiprofreelancer.com/posts/best-ai-tools-2026/",
    "https://aiprofreelancer.com/posts/dmca-ignored-hosting-2026/"
)

$body = @{
    host        = $siteHost
    key         = $key
    keyLocation = "https://$siteHost/$key.txt"
    urlList     = $urls
} | ConvertTo-Json

$engines = @(
    "https://api.indexnow.org/indexnow",
    "https://www.bing.com/indexnow",
    "https://search.seznam.cz/indexnow",
    "https://yandex.com/indexnow"
)

Write-Host "=== IndexNow Submission ===" -ForegroundColor Cyan
Write-Host "Submitting $($urls.Count) URLs to $($engines.Count) engines..." -ForegroundColor Yellow
Write-Host ""

foreach ($engine in $engines) {
    try {
        $response = Invoke-RestMethod -Uri $engine -Method POST -Body $body `
            -ContentType "application/json; charset=utf-8" -TimeoutSec 15
        Write-Host "OK: $engine" -ForegroundColor Green
    } catch {
        $code = $_.Exception.Response.StatusCode.value__
        if ($code -eq 200 -or $code -eq 202) {
            Write-Host "OK ($code): $engine" -ForegroundColor Green
        } else {
            Write-Host "WARN ($code): $engine" -ForegroundColor Yellow
        }
    }
}

Write-Host ""
Write-Host "=== XONG! $($urls.Count) URLs submitted ===" -ForegroundColor Green
Write-Host "