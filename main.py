from mpris_server.adapters import MprisAdapter
from mpris_server import Metadata

class PresentAdapter(MprisAdapter):
    def metadata(self) -> Metadata:
        return Metadata()

adap = MprisAdapter()
adap.