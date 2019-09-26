# DCPAssistant
A GUI tool for easy input and selection of the best decensoring from multiple instances of [DeepCreamPy created by deeppomf](https://github.com/deeppomf/DeepCreamPy)

Current version: [beta 1.1.0 (PrettyBackwards)](https://github.com/DCPAssistant/DCPAssistant/releases/tag/v1.1.0-beta)

Note: DCPAssistant works only on windows and only with the windows versions of DeepCreamPy as of now

KNOWN ISSUES:
1.Time Counter doesnt roll over at 01:59:59, istead counts minutes
2.Windows' Thumbs.db file counts towards input which leads the program to never finish and spit out an Error in Image select
  Quick Fix: Put any extra image into the decensor_output folder of the chosen DCP-versions
  
How To use DCPAssistant:
1. Click 'Open DCP-versions' and put an untouched copy of every version of DeepCreamPy you want to use in there
2. Click 'Set output' and select the output you want your selected images saved in later
3. Click 'Open input' and put all images (bar AND mosaic, the program will sort them out for you) you want to decensor in after you marked the area that should be decensored
4. If you want to decensor mosaic images, click 'Open original' and put the original images in the mosaic folder
5. [optional] Since you will be able to compare all images later it is recommended but not neccessary that you put the originals for the bar images into the bar folder
6. Click the 'Start bar decensor' or 'Start mosaic decensor' button
7. Select the versions you want to decensor with
8. Wait
9. If you want to save all decensored pictures, you want to 'Choose all'
10. If you want to compare the versions decensorings and the original you want to 'Choose manually'
11. For every image you want to have in your selected output folder, check the 'Keep' box
12. Archive the stuff you want to have saved seperately from your output, otherwise it will get deleted. I recommend archiving the input and the originals. The originals in the archive can be used by the program for future decensorings, so you need not re-add them if you want to decensor an image a second time
13. Profit

[Twitter](https://twitter.com/DCPAssistant)
