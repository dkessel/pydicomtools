
import subprocess
from pydicomtools.dcmtk.processexception import ProcessException


class EchoSCU():

    def __init__(self, peer, port):
        if peer is None:
            raise ProcessException("peer must not be None")
        if port == 0:
            raise ProcessException("port must not be 0")

        self.peer = peer
        self.port = port

    def execute(self):
        result = subprocess.call(["echoscu", self.peer, str(self.port)])
        if result:
            raise ProcessException("verification with C-Echo-RQ failed! process returned: " + str(result))

