<powershell>
$admin = [adsi]("WinNT://./administrator, user")
$admin.psbase.invoke("SetPassword", "Zapcom99")
Start-Service docker
docker swarm join --token SWMTKN-1-6bp0mpor8u7lpmqk91sfncdq0sd270dnrnns1col6hbx5ftjm2-c1xtofgrknyirvxux6k04veoy 192.168.3.59:2377
</powershell>
