
class ImporterConfig():

    def __init__(self):
        self.cStoreAddress = "192.168.0.1"
        self.cStorePort = 104
        self.defaultDirectory = "/tmp/"
        self.verifyCEcho = False
        self.verifyCommitment = False
        self.verifyQueryRetrieve = False

    def get_cstore_address(self):
        return self.cStoreAddress

    def get_cstore_port(self):
        return self.cStorePort

    def get_default_directory(self):
        return self.defaultDirectory

    def is_verify_cecho(self):
        return self.verifyCEcho

    def is_verify_commitment(self):
        return self.verifyCommitment

    def is_verify_query_retrieve(self):
        return self.verifyQueryRetrieve
