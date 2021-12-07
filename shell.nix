with (import <nixpkgs> {});
mkShell {
  packages = with pkgs; [
    poetry
  ];

  shellHook = ''
    poetry install
    poetry shell
  '';
}

