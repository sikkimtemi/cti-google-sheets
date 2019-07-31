from __future__ import print_function
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow

# APIに対して権限を付与したいスコープ
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def main():
    """対話型で初期設定を行います。
    ・Google APIのOAuth2認証
    ・スプレッドシートのIDとシート名、および最終行
    """

    # OAuth2認証を実施
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)

    # 認証結果を保存
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)

    # スプレッドシートの情報を入力
    print('スプレッドシートのIDを入力してください。')
    sheet_id = input('>> ')

    print('シート名を入力してください。')
    sheet_name = input('>> ')

    print('最終行を入力してください。')
    lastrow = input('>> ')

    save_data = {
        'SHEET_ID': sheet_id,
        'SHEET_NAME': sheet_name,
        'LAST_ROW': int(lastrow),
    }
    with open('save.pickle', 'wb') as save:
        pickle.dump(save_data, save)

if __name__ == '__main__':
    main()