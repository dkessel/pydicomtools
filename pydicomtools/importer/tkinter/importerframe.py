
import tkinter
import tkinter.filedialog


class ImporterFrame(tkinter.Frame):
    def __init__(self, master=None):
        tkinter.Frame.__init__(self, master)
        self.pack()

        self.topText = tkinter.StringVar()
        self.topText.set("Where is the data you want to import?")

        self.create_widgets()

    def create_widgets(self):
        self.topLabel = tkinter.Label(self, textvariable=self.topText)
        self.topLabel.pack()

        self.selectDirectoryButton = tkinter.Button(self)
        self.selectDirectoryButton["text"] = "in a directory..."
        self.selectDirectoryButton["command"] = self.select_directory
        self.selectDirectoryButton.pack()

    def select_directory(self):
        selectedDir = tkinter.filedialog.askdirectory(mustexist=True, title="select the directory to import")
        print(selectedDir)


def main():
    root = tkinter.Tk()
    root.wm_title("pydicomtools importer")
    app = ImporterFrame(root)
    app.mainloop()

if __name__ == "__main__":
    main()
