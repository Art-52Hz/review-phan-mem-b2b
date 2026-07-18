# open-partnerstack-programs.ps1
# Mo PartnerStack marketplace de dang ky cac chuong trinh CO TREN PartnerStack.
# Chay: powershell -ExecutionPolicy Bypass -File open-partnerstack-programs.ps1
#
# LUU Y (kiem tra truc tiep 2026-06-24):
#  - Tham so ?query= KHONG loc duoc -> phai GO ten vao o Search tren trang.
#  - Mo thang URL /page/<slug> trong tab moi hay bi "page-not-found" (SPA) ->
#    cach dung duy nhat: vao marketplace -> go ten -> click card -> "Apply to program".
#  - Phai DANG NHAP (Partner sign in) truoc khi Apply.
#
# CHI 6/13 chuong trinh co tren PartnerStack. 7 cai con lai dang ky o noi khac.

$chrome = "C:\Program Files\Google\Chrome\Application\chrome.exe"

Write-Host "=== PartnerStack: cac chuong trinh CO the apply ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "Mo marketplace... Hay dang nhap (Partner sign in) truoc." -ForegroundColor Yellow
Start-Process $chrome "https://market.partnerstack.com/"
Start-Sleep -Seconds 2

Write-Host ""
Write-Host "Tren trang marketplace, GO tung ten vao o Search -> click card -> 'Apply to program':" -ForegroundColor Green
Write-Host "  1. ActiveCampaign   (go: activecampaign)" -ForegroundColor White
Write-Host "  2. GetResponse      (go: getresponse)" -ForegroundColor White
Write-Host "  3. monday.com       (go: monday)" -ForegroundColor White
Write-Host "  4. Webflow          (go: webflow)" -ForegroundColor White
Write-Host "  5. ClickUp          (go: clickup)" -ForegroundColor White
Write-Host "  6. Kit (ConvertKit) (go: convertkit)" -ForegroundColor White
Write-Host ""
Write-Host "=== KHONG co tren PartnerStack -> dang ky o noi khac ===" -ForegroundColor Cyan
Write-Host "  - Semrush    -> Impact.com (loi moi dang cho accept)" -ForegroundColor DarkYellow
Write-Host "  - Grammarly  -> Impact.com (loi moi dang cho accept)" -ForegroundColor DarkYellow
Write-Host "  - HubSpot    -> chuong trinh affiliate rieng cua HubSpot" -ForegroundColor DarkYellow
Write-Host "  - Jasper     -> chuong trinh rieng / Impact" -ForegroundColor DarkYellow
Write-Host "  - Zapier     -> chuong trinh rieng cua Zapier" -ForegroundColor DarkYellow
Write-Host "  - Typeform   -> chuong trinh rieng / Impact" -ForegroundColor DarkYellow
Write-Host "  - Notion     -> chuong trinh affiliate rieng cua Notion" -ForegroundColor DarkYellow
Write-Host "  - Loom       -> chuong trinh rieng" -ForegroundColor DarkYellow
Write-Host ""
Write-Host "=== XONG ===" -ForegroundColor Green
pause
