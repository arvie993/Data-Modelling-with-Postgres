import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    # open song file
    df = pd.read_json(filepath,lines=True)

    # insert song record
    song_data = df.values
    song_data = song_data[0].tolist()

    a_list = song_data
    indices = [-3,-2,0,-1,5]
    selected_elements = []
    for index in indices:
        selected_elements.append(a_list[index])
    song_data = selected_elements
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = df.values
    artist_data = artist_data[0].tolist()

    a_list
    indices = [0,4,2,1,3]
    selected_elements = []
    for index in indices:
        selected_elements.append(a_list[index])
    
    artist_data = selected_elements 
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    # open log file
    log_files = get_files('data/log_data')
    filepath = log_files[0]
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    is_NextSong =  df['page']=='NextSong'
    df_NextSong = df[is_NextSong]
    df = df_NextSong 

    # convert timestamp column to datetime
    t = pd.to_datetime(df['ts'], unit='ms') 
    
    # insert time data records
    time_data = [t, \
             t.dt.hour, \
             t.dt.day, \
             t.dt.week, \
             t.dt.month, \
             t.dt.year, \
             t.dt.dayofweek]
    column_labels = ['ts', 'hour', 'day', 'week', 'month', 'year', 'dayofweek']
    time_df = pd.DataFrame(dict(zip(column_labels, time_data))) 

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['userId','firstName','lastName','gender','level']]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (index, row.ts, row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()