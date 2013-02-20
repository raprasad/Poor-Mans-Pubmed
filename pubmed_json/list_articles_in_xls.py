import xlwt
from xlwt import easyxf
from xls_styles import *
import os, sys
from os.path import join, getsize
from format_article import ArticleFormatter

def write_article_list(xls_fname, article_dir):
    
    #for f in os.listdir(article_dir):
    #    is f.endswith()
    cnt =0 
    outlines = []
    for root, dirs, files in os.walk(article_dir):
        for f in files:
            if f.startswith('json') and f.endswith('.txt'):
                cnt+=1
                fname = os.path.join(root, f)
                af = ArticleFormatter.get_formatter_with_json_file(json_fname=fname)
                print af.get_t32_citation()
                print '(%s) %s %s' % (cnt, af.article_year, af.title)
                print fname
                fmt_line = '%s|%s|%s|%s' % (af.article_year.strip(), af.pmid, af.title.strip(), af.citation.strip())
                outlines.append(fmt_line)

    #print '\n'.join(outlines)
    #fh = open('sanes_pubs.txt', 'a')
    
    book = xlwt.Workbook(encoding="utf-8")
    sheet1 = book.add_sheet('Sanes Lab')
    row_num = 0

    sheet1.write(row_num, 0, 'Year', style_header)
    sheet1.write(row_num, 1, 'PMID', style_header)
    sheet1.write(row_num, 2, 'Title', style_header)
    sheet1.write(row_num, 3, 'Citation', style_header)
    
    for line in outlines:
        row_num+=1
        #fh.write(line+ '\n')
        yr, pmid, title, citation = line.split('|')
        sheet1.write(row_num, 0, yr , style_info_cell)   # 
        sheet1.write(row_num, 1, pmid , style_info_cell)   # 
        sheet1.write(row_num, 2, title , style_info_cell)   # 
        sheet1.write(row_num, 3, citation , style_info_cell)   # 
    book.save('sanes_publications.xls')
    #.write('\n'.join(outlines))
    
            #break
    #    break
    #    
    #    print(root, "consumes", end=" ")
    #    print(sum(getsize(join(root, name)) for name in files), end=" ")
    #    print("bytes in", len(files), "non-directory files")
    #    if 'CVS' in dirs:
    #        dirs.remove('CVS')  # don't visit CVS directories

if __name__=='__main__':
    write_article_list(xls_fname='article_list.xls', article_dir='sanes_pubs')