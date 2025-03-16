import pandas as pd
from scipy import stats
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats

# Загрузка и просмотр данных
file_path = r'C:\Users\user\Desktop\project-ab\marketpele_ab_test.xlsx' # загружаем данные из файла Excel
data = pd.read_excel(file_path)

# Предварительная обработка данных
print("\nКоличество пропусков данных в каждом столбце:") 
print(data.isnull().sum())  # проверяем, сколько пропусков в каждом столбце
print("\nКоличество дубликатов данных:")
print(data.duplicated().sum())  # проверяем, сколько дубликатов в данных

data = data.drop_duplicates() # удаляем дубликаты данных (если они есть)

if 'date' in data.columns:
    data['date'] = pd.to_datetime(data['date']) # преобразуем столбец с датой в формат datetime

print("\nПроверка данных после очистки:") # проверяем данные после очистки
print(data.head())

# Промежуточный вывод
print("\nДанные загружены и очищены. Добавлены расчетные метрики: Paid CTR, Organic CTR, RPM, RPS, Views per session")

# Вычисление метрик
data['paid_ctr'] = data['sponsord_clicks'] / data['pageviews'] # вычисляем Paid CTR (Sponsored Click-Through Rate)

data['organic_ctr'] = data['organic_clicks'] / data['pageviews'] # вычисляем Organic CTR (Organic Click-Through Rate)

data['rpm'] = (data['revenue'] / data['pageviews']) * 1000 # вычисляем RPM (Revenue per Mille)

data['rps'] = (data['revenue'] / data['sessions']) * 1000 # вычисляем RPS (Revenue per Session)

data['views_per_session'] = data['pageviews'] / data['sessions'] # вычисляем количество просмотров за сессию

print("\nРасчет метрик:")
print(data[['paid_ctr', 'organic_ctr', 'rpm', 'rps', 'views_per_session']].head())

# Сравнительный анализ
grouped_data = data.groupby('group_name').agg({
    'paid_ctr': 'mean',
    'organic_ctr': 'mean',
    'rpm': 'mean',
    'rps': 'mean',
    'views_per_session': 'mean'
}).reset_index() # делаем группировку по 'group_name' и вычисляем средние значения для каждой группы

print("\nРасчет средних значений для каждой группы:")
print(grouped_data)

# Статистическая проверка (t-тест)
group_a = data[data['group_name'] == 'A'] # разделяем данные на группы A и B
group_b = data[data['group_name'] == 'B']

def perform_t_test(group_a, group_b, metric): # Функция для выполнения t-теста и вывода результатов
    t_stat, p_value = stats.ttest_ind(group_a[metric], group_b[metric], nan_policy='omit')
    return t_stat, p_value 

# Визуализация распределения метрик по группам
metrics = ['paid_ctr', 'organic_ctr', 'rpm', 'rps', 'views_per_session']

plt.figure(figsize=(15, 10))
for i, metric in enumerate(metrics, 1):
    plt.subplot(2, 3, i)
    sns.boxplot(x='group_name', y=metric, data=data, hue='group_name', palette='Set2', legend=False)
    plt.title(f'Распределение {metric} по группам A и B')
    plt.xlabel("Группа") # добавляем заголовок для оси X
plt.tight_layout()
plt.show()

# Промежуточный вывод
print("\nВизуальный анализ: по Organic CTR видно снижение в группе B. Остальные метрики не демонстрируют явных отличий")

# Выполняем t-тест для каждой метрики
metrics = ['paid_ctr', 'organic_ctr', 'rpm', 'rps', 'views_per_session']
for metric in metrics:
    t_stat, p_value = perform_t_test(group_a, group_b, metric)
    print(f"\n📊 Тест для метрики {metric}:")
    print(f"T-статистика: {t_stat:.4f}, P-значение: {p_value:.4f}")
    
    # Проверим, является ли результат статистически значимым (p < 0.05)
    if p_value < 0.05:
        print(f"✅ Результат статистически значим. Различия между группами по {metric} существуют")
    else:
        print(f"❌ Результат не статистически значим. Различий между группами по {metric} нет")

print("\nИтог по t-тестам: единственная метрика с существенными различиями — Organic CTR (значимое снижение в группе B)\n")

# Формулировка гипотез
# Гипотеза 1: Размещение органических элементов в верхней части списка увеличит количество кликов по ним (повышение Organic CTR)
#Обоснование: Платформа будет более ориентирована на органический контент, что стимулирует пользователей к кликам по органическим элементам
#Гипотеза 2: Размещение платных элементов в верхней части списка увеличит количество кликов по ним (повышение Paid CTR)
#Обоснование: Платные элементы, размещенные в верхней части списка, привлекут больше внимания пользователей, что приведет к увеличению кликов по ним
#Гипотеза 3: Снижение числа платных элементов в ленте улучшит качество пользовательского опыта и повысит количество просмотров за сессию (Views per session)
#Обоснование: Если рекламные блоки будут менее навязчивыми, пользователи смогут просматривать больше страниц, что увеличит время, проведенное на платформе
#Гипотеза 4: Изменение порядка показов элементов (например, перемещение органического контента в верхнюю часть списка) повысит количество кликов по органическим элементам и улучшит Organic CTR
#Обоснование: Пользователи могут быть более заинтересованы в органическом контенте, если он будет представлен на более видных позициях
#Гипотеза 5: Увеличение видимости платных элементов в ленте приведет к росту дохода (RPM и RPS)
#Обоснование: Большее количество кликов по платным элементам может напрямую увеличить доход на 1000 просмотров и сессий
#Гипотеза 6: Использование более персонализированных рекламных предложений для пользователей увеличит их вовлеченность и повысит Paid CTR
#Обоснование: Персонализированные рекламные блоки могут повысить вероятность кликов, так как они будут более релевантны интересам пользователей
#Гипотеза 7: Размещение платных и органических элементов в случайном порядке повысит общее количество кликов, равномерно распределив внимание пользователей между различными типами контента
#Обоснование: Случайное размещение может создать эффект неожиданности и повысить интерес пользователей как к платным, так и к органическим элементам

