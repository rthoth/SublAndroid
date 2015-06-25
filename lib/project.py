from os.path import join, exists

_BUILD_DOT_GRADLE = 'build.gradle'
_ANDROID_MANIFEST_DOT_XML = join('src', 'main', 'AndroidManifest.xml')


def _is_project(folder):
    return exists(join(folder, _BUILD_DOT_GRADLE)) \
        and exists(join(folder, _ANDROID_MANIFEST_DOT_XML))


def has_project(folders):
    for folder in folders:
        if _is_project(folder):
            return True
    return False


def search_project_folders(folders):
    return [folder for folder in folders if _is_project(folder)]
