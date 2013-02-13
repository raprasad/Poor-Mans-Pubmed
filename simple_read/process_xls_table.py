import xlrd
from pubmed_puller import pubmed_esearch, pubmed_efetch
from title_dict import TITLE_UPDATE_DICT
#sheet = book.sheet_by_name("qqqq") #we can pull by name
#sheet = book.sheet_by_index(0) #or by the index it has in excel's sheet collection

def msg(s): print s
def dashes():msg(40*'-')
def msgt(s): dashes(); msg(s); dashes()

#print sheet.col_values(0) 
def get_publication_title(citation):
    idx = citation.find('"')
    if idx==-1:
        return None
        
    end_idx = citation.find('"', idx+3)
    if end_idx == -1:
        return None

    title = citation[idx+1:end_idx ]
    if title.endswith(','):
        title = title[:-1]
    return title.strip()

TITLE_PUBMED_ID_FILE = 'title_pubmed_id.txt'
TITLE_DOI_ID_FILE = 'title_doi_id.txt'

def write_pubmed_id(title, pubmed_id):
    fh = open(TITLE_PUBMED_ID_FILE, 'a')
    fh.write('%s|%s\n' % (title, pubmed_id))
    fh.close()
    
def get_doi_title_lookup():
    """Used to not repeat searches"""
    lu = {}
    for line in open(TITLE_DOI_ID_FILE, 'r').readlines():
        id_parts = line.split('|')
        if len(id_parts) == 2:
            title = id_parts[0]
            doi_id = id_parts[1].strip()
            lu.update({ title:doi_id })
    return lu
    
    
def get_pubmed_title_lookup():
    """Used to not repeat searches"""
    lu = {}
    for line in open(TITLE_PUBMED_ID_FILE, 'r').readlines():
        id_parts = line.split('|')
        if len(id_parts) >= 2:
            title = id_parts[0]
            pubmed_id = id_parts[1].strip()
        if len(id_parts) >= 3:
            pmc_id = id_parts[2].strip()
            
        lu.update({ title:pubmed_id })
    return lu

def search_for_pubmed_id(title):
    return pubmed_esearch(title)

def get_pubmed_article_info():
    title_lookup = get_pubmed_title_lookup()
    cnt =0
    for pubmed_id in title_lookup.values():
        cnt+=1
        print '(%s) Retrieve article: %s' % (cnt, pubmed_id )
        pubmed_efetch(pubmed_id)
        #if cnt==5:  break
        #print pubmed_id
    #pubmed_efetch

#tdict = { 'A New Family of Candidate Pheromone Receptors in Mammals': 'A novel family of candidate pheromone receptors in mammals'}
def translate_title(title):
    if title is None:
        return None
    
    if TITLE_UPDATE_DICT.get(title, None) is not None:
        return TITLE_UPDATE_DICT.get(title)
    
    return title
    

def process_xls_sheet():
    book = xlrd.open_workbook("../last_grant/Table-6sf-2002-onwards.xls") #Table-6sf-working.xls") #open our xls file, there's lots of extra      
    sheet = book.sheets()[0] #book.sheets() returns a list of sheet objects... alternatively...
    cnt =0
    title_not_found_cnt =0
    no_pubs_cnt =0
    lookup_fail_cnt = []
    pubmed_lookup_success_cnt =0
    doi_lookup_success = []
    title_lookup = get_pubmed_title_lookup()
    doi_lookup = get_doi_title_lookup()
    
    for row_idx in range(4, 585):   #827):
        row_values = sheet.row(row_idx)
        
        if len(row_values) == 3:
            trainee, mentor, publication = row_values
            cnt+=1
            msgt('(%s) %s' % (cnt, publication.value))
        else:
            continue
            
        if publication.value == 'No Publications':
            print 'no publications'
            no_pubs_cnt +=1
            continue
            
        #print dir(publication)
        #print publication.value
        #print ''
        title = get_publication_title(publication.value)
        if title is None:
            title_not_found_cnt +=1
            print 'title not found cnt: (%s)' % (title_not_found_cnt)
                
        else:
            title = translate_title(title)

            print 'xls title: [%s]' % title
            # Do we already have the pubmed
            if title_lookup.get(title, None) is not None:
                print 'Have pubmed: %s' % title_lookup.get(title)
                pubmed_lookup_success_cnt+=1
                continue
            
            if doi_lookup.get(title, None) is not None:
                print 'Have DOI: %s' % doi_lookup.get(title)
                doi_lookup_success.append(title)
                continue
            
            pubmed_id = search_for_pubmed_id(title)
            if pubmed_id is not None:
                print 'pubmed id found!: %s' % pubmed_id
                pubmed_lookup_success_cnt+=1
                #print '(%s) %s %s'  % (cnt, title, pubmed_id)
                write_pubmed_id(title, pubmed_id)
            else:
                lookup_fail_cnt.append(title)
                print 'Pubmed search failed'
    
    msgt('Failed lookups')
    for fc in lookup_fail_cnt:
        print fc

    dashes(); dashes()
    print 'Total valid lines: %s' %  cnt
    print 'No publications: %s' %  no_pubs_cnt
    print 'Title not found: %s' %  title_not_found_cnt
    print 'Pubmed lookup fail: %s' %  len(lookup_fail_cnt)
    print 'Pubmed lookup SUCCESS: %s' %  pubmed_lookup_success_cnt
    print 'DOI lookup SUCCESS: %s' % len(doi_lookup_success)
    
                
if __name__=='__main__':
    process_xls_sheet()
    #get_pubmed_article_info()
#r = sheet.row(0) #returns all the CELLS of row 0,
#c = sheet.col_values(0) #returns all the VALUES of row 0,
 
#data = [] #make a data store
#for i in xrange(sheet.nrows):
#  data.append(sheet.row_values(i)) #drop all the values in the rows into data