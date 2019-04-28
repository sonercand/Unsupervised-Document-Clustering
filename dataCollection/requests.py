import httplib2
import json
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import time
import datetime

api_csv = pd.read_csv('C:\\Users\\sismc\\Desktop\\projects\\misc\\api.csv')
global API_ID
API_ID = api_csv['id'].values[0]
global API_SECRET
API_SECRET = api_csv['secret'].values[0]
global API_BASE_URL
API_BASE_URL = api_csv['base_url'].values[0]
global CURRENT_TIMESTAMP
CURRENT_TIMESTAMP = str(datetime.datetime.utcnow().timestamp())



def getJobAds(parameters):
    '''
    :param parameters:
    :return: result
    '''
    url = API_BASE_URL
    url += '''api_id={}'''.format(API_ID)
    url += '''&api_key={}'''.format(API_SECRET)
    for key, value in parameters.items():
        url += '&' + str(key) + '=' + str(value).replace(' ', '+')
    h = httplib2.Http()
    response, content = h.request(url, 'GET')
    result = json.loads(content)
    return result


def getNumberOfPages(search_phrase):
    '''
    :param search_phrase:
    :return:
    '''
    parameters = {}
    parameters['p'] = '1'
    parameters['q'] = str(search_phrase)
    result = getJobAds(parameters)
    return int(result['pager']['pages'])


def convertToDF(result):
    '''
    :param result:
    :return:
    '''
    return pd.DataFrame(result['jobs'])


def writeAddsToParquet(search_phrase):
    '''
    :param search_phrase:
    :return:
    '''
    number_of_pages = getNumberOfPages(search_phrase)
    time.sleep(5)
    i = 0
    t0 = time.time()
    try:
        for page in range(1, number_of_pages + 1, 1):
            print(page)
            parameters = {}
            parameters['p'] = str(page)
            parameters['q'] = str(search_phrase)
            temp_results = getJobAds(parameters)
            temp_pdf = convertToDF(temp_results)
            table = pa.Table.from_pandas(temp_pdf)
            if i == 0:
                pqwriter = pq.ParquetWriter('C:\\Users\\sismc\\Desktop\\projects\\documentClusteringDNN\data\\' + str(search_phrase) + '_' + CURRENT_TIMESTAMP + '.parquet',
                                            table.schema)
                pqwriter.write_table(table)
            else:
                pqwriter.write_table(table)
            i += 1
            time.sleep(5)
            print(time.time() - t0)
        # close the parquet writer
        if pqwriter:
            pqwriter.close()
        return True
    except Exception as e:
        print(e)
        return False


if __name__ == '__main__':
    search_phrase = 'data scientist'
    writeAddsToParquet(search_phrase)
