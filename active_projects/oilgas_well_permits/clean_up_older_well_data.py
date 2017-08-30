import pandas as pd

# Need to clean up data, splitting some columns, making strings dates, etc.
def cleanup(df):
    df['facility_name'], df['facility_num'] = df['facility_name_num'].str\
                                                          .split("    ", 1).str
    df['field_name'], df['field_num'] = df['field_name_num'].str\
                                                          .split("    ", 1).str
    df['county'], df['coord'] = df['location'].str\
                                              .split("    ", 1).str
    df['operator_name'], df['operator_num'] = df['operator_name_num'].str\
                                                          .split("    ", 1).str
    df['status'] = pd.to_datetime(df['status'].str\
                                              .replace("XX","")\
                                              .str.decode('utf-8'))
    df.drop(['facility_name_num', 'field_name_num', 'operator_name_num'],\
             axis=1, inplace=True)
    return df


if __name__ == '__main__':
    df = pd.read_csv("older_well_permits.csv")
    df = cleanup(df)
