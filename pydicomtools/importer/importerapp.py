import os
import dicom


class ImporterApp():
    def __init__(self):
        self.directory = None
        self.patientIDs = set()
        self.studyUIDs = dict()
        self.seriesUIDs = dict()
        self.instanceUIDs = dict()
        self.files = dict()
        self.callback = None

    def set_directory(self, selected_dir):
        self.directory = selected_dir

    def get_directory(self):
        return self.directory

    def get_directory_content_summary(self):
        if self.directory:
            if len(self.patientIDs) > 0:
                total_size = 0
                for f in self.files.values():
                    total_size += os.path.getsize(f)
                total_size /= 1000000
                total_size = round(total_size)

                return "Patients: " + str(len(self.patientIDs)) + "\n" \
                        + "Studies: " + str(len(self.studyUIDs)) + "\n" \
                        + "Series: " + str(len(self.seriesUIDs)) + "\n" \
                        + "Instances: " + str(len(self.instanceUIDs)) + "\n" \
                        + "Total size: " + str(total_size) + " MB"

            else:
                return "Scanning ..."
        else:
            return "No DICOM data found"

    def set_scan_callback(self, callback):
        self.callback = callback

    def scan_directory(self):
        if self.directory:
            dir_content = os.listdir(self.directory)
            # only try files
            filter(os.path.isfile, dir_content)
            # sort by name
            dir_content.sort()

            for file in dir_content:
                file = os.path.join(self.directory, file)
                dcm = dicom.read_file(file)
                # Patient ID
                pid = dcm.PatientID
                if not pid in self.patientIDs:
                    self.patientIDs.add(pid)
                # Study Instance UID
                study_uid = dcm.StudyInstanceUID
                if not study_uid in self.studyUIDs:
                    self.studyUIDs[study_uid] = pid
                # Series Instance UID
                series_uid = dcm.SeriesInstanceUID
                if not series_uid in self.seriesUIDs:
                    self.seriesUIDs[series_uid] = study_uid
                # SOP Instance UID
                instance_uid = dcm.SOPInstanceUID
                if not instance_uid in self.instanceUIDs:
                    self.instanceUIDs[instance_uid] = series_uid
                    self.files[instance_uid] = file

        # tell callback that we are done
        if self.callback:
            self.callback()
