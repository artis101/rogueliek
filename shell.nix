{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    python312
    python312Packages.pip
    python312Packages.virtualenv
    python312Packages.setuptools
    python312Packages.wheel
    python312Packages.pylint
    python312Packages.black
    python312Packages.mypy
    python312Packages.pytest
    pyright
    git
  ];

  shellHook = ''
    echo "Python development environment"
    python --version
  '';
}
