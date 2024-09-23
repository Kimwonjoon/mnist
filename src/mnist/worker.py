from datetime import datetime
from pytz import timezone
from mnist.db import get_conn, select, dml

import random
import requests
import os
def run():
    """image_processing 테이블을 읽어서 가장 오래된 요청 하나씩을 처리"""
  
    # STEP 1
    # image_processing 테이블의 prediction_result IS NULL 인 ROW 1 개 조회 - num 갖여오기
    connection = get_conn()
    with connection:
        with connection.cursor() as cursor:
            sql = "SELECT num FROM image_processing WHERE prediction_result IS NULL ORDER BY num"
            cursor.execute(sql)
            result = cursor.fetchone() # 형식 : {'num' : ?}
            #print(result)
    #return result

    # STEP 2
    # RANDOM 으로 0 ~ 9 중 하나 값을 prediction_result 컬럼에 업데이트
    # 동시에 prediction_model, prediction_time 도 업데이트
    ts = datetime.now(timezone('Asia/Seoul')).strftime('%Y-%m-%d %H:%M:%S')
    if result == None:
        ind = None
    else:
        ind = result['num']
        pred = random.randint(0,9)
        connection = get_conn()
        with connection:
            with connection.cursor() as cursor:
                sql = f"UPDATE image_processing SET prediction_result={pred}, prediction_model='randint', prediction_time='{ts}' WHERE num={ind}"
                cursor.execute(sql)
            connection.commit()
    # STEP 3
    # LINE 으로 처리 결과 전송
    headers = {
        'Authorization': 'Bearer ' + os.getenv('LINE_NOTI_PATH', '0CexLLmrOvvWXwb21FLPvNXiwV3JKpqh7tcC9mjEmc2'),
    }

    if result == None:
        files = {
        'message': (None, f"업데이트 할 데이터가 없습니다."),
    }
        response = requests.post('https://notify-api.line.me/api/notify', headers=headers, files=files)

        print(f"업데이트 할 데이터가 없습니다.")

        return {
            "prediction_time":ts,
            "train_data_nth":ind,
        }

    files = {
        'message': (None, f"{ind}번째 이미지의 예측결과는 {pred}입니다."),
    }

    response = requests.post('https://notify-api.line.me/api/notify', headers=headers, files=files)

    print(f"[{ts}] {result['num']}번째 이미지의 예측결과는 {pred}입니다.")

    return {
        "prediction_time":ts,
        "train_data_nth":result['num'],
        "pred":pred
    }
#print(run())
