import click

import t8_client.functions as fun
from t8_client.waveform import Waveform


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


@cli.command()
@click.option("-M", "--machine", required=True, help="Machine name.")
@click.option("-p", "--point", required=True, help="Point name.")
@click.option("-m", "--pmode", required=True, help="Pmode value.")
@click.pass_context
def list_waves(ctx, machine, point, pmode):
    """Lists the waveform capture dates for the specified machine, point, and pmode."""
    timestamps = Waveform.get_waves_timestamps(machine, point, pmode)

    for ts in timestamps:
        formatted_ts = fun.get_str_from_unix_timestamp(int(ts))
        click.echo(formatted_ts)


if __name__ == "__main__":
    cli()
