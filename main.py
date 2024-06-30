import pandas as pd


# Function to process play data
def process_play_data(play_data, FTData):
    # Merge with FTData
    play_data = pd.merge(play_data, FTData.rename(columns={'Player': 'PLAYER_NAME'}), on='PLAYER_NAME', how='left')

    # Calculate playoutputscore
    play_data['playoutputscore'] = (play_data['PPP'] * 100) + ((play_data['FTA_FREQ'] * 100) * play_data['FT%']) - (
                play_data['TOV_FREQ'] * 100)

    return play_data


# Function to get top play types for a given player and season
def get_top_play_types(player_name, season, data, top_n=3):
    player_data = data[(data['PLAYER_NAME'] == player_name) & (data['SEASON'] == season)]
    if player_data.empty:
        return pd.DataFrame()
    top_play_types = player_data.nlargest(top_n, 'playoutputscore')
    return top_play_types[['PLAYER_NAME', 'SEASON', 'PLAY_TYPE', 'playoutputscore']]


# Function to process play types and print results
def process_and_print_play_types(play_data, FTData, play_type_name):
    # Process play data
    play_data = process_play_data(play_data, FTData)

    # Get unique players and seasons
    players = play_data['PLAYER_NAME'].unique()
    seasons = play_data['SEASON'].unique()

    # Initialize DataFrame to store results
    top_play_types_df = pd.DataFrame()

    # Loop through each player and season to populate the DataFrame
    for player in players:
        for season in seasons:
            top_play_types = get_top_play_types(player, season, play_data)
            if not top_play_types.empty:
                top_play_types_df = pd.concat([top_play_types_df, top_play_types], ignore_index=True)

    # Sort results
    top_play_types_df = top_play_types_df.sort_values(by=['PLAY_TYPE', 'playoutputscore'], ascending=[True, False])

    # Print results
    print(f"\nTop {play_type_name} Plays:\n", top_play_types_df)


# Read each CSV file
isolation_data = pd.read_csv(r'C:\Users\kushh\Downloads\Projects\SportsAnalytics\BGA\OrlandoMagicBGA\Playtype_Orlando_Data\8155530\Isolation.csv')
cut_data = pd.read_csv(r'C:\Users\kushh\Downloads\Projects\SportsAnalytics\BGA\OrlandoMagicBGA\Playtype_Orlando_Data\8155530\Cut.csv')
handoff_data = pd.read_csv(r'C:\Users\kushh\Downloads\Projects\SportsAnalytics\BGA\OrlandoMagicBGA\Playtype_Orlando_Data\8155530\Handoff.csv')
misc_data = pd.read_csv(r'C:\Users\kushh\Downloads\Projects\SportsAnalytics\BGA\OrlandoMagicBGA\Playtype_Orlando_Data\8155530\Misc.csv')
off_screens_data = pd.read_csv(r'C:\Users\kushh\Downloads\Projects\SportsAnalytics\BGA\OrlandoMagicBGA\Playtype_Orlando_Data\8155530\Off_Screens.csv')
pnR_ball_handler_data = pd.read_csv(r'C:\Users\kushh\Downloads\Projects\SportsAnalytics\BGA\OrlandoMagicBGA\Playtype_Orlando_Data\8155530\PnR_Ball_Handler.csv')
pnR_roll_man_data = pd.read_csv(r'C:\Users\kushh\Downloads\Projects\SportsAnalytics\BGA\OrlandoMagicBGA\Playtype_Orlando_Data\8155530\PnR_Roll_Man.csv')
postup_data = pd.read_csv(r'C:\Users\kushh\Downloads\Projects\SportsAnalytics\BGA\OrlandoMagicBGA\Playtype_Orlando_Data\8155530\Postup.csv')
spotup_data = pd.read_csv(r'C:\Users\kushh\Downloads\Projects\SportsAnalytics\BGA\OrlandoMagicBGA\Playtype_Orlando_Data\8155530\Spotup.csv')
transition_data = pd.read_csv(r'C:\Users\kushh\Downloads\Projects\SportsAnalytics\BGA\OrlandoMagicBGA\Playtype_Orlando_Data\8155530\Transition.csv')

# Read FTData
FTData = pd.read_csv(r'C:\Users\kushh\Downloads\Projects\SportsAnalytics\BGA\OrlandoMagicBGA\Playtype_Orlando_Data\8155530\FTData.csv')

# Modify FTData column names
FTData = FTData.rename(columns={'Player': 'PLAYER_NAME'})

# Process and print plays for each play type
process_and_print_play_types(isolation_data, FTData, "Isolation")
process_and_print_play_types(cut_data, FTData, "Cut")
process_and_print_play_types(handoff_data, FTData, "Handoff")
process_and_print_play_types(misc_data, FTData, "Misc")
process_and_print_play_types(off_screens_data, FTData, "Off_Screens")
process_and_print_play_types(pnR_ball_handler_data, FTData, "PnR_Ball_Handler")
process_and_print_play_types(pnR_roll_man_data, FTData, "PnR_Roll_Man")
process_and_print_play_types(postup_data, FTData, "Postup")
process_and_print_play_types(spotup_data, FTData, "Spotup")
process_and_print_play_types(transition_data, FTData, "Transition")
