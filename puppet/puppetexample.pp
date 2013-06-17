Package { ensure => "installed" }
    $packages = [ "screen", "mc","lsof","mlocate","mailx","xfsprogs","strace","sysstat"]
    package { $packages: }