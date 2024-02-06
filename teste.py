from ctpaperclip import PyClipboardPlus as pc

pycl = pc()
pycl.write_image_to_clipboard('dist\img.png')
print('Deu bom')