import psycopg2
import json

#conn=psycopg2.connect(database= 'Weather_app', user='postgres', password='0000')
#cur=conn.cursor()


with open('de.json') as d:
    datas= json.load(d)
    #for data in datas:
    #    print(data)
    #print(len(datas))
    
    sql_data='INSERT INTO de'
if type(datas) == list:
    first_data = datas[0]

    columns = list(first_data.keys())
    print ("\ncolumn names:", columns)
    
    sql_data += " (" + ', '.join(columns) + ")\nVALUES "
    
    #values= [list(data.values()) for data in datas]
    
for i, data_dict in enumerate(datas):
    print(i+1, data_dict)
    # iterate over the values of each record dict object
    values = []
    for col_names, val in data_dict.items():

        # Postgres strings must be enclosed with single quotes
        if type(val) == str:
            # escape apostrophies with two single quotations
            #val = val.replace("'", "''")
            print(val)
        values += [ str(val) ]
    print(values)
    values_join= '(' + ', '.join(values) + ')'
    print(values_join)
    #join the list of values and enclose record in parenthesis
    sql_data += values_join
    print(sql_data)
    values=[]
    #print(sql_data)
    