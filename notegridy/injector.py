# from updatable_zipfile import UpdatableZipFile

from os import path
from os.path import basename, dirname
from shutil import copyfile
from typing import List, Optional

from updateablezipfile import UpdateableZipFile


class Injector:
    plugin: UpdateableZipFile
    plugin_name: str
    plugin_root: str

    def __init__(self, original_plugin: str, output_path: str | None) -> None:
        # get the filename of the path to the plugin
        original_plugin_name = basename(original_plugin)

        # copy the plugin to its final location
        final_plugin_name = "{0}-with-tegrity.{1}".format(
            *original_plugin_name.rsplit(".", 1)
        )
        if output_path == None:
            final_plugin_path = path.join(dirname(original_plugin), final_plugin_name)
        else:
            final_plugin_path = path.join(output_path, final_plugin_name)
        copyfile(original_plugin, final_plugin_path)

        # initialize the Updatable zip file with the copied plugin
        self.plugin = UpdateableZipFile(final_plugin_path, "a")

        # set the plugin name, this is later used to figure out the init file
        self.plugin_name = original_plugin_name.removesuffix(".zip")

        # WordPress plugins sometimes have a single folder
        # with the name of the plugin in which every file is stored
        # the following handles that case
        top_level_directorys = {item.split("/")[0] for item in self.plugin.namelist()}
        if len(top_level_directorys) == 1:
            top_level_directory = list(top_level_directorys)[0]
            self.plugin_root = top_level_directory + "/"
            self.plugin_name = top_level_directory
        else:
            self.plugin_root = "/"

    def inject_archive(self, archive: str):
        # get the filename of the path to the archive
        archive_file_name = basename(archive)

        # writes the archive to the zip file
        self.plugin.write(archive, path.join(self.plugin_root, archive_file_name))

        # tries to find the by WordPress initially loaded file
        possible_init_files = self._possible_init_files()
        if len(possible_init_files) == 0:
            init_file = self._backup_init_file()
            if init_file == None:
                raise Exception("Could not find init file")
        else:
            init_file = possible_init_files[0]

        # read the actual init file and appends a new line to it
        # in order to load the archive as soon as the plugin
        # is loaded by WordPress
        init_data = self.plugin.read(init_file).decode()
        init_data += f"""\nrequire "phar://" . dirname(__FILE__) . "/{archive_file_name}/init.php";\n"""
        self.plugin.writestr(init_file, str.encode(init_data))

    def write_file(self, filename, contents):
        absolute_path = path.join(self.plugin_root, filename)
        self.plugin.writestr(absolute_path, contents)

    def _possible_init_files(self) -> List[str]:
        possible_init_file_names = self.plugin_name.split("-")

        possible_init_files = []

        for index in range(len(possible_init_file_names)):
            possible_init_file = (
                self.plugin_root
                + "-".join(possible_init_file_names[: index + 1])
                + ".php"
            )

            if possible_init_file in self.plugin.namelist():
                possible_init_files.append(possible_init_file)

        return possible_init_files

    def _backup_init_file(self) -> Optional[str]:
        possible_init_files = list(
            filter(
                lambda s: s.endswith(".php"),
                list({item.split("/")[1] for item in self.plugin.namelist()}),
            )
        )
        possible_init_files.sort()

        if len(possible_init_files) >= 1:
            return self.plugin_root + possible_init_files[-1]

    def __enter__(self):
        # actually opens the zip file
        self.plugin = self.plugin.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # closes the underlying zip file
        self.plugin.__exit__(exc_type, exc_val, exc_tb)
