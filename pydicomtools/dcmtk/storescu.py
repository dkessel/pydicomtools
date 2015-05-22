
import subprocess


class StoreSCU():

    def __init__(self, peer, port, dcmfile_in):
        if peer is None:
            raise ProcessException("peer must not be None")
        if port == 0:
            raise ProcessException("port must not be 0")
        if dcmfile_in is None:
            raise ProcessException("dcmfile_in must not be None")

        self.peer = peer
        self.port = port
        self.dcmfile_in = dcmfile_in

    def execute(self):
        result = subprocess.call(["storescu", "--scan-directories", self.peer, str(self.port), str(self.dcmfile_in) + "/*.*"])
        if result:
            raise ProcessException("error sending the data! process returned: " + str(result))


class ProcessException(Exception):

    def __init__(self, *args, **kwargs):
        Exception.__init__(self, args)
