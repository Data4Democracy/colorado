import pandas as pd

def cleanup(df):
    df['App_Received'] = df['Received\nPosted'].str.slice(0, 10)
    df['App_Posted'] = df['Received\nPosted'].str.slice(11, 21)
    df['App_Approved'] = df['Approved Date\nAPI No.\n(Scout Card Link)'].str.slice(0,10)
    df['App_Received'] = pd.to_datetime(df['App_Received'])
    df['App_Posted'] = pd.to_datetime(df['App_Posted'])
    df['App_Approved'] = pd.to_datetime(df['App_Approved'])
    df['Operator Name\nNumber'].str.split()
    df['Operator_Name'] = [df_wells['Operator Name\nNumber'][i]\
                           .split('\n')[0] for i in xrange(len(df_wells))]
    df['Operator_Number'] = [df_wells['Operator Name\nNumber'][i]\
                           .split('\n')[1] for i in \
                           xrange(len(df_wells))]
    df['Days_Recvd_to_Approval'] = (df['App_Approved'] - \
                                    df['App_Received']).dt.days
    df['Days_Posted_to_Approval'] = (df['App_Approved'] - \
                                     df['App_Posted']).dt.days

    df.drop(['Received\nPosted', 'Approved Date\nAPI No.\n(Scout Card Link)'], axis=1, inplace=True)
    return df

if __name__ == '__main__':
    df_wells = pd.read_csv("CO_Well_Permits_2016-06-08_2017-06-26.csv")
    df_wells = cleanup(df_wells)

    # Try plotting permits per day, does the approval change significantly
    #    before & after new admin?  Does it change significantly at any point
    #    during the year June 2016 - June 2017?
    # Try using the probabilistic programming in PyMC3 book.
