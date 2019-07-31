#!/usr/bin/python3
from __future__ import print_function
import datetime
import os.path
import pickle
import sys
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from pytz import timezone

# トークンおよび設定ファイル
TOKEN_PICKLE = '/var/lib/asterisk/agi-bin/token.pickle'
SAVEDATA_PICKLE = '/var/lib/asterisk/agi-bin/save.pickle'

# GoogleスプレッドシートのAPI呼び出し用
INPUT_OPTION = 'USER_ENTERED'

def main(update_data):
    """Googleスプレッドシートにタイムスタンプと電話番号を書き込む。
    事前にsetup.pyを実行しておく必要がある。
    """
    creds = None

    # OAuth2のトークンを読み込む
    if os.path.exists(TOKEN_PICKLE):
        with open(TOKEN_PICKLE, 'rb') as token:
            creds = pickle.load(token)
    else:
        print('最初にセットアップを実行してください。')
        return

    # セーブデータを読み込む
    if os.path.exists(SAVEDATA_PICKLE):
        with open(SAVEDATA_PICKLE, 'rb') as save:
            save_data = pickle.load(save)
    else:
        print('最初にセットアップを実行してください。')
        return

    # トークンのリフレッシュと保存
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            print('トークンが無効です。再度セットアップを実施してください。')
            return
        # 次回再利用するためトークンを保存する
        with open(TOKEN_PICKLE, 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # 最終行の更新
    curr_row = save_data['LAST_ROW'] + 1
    save_data['LAST_ROW'] = curr_row

    # Sheets APIの呼び出し
    sheet = service.spreadsheets()
    my_body = {}
    my_range = save_data['SHEET_NAME'] + '!A' + str(curr_row) + ':B' + str(curr_row)
    my_body['range'] = my_range
    my_body['majorDimension'] = 'ROWS'
    my_body['values'] = [update_data]
    result = sheet.values().update(spreadsheetId=save_data['SHEET_ID'], range=my_range, valueInputOption=INPUT_OPTION, body=my_body).execute()

    with open(SAVEDATA_PICKLE, 'wb') as save:
        pickle.dump(save_data, save)

if __name__ == '__main__':
    now = datetime.datetime.now(timezone('Asia/Tokyo'))    # タイムスタンプ

    # 引数から電話番号を取得
    args = sys.argv
    caller_id = args[1]

    # スプレッドシート更新用の配列
    update_data = [now.strftime('%Y/%m/%d %H:%M:%S'), caller_id]

    main(update_data)
