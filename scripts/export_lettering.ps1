# Optional Windows-only authoring step. The exported SVG outlines are portable.
Add-Type -AssemblyName System.Drawing
$lettering = [ordered]@{}
$phrases = [ordered]@{
    chinese = @('知行合一', 'STXingkai', [System.Drawing.FontStyle]::Regular)
    english = @('Unity of Knowledge and Action', 'Baskerville Old Face', [System.Drawing.FontStyle]::Italic)
}
foreach ($key in $phrases.Keys) {
    $phrase = $phrases[$key]
    $family = [System.Drawing.FontFamily]::new($phrase[1])
    $path = [System.Drawing.Drawing2D.GraphicsPath]::new()
    $format = [System.Drawing.StringFormat]::GenericTypographic
    $path.AddString($phrase[0], $family, $phrase[2], 1000, [System.Drawing.PointF]::new(0, 0), $format)
    $points = $path.PathPoints
    $types = $path.PathTypes
    $segments = [System.Collections.Generic.List[string]]::new()
    function Number($value) { $value.ToString('0.##', [Globalization.CultureInfo]::InvariantCulture) }
    for ($i = 0; $i -lt $points.Length; $i++) {
        $type = $types[$i] -band 7
        $point = $points[$i]
        if ($type -eq 0) {
            $segments.Add('M' + (Number $point.X) + ' ' + (Number $point.Y))
        } elseif ($type -eq 1) {
            $segments.Add('L' + (Number $point.X) + ' ' + (Number $point.Y))
        } elseif ($type -eq 3) {
            $second = $points[$i + 1]
            $third = $points[$i + 2]
            $segments.Add('C' + (Number $point.X) + ' ' + (Number $point.Y) + ' ' +
                (Number $second.X) + ' ' + (Number $second.Y) + ' ' +
                (Number $third.X) + ' ' + (Number $third.Y))
            $i += 2
        }
        if (($types[$i] -band 128) -ne 0) { $segments.Add('Z') }
    }
    $bounds = $path.GetBounds()
    $lettering[$key] = [ordered]@{
        text = $phrase[0]
        family = $family.Name
        path = ($segments -join '')
        width = $bounds.Right
        ascent = $family.GetCellAscent($phrase[2]) / $family.GetEmHeight($phrase[2])
    }
    $path.Dispose()
    $family.Dispose()
}
$destination = Join-Path (Split-Path -Parent $PSScriptRoot) 'assets\lettering.json'
$lettering | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $destination -Encoding utf8
