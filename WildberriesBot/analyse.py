import glob
import pandas
import xlsxwriter
import numpy


list_niches = glob.glob(r'.\Niches\*.xlsx')
list_niches = [i[(i.index('Niches')+7):i.index('.xlsx')] for i in list_niches]

workbook = xlsxwriter.Workbook(f'Analyze.xlsx')
worksheet_info = workbook.add_worksheet('Analyze of niche')
bold_orange_right = workbook.add_format({'bold': True, 'align': 'right', 'bg_color': '#F7B879', 'border': 1})
bold_orange_left = workbook.add_format({'bold': True, 'bg_color': '#F7B879', 'border': 1})
bold = workbook.add_format({'bold': True, 'border': 1})
right = workbook.add_format({'align': 'right', 'border': 1})
bold_right = workbook.add_format({'bold': True, 'align': 'right', 'border': 1})
bold_right_percent = workbook.add_format({'bold': True, 'align': 'right', 'border': 1})
bold_right_percent.set_num_format(10)
border = workbook.add_format({'border': 1})
right_ruble = workbook.add_format({'align': 'right', 'border': 1})
right_ruble.set_num_format(7)
bold_right_ruble = workbook.add_format({'bold': True, 'align': 'right', 'border': 1})
bold_right_ruble.set_num_format(7)
italic_pink = workbook.add_format({'italic': True, 'align': 'center', 'bg_color': '#EDA9A9', 'border': 1})
italic_green = workbook.add_format({'italic': True, 'align': 'center', 'bg_color': '#ACD19F', 'border': 1})
italic_blue = workbook.add_format({'italic': True, 'align': 'center', 'bg_color': '#97B7F1', 'border': 1})

worksheet_info.write('A1', 'Ниша:  ', bold_orange_right)
worksheet_info.write('A2', 'Спрос', italic_pink)
worksheet_info.write('A3', 'Объём рынка', border)
worksheet_info.write('A4', 'Объём упущенной выручки', border)
worksheet_info.write('A5', 'Итоговый потенциал рынка', bold)
worksheet_info.write('A6', 'Ср. выручка на поставщика в топ 30', border)
worksheet_info.write('A7', 'Ср. выручка на всех поставщиков', bold)
worksheet_info.write('A8', 'Маржинальность (доходность)', italic_green)
worksheet_info.write('A9', 'Ср. цена продажи на WB', border)
worksheet_info.write('A10', 'Найденная себестоимость', border)
worksheet_info.write('A11', 'Планируемая маржинальность', bold)
worksheet_info.write('A12', 'Уровень конкуренции', italic_blue)
worksheet_info.write('A13', 'Выручка топ 30 поставщиков', border)
worksheet_info.write('A14', 'Доля выручки топ 30 поставщиков от всего объёма продаж', bold)
worksheet_info.write('A15', 'Сколько поставщиков сохранено', border)
worksheet_info.write('A16', 'Кол-во позиций в нише', bold)
worksheet_info.write('A17', 'Среднее кол-во отзывов на 1 товаре', bold)
worksheet_info.write('A18', 'Средний рейтинг', bold)

i = 1
for niche in list_niches:
	sheet_main = pandas.read_excel(f'.\\Niches\\{niche}.xlsx', sheet_name='Data of niche', usecols=['Name of product', 'Articul', 'Brand', 'Manufacturer', 'Rating', 'Amount of feedbacks', 'Averaged price', 'Lost profit', 'Profit'])
	sheet_extra = pandas.read_excel(f'.\\Niches\\{niche}.xlsx', sheet_name='Data of niche', usecols=['Unic manufacturer', 'Summary profit', 'Percentage of niche']).dropna()
	worksheet_info.write(0, i, niche, bold_orange_left)
	worksheet_info.write(1, i, '', italic_pink)
	worksheet_info.write(2, i, sheet_main['Profit'].sum(), right_ruble)
	worksheet_info.write(3, i, sheet_main['Lost profit'].sum(), right_ruble)
	worksheet_info.write(4, i, sheet_main['Profit'].sum()+sheet_main['Lost profit'].sum(), bold_right_ruble)
	worksheet_info.write(5, i, sum(list(reversed(sorted(sheet_extra['Summary profit'].tolist())))[:30])//min(30, len(sheet_extra.index)), right_ruble)
	worksheet_info.write(6, i, sheet_extra['Summary profit'].mean(), bold_right_ruble)
	worksheet_info.write(7, i, '', italic_green)
	worksheet_info.write(8, i, sheet_main['Averaged price'].mean(), right_ruble)
	worksheet_info.write(9, i, '', border)
	worksheet_info.write(10, i, '', border)
	worksheet_info.write(11, i, '', italic_blue)
	worksheet_info.write(12, i, sum(list(reversed(sorted(sheet_extra['Summary profit'].tolist())))[:30]), right_ruble)
	worksheet_info.write(13, i, sum(list(reversed(sorted(sheet_extra['Percentage of niche'].tolist())))[:30]), bold_right_percent)
	worksheet_info.write(14, i, len(sheet_extra.index), right)
	worksheet_info.write(15, i, '', border)
	feedbacks = sheet_main['Amount of feedbacks'].tolist()
	ratings_list = sheet_main['Rating'].tolist()
	ratings = []
	for j in range(len(feedbacks)):
		if feedbacks[j] != 0:
			ratings.append(ratings_list[j])
	worksheet_info.write(16, i, round(numpy.mean(list(filter((0).__ne__, feedbacks)))), bold_right)
	worksheet_info.write(17, i, round(numpy.mean(ratings), 1), bold_right)
	worksheet_info.set_column(i, i, max(18, len(niche)+3))
	i += 1

worksheet_info.set_column('A:A', 60)
workbook.close()

