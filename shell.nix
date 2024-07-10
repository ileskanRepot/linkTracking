{ pkgs ? import <nixpkgs> {}}:
  pkgs.mkShell {
    nativeBuildInputs = let
      env = pyPkgs : with pyPkgs; [
        fastapi
        uvicorn
        psycopg2
      ];
    in with pkgs; [
      (python311.withPackages env)
    ];
}
