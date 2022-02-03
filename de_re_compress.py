#Requires patool to be installed
import patoolib
import os
import subprocess

#get input and output folder from user
inputFolder = input("Enter folder containing archives: ")
outputFolder = input("Enter output folder for .xz files: ")
#Tell user the folders
print("Input: " + inputFolder)
print("Output: " + outputFolder)

#Create the outputFolder and a temp folder in it to store working files
#tempFolder is equal to the variable outputFolder/temparchive (which is the folder name we want to create)
#Make sure the directory does not exist before we create it
tempFolder = os.path.join(outputFolder, "temparchive")
if not os.path.exists(outputFolder):
	os.mkdir(outputFolder)
if not os.path.exists(tempFolder):
	os.mkdir(tempFolder)

#For every file in the inputFolder start looping
for file in os.listdir(inputFolder):
	#If the file ends in .rar .tar .zip or .gz continue
	if file.endswith(".rar") or file.endswith(".tar") or file.endswith(".zip") or file.endswith(".gz") or file.endswith(".bz2"):
		#Create an absolute path to the file. inputFolder + file name
		fileAbsolute = os.path.join(inputFolder, file)
		#Extract the absolute filename to the tempFolder in outputFolder
		patoolib.extract_archive(fileAbsolute,outdir=tempFolder)
		#Compress the extract file to xz
		for tempFile in os.listdir(tempFolder):
			decompressed = os.path.join(tempFolder, tempFile)
			#print("Now compressing: " + decompressed)
			#Run XZ from the host OS to compress the file
			#XZ will also delete the input file once complete
			subprocess.run(["xz", "-v9eT4", decompressed])
			#subprocess.run(["7z", "-y", "-sdel", "-mx9", "-mmt4", "a", decompressed])
			#Next move the file by renaming it. tempFile is the exact name of the file so we add .xz to the end to get compressed file
			os.rename(decompressed+".xz", outputFolder+"/"+tempFile+".xz")
#Delete the tempFolder once all files are compressed
os.rmdir(tempFolder)
