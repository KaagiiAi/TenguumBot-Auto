{ pkgs }: {
  deps = [
    pkgs.python311
    pkgs.python311Packages.pip
    pkgs.python311Packages.requests
    pkgs.python311Packages.firebase-admin
    pkgs.python311Packages.python-telegram-bot
    pkgs.python311Packages.setuptools
    pkgs.python311Packages.wheel
  ];
}