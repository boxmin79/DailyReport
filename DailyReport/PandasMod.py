from datetime import timedelta
import pandas as pd
import ExcelMod


def get_df_from_xl(workbook, sheet, return_by_dict=False):
    df = pd.read_excel(io=workbook, sheet_name=sheet)
    if return_by_dict:
        result = df.to_dict('index')
    else:
        result = df.copy()
    return result


def get_deposit_dict(file_name, xls=True):
    if xls:
        xlsx_file_name = ExcelMod.xls_to_xlsx(file_name)
    else:
        xlsx_file_name = file_name

    df = pd.read_excel(xlsx_file_name, skiprows=4)
    df.rename(columns={'보낸분/받는분': '보낸분', '거래일시': '입금일'}, inplace=True)
    # print(df)

    df.dropna(subset=['입금일'], inplace=True)
    # print(df)

    zero_dp = df.index[df['입금액'] == 0]
    df.drop(zero_dp, inplace=True)

    max_date = pd.to_datetime(ExcelMod.get_max_date()) + timedelta(hours=23, minutes=59)
    # print(max_date)
    df['입금일'] = pd.to_datetime(df['입금일'])
    under_date = df.index[df['입금일'] < max_date]
    df.drop(under_date, inplace=True)
    # print('입금일 제거')
    # print(df)

    exception_list = ExcelMod.get_exception_list()
    # print('예외단어리스트')
    # print(exception_list)
    for ex_word in exception_list:
        ex_idx = df.index[df['보낸분'] == ex_word]
        df.drop(ex_idx, inplace=True)
    # print('예외 단어 제거')
    # print(df)

    # NaN 공백으로 채우기
    df.fillna('', inplace=True)

    # '번호'열 추가
    df['번호'] = df.index
    df.reset_index(inplace=True, drop=True)

    # 딕셔너리로 변환
    dp_dict = df.to_dict('index')
    for idx in dp_dict:
        # '\xa0' 제거
        dp_dict[idx]['보낸분'] = dp_dict[idx]['보낸분'].strip('\xa0')
        dp_dict[idx]['적요'] = dp_dict[idx]['적요'].strip('\xa0')
        if dp_dict[idx]['보낸분'] == '':
            dp_dict[idx]['보낸분'] = dp_dict[idx]['적요']

    # print(dp_dict)

    return dp_dict
                

def get_receivable_dict():
    df = get_df_from_xl('D:/My Documents/운행일보/dr.xlsm', '세금계산서')
    re_df = df[df['수금상태'].isna()]
    re_df.set_index('일보ID', inplace=True)
    re_df.reset_index(inplace=True)
    receivable_dict = re_df.to_dict('index')
    return receivable_dict


def get_before_issue_dict():
    df = get_df_from_xl('D:/My Documents/운행일보/dr.xlsm', '세금계산서')
    df.set_index('일보ID', inplace=True)
    bi_df = df[df['계산서'].isna()]
    bi_dict = bi_df.to_dict('index')

    return bi_dict


def get_print_dict(bi_dict):
    print_dict = {}
    dr_df = get_df_from_xl('D:/My Documents/운행일보/dr.xlsm', '운행일보')
    dr_df.set_index('일보ID', inplace=True)
    dr_dict = dr_df.to_dict('index')
    csn_df = get_df_from_xl('D:/My Documents/운행일보/dr.xlsm', '운송사목록')
    csn_df.set_index('화주ID', inplace=True)
    csn_dict = csn_df.to_dict('index')
    for idx in bi_dict:
        print_dict[idx] = {'일보ID': idx,
                           '상차지': dr_dict[idx]['상차지'],
                           '하차지': dr_dict[idx]['하차지'],
                           '배차시간': dr_dict[idx]['배차시간'],
                           '합계금액': bi_dict[idx]['합계금액'],
                           '사업자번호': csn_dict[bi_dict[idx]['화주ID']]['사업자번호'],
                           '상호': csn_dict[bi_dict[idx]['화주ID']]['상호'],
                           '대표자명': csn_dict[bi_dict[idx]['화주ID']]['대표자명'],
                           '사업장주소': csn_dict[bi_dict[idx]['화주ID']]['사업장주소'],
                           '업태': csn_dict[bi_dict[idx]['화주ID']]['업태'],
                           '업종': csn_dict[bi_dict[idx]['화주ID']]['업종'],
                           '우편물주소': csn_dict[bi_dict[idx]['화주ID']]['우편물주소'],
                           '우편번호': csn_dict[bi_dict[idx]['화주ID']]['우편번호']}

    return print_dict


