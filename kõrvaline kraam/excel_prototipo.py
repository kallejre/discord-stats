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

data1='''6\t11\t4\t4\t4\t11\t0\t7\t7\t11\t7\t11\t1\t11\t14\t5\t11
13\t11\t5\t1\t2\t4\t11\t6\t4\t10\t8\t14\t2\t8\t0\t7\t8
4\t7\t1\t4\t13\t8\t0\t4\t4\t5\t10\t8\t10\t2\t9\t0\t2
4\t10\t7\t10\t2\t11\t0\t11\t8\t11\t1\t1\t8\t3\t8\t14\t5
3\t4\t13\t4\t4\t6\t5\t7\t5\t9\t6\t1\t11\t5\t9\t11\t11
7\t8\t2\t7\t4\t5\t5\t4\t12\t5\t6\t8\t2\t10\t13\t6\t4
14\t14\t5\t3\t13\t11\t2\t12\t13\t7\t14\t14\t5\t9\t6\t14\t7
12\t1\t8\t10\t13\t0\t13\t5\t12\t3\t5\t1\t1\t8\t13\t13\t0
14\t5\t13\t9\t9\t7\t6\t3\t3\t2\t5\t8\t7\t12\t11\t10\t13
11\t8\t3\t2\t0\t2\t9\t6\t1\t13\t0\t10\t7\t2\t10\t13\t7
10\t13\t9\t7\t11\t0\t13\t13\t3\t12\t14\t1\t9\t9\t0\t5\t11
4\t2\t12\t6\t1\t1\t4\t6\t14\t1\t6\t5\t1\t5\t8\t2\t14
3\t0\t5\t6\t2\t13\t4\t14\t1\t8\t6\t4\t12\t7\t4\t4\t14
4\t9\t2\t13\t14\t10\t5\t14\t11\t0\t8\t1\t7\t12\t14\t6\t1
0\t5\t5\t10\t8\t1\t6\t6\t12\t8\t4\t13\t0\t7\t5\t11\t9
14\t6\t5\t8\t5\t13\t2\t3\t12\t5\t12\t11\t11\t13\t9\t3\t1
9\t10\t1\t7\t2\t11\t8\t3\t2\t1\t13\t1\t9\t1\t6\t5\t7
1\t9\t8\t10\t6\t12\t12\t6\t0\t4\t9\t5\t3\t9\t12\t8\t12
14\t12\t3\t9\t4\t3\t3\t10\t6\t14\t8\t0\t0\t14\t1\t11\t14
12\t13\t5\t10\t0\t10\t4\t2\t10\t1\t14\t2\t8\t2\t14\t14\t10
9\t6\t3\t10\t8\t10\t9\t14\t0\t10\t2\t7\t14\t13\t3\t1\t11
6\t1\t14\t10\t8\t10\t12\t0\t4\t12\t14\t1\t2\t11\t13\t5\t12
10\t12\t6\t10\t1\t0\t6\t0\t6\t8\t9\t4\t10\t8\t6\t2\t10
13\t1\t4\t12\t13\t4\t13\t12\t12\t11\t10\t11\t8\t6\t10\t10\t5
10\t9\t14\t12\t4\t1\t3\t6\t2\t5\t6\t1\t13\t9\t14\t8\t14'''
data2='''Ago\tPäev\t0\t1\t2\t3\t4\t5\t6\t7\t8\t9\t10\t11\t12\t13\t14\t15\t16\t17\t18\t19\t20\t21\t22\t23
\tEsmasp.\t181\t104\t57\t55\t65\t79\t0\t14\t13\t45\t22\t89\t50\t90\t93\t103\t109\t88\t58\t69\t77\t99\t138\t212
\tTeisip.\t336\t82\t16\t5\t0\t1\t0\t11\t9\t39\t13\t71\t49\t73\t98\t128\t157\t89\t66\t103\t113\t149\t250\t477
\tKolmap.\t241\t47\t66\t65\t21\t2\t0\t14\t13\t50\t33\t75\t69\t130\t102\t196\t123\t165\t37\t124\t133\t88\t74\t234
\tNeljap.\t227\t102\t55\t66\t67\t1\t0\t16\t25\t54\t72\t54\t97\t84\t212\t106\t85\t78\t152\t89\t82\t175\t190\t342
\tReede\t82\t88\t87\t18\t4\t0\t3\t3\t19\t48\t39\t38\t74\t85\t78\t117\t132\t87\t53\t56\t85\t170\t95\t189
\tLaup.\t147\t223\t138\t25\t9\t0\t1\t1\t3\t25\t14\t44\t38\t51\t22\t26\t58\t19\t42\t93\t56\t9\t102\t141
\tPühap.\t86\t230\t239\t118\t121\t33\t0\t0\t0\t7\t18\t16\t47\t50\t48\t66\t28\t41\t72\t119\t45\t60\t102\t97'''

# Andete allikas:
# print(sts.ajatabel_vaiksem(2,'Kokku').replace('\t','\\t'))

def colnum_string(n):
    string = ""
    while n > 0:
        n, remainder = divmod(n - 1, 26)
        string = chr(65 + remainder) + string
    return string

excel=xlsx('proto.xlsx')
excel.ws('Pikkused')

def uus_funk(data):
    """Eeldame, et hakkame kirjutama aktiivsele lehele."""
    excel.write(data2)
    column=excel.col
    m23=colnum_string(column-23)
    p0=colnum_string(column)
    p1=colnum_string(column+1)
    x=m23+str(excel.row-6)+':'+p0+str(excel.row)
    rows=[]
    cols=[]
    locs=[]
    excel.current_sheet.conditional_format(x, {'type': '2_color_scale', 'min_color': '#FFFFFF', 'max_color': '#63BE7B'})
    for row in range(excel.row-6,excel.row+1):
        rows.append(m23+str(row)+':'+p0+str(row))
        locs.append(p1+str(row))
    excel.current_sheet.add_sparkline(locs[0], {'location': locs,  'type': 'column', 'range': rows,'max': 'group','min': 'group'})
    locs=[]
    for col in range(column-23,column+1):
        col_str=colnum_string(col)
        cols.append(col_str+str(row-6)+':'+col_str+str(row))
        locs.append(col_str+str(row+1))
    excel.current_sheet.add_sparkline(locs[0], {'location': locs,  'type': 'column', 'range': cols,'max': 'group','min': 'group'})

excel.close()
