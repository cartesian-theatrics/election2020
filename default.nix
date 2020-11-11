{ nixpkgs ? import <nixpkgs> {  } }:

with nixpkgs.python38.pkgs;

let 
   pypkg = nixpkgs.python38.pkgs;
   pkgs = [ nixpkgs.python38 pypkg.numpy pypkg.numpy pypkg.ipython pypkg.pandas pypkg.requests pypkg.plotly ];

in
  nixpkgs.stdenv.mkDerivation {
    name = "env";
    buildInputs = pkgs;
  }
