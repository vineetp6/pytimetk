import pytest
import pandas as pd
from pytimetk import ts_summary, get_frequency

from pytimetk.core.frequency import _get_manual_frequency  # Adjust the module name accordingly

# Sample test data
dates = pd.to_datetime(["2023-10-02", "2023-10-03", "2023-10-04", "2023-10-05", "2023-10-06", "2023-10-09", "2023-10-10"])
df_sample = pd.DataFrame(dates, columns=["date"])

# Test ts_summary on a regular dataframe
def test_ts_summary_regular_df():
    result = df_sample.ts_summary(date_column='date')
    
    # Basic checks
    assert 'date_n' in result.columns
    assert result['date_n'].values[0] == len(df_sample)
    assert result['date_start'].values[0] == df_sample['date'].min()
    assert result['date_end'].values[0] == df_sample['date'].max()

# Test ts_summary on a grouped dataframe
def test_ts_summary_grouped_df():
    # Grouped DataFrame sample
    df_grouped = df_sample.copy()
    df_grouped['group'] = ['A', 'B', 'A', 'B', 'A', 'B', 'A']
    
    result = df_grouped.groupby('group').ts_summary(date_column='date')
    
    # Basic checks
    assert 'group' in result.columns
    assert result['date_n'].sum() == len(df_grouped)

# Test ts_summary type check for invalid data
def test_ts_summary_invalid_data_type():
    with pytest.raises(TypeError):
        ts_summary(data=[1, 2, 3], date_column='date')

# Test get_diff_summary for numeric flag
def test_get_diff_summary_numeric_flag():
    from pytimetk import get_diff_summary  # Adjust the module name accordingly
    result = get_diff_summary(df_sample['date'], numeric=True)
    
    # Checking columns for numeric flag
    assert 'diff_min_seconds' in result.columns
    assert 'diff_median_seconds' in result.columns

# Test get_date_summary for basic output
def test_get_date_summary():
    from pytimetk import get_date_summary  # Adjust the module name accordingly
    result = get_date_summary(df_sample['date'])
    
    # Basic checks
    assert 'date_n' in result.columns
    assert result['date_n'].values[0] == len(df_sample)

# Test get_frequency_summary for basic output
def test_get_frequency_summary():
    from pytimetk import get_frequency_summary  # Adjust the module name accordingly
    result = get_frequency_summary(df_sample['date'])
    
    # Basic checks
    assert 'freq_inferred_unit' in result.columns
    assert 'freq_median_timedelta' in result.columns

# *** FREQUENCY TESTS *** ---- 

def test_no_pandas_frequency():
    
    # MONTH WITH 2 TIMESTAMPS DOES NOT HAVE A FREQUENCY IN PANDAS
    dates = pd.to_datetime(["2018-01-01", "2018-02-01"])
    df_sample = pd.DataFrame(dates, columns=["date"])
    
    result = ts_summary(df_sample, 'date')
    
    assert result['freq_median_scale'].values[0] == 1.0
    assert result['freq_median_unit'].values[0] == 'M'
    
    result = get_frequency(dates)
    
    assert result == '1MS'
    
    result = _get_manual_frequency(dates)
    
    assert result == '1MS'

def test_minute():
    
    dates = pd.date_range(start='2018-01-01', end='2018-01-02', freq='12min')
    
    df_sample = pd.DataFrame(dates, columns=["date"])
    
    result = ts_summary(df_sample, 'date')
    
    assert result['freq_median_scale'].values[0] == 12.0
    assert result['freq_median_unit'].values[0] == 'T'
    
    result = get_frequency(dates)
    
    assert result == '12T'
    
    result = _get_manual_frequency(dates)
    
    assert result == '12T'
    
def test_hour():
    
    dates = pd.date_range(start='2018-01-01', end='2018-01-02', freq='3H')
    
    df_sample = pd.DataFrame(dates, columns=["date"])
    
    result = ts_summary(df_sample, 'date')
    
    assert result['freq_median_scale'].values[0] == 3.0
    assert result['freq_median_unit'].values[0] == 'H'
    
    result = get_frequency(dates)
    
    assert result == '3H'
    
    result = _get_manual_frequency(dates)
    
    assert result == '3H'
    
def test_day():
    
    dates = pd.date_range(start='2018-01-01', end='2018-02-01', freq='3D')
    
    df_sample = pd.DataFrame(dates, columns=["date"])
    
    result = ts_summary(df_sample, 'date')
    
    assert result['freq_median_scale'].values[0] == 3.0
    assert result['freq_median_unit'].values[0] == 'D'
    
    result = get_frequency(dates)
    
    assert result == '3D'
    
    result = _get_manual_frequency(dates)
    
    assert result == '3D'
    
