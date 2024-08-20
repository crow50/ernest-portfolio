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
import logging

logging.basicConfig(level=logging.INFO)

def get_db_params(config_file, section):
    """
    Retrieves database configuration parameters from a given section of the config file.
    """
    parser = ConfigParser()
    parser.read(config_file)
    if parser.has_section(section):
        return {param[0]: param[1] for param in parser.items(section)}
    else:
        raise Exception(f'Section {section} not found in the {config_file} file')
    
def connect_to_db(db_params):
    """
    Connects to the database using SQLAlchemy and returns the engine and session objects.
    """
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
    """
    Reflects only the desired views from the specified schema.
    """
    metadata = MetaData()
    inspector = inspect(engine)
    all_view_names = inspector.get_view_names(schema=schema)
    view_names = [view for view in all_view_names if view in desired_views]
    return {view_name: 
            Table(view_name, metadata, autoload_with=engine, schema=schema) 
            for view_name in view_names}

def process_meter_data(session, meters_view, meter_voltage_intervals_view, 
                       circuit_number, start_date, end_date):
    """
    Processes meter data within the given circuit and time range.
    """
    matching_meters = session.query(meters_view).filter(
        meters_view.c.circuit_common_id == circuit_number,
        meters_view.c.updated_at > start_date
    ).all()  
    
    output_dir = 'output_by_sp_id'
    os.makedirs(output_dir, exist_ok=True)
    
    for meter in matching_meters:
        process_single_meter(session, meter, meter_voltage_intervals_view, 
                             start_date, end_date, output_dir)
        
def process_single_meter(session, meter, meter_voltage_intervals_view, start_date, end_date, output_dir):
    """
    Processes a single meter, querying voltage data and saving the results.
    """
    df_meters = pd.DataFrame([meter])
    logging.info(f"Processing: {df_meters.at[0, 'sp_common_id']} ")
    meter_voltage_intervals_results = session.query(meter_voltage_intervals_view).filter(
        meter_voltage_intervals_view.c.meter_id == meter[30],
        meter_voltage_intervals_view.c.interval_time >= start_date,
        meter_voltage_intervals_view.c.interval_time <= end_date
    ).all()
    
    df_voltage_intervals = pd.DataFrame([dict(row) for row in meter_voltage_intervals_results])
    if df_voltage_intervals.empty:
        save_no_data(df_meters)
    else:
        process_voltage_intervals(df_meters, df_voltage_intervals, output_dir)

def save_no_data(df_meters):
    """
    Saves meter data with no associated voltage data to a separate file.
    """
    no_data_file = "SP_W_No_Data.xlsx"
    write_to_excel(df_meters, no_data_file, str(df_meters.at[0, 'sp_common_id']))

def process_voltage_intervals(df_meters, df_voltage_intervals, output_dir):
    """
    Processes and formats voltage intervals before merging with meter data and saving.
    """
    df_voltage_intervals['value'] = df_voltage_intervals['value'].astype(float).round(3)
    df_pivot = df_voltage_intervals.pivot(index=['meter_id', 'interval_time'], 
                                          columns='unit', values='value')
    df_pivot = df_pivot.rename_axis(index={'meter_id': 'electronic_serial_number'}).reset_index()
    df_pivot.columns = [col.replace(' ', '_') for col in df_pivot.columns]
    df_merged = pd.merge(df_pivot, df_meters, on='electronic_serial_number', how='inner')
    df_filtered = select_and_rename_columns(df_merged)
    save_filtered_data(df_filtered, output_dir)

def select_and_rename_columns(df_filtered):
    """
    Selects relevant columns and renames them for clarity, handling missing data.
    """
    desired_columns = ['sp_common_id', 'interval_time', 'serial_number',
                       'AVG_V(a)', 'AVG_V(b)', 'AVG_V(c)',
                       'MAX_V(a)', 'MAX_V(b)', 'MAX_V(c)',
                       'MIN_V(a)', 'MIN_V(b)', 'MIN_V(c)']
    for col in desired_columns:
        if col not in df_filtered.columns:
            df_filtered[col] = pd.NA
    df_filtered = df_filtered[desired_columns].rename(columns={'sp_common_id': 'SP_ID', 'interval_time': 'TIME', 
                                                      'serial_number': 'SERIAL_NUMBER'})
    df_filtered = remove_timezone(df_filtered)
    df_filtered['Month'] = pd.to_datetime(df_filtered['TIME']).dt.strftime('%Y-%m')
    return df_filtered

def save_filtered_data(df_filtered, output_dir):
    """
    Saves the filtered and processed data to an Excel file, grouped by month.
    """
    grouped = df_filtered.groupby(['Month'])
    for month, group in grouped:
        file_name = f"{output_dir}/SP_ID_{df_filtered.at[0,'SP_ID']}.xlsx"
        write_to_excel(group, file_name, month)

def write_to_excel(df, file_name, sheet_name):
    """
    Writes the DataFrame to an Excel file, either creating a new file or appending to an existing one.
    """
    if os.path.isfile(file_name):
        with pd.ExcelWriter(file_name, mode='a', engine='openpyxl', if_sheet_exists='new') as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    else:
        with pd.ExcelWriter(file_name, mode='w', engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=False)

def remove_timezone(df):
    """
    Removes timezone information from datetime columns in the DataFrame.
    """
    for col in df.columns:
        if pd.api.types.is_datetime64tz_dtype(df[col]):
            df[col] = df[col].dt.tz_localize(None)
    return df

if __name__ == '__main__':
    """
    Entry point for the script. Retrieves configuration, connects to the database, and processes data.
    """
    db_config_file = 'postgres_db.ini'  # Ensure this file is not shared publicly.
    db_section = 'my_database_section'
    
    db_params = get_db_params(db_config_file, db_section)
    engine, session = connect_to_db(db_params)
    
    reflected_views = reflect_views(engine, 'schema_name', ['view1', 'view2'])
    
    circuit_number = input("Circuit Number: ")
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 12, 31)
    
    process_meter_data(session, reflected_views['view1'], 
                       reflected_views['view2'], circuit_number, start_date, end_date)
