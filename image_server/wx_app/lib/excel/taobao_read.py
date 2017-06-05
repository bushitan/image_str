# -*- coding:utf-8 -*-

# import xlrd
# data = xlrd.open_workbook('1.xlsx') # 打开xls文件
# table = data.sheets()[0] # 打开第一张表
# nrows = table.nrows # 获取表的行数
# print nrows
#
# for i in range(nrows): # 循环逐行打印
# 	if i == 0: # 跳过第一行
# 		continue
# 	# print table.row_values(i)[1]
# 	# print table.row_values(i)[4]
# 	# print table.row_values(i)[6]
# 	print table.row_values(i)[17].split(u"减")[1]
# 	# print table.row_values(i)[20]
# # for i in range(nrows): # 循环逐行打印
# # 	if i == 0: # 跳过第一行
# # 		continue
# # 	category = table.row_values(i)[4] # 取前十三列
# # 	print category.split("/")[0]