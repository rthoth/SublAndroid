import glob, os, sublime

def _is_project(folder):
    return True if glob.glob(os.path.join(folder, 'build.gradle')) else False

def has_project(window):
    for folder in window.folders():
        if _is_project(folder):
            return True
    return False

def search_project_folders(window):
    return [folder for folder in window.folders() if _is_project(folder)]

class Project:
    def __init__(self, folder):
        self._folder = folder

    def path(self, path):
        path = os.path.join(self._folder, path)
        return path if os.path.exists(path) else None
