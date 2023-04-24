![Image of Randy Marsh](./header-image.webp)

# no-tegridy

`no-tegridy` is a small red team script for injecting login interception code into existing WordPress plugins.

## Installation

To install the script just run:

```bash
pip install no-tegridy
```

## Command overview

To inject the login interception code into a plugin run the `inject` command.
If you would like to have and overview of the available options run:

```bash
no-tegridy inject --help
```

In order to fetch logged data from a WordPress instance,
with the respectively installed plugin, run the `fetch` command.
If you would like to have and overview of the available options run:

```bash
no-tegridy fetch --help
```
