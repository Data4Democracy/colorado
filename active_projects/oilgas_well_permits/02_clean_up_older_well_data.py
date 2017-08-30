import pandas as pd

def cleanup(df):
    # Splitting facility_name_num into 2 columns for facility_name &
    #    facility_num.  Stripping spaces from start/end of facility_num
    df['facility_name'], df['facility_num'] = df['facility_name_num']\
                                                 .str.split("    ", 1)\
                                                 .str
    df['facility_num'] = df['facility_num'].str.strip()

    # Splitting field_name_num into 2 columns for field_name &
    #    field_num.  Stripping spaces from start/end of field_num
    df['field_name'], df['field_num'] = df['field_name_num']\
                                           .str.split("    ", 1)\
                                           .str
    df['field_num'] = df['field_num'].str.strip()

    # Splitting location into 2 columns for county &
    #    coord.  Stripping spaces from start/end of coord
    df['county'], df['coord'] = df['location']\
                                   .str.split("    ", 1)\
                                   .str
    df['coord'] = df['coord'].str.strip()

    # Splitting operator_name_num into 2 columns for operator_name &
    #    operator_num.  Stripping spaces from start/end of field_num
    df['operator_name'], df['operator_num'] = df['operator_name_num']\
                                                 .str.split("    ", 1)\
                                                 .str
    df['operator_num'] = df['operator_num'].str.strip()

    # Removing leading X's from the permit status date, and converting from a
    #    string to utf-8 format
    df['status'] = pd.to_datetime(df['status']\
                                     .str.replace("XX","")\
                                     .str.decode('utf-8'))

    # Dropping the original combined columns from the DataFrame & unneeded
    #    columns
    df.drop(['facility_name_num', 'field_name_num', 'operator_name_num', \
             'location'],\
             axis=1, inplace=True)
    df.drop(['Unnamed: 0', 'related_facilities'], axis=1, inplace=True)

    # Drop any duplicate rows
    df.drop_duplicates()

    return df


if __name__ == '__main__':
    df = pd.read_csv("data/older_well_permits.csv")
    df = cleanup(df)
    df.to_csv("data/older_well_permits_clean.csv")
