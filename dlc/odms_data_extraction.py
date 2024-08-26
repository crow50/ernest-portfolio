#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ODMS Data Extract
Author: Ernest Baker ernestleroybaker@gmail.com
"""

from sqlalchemy import create_engine, inspect, Table, MetaData
from sqlalchemy.orm import sessionmaker
import pandas as pd
from datetime import datetime
import os
from configparser import ConfigParser
import logging, logging.handlers

logging.basicConfig(filename='extract.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logging.getLogger().addHandler(logging.StreamHandler())

def get_db_params(config_file, section):
    '''
    get_db_params(config_file, section)
    Sets the parameters for the ConfigParser, currently set to prod
    '''
    parser = ConfigParser()
    parser.read(config_file)
    if parser.has_section(section):
        logging.info('Config file loaded')
        return {param[0]: param[1] for param in parser.items(section)}
    else:
        raise Exception(f'Section {section} not found in the {config_file} file')

def connect_to_db(db_params):
    '''
    Connecting to the database using the items returned from the ConfigParser
    '''
    try:
        logging.info('Connecting to the PostgreSQL database...')
        engine = create_engine(f"postgresql+psycopg2://{db_params['user']}:{db_params['password']}@{db_params['host']}/{db_params['database']}")
        Session = sessionmaker(bind=engine)
        logging.info(f'Connected to the {db_params["database"]} database...')
        return engine, Session()
    except Exception as error:
        logging.error(f"Error connecting to the database: {error}")
        raise

def reflect_views(engine, schema, desired_views):
    '''
    Only keep the desired views in memory
    '''
    try:
        metadata = MetaData()
        inspector = inspect(engine)
        all_view_names = inspector.get_view_names(schema=schema)
        view_names = [view for view in all_view_names if view in desired_views]
        logging.debug(f'Reflected: {view_names}')
        logging.info('Successfully refelected views')
        return {view_name: 
                Table(view_name, metadata, autoload_with=engine, schema=schema) 
                for view_name in view_names}
    except Error as error:
        logging.error('Unable to reflect views')

def process_meter_data(session, meters_view, meter_voltage_intervals_view, 
                       circuit_number, start_date, end_date):
    '''
    We begin by taking our query parameters to query the meters_view and only select the meters that
    are in our desired circuit.
    '''
    logging.info(f'Executing query for meters matching {circuit_number}')
    logging.debug(f'CIRCUIT: {circuit_number}', 
                  f'QUERY START DATE: {start_date}', 
                  f'QUERY END DATE: {end_date}')
    matching_meters = session.query(meters_view).filter(
        meters_view.c.circuit_common_id == circuit_number,
        meters_view.c.updated_at > start_date
    ).all()  # Refactored to fetch all at once, or consider yield_per()
    
    output_dir = 'output_by_sp_id'
    os.makedirs(output_dir, exist_ok=True)
    logging.debug(f'OUTPUT DIRECTORY MADE {output_dir}')
    for meter in matching_meters:
        process_single_meter(session, meter, meter_voltage_intervals_view, 
                             start_date, end_date, output_dir)
        
def process_single_meter(session, meter, meter_voltage_intervals_view, start_date, end_date, output_dir):
    '''
    After we get all of the meters that match our circuit, we take one ESN at a time, and query the
    voltages for that meter for the given timeframe.
    '''
    df_meters = pd.DataFrame([meter])
    logging.info(f"Processing: {df_meters.at[0, 'sp_common_id']} ")
    meter_voltage_intervals_results = session.query(meter_voltage_intervals_view).filter(
        meter_voltage_intervals_view.c.meter_id == meter[30],
        meter_voltage_intervals_view.c.interval_time >= start_date,
        meter_voltage_intervals_view.c.interval_time <= end_date
    ).all()
    
    df_voltage_intervals = pd.DataFrame([dict(row) for row in meter_voltage_intervals_results])
    if df_voltage_intervals.empty:
        '''
        If there is no voltage information, the results from the meters_view get written to a separate file
        '''
        logging.info(f"No data for {df_meters.at[0, 'sp_common_id']} during selected timeframe")
        save_no_data(df_meters)
    else:
        process_voltage_intervals(df_meters, df_voltage_intervals, output_dir)

def save_no_data(df_meters):
    '''
    The process to write empty voltage values
    '''
    no_data_file = "SP_W_No_Data.xlsx"
    df_filtered = remove_timezone(df_meters)
    write_to_excel(df_meters, no_data_file, str(df_meters.at[0, 'sp_common_id']),
                   record_id=str(df_meters.at[0, 'sp_common_id']))

def process_voltage_intervals(df_meters, df_voltage_intervals, output_dir):
    '''
    With the raw, but filtered voltage data, we need to do a bit more massaging.
    We start by changing the number of decimal places for the values,
    Then we rename the ID to ESN since that makes sense and will be easier for a later step
    Finally, we merge the now massage voltage data onto our meter data before proceeding.
    '''
    df_voltage_intervals['value'] = df_voltage_intervals['value'].astype(float).round(3)
    df_pivot = df_voltage_intervals.pivot(index=['meter_id', 'interval_time'], 
                                          columns='unit', values='value')
    df_pivot = df_pivot.rename_axis(index={'meter_id': 'electronic_serial_number'}).reset_index()
    df_pivot.columns = [col.replace(' ', '_') for col in df_pivot.columns]
    df_merged = pd.merge(df_pivot, df_meters, on='electronic_serial_number', how='inner')
    df_filtered = select_and_rename_columns(df_merged)
    save_filtered_data(df_filtered, output_dir)

def select_and_rename_columns(df_filtered):
    '''
    since we don't need 72 columns, this process filters it down to the ones we want
    It also writes null values in the columns without data.
    This is typical in residential meters as they don't have B and C voltage
    '''
    desired_columns = ['sp_common_id', 'interval_time', 'serial_number',
                       'AVG_V(a)', 'AVG_V(b)', 'AVG_V(c)',
                       'MAX_V(a)', 'MAX_V(b)', 'MAX_V(c)',
                       'MIN_V(a)', 'MIN_V(b)', 'MIN_V(c)']
    for col in desired_columns:
        if col not in df_filtered.columns:
            df_filtered[col] = pd.NA
    df_filtered = df_filtered[desired_columns].rename(columns={'sp_common_id': 'SP_ID',
                                                               'interval_time': 'TIME', 
                                                      'serial_number': 'SERIAL_NUMBER'})
    df_filtered = remove_timezone(df_filtered)
    return df_filtered

def save_filtered_data(df_filtered, output_dir):
    '''
    Process to save the filtered and massaged data
    '''
    file_name = f"{output_dir}/SP_ID_{df_filtered.at[0,'SP_ID']}.xlsx"
    write_to_excel(df_filtered, file_name, df_filtered.at[0,'SP_ID'], record_id=df_filtered.at[0,'SP_ID'])

def write_to_excel(df, file_name, sheet_name, record_id):
    '''
    Excel writing engine
    If there is no file for a given sp, this process will create one
    Then it will append to that file for each month requested
    '''
    if os.path.isfile(file_name):
        with pd.ExcelWriter(file_name, mode='a', engine='openpyxl', if_sheet_exists='new') as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    else:
        with pd.ExcelWriter(file_name, mode='w', engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    logging.info(f"{record_id} complete")

def remove_timezone(df):
    '''
    Excel doesn't like timezone aware columns, this removes them.
    '''
    for col in df.columns:
        if pd.api.types.is_datetime64tz_dtype(df[col]):
            df[col] = df[col].dt.tz_localize(None)
    return df

if __name__ == '__main__':
    '''
    This is the real beginning of the process. 
    Values changed here will modify the entire output even slightly.
    '''
    db_config_file = 'postgres_db.ini'
    db_section = 'prod'
    
    db_params = get_db_params(db_config_file, db_section)
    engine, session = connect_to_db(db_params)
    
    reflected_views = reflect_views(engine, 'client', ['meters', 'meter_voltage_intervals'])
    
    circuit_number = input("Circuit Number: ")
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 12, 31)
    
    process_meter_data(session, reflected_views['meters'], 
                       reflected_views['meter_voltage_intervals'], circuit_number, start_date, end_date)