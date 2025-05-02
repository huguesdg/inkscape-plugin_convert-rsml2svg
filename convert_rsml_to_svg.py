#!/usr/bin/env python

'''
  This extension imports in Inkscape *.rsml files from RootNav 
  (http://sourceforge.net/projects/rootnav/).
  
  Version note: Roots are imported as combined SVG paths and representative
                plants (given by a list, that users need to modify in the 
                script itself) are colored in red.
                In the file name field, users can either write the name of a 
                particular file or a pattern matching one or more names of the  
                files found the working directory.
  
  Last modification: 2025/05/02
  
  For questions, see: https://github.com/huguesdg/inkscape-plugin_convert-rsml2svg
  
  Copyright (C) 2014 Hugues De Gernier
  
  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 3 of the License, or
  (at your option) any later version.
  
  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.
  
  You should have received a copy of the GNU General Public License
  along with this program; if not, write to the Free Software
  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
'''

'''
Loading dependencies (ie. other extensions).
'''
# To override functions of the base class.
import inkex
# OS-independent functions for manipulating files and directories.
from os import listdir
from os.path import isdir, isfile, join, split, splitext
# Useful functions for working with inline css.
import simplestyle
# XML support (reading, manipulating and writing).
from lxml import etree


'''
Create a class which inherits from the 'Effect' class of the 'inkex' extension.
This class contains an initialisation function (parsing user options) and a 'effect' function (telling what the script should do).
'''
class ConvertRSMLtoSVG(inkex.Effect):
    '''
    First initialize the 'inkex.py' script (override the initialisation function of 'inkex.py') then parse user options.
    '''
    def __init__(self):
        inkex.Effect.__init__(self)
        self.arg_parser.add_argument('-d', '--workingDirectory', action = 'store',
                                     type = str, dest = 'workingDirectory', default = '',
                                     help = 'Path of the working directory (ie. which contains the RSML files to convert to SVG)')
        self.arg_parser.add_argument('-f', '--file', action = 'store',
                                     type = str, dest = 'file', default = '',
                                     help = 'Path of the RSML file to convert to SVG')
        self.arg_parser.add_argument('-r', '--resolution', action = 'store',
                                     type = float, dest = 'resolution', default = '15.75',
                                     help = 'The resolution (in pixels/mm) of the image from which the rsml file was created')
    
    '''
    Override the base class 'effect' function.
    '''
    def effect(self):

        # Fill the list with file names if you want to color in red the roots of some representative plants.
        representativePlants = []

        # Getting user options (parameters).
        wd = self.options.workingDirectory
        file = self.options.file
        resolution = self.options.resolution
        
        # Check if the working directory exists.
        if not isdir(wd):
          inkex.debug("Error: No such directory.")
          exit(1)
        
        # Loop for all files in the working directory (but not subdirectories) but only open RSML files and those whose names contain the file name given by the user.
        countFiles = -1
        for f in listdir(wd):
          if isfile(join(wd, f)) and (file in f) and ('rsml' in splitext(f)[1]):
            # Getting the XML root.
            tree = etree.parse(join(wd, f))
            root = tree.getroot()
            if root.tag != 'rsml':
              inkex.debug("Warning: the file named '" + f + "' is not a RSML file and will be discarded.")
            else:
              countFiles = countFiles + 1
    
              # Getting RSML file arborescence.
              metadata = root.find('metadata')
              scene = root.find('scene')
      
              # Getting some metadata.
              #version = metadata.find('version').text
              software = metadata.find('software').text
              fileName = metadata.find('file-key').text
      
              # Convert RSML to SVG.
              if software == 'RootNav':
                  if len(scene) > 0:
                      for i, plant in enumerate(scene):
                          # The plant ID is the file name but the RSML ID may be added if several plants are found in the RSML file.
                          if len(scene) > 1:
                              plantID = fileName + '.' + str(plant.get('ID'))
                              if plant.get('label') and len(str(plant.get('label'))) > 0:
                                  plantID = plantID + '.' + str(plant.get('label'))
                          else:
                              plantID = fileName
      
                          # Combine all roots in one SVG path.
                          path = ""
      
                          if len(plant) > 0:
                              # Loop for all primary roots.
                              for j, primary_root in enumerate(plant):
                                  points = primary_root.find('geometry').find('rootnavspline').findall('point')
                                  path = path + 'M '
                                  for point in points:
                                      path = path + str(float(point.get('x')) + (countFiles * 1890)) + ',' + str(point.get('y')) + ' '
      
                                  # Get all first order lateral roots.
                                  second_order_roots = primary_root.findall('root')
                                  if len(second_order_roots) > 0:
                                      # Loop for all first order lateral roots.
                                      for second_order_root in second_order_roots:
                                          points = second_order_root.find('geometry').find('rootnavspline').findall('point')
                                          path = path + 'M '
                                          for point in points:
                                              path = path + str(float(point.get('x')) + (countFiles * 1890)) + ',' + str(point.get('y')) + ' '
                          
                              # Color roots in red if the plant is within the representative plants list.
                              col = '#000000'
                              if plantID in representativePlants:
                                col = '#ff0000'
      
                              # Line style to use for roots.
                              line_style = { 'stroke': col,
                                             'stroke-width': '5px',
                                             'stroke-linecap': 'round',
                                             'fill': 'none',
                                            }
                    
                              svgPath = {'style' : str(inkex.Style(line_style)),
                                         inkex.addNS('id') : plantID,
                                         'd' : path
                                        }
                              etree.SubElement(self.svg.get_current_layer(), inkex.addNS('path','svg'), svgPath)



'''
Run the script.
First create an instance of the class 'ConvertRSMLtoSVG' then execute it (ie. run the script).
'''
if __name__ == '__main__':
    effect = ConvertRSMLtoSVG()
    effect.run()
