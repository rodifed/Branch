import sublime
import sublime_plugin

class BranchInterpretCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        if not self.view.file_name().endswith(".b"):
            sublime.error_message("Not a .b (Branch) file!")
            return

        content = self.view.substr(sublime.Region(0, self.view.size()))
        interpreted_content = self.interpret(content)

        new_view = self.view.window().new_file()
        new_view.insert(edit, 0, interpreted_content)
        new_view.set_syntax_file('Packages/Branch/BranchLog.sublime-syntax')

    def interpret(self, content):
        lines = content.split('\n')
        current_path = []
        struct_content = {}
        current_struct_content = []
        inside_struct = False

        debug_info = []  # to store debugging information

        for line in lines:
            line = line.strip()

            if line.startswith("@Package"):
                package_name = line.split(" ")[1]
                current_path.append(package_name)

            elif line.startswith("struct"):
                struct_parts = line.split(" ")
                struct_name = struct_parts[1]
                current_path.append(struct_name)
                inside_struct = True
                current_struct_content = []

            elif line == "}":
                path_representation = ".".join(current_path)
                struct_content[path_representation] = current_struct_content
                debug_info.append(f"Stored struct: {path_representation}")
                if current_path:
                    current_path.pop()
                if inside_struct:
                    inside_struct = False

            elif inside_struct:
                current_struct_content.append(line)

        result = []
        for line in lines:
            if line.endswith("()"):
                path_to_run = line[:-2]
                if path_to_run in struct_content:
                    result.extend(struct_content[path_to_run])
                else:
                    debug_info.append(f"Path not found: {path_to_run}")

        #if not result:  # If no content is found to display
        result = debug_info + result

        return "\n".join(result)
