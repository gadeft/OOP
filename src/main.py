from file_manager import FileManager


if __name__ == '__main__':
    fm = FileManager()

    print("\n---------------root folder content---------------\n")
    print(fm.get_record_by_path('/').payload)

    # Creating files and directories
    fm.create_directory('/', name="users")
    fm.create_directory('/', name="home")
    fm.create_directory('/users', name="admin")
    file_record = fm.create_file('/users/admin', name="top_secret", file_type='txt', payload=b"SuperDuperMegaSecretPasswordYouAreNotGonnaKnowIt")

    # Testing for errors
    try:
        fm.create_file('/users/admin', name="top_secret", file_type='txt', payload=b'asdf')
    except FileExistsError:
        print("File already exists")

    try:
        fm.create_file('/unexisting_folder', name="test", file_type='test', payload=b'asdf')
    except FileNotFoundError:
        print("Not existing path")

    # Changing file content
    print(file_record.payload)
    file_record = fm.change_file_content('/users/admin/top_secret', 'EasyHacked')
    print(file_record.payload)

    print("\n---------------root folder content---------------\n")
    print(fm.get_record_by_path('/').payload)

    # Renaming, moving and copying files
    fm.rename(path='/users/admin/top_secret', new_name='not_at_all')
    fm.change_path(path='/home', new_dir_path='/users/admin/')
    fm.copy(path='/users/admin/home', new_dir_path='/', new_name="not_home")

    print("\n---------------root folder content---------------\n")
    print(fm.get_record_by_path('/').payload)

    # Deleting files and directories
    fm.delete('/not_home')
    fm.delete('/users/admin/not_at_all')

    print("\n---------------root folder content---------------\n")
    print(fm.get_record_by_path('/').payload)