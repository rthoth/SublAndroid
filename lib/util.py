import sublime


def show_java_failure(failure, window):
    for view in window.views():
        if view.file_name() == failure.file:
            sublime.message_dialog('Achei')
