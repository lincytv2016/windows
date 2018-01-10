<powershell>
$admin = [adsi]("WinNT://./administrator, user")
$admin.psbase.invoke("SetPassword", "Zapcom99")
docker swarm join --token SWMTKN-1-2ogh9j6o57xen95cg857kjkgzw6z5fiarp5er3nwkqrs5hm5oi-0o9clfe5tiaa6f6lk1xuzh3dh 192.168.3.254:2377
</powershell>
