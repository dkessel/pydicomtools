import tkinter
import tkinter.filedialog
import time
from pydicomtools.importer.importerapp import ImporterApp


class ImporterFrame(tkinter.Frame):
    def __init__(self, app, master=None):
        tkinter.Frame.__init__(self, master)
        self.app = app

        self.pack(padx=10, pady=10)

        self.topText = tkinter.StringVar()
        self.topText.set("Where is the data you want to import?")

        self.topLabel = tkinter.Label(self, textvariable=self.topText)
        self.topLabel.pack(fill="both")

        self.selectDirectoryButton = tkinter.Button(self)
        self.selectDirectoryButton["text"] = "in a directory..."
        self.selectDirectoryButton["command"] = self.select_directory
        self.selectDirectoryButton.pack(padx=5, pady=5)

        self.backButton = tkinter.Button(self)
        self.backButton["text"] = "< Back"

        self.addMoreButton = tkinter.Button(self)
        self.addMoreButton["text"] = "Add more…"
        self.addMoreButton["command"] = self.go_to_step_one

        self.continueButton = tkinter.Button(self)
        self.continueButton["text"] = "Continue >"
        self.continueButton["command"] = self.go_to_step_three

        self.networkAddressLabel = tkinter.Label(self)
        self.networkAddressLabel["text"] = "Network Address"

        self.networkAddressEntry = tkinter.Entry(self)
        self.networkAddress = tkinter.StringVar()
        self.networkAddress.set(self.app.get_config().get_cstore_address())
        self.networkAddressEntry["textvariable"] = self.networkAddress

        self.cStorePortLabel = tkinter.Label(self)
        self.cStorePortLabel["text"] = "Port (C-Store)"

        self.cStorePortEntry = tkinter.Entry(self)
        self.cStorePort = tkinter.StringVar()
        self.cStorePort.set(str(self.app.get_config().get_cstore_port()))
        self.cStorePortEntry["textvariable"] = self.cStorePort

        self.cEchoCheckButton = tkinter.Checkbutton(self)
        self.cEchoCheckButton["text"] = "Check if system is available before sending"
        self.cEchoChecked = tkinter.BooleanVar()
        self.cEchoChecked.set(self.app.get_config().is_verify_cecho())
        self.cEchoCheckButton["variable"] = self.cEchoChecked

        self.dicomCommitmentCheckButton = tkinter.Checkbutton(self)
        self.dicomCommitmentCheckButton["text"] = "Request DICOM Commitment after sending"
        self.dicomCommitmentChecked = tkinter.BooleanVar()
        self.dicomCommitmentChecked.set(self.app.get_config().is_verify_commitment())
        self.dicomCommitmentCheckButton["variable"] = self.dicomCommitmentChecked

        self.qrVerifyCheckButton = tkinter.Checkbutton(self)
        self.qrVerifyCheckButton["text"] = "Use DICOM Q/R to verify data was received"
        self.qrVerifyChecked = tkinter.BooleanVar()
        self.qrVerifyChecked.set(self.app.get_config().is_verify_query_retrieve())
        self.qrVerifyCheckButton["variable"] = self.qrVerifyChecked

        self.sendDataButton = tkinter.Button(self)
        self.sendDataButton["text"] = "Send data"

    def select_directory(self):
        selected_dir = tkinter.filedialog.askdirectory(mustexist=True, title="select the directory to import from",
                                                       initialdir=self.app.get_directory())
        if selected_dir:
            self.app.set_directory(selected_dir)
            # TODO: start background scan of data... show text 'Searching for data'
            self.go_to_step_two(scan=True)

    def go_to_step_two(self, scan=False):
        # remove elements
        # from step 1
        self.selectDirectoryButton.pack_forget()
        # from step 3
        self.networkAddressLabel.pack_forget()
        self.networkAddressEntry.pack_forget()
        self.cStorePortLabel.pack_forget()
        self.cStorePortEntry.pack_forget()
        self.cEchoCheckButton.pack_forget()
        self.dicomCommitmentCheckButton.pack_forget()
        self.qrVerifyCheckButton.pack_forget()
        self.sendDataButton.pack_forget()
        # add elements
        self.backButton["command"] = self.forget_directory_and_go_to_step_one
        self.backButton.pack(padx=5, pady=5, side="left")
        self.addMoreButton.pack(padx=5, pady=5, side="left")
        self.continueButton.pack(padx=5, pady=5, side="left")
        # start scanning...
        if scan:
            self.continueButton["state"] = "disabled"
            self.app.set_scan_callback(self.update_result)
            self.app.scan_directory()
            self.topText.set('Summary of data to import:\n\n' + self.app.get_directory_content_summary())
        else:
            self.continueButton["state"] = "normal"
            self.topText.set('Summary of data to import:\n\n' + self.app.get_directory_content_summary())

    def update_result(self):
        self.topText.set('Summary of data to import:\n\n' + self.app.get_directory_content_summary())
        self.continueButton["state"] = "normal"

    def forget_directory_and_go_to_step_one(self):
        self.app.set_directory(None)
        self.go_to_step_one()

    def go_to_step_one(self):
        # remove elements
        # from step 2
        self.backButton.pack_forget()
        self.addMoreButton.pack_forget()
        self.continueButton.pack_forget()
        # add elements
        self.topText.set("Where is the data you want to import?")
        self.selectDirectoryButton.pack(padx=5, pady=5)

    def go_to_step_three(self):
        # remove elements
        self.backButton.pack_forget()
        self.addMoreButton.pack_forget()
        self.continueButton.pack_forget()
        # add elements
        self.topText.set("Transfer Configuration")
        self.networkAddressLabel.pack()
        self.networkAddressEntry.pack()
        self.cStorePortLabel.pack()
        self.cStorePortEntry.pack()
        self.cEchoCheckButton.pack(padx=5, pady=5)
        self.dicomCommitmentCheckButton.pack(padx=5, pady=5)
        self.qrVerifyCheckButton.pack(padx=5, pady=5)

        self.backButton["command"] = self.go_to_step_two
        self.backButton.pack(padx=5, pady=5, side="left")
        self.sendDataButton.pack(padx=5, pady=5, side="right")


def main():
    root = tkinter.Tk()
    root.wm_title("pydicomtools importer")

    app = ImporterApp()
    frame = ImporterFrame(app, root)
    frame.mainloop()


if __name__ == "__main__":
    main()
