<powershell>
$admin = [adsi]("WinNT://./administrator, user")
$admin.psbase.invoke("SetPassword", "Zapcom99")
Install-Module DockerProvider -Force
Install-Package Docker -ProviderName DockerProvider -Force
Start-Service docker
docker swarm join --token SWMTKN-1-22t1bdzt5rjxwvmkmbi715rafecmee6a0sqxwtrrtymttx8kub-e060vpckf3b5xug13fkufrfjb 192.168.3.31:2377
</powershell>
