from pathlib import Path
import sys
import shutil

# Creating translation table
CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
            "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

TRANS = {}

for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()


def file_replacement(elem, folders_pathes, extensions, files_in_folder):


    files = {
        "images": ("JPEG", "PNG", "JPG", "SVG"),
        "video": ("AVI", "MP4", "MOV", "MKV"),
        "documents": ("DOC", "DOCX", "TXT", "PDF", "XLSX", "PPTX"),
        "audio": ("MP3", "OGG", "WAV", "AMR"),
        "archives": ("ZIP", "GZ", "TAR")
    }

    def transering_files(elem, category):

        elem_path = elem.absolute()
        print(f"{elem_path} will be replaced to {folders_pathes[category]}")
        element_name = normalize(elem.stem)

        if category == "archives":
            
            shutil.unpack_archive(elem, f"{folders_pathes[category]}\{element_name}")
            elem_path.unlink()

        else:
            elem_path.replace(f"{folders_pathes[category]}\{element_name}")

        extensions[category].add(elem.suffix[1:])
        files_in_folder[category].append(element_name)

    for key, word in files.items():
        if elem.suffix[1:].upper() in word:
            transering_files(elem, key)

    if elem.is_file():

        if len(elem.suffix) != 0:
            extensions['unknown'].add(elem.suffix[1:])
        
        else:
            extensions['unknown'].add('no extension')
    

def folders_creation(path, folders_tuple):

    folders = {}

    for elem in folders_tuple:
        folders[elem] = f"{path.absolute()}\{elem}"

    for w in folders.values():

        folder_path = Path(w)
        folder_path.mkdir(exist_ok=True)

    return folders


def normalize(name):

    name = name.translate(TRANS)

    for index, char in enumerate(name):
        
        if not char.isalnum():
            name = name[:index] + '_' + name[index+1:]
    
    return name


def recursion_directory(folder_path, folders_pathes, extensions, files_in_folder):

    for elem in folder_path.iterdir():
        
        if elem.is_file():
            file_replacement(elem, folders_pathes, extensions, files_in_folder)

        elif elem.is_dir():
     
            elem_path = elem.absolute()
            folder_name = normalize(elem_path.name)
            if folder_name != elem_path.name:
                folder_name = normalize(elem_path.name)
                elem_path = elem_path.replace(elem_path.with_stem(folder_name))

            recursion_directory(elem_path, folders_pathes, extensions, files_in_folder)

            try:
                elem_path.rmdir()
            except OSError:
                print(f"Folder {elem_path} contains files or folders with unknown extensions")


def main():

    # Перелік заданих тек
    folders = ("archives", "audio", "documents", "images", "video")
    # Словник для списку знайдених розширень
    extensions = {'unknown': set()}
    # Словник для списку файлів у теці
    files_in_folder = {}
    # Створення словників з типами файла в якості ключів
    for folder in folders:
        extensions[folder] = set()
        files_in_folder[folder] = []

    # Перевірка на введені аргументи
    if len(sys.argv) < 2:
        
        print("No path was given")
        user_path = ""  
        
    else:
        user_path = sys.argv[1]

    # Шлях, який необхідно розібрати
    path = Path(user_path)
   
    # Перевірка чи існує введений шлях
    if path.exists():
        
        # Перевірка чи вказаний шлях є текою
        if path.is_dir():
            
            # Створення заданих папок та 
            folders_pathes = folders_creation(path, folders)

            # Перевірка на наявність інших тець у вказаному шляху
            for elem in path.iterdir():

                # Перевірка чи тека є заданою
                if elem.name not in folders and elem.is_dir():
                    
                    # Якщо теки немає в заданих, то присвоюємо цій теці поточний шлях та розбираємо 
                    folder_path = elem.absolute()
                    folder_name = normalize(folder_path.stem)
                    if folder_name != folder_path.stem:

                        folder_name = normalize(folder_path.stem)
                        folder_path = folder_path.replace(folder_path.with_stem(folder_name))
                    
                    try:
                        recursion_directory(folder_path, folders_pathes, extensions, files_in_folder)
                    except:
                        pass
                    # Якщо в теці знаходиться файл з невідомим розширенням то не видаляємо її
                    try:
                        folder_path.rmdir()
                    except OSError:
                        print(f"Folder {folder_path} contains file with unknown extensions")    
                else:
                    file_replacement(elem, folders_pathes, extensions, files_in_folder)

        else:
            print(f"Path '{path.absolute()}' is a file")

        for k, w in extensions.items():

            if len(w) > 0:
                print(f"{k:<10} extensions are: {', '.join(w)}")
            
            else:
                print(f"{k:<10} extensions haven't been found")

        for k, w in files_in_folder.items():

            if len(w) > 0:
                print(f"{k:<10} files are: {', '.join(w)}")
            
            else:
                print(f"{k:<10} files haven't been found")

    else:
        print(f"Path '{path.absolute()}' doesn't exist")

    
if __name__ == "__main__":
    main()