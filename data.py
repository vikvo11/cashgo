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
#for b in a[-1].keys():
    #print (b)
for c in b:
    print (c)
#print (a[-1].keys())
