import os
from pathlib import Path
from shutil import rmtree, unpack_archive
import sys


def creation_folders(path):

    """Створення пустих папок для переміщень"""

    for key in template_extensions.keys():
        folders_path = path / key
        Path(folders_path).mkdir(exist_ok=True)

def delete_empty_folders(path):
    
    """Видалення порожніх папок та папок в папках"""

    for f in os.listdir(path):
        new_path = path / f

        if os.path.isfile(new_path):
            continue
        elif f in "images, video, documents, music, archives, unknown": # пошук власноруч створених папок             
            if os.path.isdir(new_path):
                try:
                    Path(new_path).rmdir()
                except OSError:
                    continue
        else:
            rmtree(new_path)

def main():

    """Старт програми"""
    start_path = None
    try:
        start_path = Path(sys.argv[1])
        
    except IndexError:
        print("Шлях введений неправильно. Спробуйте ще раз")

    creation_folders(start_path)
    recursive_finding(start_path, start_path, level=1)
    unpack_archives(start_path)
    delete_empty_folders(start_path)

def normalize(path, moved_path):
    path_to_file = Path(path)
    file_name = path_to_file.stem # отримали ім'я без розширення
    normalized_file_name = file_name.translate(TRANS)+path_to_file.suffix # нормалізували ім'я
    full_normalized_name = path_to_file.replace(Path(moved_path) / normalized_file_name) # перемістили файл в нове місце
    
    return full_normalized_name


def recursive_finding(path, start_path, level=1):

    """Рекурсивний прохід по папкам в пошуці файлів"""
    for i in os.listdir(path):
    
        if i not in "images, video, documents, music, archives, unknown": # пропуск власноруч створених папок
            
            new_path = path / i
        
            if os.path.isdir(new_path):
                recursive_finding(new_path, start_path, level+1)

            elif os.path.isfile(new_path):
                file_extension_full = Path(new_path).suffix.upper()
                file_extension = file_extension_full[1:]
                sorting_files(file_extension, new_path, start_path)
            else:
                print('ELSE')
        else:
            continue
        

def sorting_files(extension, path, start_path):

    """Створення путі для переміщення. 
    Виклик функції нормалізування (перейменовує файл й переміщує файл).
    Додавання нового путі в список в словнику."""
    
    if extension in template_extensions["images"]:
        moved_path = start_path / "images"     
        new_moved_path = normalize(path, moved_path)
        finded_extensions["images"].append(new_moved_path)

        if extension not in finded_extensions["known"]:
            finded_extensions["known"].append(extension)

    elif extension in template_extensions["video"]:
        moved_path = start_path / "video"
        new_moved_path = normalize(path, moved_path)
        finded_extensions["video"].append(new_moved_path)

        if extension not in finded_extensions["known"]:
            finded_extensions["known"].append(extension)

    elif extension in template_extensions["documents"]:
        moved_path = start_path / "documents"
        new_moved_path = normalize(path, moved_path)
        finded_extensions["documents"].append(new_moved_path)

        if extension not in finded_extensions["known"]:
            finded_extensions["known"].append(extension)

    elif extension in template_extensions["music"]:
        moved_path = start_path / "music"
        new_moved_path = normalize(path, moved_path)
        finded_extensions["music"].append(new_moved_path)

        if extension not in finded_extensions["known"]:
            finded_extensions["known"].append(extension)

    elif extension in template_extensions["archives"]:
        moved_path = start_path / "archives"
        new_moved_path = normalize(path, moved_path)
        finded_extensions["archives"].append(new_moved_path)

        if extension not in finded_extensions["known"]:
            finded_extensions["known"].append(extension)

    else:
        moved_path = start_path / "unknown"
        new_moved_path = normalize(path, moved_path)

        if extension not in finded_extensions["unknown"]:
            finded_extensions["unknown"].append(extension)

    return finded_extensions # словник усіх знайдених файлів


def unpack_archives(start_path):
    path_folder = start_path / "archives"
    for folder in path_folder.iterdir():
        unpack_archive(folder, start_path / "archives" / folder.stem)

# Оголошення базових розширень
template_extensions = {
    "images": ['JPEG', 'PNG', 'JPG', 'SVG', 'WEBP'],
    "video": ['AVI', 'MP4', 'MOV', 'MKV'],
    "documents": ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'XLS', 'FB2', 'EPUB', 'PPTX'],
    "music": ['MP3', 'OGG', 'WAV', 'AMR'],
    "archives": ['ZIP', 'GZ', 'TAR'],
    "unknown": []
}
finded_extensions = {
    "images": [],
    "video": [],
    "documents": [],
    "music": [],
    "archives": [],
    "known": [],
    "unknown": []
}

CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ?<>,!@#[]#$%^&*()-=; "
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g", "_", "_", "_", "_",
               "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_")

# створення словника
TRANS = {}
for c, l in zip (CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()    



if __name__ == "__main__":
    main()