import pandas as pd

# Данные по гипотезам RICE: Reach, Impact, Confidence, Effort
data = {
    'Hypothesis': [
        'Гипотеза 1: Размещение органических элементов в верхней части списка увеличит количество кликов по ним (повышение Organic CTR)',
        'Гипотеза 2: Размещение платных элементов в верхней части списка увеличит количество кликов по ним (повышение Paid CTR)',
        'Гипотеза 3: Снижение числа платных элементов улучшит просмотры за сессию',
        'Гипотеза 4: Изменение порядка показов элементов повысит клики по органическим элементам',
        'Гипотеза 5: Увеличение видимости платных элементов повысит доход (RPM, RPS)',
        'Гипотеза 6: Персонализированные рекламные предложения увеличат Paid CTR',
        'Гипотеза 7: Случайное размещение элементов повысит клики по платным и органическим элементам'
    ],
    'Reach': [8, 7, 6, 7, 9, 8, 6],
    'Impact': [7, 6, 5, 6, 8, 7, 5],
    'Confidence': [7, 8, 6, 7, 6, 9, 5],
    'Effort': [4, 3, 6, 5, 7, 6, 4]
}

df = pd.DataFrame(data) # создаем dataframe

df['RICE'] = (df['Reach'] * df['Impact'] * df['Confidence']) / df['Effort'] # рассчитываем RICE-оценку

df_sorted = df.sort_values(by='RICE', ascending=False) # делаем сортировку по RICE

print(df_sorted[['Hypothesis', 'RICE']]) # выводим результаты
print("\nВыбираем для тестирования следующие гипотезы:")
print(df_sorted[['Hypothesis', 'RICE']].head(2))  # выводим первые две строки

# Вывод: выбрали гипотезу 1 и 2

#Гипотеза 1: Размещение органических элементов в верхней части списка увеличит количество кликов по ним (повышение Organic CTR)
#H0: средний Organic CTR в группах A и B не различается
#H1: средний Organic CTR в группах A и B различается

t_stat, p_value = stats.ttest_ind(group_a['organic_ctr'], group_b['organic_ctr'], nan_policy='omit')

print("\n Проведем тестирование гипотез:")

print("\n📊 Гипотеза 1: Размещение органических элементов в верхней части списка увеличит Organic CTR")
print("H0: средний Organic CTR в группах A и B не различается")
print("H1: средний Organic CTR в группах A и B различается")
print(f"T-статистика: {t_stat:.4f}")
print(f"P-значение: {p_value:.4f}")

if p_value < 0.05:
    print("🚨 Отклоняем H₀: изменение размещения органических элементов значимо повлияло на Organic CTR")
else:
    print("✅ Не отклоняем H₀: различий в Organic CTR нет")

# Визуализация Organic CTR по группам
plt.figure(figsize=(8, 5))
sns.histplot(group_a['organic_ctr'], label="Группа A", kde=True, color="blue", alpha=0.6)
sns.histplot(group_b['organic_ctr'], label="Группа B", kde=True, color="red", alpha=0.6)
plt.legend()
plt.title("Распределение Organic CTR по группам")
plt.show()

#Гипотеза 2: Размещение платных элементов в верхней части списка увеличит количество кликов по ним (повышение Paid CTR)
#H0: средний Paid CTR в группах A и B не различается
#H1: средний Paid CTR в группах A и B различается

t_stat, p_value = stats.ttest_ind(group_a['paid_ctr'], group_b['paid_ctr'], nan_policy='omit')

print("\n📊 Гипотеза 2: Размещение платных элементов в верхней части списка увеличит Paid CTR")
print("H0: средний Paid CTR в группах A и B не различается")
print("H1: средний Paid CTR в группах A и B различается")
print(f"T-статистика: {t_stat:.4f}")
print(f"P-значение: {p_value:.4f}")

if p_value < 0.05:
    print("🚨 Отклоняем H₀: изменение размещения платных элементов значимо повлияло на Paid CTR")
else:
    print("✅ Не отклоняем H₀: различий в Paid CTR нет")

# Визуализация Paid CTR по группам
plt.figure(figsize=(8, 5))
sns.histplot(group_a['paid_ctr'], label="Группа A", kde=True, color="blue", alpha=0.6)
sns.histplot(group_b['paid_ctr'], label="Группа B", kde=True, color="red", alpha=0.6)
plt.legend()
plt.title("Распределение Paid CTR по группам")
plt.show()

# Итоговое сообщение
print("\nВывод: проверка гипотез показала, влияет ли размещение органических и платных элементов в верхней части списка на их кликабельность")

