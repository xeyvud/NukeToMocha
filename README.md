# NukeToMocha

							INSTALLATION
How to INSTALL Nuke2Mocha plugin.

1) Close Nuke (not necessary, you can do it after installation)
2) Open finalNUKE2MOCHA_v2.py in any text editor
3) Select all(Ctrl+A) and copy
4) Close finalNUKE2MOCHA_v2.py
5) Open menu.py (usually it is in "Nuke9.0v9\plugins" folder) with any text editor
6) Insert copied code in the end of file
7) Save file
8) Run or Restart(if it was opened) Nuke 

__________________________________________________________________________________________________________________________
							
							POSSIBLE PROBLEMS
If Nuke says that it can't open or read plugins.

OPTION 1: Open meny.py (usually it is in "Nuke9.0v9\plugins" folder) 
	  in any text edtior(Nodepad++ is preferable) 
	  check if there are the same import lines:
						   import platform
						   import subprocess
						   import os
If there are more than one such line delete all other except the first one.

OPTION 2: Open meny.py and finalNUKE2MOCHA_v2.py in any text edtior(again Nodepad++ is preferable) 
	  and compare indentations of code in menu.py it should be the same as in finalNUKE2MOCHA_v2.py

__________________________________________________________________________________________________________________________

OPTION 3: If you reached this option you need to install Nuke2Mocha plugin using any other computer which already has it.

1) Close Nuke (not necessary, you can do it after installation)
2) Open menu.py on OTHER computer (usually it is in "Nuke9.0v9\plugins" folder) with any text editor
3) Select Nuke2Mocha code (look in finalNUKE2MOCHA_v2.py) and copy
4) Close menu.py
4) Open new text file (Nodepad++ is a preferable program)
4) Insert copied code
5) Open menu.py on YOUR computer (usually it is in "Nuke9.0v9\plugins" folder) with any text editor
6) Insert code from text file, created before, in the end of menu.py
7) Save file
8) Run or Restart(if it was opened) Nuke 
