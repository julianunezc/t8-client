"""
This script is a CLI client that interacts with the T8 API to manage waveform
and spectrum data.

This file contains the following functions:

    * list_waves - Lists available waveform capture timestamps.
    * list_spectra - Lists available spectrum capture timestamps.
    * get_wave - Fetches and saves waveform data to a CSV file.
    * get_spectrum - Fetches and saves spectrum data to a CSV file.
    * plot_wave - Plots and saves waveform data as a PNG image.
    * plot_spectrum - Plots and saves spectrum data as a PNG image.
"""

import functools
import os
from typing import Callable

import click

import t8_client.functions as fun
from t8_client.spectrum import Spectrum as Sp
from t8_client.waveform import Waveform as Wf


@click.group()
@click.option("-u", "--user", default=None, help="User for authentication")
@click.option("-p", "--passw", default=None, help="Password for authentication")
@click.option("-h", "--host", default=None, help="T8 host")
@click.pass_context
def main(
    ctx: click.Context, user: str | None, passw: str | None, host: str | None
) -> None:
    """
    CLI client to interact with the T8 API.

    Parameters
    ----------
    user : str, optional
        Username. Can be provided via the '-u' flag or loaded from the
        environment variable 'USER'.
    passw : str, optional
        Password. Can be provided via the '-p' flag or loaded from the
        environment variable 'PASSW'.
    host : str, optional
        T8 host. Can be provided via the '-h' flag or loaded from the
        environment variable 'HOST'.
    """
    env_user = os.getenv("USER")
    env_passw = os.getenv("PASSW")
    env_host = os.getenv("HOST")

    user = user or env_user
    passw = passw or env_passw
    host = host or env_host

    # Check if any of the required variables are missing
    missing_vars = []
    if not user:
        missing_vars.append("USER")
    if not passw:
        missing_vars.append("PASSW")
    if not host:
        missing_vars.append("HOST")

    # If any variables are missing, print an error message and exit
    if missing_vars:
        missing_vars_str = ", ".join(missing_vars)
        click.echo(
            f"Error: Missing the following required credentials: {missing_vars_str}",
            err=True,
        )
        ctx.exit(1)

    ctx.ensure_object(dict)
    ctx.obj["USER"] = user
    ctx.obj["PASSW"] = passw
    ctx.obj["HOST"] = host


def common_options(f: Callable) -> Callable:
    """
    Decorator that adds the common options (machine, point and pmode) to subcommands.
    """

    @click.option("-M", "--machine", required=True, help="Machine tag")
    @click.option("-p", "--point", required=True, help="Point tag")
    @click.option("-m", "--pmode", required=True, help="Processing mode tag")
    @functools.wraps(f)
    def wrapper(*args: tuple, **kwargs: dict) -> None:
        return f(*args, **kwargs)

    return wrapper


@main.command()
@common_options
@click.pass_context
def list_waves(ctx: click.Context, machine: str, point: str, pmode: str) -> list:
    """
    Lists the waveform capture dates for the specified machine, point and pmode
    in the format 'YYYY-MM-DDTHH:MM:SS' in local time.

    Parameters
    ----------
    machine : str
        Machine tag.
    point : str
        Point tag.
    pmode : str
        Processing mode tag.

    Returns
    -------
    list
        A list of waveforms timestamps in the format 'YYYY-MM-DDTHH:MM:SS'
        in local time.
    """
    url = f"{ctx.obj['HOST']}/rest/waves/{machine}/{point}/{pmode}"
    timestamps = fun.get_timestamps(url, ctx.obj["USER"], ctx.obj["PASSW"])
    for ts in timestamps:
        click.echo(ts)


@main.command()
@common_options
@click.pass_context
def list_spectra(ctx: click.Context, machine: str, point: str, pmode: str) -> list:
    """
    Lists the spectra capture dates for the specified machine, point and pmode
    in the format 'YYYY-MM-DDTHH:MM:SS' in local time.

    Parameters
    ----------
    machine : str
        Machine tag.
    point : str
        Point tag.
    pmode : str
        Processing mode tag.

    Returns
    -------
    list
        A list of spectra timestamps in the format 'YYYY-MM-DDTHH:MM:SS' in local time.
    """
    url = f"{ctx.obj['HOST']}/rest/spectra/{machine}/{point}/{pmode}"
    timestamps = fun.get_timestamps(url, ctx.obj["USER"], ctx.obj["PASSW"])
    for ts in timestamps:
        click.echo(ts)


