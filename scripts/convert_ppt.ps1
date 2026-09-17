$pptxPath = "C:\Users\unsto\OneDrive\Desktop\Senitel-x\Sentinel-X_Presentation.pptx"
$pdfPath = "C:\Users\unsto\OneDrive\Desktop\Senitel-x\Sentinel-X_Presentation.pdf"

try {
    $ppt = New-Object -ComObject PowerPoint.Application
    $pres = $ppt.Presentations.Open($pptxPath, 1, 0, 0)
    $pres.SaveAs($pdfPath, 32)
    $pres.Close()
    $ppt.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($ppt) | Out-Null
    Write-Output "SUCCESS: PDF created at $pdfPath"
} catch {
    Write-Output "COM_FAILED: $($_.Exception.Message)"
}
