import sublime, glob, os

def _is_project(folder):
	return True if glob.glob(os.path.join(folder, 'build.gradle')) else False

def has_project(window):
	for folder in window.folders():
		if _is_project(folder):
			return True
	return False

def search_projects(window):

	projects = [Project(folder, window) for folder in window.folders() if _is_project(folder)]

	sublime.status_message(str(projects))

	return None if projects else projects

class Project:

	def __init__(self, folder, window):
		self._window = window
