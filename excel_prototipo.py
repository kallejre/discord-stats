# Excel protipo
# Eesmärk genereerida automaatselt värviskaala.

import xlsxwriter

class xlsx:
    def __init__(self, fname='stats.xlsx'):
        self.excel=xlsxwriter.Workbook(fname)
        self.sheets=[]
        self.current_sheet=None
        self.row=None
        self.col=None
    def ws(self,name):
        """Lisab uue töölehe ja muudab aktiivseks."""
        self.current_sheet = self.excel.add_worksheet(name)
        self.sheets.append(self.current_sheet)
        self.row=0
        self.col=0
    def write(self,line):
        """Lisa \t-ga eraldatud rida faili nagu kleebiks tavalisse exceli tabelisse."""
        if line=='\n': return
        # print([line])
        lines=line.rstrip('\n').split('\n')
        for line in lines:
            self.col=0
            for cell in line.split('\t'):
                try: self.current_sheet.write(self.row, self.col,float(cell))
                except ValueError: self.current_sheet.write(self.row, self.col,cell)
                self.col+=1
            self.row+=1
    def close(self):
        self.excel.close()

data='''6\t11\t4\t4\t4\t11\t0\t7\t7\t11\t7\t11\t1\t11\t14\t5\t11\t
13\t11\t5\t1\t2\t4\t11\t6\t4\t10\t8\t14\t2\t8\t0\t7\t8\t
4\t7\t1\t4\t13\t8\t0\t4\t4\t5\t10\t8\t10\t2\t9\t0\t2\t
4\t10\t7\t10\t2\t11\t0\t11\t8\t11\t1\t1\t8\t3\t8\t14\t5\t
3\t4\t13\t4\t4\t6\t5\t7\t5\t9\t6\t1\t11\t5\t9\t11\t11\t
7\t8\t2\t7\t4\t5\t5\t4\t12\t5\t6\t8\t2\t10\t13\t6\t4\t
14\t14\t5\t3\t13\t11\t2\t12\t13\t7\t14\t14\t5\t9\t6\t14\t7\t
12\t1\t8\t10\t13\t0\t13\t5\t12\t3\t5\t1\t1\t8\t13\t13\t0\t
14\t5\t13\t9\t9\t7\t6\t3\t3\t2\t5\t8\t7\t12\t11\t10\t13\t
11\t8\t3\t2\t0\t2\t9\t6\t1\t13\t0\t10\t7\t2\t10\t13\t7\t
10\t13\t9\t7\t11\t0\t13\t13\t3\t12\t14\t1\t9\t9\t0\t5\t11\t
4\t2\t12\t6\t1\t1\t4\t6\t14\t1\t6\t5\t1\t5\t8\t2\t14\t
3\t0\t5\t6\t2\t13\t4\t14\t1\t8\t6\t4\t12\t7\t4\t4\t14\t
4\t9\t2\t13\t14\t10\t5\t14\t11\t0\t8\t1\t7\t12\t14\t6\t1\t
0\t5\t5\t10\t8\t1\t6\t6\t12\t8\t4\t13\t0\t7\t5\t11\t9\t
14\t6\t5\t8\t5\t13\t2\t3\t12\t5\t12\t11\t11\t13\t9\t3\t1\t
9\t10\t1\t7\t2\t11\t8\t3\t2\t1\t13\t1\t9\t1\t6\t5\t7\t
1\t9\t8\t10\t6\t12\t12\t6\t0\t4\t9\t5\t3\t9\t12\t8\t12\t
14\t12\t3\t9\t4\t3\t3\t10\t6\t14\t8\t0\t0\t14\t1\t11\t14\t
12\t13\t5\t10\t0\t10\t4\t2\t10\t1\t14\t2\t8\t2\t14\t14\t10\t
9\t6\t3\t10\t8\t10\t9\t14\t0\t10\t2\t7\t14\t13\t3\t1\t11\t
6\t1\t14\t10\t8\t10\t12\t0\t4\t12\t14\t1\t2\t11\t13\t5\t12\t
10\t12\t6\t10\t1\t0\t6\t0\t6\t8\t9\t4\t10\t8\t6\t2\t10\t
13\t1\t4\t12\t13\t4\t13\t12\t12\t11\t10\t11\t8\t6\t10\t10\t5\t
10\t9\t14\t12\t4\t1\t3\t6\t2\t5\t6\t1\t13\t9\t14\t8\t14\t'''
excel=xlsx('proto.xlsx')
excel.ws('Pikkused')
excel.write(data)
def colnum_string(n):
    string = ""
    while n > 0:
        n, remainder = divmod(n - 1, 26)
        string = chr(65 + remainder) + string
    return string
excel.current_sheet.conditional_format('A1:Q25', {'type': '2_color_scale',
                                                  'min_color': '#FFFFFF',
                                                  'max_color': '#63BE7B'})

# Kui natuke optimeerida, saab hakata genereerima aktiivsustabeleid.
column=excel.col
col2=colnum_string(excel.col-1)

rows=[]
locs=[]
for row in range(1,excel.row+1):
    st='A'+str(row)+':'+col2+str(row)
    print(st)
    rows.append(st)
    locs.append(colnum_string(excel.col)+str(row))
excel.current_sheet.add_sparkline(locs[0], {'location': locs,  'type': 'column', 'range': rows,'max': 'group','min': 'group'})
# TODO: Lisada vertikaalsed jooned.

# Seejärel optimeerida aktiivsustabelite koostamisele.
# $R$1:$R$25
excel.current_sheet
excel.close()
