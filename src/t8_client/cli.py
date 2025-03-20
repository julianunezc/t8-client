import click

import t8_client.functions as fun


@click.group()
@click.pass_context
def cli(ctx):
    """CLI client to interact with the T8 API.
    This command manages the global credentials (user, password, and host) needed to
    perform actions via the API. The credentials are loaded from environment variables.
    """
    ctx.ensure_object(dict)
    user, password, host = fun.load_env_variables()

    ctx.obj["USER"] = user
    ctx.obj["PASSWORD"] = password
    ctx.obj["HOST"] = host


def common_options(func):
    """Decorator to add common options: machine, point, and pmode."""
    func = click.option("-M", "--machine", required=True, help="Machine name.")(func)
    func = click.option("-p", "--point", required=True, help="Point name.")(func)
    func = click.option("-m", "--pmode", required=True, help="Pmode value.")(func)
    return func


@cli.command()
@click.pass_context
@common_options
def list_waves(ctx, machine, point, pmode):
    """Lists the waveform capture dates for the specified machine, point, and pmode.

    Parameters:
    machine (str): Machine name.
    point (str): Point name.
    pmode (str): Pmode value.
    """
    # API URL
    url = f"http://{ctx.obj['HOST']}/rest/waves/{machine}/{point}/{pmode}"
    timestamps = fun.get_timestamps(url, machine, point, pmode)
    for ts in timestamps:
        click.echo(ts)


@cli.command()
@click.pass_context
@common_options
def list_spectra(ctx, machine, point, pmode):
    """Lists the spectrum capture dates for the specified machine, point, and pmode.

    Parameters:
    machine (str): Machine name.
    point (str): Point name.
    pmode (str): Pmode value.
    """
    # API URL
    url = f"http://{ctx.obj['HOST']}/rest/spectra/{machine}/{point}/{pmode}"
    timestamps = fun.get_timestamps(url, machine, point, pmode)
    for ts in timestamps:
        click.echo(ts)


if __name__ == "__main__":
    cli()
