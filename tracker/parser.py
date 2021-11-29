import json
from os import path
from urllib.request import urlopen
import xml.etree.ElementTree as ET


class KernelParser:
    """Base parser class."""

    def __init__(self, db_file: str) -> None:
        self.db_file = db_file
        self.version_table = {
            "mainline": {},
            "stable": {},
            "longterm": {},
            "linux-next": {},
        }
        self._parse_release()

    # Populates kernel release version table as a python dictionary
    def _parse_release(self) -> None:
        # https://stackoverflow.com/a/35591479
        nbsp_hax = """<!DOCTYPE html [
            <!ENTITY nbsp ' '>
            ]>"""

        with urlopen("https://kernel.org") as raw:
            fixed_up_html = raw.read().decode().replace("<!DOCTYPE html>", nbsp_hax)
            raw_data = ET.fromstring(fixed_up_html)
        raw_table = raw_data.findall('.//table[@id="releases"]/tr')

        for i in raw_table:
            td_list = i.findall("./td")
            release = td_list[0].text[:-1]
            if release in self.version_table:
                self._update_table(td_list, release)

    # Update the global version table from values passed by parser function
    def _update_table(self, td_list: list, title: str) -> None:
        # itering over text since releases can contain '[EOL]' sometimes
        version = "".join(td_list[1].itertext())
        release_date = td_list[2].text

        links = {}
        for i in td_list:
            if i.find("a") is not None:
                link = i.find("a")
                links = {**links, link.text: link.get("href")}

        # self.version_table[title].update({version: {"date": release_date, **links}})
        self.version_table[title] = {
            **self.version_table[title],
            version: {"date": release_date, **links},
        }

    def to_json(self, indent: int = None) -> str:
        """Returns latest kernel release version table as json."""
        return json.dumps(self.version_table, indent=indent)

    def write_json(self) -> None:
        """Writes version table as a database file."""
        with open(
            path.dirname(__file__) + "/../" + self.db_file, "w", encoding="utf-8"
        ) as data:
            data.write(self.to_json(4))

    def get_updated_kernels(self) -> dict:
        """Returns a dictionary of updated kernel version(s) with there links."""
        updated_kernels = {
            "mainline": {},
            "stable": {},
            "longterm": {},
            "linux-next": {},
        }
        try:
            with open(
                path.dirname(__file__) + "/../" + self.db_file, "r", encoding="utf-8"
            ) as local:
                local_db = json.loads(local.read())
        except FileNotFoundError:
            print("Local db not found! Printing all releases!\n")
            return self.version_table

        for rel in self.version_table:
            for ver in self.version_table[rel]:
                if ver not in local_db[rel].keys():
                    updated_kernels[rel] = {
                        **updated_kernels[rel],
                        ver: self.version_table[rel].get(ver),
                    }
        return updated_kernels

    def to_hooman(self, kvd: dict = None) -> str:
        """Returns a decently formatted table of kernel version for hoomans by hoomans."""
        if kvd is None:
            kvd = self.version_table
        msg = ""
        for rel in kvd:
            for ver in kvd[rel]:
                msg += f"{rel: <10} -- {ver: <15} -- {kvd[rel][ver].get('date'): <10}\n"
        return msg
