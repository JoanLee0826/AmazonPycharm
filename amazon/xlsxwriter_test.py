import xlsxwriter

f = xlsxwriter.Workbook("first.xlsx")

worksheet1 = f.add_worksheet()

worksheet1.insert_image("A2", 'data/pic/B00KTJIIFG.png',
                        {'x_scale':0.8}
                        )

worksheet1.insert_image("A3", 'data/pic/B00KTJIIFG.png',
                        {'x_scale':1}
                        )

f.close()



