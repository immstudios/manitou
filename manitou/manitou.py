import os
import time
import datetime

from nxtools import *
from mpd import *

from .common import *
from .isodate import *

class Manitou(object):
    def __init__(self, output_map, **kwargs):
        self.output_map = output_map
        self.source_manifests = {}
        self.mpd_attrib = {}
        self.settings = DEFAULT_SETTINGS
        self.settings.update(kwargs)

    def get_source_manifest(self, manifest_name):
        if not manifest_name in self.source_manifests:
            logging.debug("Loading source manifest {}".format(manifest_name))
            manifest_path = os.path.join(
                    self.settings["mpd_dir"],
                    manifest_name + ".mpd"
                )
            manifest = xml(open(manifest_path).read())
            self.source_manifests[manifest_name] = manifest
            if not self.mpd_attrib:
                self.mpd_attrib = manifest.attrib
        return self.source_manifests[manifest_name]

    def get_representation(self, manifest_name, representation_id):
        try:
            manifest = self.get_source_manifest(manifest_name)
        except Exception:
            log_traceback()
            return None
        period = manifest.find(NS + "Period")
        for adaptation_set in period.findall(NS + "AdaptationSet"):
            for representation in adaptation_set.findall(NS + "Representation"):
                if representation.attrib.get("id", False) == representation_id:
                    return representation
        return None


    def render(self, **kwargs):
        mpd = None
        period = None
        ta_sets = {}

        for ma in self.output_map:
            for mr in ma["representations"]:
                sr = self.get_representation(
                        mr["manifest_name"],
                        mr["source_id"]
                    )

                if mpd is None:
                    if "mpd_attrib" in kwargs:
                        self.mpd_attrib.update(kwargs["mpd_attrib"])
                    mpd = MPD(**self.mpd_attrib)
                    period = mpd.add_period()

                ta_id = ma["id"]
                if not ta_id in ta_sets:
                    a_attr = {k : ma[k] for k in ma if k != "representations"}
                    ta_sets[ta_id] = period.add_adaptation_set(**a_attr)
                ta = ta_sets[ta_id]
                tr = ta.add_representation(**sr.attrib)
                tr["id"] = mr["target_id"]

                tr.segment_template = SegmentTemplate(
                        **sr.find(NS+"SegmentTemplate").attrib
                    )
        if mpd["availabilityStartTime"] is not None:
            astart = parse_iso_datetime(mpd["availabilityStartTime"])
            astart += datetime.timedelta(seconds=kwargs.get("ats_offset", 10))
            mpd["availabilityStartTime"] = astart.isoformat()

        return mpd.xml


    def save(self, target, **kwargs):
        path = str(target)
        with open(path, "w") as f:
            f.write(self.render(**kwargs))
