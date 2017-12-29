$admin = [adsi]("WinNT://./administrator, user")
$admin.psbase.invoke("SetPassword", "Zapcom99")
