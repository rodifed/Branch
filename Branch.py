import sublime
import sublime_plugin
import re

class AutoRenameBasedOnContentCommand(sublime_plugin.EventListener):
    def on_post_save_async(self, view):
        # Ensure we're only working on .timeline files
        if not view.file_name().endswith(".b"):
            return

        content = view.substr(sublime.Region(0, view.size()))

        # Sample regex to capture the package name
        match = re.search(r'@Package\s+(\w+)', content)
        if match:
            new_name = match.group(1) + ".b"
            old_path = view.file_name()
            directory = old_path.rsplit("/", 1)[0]
            new_path = directory + "/" + new_name

            # Rename the file
            import os
            os.rename(old_path, new_path)

            # Open the newly named file in the editor
            view.window().open_file(new_path)
