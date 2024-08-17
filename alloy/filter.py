import os


def ignore_comments(file_path):
    ignore_list = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):  # ignore comments in .alloyignore and DEFAULT_IGNORE_LIST
                ignore_list.append(line)
    return ignore_list


def read_alloyignore(project_root, extension_filter):
    """
    Excludes all files, extensions and directories specified in .alloyignore, located inside the root directory.
    """
    alloyignore = os.path.join(project_root, ".alloyignore")
    default_ignore_list = DEFAULT_IGNORE_LIST.copy()

    print(f"Project root: {project_root}")
    print(f"Extension filter: {extension_filter}")
    print(f"Default ignore list: {default_ignore_list}")

    custom_ignore_list = []
    if os.path.exists(alloyignore):
        with open(alloyignore, "r", encoding="utf-8") as f:
            custom_ignore_list = [line.strip() for line in f if line.strip() and not line.startswith("#")]
    else:
        print(f"Warning: .alloyignore file not found at {alloyignore}")

    print(f"Custom ignore list: {custom_ignore_list}")

    default_ignore_list.extend(custom_ignore_list)
    print(f"Final ignore list: {default_ignore_list}")

    def exclude_files(file_path):
        file_path = file_path.replace(os.sep, "/")
        print(f"Checking file: {file_path}")

        if extension_filter:
            _, file_extension = os.path.splitext(file_path)
            if file_extension[1:] in extension_filter:
                print(f"File {file_path} not excluded due to extension filter")
                return False

        for pattern in default_ignore_list:
            pattern = pattern.replace(os.sep, "/")
            print(f"Checking pattern: {pattern}")
            if pattern.startswith("/"):  # covers absolute paths from the root
                if file_path.startswith(pattern[1:]):
                    print(f"File {file_path} excluded by pattern {pattern}")
                    return True
            elif pattern.endswith("/"):  # ignores certain directories
                if any(part == pattern[:-1] for part in file_path.split("/")):
                    print(f"File {file_path} excluded by pattern {pattern}")
                    return True
            elif "*" in pattern:  # handle wildcard patterns
                parts = pattern.split("*")
                if len(parts) == 2:
                    if file_path.startswith(parts[0]) and file_path.endswith(parts[1]):
                        print(f"File {file_path} excluded by pattern {pattern}")
                        return True
            elif (
                pattern == file_path
                or pattern == os.path.basename(file_path)
                or (pattern.startswith(".") and file_path.endswith(pattern))
            ):
                print(f"File {file_path} excluded by pattern {pattern}")
                return True

        print(f"File {file_path} not excluded")
        return False

    return exclude_files


def filter_extensions(file_path, extensions):
    """
    Optional filter to include only certain provided extensions in the consolidated markdown file. If no extensions are
    provided, all files are considered except files, extensions and directories that are explicitly excluded in the
    specified .alloyignore file, located inside the root directory.
    """
    if not extensions:
        return True
    _, file_extension = os.path.splitext(file_path)
    return file_extension[1:] in extensions


def parse_extensions(_csx, _param, value):
    """
    Converts a comma-separated string of file extensions into a list of individual extensions, which - in turn - is
    parsed to the main function to filter files during the consolidation process.
    """
    if not value:
        return None
    return [ext.strip() for item in value for ext in item.split(",")]


DEFAULT_IGNORE_LIST = [
    ".cache/",
    ".coverage",
    "dist/",
    ".DS_Store",
    ".git",
    ".idea",
    "Thumbs.db",
    ".venv/",
    ".vscode/",
    # JS
    "node_modules/",
    # Python
    "*.pyc",
    # alloy-specific files
    ".alloyignore",
    ".alloy.example",
    "alloy.md",
]
