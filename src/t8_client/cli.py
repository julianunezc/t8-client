import click

import t8_client.functions as fun
from t8_client.spectrum import Spectrum as sp
from t8_client.waveform import Waveform as wf


@click.group()
@click.pass_context
def cli(ctx):
    """CLI client to interact with the T8 API.
    This command manages the global credentials (user, password and host) needed to
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
    func = click.option("-p", "--point", required=True, help="Point name")(func)
    func = click.option("-m", "--pmode", required=True, help="Processing mode value.")(
        func
    )
    return func


@cli.command()
@click.pass_context
@common_options
def list_waves(ctx, machine, point, pmode) -> list:
    """Lists the waveform capture dates for the specified machine, point and pmode
    in the format 'YYYY-MM-DDTHH:MM:SS'.

    Parameters:
    machine (str): Machine name.
    point (str): Point name.
    pmode (str): Processing mode value.

    Returns:
    list: A list of timestamps in the format 'YYYY-MM-DDTHH:MM:SS'.
    """
    url = f"http://{ctx.obj['HOST']}/rest/waves/{machine}/{point}/{pmode}"
    timestamps = fun.get_timestamps(url, machine, point, pmode)
    for ts in timestamps:
        click.echo(ts)


@cli.command()
@click.pass_context
@common_options
def list_spectra(ctx, machine, point, pmode) -> list:
    """Lists the spectrum capture dates for the specified machine, point, and pmode
    in the format 'YYYY-MM-DDTHH:MM:SS'.

    Parameters:
    machine (str): Machine name.
    point (str): Point name.
    pmode (str): Processing mode value.

    Returns:
    list: A list of timestamps in the format 'YYYY-MM-DDTHH:MM:SS'.
    """
    url = f"http://{ctx.obj['HOST']}/rest/spectra/{machine}/{point}/{pmode}"
    timestamps = fun.get_timestamps(url, machine, point, pmode)
    for ts in timestamps:
        click.echo(ts)


@cli.command()
@click.pass_context
@common_options
@click.option("-t", "--datetime", required=True, help="Datetime value.")
def get_wave(ctx, machine, point, pmode, datetime):
    """Gets the waveform data for the specified machine, point, pmode, and datetime,
    and saves it as a CSV file.

    Parameters:
    machine (str): Machine name.
    point (str): Point name.
    pmode (str): Pmode value.
    datetime (str): Datetime value in 'YYYY-MM-DDTHH:MM:SS' format.
    """
    wave = wf.from_api(machine, point, pmode, datetime)

    safe_datetime = datetime.replace(":", "-")
    filename = f"waveform_{machine}_{point}_{pmode}_{safe_datetime}.csv"

    wave.save_to_csv(filename)


@cli.command()
@click.pass_context
@common_options
@click.option("-t", "--datetime", required=True, help="Datetime value.")
def get_spectrum(ctx, machine, point, pmode, datetime):
    """Gets the spectrum data for the specified machine, point, pmode, and datetime,
    and saves it as a CSV file.

    Parameters:
    machine (str): Machine name.
    point (str): Point name.
    pmode (str): Pmode value.
    datetime (str): Datetime value in 'YYYY-MM-DDTHH:MM:SS' format.
    """
    spectrum = sp.from_api(machine, point, pmode, datetime)

    safe_datetime = datetime.replace(":", "-")
    filename = f"spectrum_{machine}_{point}_{pmode}_{safe_datetime}.csv"

    spectrum.save_to_csv(filename)


if __name__ == "__main__":
    cli()
