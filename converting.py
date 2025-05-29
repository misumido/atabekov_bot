import pandas as pd
import sqlite3
import random
from datetime import date
# def convert_to_excel(table):
#     conn = sqlite3.connect('data.db')
#     df = pd.read_sql_query(f"SELECT * FROM {table}", conn)
#     conn.close()
#     name = f"{table}"+ str(date.today())+"_" + str(random.randint(1, 1000))
#     df.to_excel(f'{name}.xlsx', index=False)
#     return f'{name}.xlsx'
def convert_to_excel(table, max_rows=1048576):  # Максимальное количество строк в Excel
    # Подключение к базе данных
    conn = sqlite3.connect('data.db')
    # Проверяем общее количество строк
    count_query = f"SELECT COUNT(*) FROM {table}"
    total_rows = pd.read_sql_query(count_query, conn).iloc[0, 0]

    # Выбираем определенное количество строк
    query = f"""
    SELECT * FROM {table} 
    ORDER BY rowid 
    LIMIT {max_rows}
    """

    # Читаем данные
    df = pd.read_sql_query(query, conn)
    conn.close()

    # Генерируем уникальное имя файла
    name = f"{table}_{date.today()}_{random.randint(1, 1000)}.xlsx"

    # Сохраняем с оптимизацией
    with pd.ExcelWriter(name, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Data')

        # Получаем workbook и worksheet
        workbook = writer.book
        worksheet = writer.sheets['Data']

        # Автоматическая ширина столбцов
        for i, col in enumerate(df.columns):
            max_len = max(df[col].astype(str).map(len).max(), len(col)) + 2
            worksheet.set_column(i, i, max_len)

        # Дополнительная оптимизация
        workbook.close()

    # Добавляем информацию о количестве строк
    print(f"Exported {len(df)} rows out of {total_rows} total rows")

    return name
