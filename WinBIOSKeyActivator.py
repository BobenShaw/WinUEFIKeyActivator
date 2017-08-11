import sys
import ctypes
import ctypes.wintypes
import os
import time

#######################################################################################
#                                                                                     #
# Original script by Christian Korneck (christian@korneck.de)                         #
# Original repository located at: https://github.com/christian-korneck/get_win8key    #
# Modifications for automation/verbosity by Bob Shaw (bob@shaw.pw)                    #
# New repository is located at: https://github.com/IchBinAsuka/WinBIOSKeyActivator    #
#                                                                                     #
#######################################################################################


print("###########################################")
print("#                                         #")
print("#      Windows UEFI Key Activator         #")
print("#                                         #")
print("###########################################")
print("")
print("Source code available at: https://github.com/IchBinAsuka/WinUEFIKeyActivator")
print("Make sure you're running this as administrator!")
print("")
print("Looking through BIOS for key...")
print("")

def EnumAcpiTables():
#returns a list of the names of the ACPI tables on this system
	FirmwareTableProviderSignature=ctypes.wintypes.DWORD(1094930505)
	pFirmwareTableBuffer=ctypes.create_string_buffer(0)
	BufferSize=ctypes.wintypes.DWORD(0)
	#http://msdn.microsoft.com/en-us/library/windows/desktop/ms724259
	EnumSystemFirmwareTables=ctypes.WinDLL("Kernel32").EnumSystemFirmwareTables
	ret=EnumSystemFirmwareTables(FirmwareTableProviderSignature, pFirmwareTableBuffer, BufferSize)
	pFirmwareTableBuffer=None
	pFirmwareTableBuffer=ctypes.create_string_buffer(ret)
	BufferSize.value=ret
	ret2=EnumSystemFirmwareTables(FirmwareTableProviderSignature, pFirmwareTableBuffer, BufferSize)
	return [pFirmwareTableBuffer.value[i:i+4] for i in range(0, len(pFirmwareTableBuffer.value), 4)]

def FindAcpiTable(table):
#checks if specific ACPI table exists and returns True/False
	tables = EnumAcpiTables()
	if table in tables:
		return True
	else:
		return False

def GetAcpiTable(table,TableDwordID):
#returns raw contents of ACPI table
	#http://msdn.microsoft.com/en-us/library/windows/desktop/ms724379x
	GetSystemFirmwareTable=ctypes.WinDLL("Kernel32").GetSystemFirmwareTable
	FirmwareTableProviderSignature=ctypes.wintypes.DWORD(1094930505)
	FirmwareTableID=ctypes.wintypes.DWORD(int(TableDwordID))
	pFirmwareTableBuffer=ctypes.create_string_buffer(0)
	BufferSize=ctypes.wintypes.DWORD(0)
	ret = GetSystemFirmwareTable(FirmwareTableProviderSignature, FirmwareTableID, pFirmwareTableBuffer, BufferSize)
	pFirmwareTableBuffer=None
	pFirmwareTableBuffer=ctypes.create_string_buffer(ret)
	BufferSize.value=ret
	ret2 = GetSystemFirmwareTable(FirmwareTableProviderSignature, FirmwareTableID, pFirmwareTableBuffer, BufferSize)
	return pFirmwareTableBuffer.raw
	
def GetWindowsKey():
	#returns Windows Key as string
	table=b"MSDM"
	TableDwordID=1296323405
	if FindAcpiTable(table)==True:
		try:
			rawtable = GetAcpiTable(table, TableDwordID)
			#http://msdn.microsoft.com/library/windows/hardware/hh673514
			#byte offset 36 from beginning = Microsoft 'software licensing data structure' / 36 + 20 bytes offset from beginning = Win Key
			return rawtable[56:len(rawtable)].decode("utf-8")
		except:
			return False
	else:
		return False
	
try:	
	WindowsKey=GetWindowsKey()
	if WindowsKey==False:
		print("No key found in BIOS!")
		print("For models that shipped with Windows 7 and older, no key will be here.")
		print("Take a look under your battery on the laptop, or on the side of the Desktop!")
		print("Keep in mind Windows 7 keys should generally work with Windows 10")
		sys.exit(1)
	else:
		print("I found your product key in BIOS!")
		print(str(WindowsKey))
		subprocess.call(["cscript", "C:\windows\system32\slmgr.vbs", "/ipk", WindowsKey])
		print("Setting system key...")
		print("Attempting activation to Microsoft servers...")
		subprocess.call(["cscript", "C:\windows\system32\slmgr.vbs", "/ato"])
		sys.exit(1)
except:
	sys.exit(1)