from rich.table import Table, Style, box
from rich.text import Text


def get_table_for_result(cost, caption='Результат') -> Table:
    tb = Table(show_header=True, show_footer=True, header_style='bold magenta', caption=caption)
    tb.add_column('№', style='dim')
    tb.add_column('Статус')
    tb.add_column('Получатель')
    tb.add_column('Отправитель', Text.from_markup("[b]Всего", justify="right"))
    tb.add_column('Цена', Text.from_markup(str(cost)))


    return tb
