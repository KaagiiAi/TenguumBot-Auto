{ pkgs }: {
  deps = [
    pkgs.python311
    pkgs.python311Packages.firebase-admin
    pkgs.python311Packages.python-dotenv
    pkgs.python311Packages.python-telegram-bot
  ];
}