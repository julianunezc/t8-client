"""
This script is a CLI client that interacts with the T8 API to manage waveform
and spectrum data.

This file contains the following functions:

    * list_waves - lists available waveform capture timestamps.
    * list_spectra - lists available spectrum capture timestamps.
    * get_wave - fetches and save waveform data to a CSV file.
    * get_spectrum - fetches and save spectrum data to a CSV file.
    * plot_wave - plots and save waveform data as a PNG image.
    * plot_spectrum - plots and save spectrum data as a PNG image.
"""

import os

import click

import t8_client.functions as fun
from t8_client.spectrum import Spectrum as sp
from t8_client.waveform import Waveform as wf


@click.group()
@click.option("-u", "--user", default=None, help="User to connect with")
@click.option("-p", "--passw", default=None, help="Password to connect with")
@click.option("-h", "--host", default=None, help="T8 host")
@click.pass_context
def main(ctx: click.Context, user: str | None, passw: str | None, host: str | None):
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

    ctx.ensure_object(dict)
    ctx.obj["USER"] = user
    ctx.obj["PASSW"] = passw
    ctx.obj["HOST"] = host


def common_options(f):
    """
    Decorator that adds the common options machine, point and pmode to subcommands.
    """
    f = click.option("-M", "--machine", required=True, help="Machine tag")(f)
    f = click.option("-p", "--point", required=True, help="Point tag")(f)
    f = click.option("-m", "--pmode", required=True, help="Processing mode tag")(f)
    return f


@main.command()
@common_options
@click.pass_context
def list_waves(ctx: click.Context, machine: str, point: str, pmode: str) -> list:
    """
    Lists the waveform capture dates for the specified machine, point and pmode
    in the format 'YYYY-MM-DDTHH:MM:SS'.

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
        A list of waveforms timestamps in the format 'YYYY-MM-DDTHH:MM:SS'.
    """
    url = f"http://{ctx.obj['HOST']}/rest/waves/{machine}/{point}/{pmode}"
    timestamps = fun.get_timestamps(url, ctx.obj["USER"], ctx.obj["PASSW"])
    for ts in timestamps:
        click.echo(ts)


@main.command()
@common_options
@click.pass_context
def list_spectra(ctx: click.Context, machine: str, point: str, pmode: str) -> list:
    """
    Lists the spectra capture dates for the specified machine, point and pmode
    in the format 'YYYY-MM-DDTHH:MM:SS'.

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
        A list of spectra timestamps in the format 'YYYY-MM-DDTHH:MM:SS'.
    """
    url = f"http://{ctx.obj['HOST']}/rest/spectra/{machine}/{point}/{pmode}"
    timestamps = fun.get_timestamps(url, ctx.obj["USER"], ctx.obj["PASSW"])
    for ts in timestamps:
        click.echo(ts)


@main.command()
@common_options
@click.pass_context
@click.option("-t", "--date", required=True, help="Timestamp")
def get_wave(ctx: click.Context, machine: str, point: str, pmode: str, date: str):
    """
    Gets the waveform data for the specified machine, point, pmode and date,
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
        Datetime value in 'YYYY-MM-DDTHH:MM:SS' format.
    """
    wave = wf.from_api(
        user=ctx.obj["USER"],
        passw=ctx.obj["PASSW"],
        host=ctx.obj["HOST"],
        machine=machine,
        point=point,
        pmode=pmode,
        date=date,
    )
    safe_datetime = date.replace(":", "-")
    filename = f"waveform_{machine}_{point}_{pmode}_{safe_datetime}.csv"

    wave.save_to_csv(filename)
    click.echo(f"Waveform data saved: output/reports/{filename}")


@main.command()
@common_options
@click.pass_context
@click.option("-t", "--date", required=True, help="Timestamp")
def get_spectrum(ctx: click.Context, machine: str, point: str, pmode: str, date: str):
    """
    Gets the spectrum data for the specified machine, point, pmode and date,
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
        Datetime value in 'YYYY-MM-DDTHH:MM:SS' format.
    """
    spectrum = sp.from_api(
        user=ctx.obj["USER"],
        passw=ctx.obj["PASSW"],
        host=ctx.obj["HOST"],
        machine=machine,
        point=point,
        pmode=pmode,
        date=date,
    )
    filename = f"spectrum_{machine}_{point}_{pmode}_{date.replace(':', '-')}.csv"

    spectrum.save_to_csv(filename)
    click.echo(f"Spectrum data saved: output/reports/{filename}")


@main.command()
@common_options
@click.pass_context
@click.option("-t", "--date", required=True, help="Timestamp")
def plot_wave(ctx: click.Context, machine: str, point: str, pmode: str, date: str):
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
        Datetime value in 'YYYY-MM-DDTHH:MM:SS' format.
    """
    wave = wf.from_api(
        user=ctx.obj["USER"],
        passw=ctx.obj["PASSW"],
        host=ctx.obj["HOST"],
        machine=machine,
        point=point,
        pmode=pmode,
        date=date,
    )
    filename = f"waveform_{machine}_{point}_{pmode}_{date.replace(':', '-')}"

    wave.plot_data(filename=filename)
    click.echo(f"Waveform plot saved: output/figures/{filename}.png")


@main.command()
@common_options
@click.pass_context
@click.option("-t", "--date", required=True, help="Timestamp")
def plot_spectrum(ctx: click.Context, machine: str, point: str, pmode: str, date: str):
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
        Datetime value in 'YYYY-MM-DDTHH:MM:SS' format.
    """
    spectrum = sp.from_api(
        user=ctx.obj["USER"],
        passw=ctx.obj["PASSW"],
        host=ctx.obj["HOST"],
        machine=machine,
        point=point,
        pmode=pmode,
        date=date,
    )
    filename = f"spectrum_{machine}_{point}_{pmode}_{date.replace(':', '-')}"

    spectrum.plot_data(filename=filename)
    click.echo(f"Spectrum plot saved: output/figures/{filename}.png")


if __name__ == "__main__":
    main()
