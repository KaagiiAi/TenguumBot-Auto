{ pkgs }: {
  deps = [
    pkgs.python311
    pkgs.python311Packages.pip
    pkgs.python311Packages.setuptools
    pkgs.python311Packages.wheel
    pkgs.python311Packages.requests
    pkgs.python311Packages.firebase_admin
    pkgs.python311Packages.python_telegram_bot
    pkgs.python311Packages.gitpython
  ];
}