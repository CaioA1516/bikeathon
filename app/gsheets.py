import pygsheets


def init_gsheet():
    gc = pygsheets.authorize('gsheets_secret.json', no_cache=True)
    sh = gc.open_by_key('1tTuWHk3c-JVvdOOSVVA1rIOjjz8eMf-Zyh1Fit5JwPc')
    wks = sh.worksheet_by_title('Data')
    return wks


def fetch_gsheet_total(wks):
    df = wks.get_as_df().set_index('Method')
    venmo_total = df.at['Venmo', 'Total']
    cash_total = df.at['Cash', 'Total']
    card_total = df.at['Card', 'Total']
    # Expecting card and venmo to be tracked automatically
    # Only report cash
    # Probably will end up deleting the extra options on the Google form
    # Unless we implement donating towards certain brothers
    return cash_total


if __name__ == "__main__":
    wks = init_gsheet()
    print("Cash money from Google Sheet: %d" % fetch_gsheet_total(wks))
