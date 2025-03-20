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
    user, password, host, *_ = fun.load_env_variables()

    ctx.obj["USER"] = user
    ctx.obj["PASSWORD"] = password
    ctx.obj["HOST"] = host


if __name__ == "__main__":
    cli()