def get_same_csn(csn_name):
    print('Run <get_same_csn()>')
    workbook = 'D:/My Documents/운행일보/dr.xlsm'
    sheet = '운송사목록'
    df = get_df_from_xl(workbook, sheet)
    # print(df)
    same_index = df.index[(df['화주명'] == csn_name)].tolist()
    print(f'type(same_index) : {type(same_index)}')
    result = df.loc[same_index]
    print(f'type(result) : {type(result)}')

    print(f"result.to_dict('index') \n type(result.to_dict('index')) : {type(result.to_dict('index'))} \n"
          f" {result.to_dict('index')}")
    return result.to_dict('index')


def search_same_value(freight_number, sheet_name, column_name):
    workbook = 'D:/My Documents/운행일보/dr.xlsm'
    # print(f'column_name : {column_name}')
    df = get_df_from_xl(workbook, sheet_name)
    # print(df[column_name])
    if freight_number in df[column_name].values:
        return True
    else:
        return False


def dict_to_series(a_dict):
    return pd.Series(a_dict)


def get_series_from_xl(idx, sheet_name, column, return_to_dict=False):
    print('Run <PandasMod.get_series_from_xl()>')
    print(f'idx : {idx}, type: {type(idx)}')
    print(f'sheet_name : {sheet_name}')
    print(f'column : {column}')
    workbook = 'D:/My Documents/운행일보/dr.xlsm'
    df = get_df_from_xl(workbook, sheet_name)
    df.fillna('', inplace=True)
    same_idx_index = df.index[(df[column] == idx)].tolist()
    print(f'same_idx_index : {same_idx_index}')
    same_df = df.loc[same_idx_index]
    print(f'same_df : {same_df}')
    if return_to_dict:
        print(f"Return : same_df.to_dict('index') \n {same_df.to_dict('index')}")
        print('Done <PandasMod.get_series_from_xl()>')
        return same_df.to_dict('index')
    else:
        print(f"Return : same_df \n {same_df}")
        print('Done <PandasMod.get_series_from_xl()>')
        return same_df


def correct_post_number_type(post_number):
    result = str(post_number)
    if '.' in result:
        result = result[:list(result).index('')]

    if len(result) == 4:
        result = '0' + result

    return result


def group(number):
    s = '%d' % number
    groups = []
    while s and s[-1].isdigit():
        groups.append(s[-3:])
        s = s[:-3]
    return s + ','.join(reversed(groups))


def translate_currency(number):
    return '￦ ' + group(number)


def currency_to_int(currency):
    if '￦' in currency:
        currency = currency.replace('￦', '').strip()
    if '원' in currency:
        currency = currency.replace('원', '').strip()
    if ',' in currency:
        currency = currency.replace(',', '').strip()
    return int(currency)


def mileage_to_int(mileage):
    if '㎞' in mileage:
        mileage = mileage.replace('㎞', '').strip()
    if ',' in mileage:
        mileage = mileage.replace(',', '').strip()
    return int(mileage)


def dict_to_df(dict_list):
    return pd.DataFrame(dict_list)


def get_cost_dict():
    df = get_df_from_xl('D:/My Documents/운행일보/dr.xlsm', '비용')
    fill_df = df.fillna(0)
    fill_df = fill_df.astype({'단가': 'int64'})
    fill_df = fill_df.astype({'수량': 'int64'})
    fill_df = fill_df.astype({'운행거리': 'int64'})
    fill_df = fill_df.astype({'비고': 'str'})
    # print(fill_df)
    # print(fill_df.dtypes)
    cost_dict = fill_df.to_dict('index')
    return cost_dict.copy()


def get_to_datetime(date):
    return pd.to_datetime(date)


def series_to_dict(series):
    return series.to_dict()


def get_filtered_dr_dict(opt, s_date, e_date):
    print(f'==============PandasMod.get_filtered_dr_dict=================')
    s_date = pd.to_datetime(s_date)
    e_date = pd.to_datetime(e_date)
    print(f'start_date : {s_date}, type : {type(s_date)}')
    print(f'end_date : {e_date}, type : {type(e_date)}')

    iti_df = get_df_from_xl('D:/My Documents/운행일보/dr.xlsm', '세금계산서')
    dr_df = get_df_from_xl('D:/My Documents/운행일보/dr.xlsm', '운행일보')

    if opt == 0:
        mask = (iti_df['배차시간'] >= s_date) & (iti_df['배차시간'] <= e_date)
    if opt == 1:
        mask = (iti_df['배차시간'] >= s_date) & (iti_df['배차시간'] <= e_date) & (iti_df['수금상태'].notna())
    if opt == 2:
        mask = (iti_df['배차시간'] >= s_date) & (iti_df['배차시간'] <= e_date) & (iti_df['수금상태'].isna())

    filtered_df = dr_df.loc[mask]

    filtered_dict = filtered_df.to_dict('index')
    print('============= 전체  =========================')
    for idx in filtered_dict:
        for dkey in filtered_dict[idx]:
            print(f'{dkey}: {filtered_dict[idx][dkey]}')
        print()
    print(f'item count : {len(filtered_dict)}')
    print('===========================================')
    return filtered_dict




