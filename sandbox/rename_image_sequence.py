import os

#img_sequence_path = r"""C:\Users\satish.goda\Downloads\building_the_scene"""
#img_sequence_path = r"""C:\Users\satish.goda\Downloads\texturing_the_ground"""
img_sequence_path = r"""C:\Users\satish.goda\Downloads\texturing_the_walls"""

images = os.listdir(img_sequence_path)

for image in images:
    new_name = f"{image.rpartition('_')[0]}.png"
    os.rename(
                f'{img_sequence_path}\{image}', 
                f'{img_sequence_path}\{new_name}'
            )
