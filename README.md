# Inkscape extension: Convert RSML to SVG
This is an Inkscape extension that converts polyline coordinates stored in a RSML file (ie. a custom XML format produced by the RootNav software) into SVG paths.

## Purpose
The RootNav software (http://sourceforge.net/projects/rootnav/) is used to semi-automatically extract plant root system architectures from images. Saving the extracted root traces as RSML files (ie. XML format) then allows to quantify the root architecture via the RootNav Viewer software. The current Inkscape plugin aims at importing the root traces stored in a RSML file into Inkscape as SVG paths for visualization purposes.

## How to install
- Download the repository.
- Find your Inkscape installation folder.
- Find the extensions folder, usually "inkscape > extensions" or "share > inkscape > extensions".
- Copy the files "convert_rsml_to_svg.py" and "convert_rsml_to_svg.inx" in the extensions folder.
- Close and restart Inkscape.

## How to use
- Run the plugin from the menu "Extensions > Root system architecture > Convert RSML to SVG...".
- In the dialog window, write the working directory, ie. the directory containing the RSML file to import.
- Indicate the name of the RSML file to import, for instance "example.rsml" (downloaded with the repository).
- Click "Apply". The roots will be displayed as SVG paths.

## Version compatibility
The plugin has been tested on Inkscape 1.1 with RSML files produced by RootNav 1.8.1.

## About
Author: Hugues De Gernier

Creation year: 2014

Last modification: 2025-05-02