@main.command()
@common_options
@click.pass_context
@click.option("-t", "--date", required=True, help="Timestamp")
def get_wave(
    ctx: click.Context, machine: str, point: str, pmode: str, date: str
) -> None:
    """
    Fetches the waveform data for the specified machine, point, pmode and date,
    and saves it as a CSV file.

    Parameters
    ----------
    machine : str
        Machine tag.
    point : str
        Point tag.
    pmode : str
        Processing mode tag.
    date : str
        Datetime value in 'YYYY-MM-DDTHH:MM:SS' format in local time.
    """
    params = {
        "user": ctx.obj["USER"],
        "passw": ctx.obj["PASSW"],
        "host": ctx.obj["HOST"],
        "machine": machine,
        "point": point,
        "pmode": pmode,
        "date": date,
    }
    wave = Wf.from_api(params)
    safe_datetime = date.replace(":", "-")
    filename = f"waveform_{machine}_{point}_{pmode}_{safe_datetime}.csv"

    wave.save_to_csv(filename)
    click.echo(f"Waveform data saved: output/reports/{filename}")


@main.command()
@common_options
@click.pass_context
@click.option("-t", "--date", required=True, help="Timestamp")
def get_spectrum(
    ctx: click.Context, machine: str, point: str, pmode: str, date: str
) -> None:
    """
    Fetches the spectrum data for the specified machine, point, pmode and date,
    and saves it as a CSV file.

    Parameters
    ----------
    machine : str
        Machine tag.
    point : str
        Point tag.
    pmode : str
        Processing mode tag.
    date : str
        Datetime value in 'YYYY-MM-DDTHH:MM:SS' format in local time.
    """
    params = {
        "user": ctx.obj["USER"],
        "passw": ctx.obj["PASSW"],
        "host": ctx.obj["HOST"],
        "machine": machine,
        "point": point,
        "pmode": pmode,
        "date": date,
    }
    spectrum = Sp.from_api(params)
    filename = f"spectrum_{machine}_{point}_{pmode}_{date.replace(':', '-')}.csv"

    spectrum.save_to_csv(filename)
    click.echo(f"Spectrum data saved: output/reports/{filename}")


@main.command()
@common_options
@click.pass_context
@click.option("-t", "--date", required=True, help="Timestamp")
def plot_wave(
    ctx: click.Context, machine: str, point: str, pmode: str, date: str
) -> None:
    """
    Plots the waveform for the specified machine, point, pmode and date.

    Parameters
    ----------
    machine : str
        Machine tag.
    point : str
        Point tag.
    pmode : str
        Processing mode tag.
    date : str
        Datetime value in 'YYYY-MM-DDTHH:MM:SS' format in local time.
    """
    params = {
        "user": ctx.obj["USER"],
        "passw": ctx.obj["PASSW"],
        "host": ctx.obj["HOST"],
        "machine": machine,
        "point": point,
        "pmode": pmode,
        "date": date,
    }
    wave = Wf.from_api(params)
    filename = f"waveform_{machine}_{point}_{pmode}_{date.replace(':', '-')}"

    wave.plot_data(filename=filename)
    click.echo(f"Waveform plot saved: output/figures/{filename}.png")


@main.command()
@common_options
@click.pass_context
@click.option("-t", "--date", required=True, help="Timestamp")
def plot_spectrum(
    ctx: click.Context, machine: str, point: str, pmode: str, date: str
) -> None:
    """
    Plots the spectrum for the specified machine, point, pmode and date.

    Parameters
    ----------
    machine : str
        Machine tag.
    point : str
        Point tag.
    pmode : str
        Processing mode tag.
    date : str
        Datetime value in 'YYYY-MM-DDTHH:MM:SS' format in local time.
    """
    params = {
        "user": ctx.obj["USER"],
        "passw": ctx.obj["PASSW"],
        "host": ctx.obj["HOST"],
        "machine": machine,
        "point": point,
        "pmode": pmode,
        "date": date,
    }
    spectrum = Sp.from_api(params)
    filename = f"spectrum_{machine}_{point}_{pmode}_{date.replace(':', '-')}"

    spectrum.plot_data(filename=filename)
    click.echo(f"Spectrum plot saved: output/figures/{filename}.png")


if __name__ == "__main__":
    main()
