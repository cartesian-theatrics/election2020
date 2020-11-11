{ nixpkgs ? import <nixpkgs> {  } }:

with nixpkgs.python38.pkgs;

let 
   pypkg = nixpkgs.python38.pkgs;
   pkgs = [ nixpkgs.python38 pypkg.ipython pypkg.requests pypkg.plotly ];

in
  nixpkgs.stdenv.mkDerivation {
    name = "env";
    buildInputs = pkgs;
  }
