def Version():
    version = [
        {
            'id': 1,
            'CAR_OWNER': 'CD21.1',
            'CRDS_OWNER': 'CD21.1',
            'STG_OWNER': 'CD21.1',
            'Instanse': 'PROD',
            'author': 'vorovik',
            'create_date': '03-01-2017'

        },
        {
            'id': 2,
            'CAR_OWNER': 'CD20.1',
            'CRDS_OWNER': 'CD20.1',
            'STG_OWNER': 'CD20.1',
            'Instanse': 'UAT',
            'author': 'vorovik',
            'create_date': '03-01-2017'
        }
    ]
    return version
a= Version()
b=a[-1].keys()
t = ((1, 'a'), (2, 'b'))
#d = dict(t)
#print(t[0:1])
#for b in a[-1].keys():
    #print (b)
#for c in b:
#    print (c)
#print (a[-1].keys())

abra={'id': 2, 'title': 'тест', 'cost': 223, 'year': 2018, 'month': 1, 'register_date': 'datetime.datetime(2018, 1, 14, 23, 31, 37)'}
print ('Затраты в текущем месяце = '+str(abra['cost'])+' рублей')
print ('Затраты в текущем месяце на '+str(abra['title'])+'= '+str(abra['cost'])+' рублей')
