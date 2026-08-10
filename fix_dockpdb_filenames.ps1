# Fix typo'd filenames in docking\static\dock-pdb
# Run from the project root: D:\ASAB\DataBases\Maryam_DB\paampdb
# Review the "would rename" output first (dry run), then re-run with -Confirm:$false removed if it looks right.

$folder = "docking\static\dock-pdb"

$renames = @{
    "PAAMP1_NDM.pdb"              = "PAAMP1_NDM1.pdb"
    "PAAMP2_NDM.pdb"               = "PAAMP2_NDM1.pdb"
    "PAAMP22_OXA10..pdb"           = "PAAMP22_OXA10.pdb"
    "PAAMP23_OXA10..pdb"           = "PAAMP23_OXA10.pdb"
    "PAAMP25_OXA10..pdb"           = "PAAMP25_OXA10.pdb"
    "PAAMP27_OXA10..pdb"           = "PAAMP27_OXA10.pdb"
    "PAAMP28_OXA10..pdb"           = "PAAMP28_OXA10.pdb"
    "PAAMP29_OXA10..pdb"           = "PAAMP29_OXA10.pdb"
    "PAAMP26._OXA10..pdb"          = "PAAMP26_OXA10.pdb"
    "PAAMP9._pqsD.pdb"             = "PAAMP9_pqsD.pdb"
    "PAMP13_MexAB-OprM.pdb"        = "PAAMP13_MexAB-OprM.pdb"
    "PAMP15_MexAB-OprM.pdb"        = "PAAMP15_MexAB-OprM.pdb"
    "PAMP16_MexAB-OprM.pdb"        = "PAAMP16_MexAB-OprM.pdb"
    "PAMP19_MexAB-OprM.pdb"        = "PAAMP19_MexAB-OprM.pdb"
    "PAMP20_MexAB-OprM.pdb"        = "PAAMP20_MexAB-OprM.pdb"
}

foreach ($old in $renames.Keys) {
    $new = $renames[$old]
    $oldPath = Join-Path $folder $old
    $newPath = Join-Path $folder $new

    if (Test-Path $oldPath) {
        if (Test-Path $newPath) {
            Write-Host "SKIP: '$new' already exists, not overwriting. Check '$old' manually." -ForegroundColor Yellow
        } else {
            Write-Host "Renaming: $old  ->  $new" -ForegroundColor Green
            Rename-Item -Path $oldPath -NewName $new
        }
    } else {
        Write-Host "NOT FOUND: $old (already renamed, or path/case differs)" -ForegroundColor DarkGray
    }
}

Write-Host "`nDone. Re-run the earlier Get-ChildItem search to confirm all filenames are now correct." -ForegroundColor Cyan
