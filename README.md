WinUEFIKeyActivator
===========

Modification of Chris Korneck's get_win8key with some verbosity explaining what is happening, and automating activation


Original Project Description
-------------
PCs with a preinstalled Windows 8.x OEM version don't seem to ship with any printed license record, CD Key, etc.
Instead it looks like that the PC's individual license has been saved in the device's firmware (ACPI). When the user tries to reinstall Windows, the Windows Setup reads the license key from the firmware memory, so there's no need to manually type in the actual Windows key.

To still be able to backup / inventorize the license key, this script tries to read the Windows 8.x key from the PC firmware.
(from ACPI -> MSDM table -> byte offset 56 to end)


Usage
-------------
Run the python script from a CMD or Batch

Requirements
-------------
-Windows Vista or higher (32 or 64 bit)  
-Tested using Python 3.6.2
-Run it as administrator for obvious reasons