def test_week():
    
    dates = pd.date_range(start='2018-01-01', end='2018-02-01', freq='2W')
    
    df_sample = pd.DataFrame(dates, columns=["date"])
    
    result = ts_summary(df_sample, 'date')
    
    assert result['freq_median_scale'].values[0] == 2.0
    assert result['freq_median_unit'].values[0] == 'W'
    
    result = get_frequency(dates)
    
    assert result == '2W'
    
    result = _get_manual_frequency(dates)
    
    assert result == '2W'
    
def test_month():
    
    dates = pd.date_range(start='2018-01-01', end='2018-12-01', freq='2M')
    
    df_sample = pd.DataFrame(dates, columns=["date"])
    
    result = ts_summary(df_sample, 'date')
    
    assert result['freq_median_scale'].values[0] == 2.0
    assert result['freq_median_unit'].values[0] == 'M'
    
    result = get_frequency(dates)
    
    assert result == '2M'
    
    result = _get_manual_frequency(dates)
    
    assert result == '2M'

def test_four_months():
    
    dates = pd.date_range(start='2018-01-01', end='2018-12-01', freq='4M')
    
    df_sample = pd.DataFrame(dates, columns=["date"])
    
    result = ts_summary(df_sample, 'date')
    
    assert result['freq_median_scale'].values[0] == 121.0
    assert result['freq_median_unit'].values[0] == 'D'
    
    result = get_frequency(dates)
    
    assert result == '4M'
    
    result = _get_manual_frequency(dates)
    
    assert result == '121D'


def test_quarter():
    
    dates = pd.to_datetime(["2018-01-01", "2018-04-01"])
    df_sample = pd.DataFrame(dates, columns=["date"])
    
    result = ts_summary(df_sample, 'date')
    
    assert result['freq_median_scale'].values[0] == 1.0
    assert result['freq_median_unit'].values[0] == 'Q'   
    
    result = get_frequency(dates)
    
    assert result == '1QS'
    
    result = _get_manual_frequency(dates)
    
    assert result == '1QS'
    

def test_quarter_start():
    
    dates = pd.date_range("2018-01-01", "2019-01-01", freq='QS')
    
    df_sample = pd.DataFrame(dates, columns=["date"])
    
    result = ts_summary(df_sample, 'date')
    
    assert result['freq_median_scale'].values[0] == 1.0
    assert result['freq_median_unit'].values[0] == 'Q'   
    
    result = get_frequency(dates)
    
    assert result == 'QS-OCT'
    
    result = _get_manual_frequency(dates)
    
    assert result == '1QS'
    
def test_quarter_end():
    
    dates = pd.date_range("2018-01-01", "2019-01-01", freq='Q')
    
    df_sample = pd.DataFrame(dates, columns=["date"])
    
    result = ts_summary(df_sample, 'date')
    
    assert result['freq_median_scale'].values[0] == 1.0
    assert result['freq_median_unit'].values[0] == 'Q'   
    
    result = get_frequency(dates)
    
    assert result == 'Q-DEC'
    
    result = _get_manual_frequency(dates)
    
    assert result == '1Q'
    
def test_year():
    
    dates = pd.date_range("2018-01-01", "2026-01-01", freq='2Y')
    
    df_sample = pd.DataFrame(dates, columns=["date"])
    
    result = ts_summary(df_sample, 'date')
    
    assert result['freq_median_scale'].values[0] == 2.0
    assert result['freq_median_unit'].values[0] == 'Y'   
    
    result = get_frequency(dates)
    
    assert result == '2A-DEC'
    
    result = _get_manual_frequency(dates)
    
    assert result == '2Y'
    
def test_custom_offset():
    from dateutil.relativedelta import relativedelta

    start_date = pd.Timestamp('2022-01-01')

    dates = [start_date + i * relativedelta(years=2, months=3) for i in range(5)]

    dates = pd.DatetimeIndex(dates)
    
    df_sample = pd.DataFrame(dates, columns=["date"])
    
    result = ts_summary(df_sample, 'date')
  
    
    assert result['freq_median_scale'].values[0] == 821.0
    assert result['freq_median_unit'].values[0] == 'D'   
    
    result = get_frequency(dates)
    
    assert result == '9QS-OCT'
    
    result = _get_manual_frequency(dates)
    
    assert result == '821D' 
    
    

if __name__ == "__main__":
    pytest.main([__file__])