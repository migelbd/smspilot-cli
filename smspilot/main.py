import os
from typing import KeysView
from rich import print, pretty
import click
import profig
from rich.console import Console
from sms_pilot import SmsPilot
from sms_pilot.exception import SmsPilotAPIError
from sms_pilot.objects import Message

from smspilot.tables import get_table_for_result
from smspilot.utils import get_row_data
from . import __version__


console = Console()
pretty.install(console)
HOME_PATH = os.getenv('USERPROFILE')
CFG_PATH = os.path.join(HOME_PATH, '.smspilot.cfg')
cfg = profig.Config(CFG_PATH, encoding='utf-8')
cfg.init('api.key', 'XXXXXXXXXXXXYYYYYYYYYYYYZZZZZZZZXXXXXXXXXXXXYYYYYYYYYYYYZZZZZZZZ')
cfg.init('api.default_sender', 'INFORM')


@click.group('SmsPilotCli', help=f'SmsPilot CLI version {".".join(map(str, __version__))}')
@click.pass_context
def cli(ctx):
    ctx.ensure_object(dict)
    ctx.obj['api'] = SmsPilot(cfg['api.key'], default_sender=cfg['api.default_sender'])


@cli.command('send', help='Send message')
@click.argument('phone')
@click.argument('message')
@click.option('-s', '--sender', 'sender', help='Sender. If not set, using default')
@click.pass_context
def send_message(ctx, phone, message, sender):
    api: SmsPilot = ctx.obj['api']

    response = api.send_message(
        to=phone,
        text=message,
        sender=sender
    )
    fields_data = (
        'id',
        'get_status_verbose',
        'to',
        'sender',
        'price',
    )
    tb = get_table_for_result(response.cost)
    for msg in response.raw_send:
        tb.add_row(*get_row_data(msg, fields_data))
    console.print(tb)


@cli.command('sends', help='Send message')
@click.argument('input', type=click.File('rb'))
@click.pass_context
def send_messages(ctx, input):
    api: SmsPilot = ctx.obj['api']
    click.echo(input.read())
    # response = api.send_message(
    #     to=phone,
    #     text=message,
    #     sender=sender
    # )
    # fields_data = (
    #     'id',
    #     'get_status_verbose',
    #     'to',
    #     'sender',
    #     'price',
    # )
    # tb = get_table_for_result(response.cost)
    # for msg in response.raw_send:
    #     tb.add_row(*get_row_data(msg, fields_data))
    # console.print(tb)


@cli.command('balance', help='Get balance')
@click.option('-c', '--count', 'as_count', help='As count', is_flag=True, default=False)
@click.option('--raw', 'raw_response', help='Raw response', is_flag=True, default=False)
@click.pass_context
def get_balance(ctx, as_count, raw_response):
    api: SmsPilot = ctx.obj['api']
    balance = api.get_balance(in_rur=not as_count)
    if raw_response:
        click.echo(balance)
    else:
        click.echo('Баланс: %s' % balance)


@cli.command('auth', help='Авторизация с помощью API ключа smspilot.ru')
@click.argument('api_key')
@click.pass_context
def auth(ctx, api_key):
    try:
        api: SmsPilot = SmsPilot(api_key, default_sender=cfg['api.default_sender'])
        user_info = api.user_info()
        print('[b]Авторизация успешна[/b]')
        print('Имя', user_info.name)
        print('Баланс', user_info.balance)
        cfg.update({'api.key': str(api_key).strip(), 'api.default_sender': user_info.default_sender})
        cfg.sync()
        print('[b]Ключ сохранен в настройках[/b]')
        print(cfg.sources)
    except SmsPilotAPIError as e:
        console.print(str(e), style='bold red')


@cli.group('config', invoke_without_command=True)
@click.pass_context
def config(ctx):
    if ctx.invoked_subcommand is None:
        print('[b]Текущие настройки[/b]')
        for cfg_key, cfg_value in cfg.as_dict(flat=True).items():
            print('[b]%s[/b]: %s' % (cfg_key, cfg_value))


@config.command('reset')
def reset_config():
    cfg.reset(clean=False)
    cfg.sync()
    print('[b]Настройки установлены по умолчанию[/b]')


@config.command('set')
@click.argument('param_key')
@click.argument('param_value')
def set_config(param_key=None, param_value=None):
    keys_v = list(cfg.keys())
    if param_key not in keys_v:
        console.print('Не верный параметр %s' % param_key, style='bold red')
        return

    cfg.update({param_key: param_value})
    cfg.sync()
    print(cfg.as_dict())
    console.print('[b]Настройки сохранены[/b]', style='green')


def main():
    cfg.sync()
    cli(obj={})


if __name__ == '__main__':
    main()
