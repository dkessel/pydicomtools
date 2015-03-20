
class ImporterApp():

    def __init__(self):
        self.directory = None

    def set_directory(self, selected_dir):
        self.directory = selected_dir

    def get_directory_content_summary(self):
        if self.directory:
            return "Fake summary here..."
        else:
            return "No directory selected"
