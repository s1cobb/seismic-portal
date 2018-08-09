# ok

$comp_objects = Get-ADComputer -Filter * | FT DNSHostName

return $comp_objects
