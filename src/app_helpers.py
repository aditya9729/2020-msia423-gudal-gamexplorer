from fuzzywuzzy import fuzz

def fuzzy_matching(hashmap, fav_game):
    """Return the closest match via fuzzy ratio.
    If no match found, return None
    :param hashmap: dict, map movie title name to index of the game in data
    :param fav_game: str, name of user input game
    :returns `int`:index of the closest match
    """
    match_tuple = []
    # get match
    for title, idx in hashmap.items():
        ratio = fuzz.token_sort_ratio(title.lower(), fav_game.lower())
        if ratio >= 60:
            match_tuple.append((title, idx, ratio))
    # sort
    match_tuple = sorted(match_tuple, key=lambda x: x[2])[::-1]
    if not match_tuple:
        return None
    return match_tuple[0][1]

def get_recommendations(title,data,model,hashmap):
    """Gives 10 recommendations from model's most similar findings
    :param title `str`: game name
    :param data `dataframe`: dataframe to get names from
    :param model `implicit.als`: ALS model
    :param hashmap `dict`: a game to index dictionary
    :return `list`: list of all characteristics of the 10 games
    """
    idx = fuzzy_matching(hashmap, title)

    similar_items = [index for index, similarity in model.similar_items(idx, N=11)[1:]]

    reco_df=data.iloc[similar_items,:]

    # get background image, game names, ratings, release date, genres, platforms and stores
    posters=reco_df.background_image.values.tolist()
    games=reco_df.name.values.tolist()
    released=reco_df.released.values.tolist()
    rating=reco_df.rating.values.tolist()
    genres=[str(x).strip("[]") for x in reco_df.genres.values.tolist()]
    platforms=[str(x).strip("[]") for x in reco_df.parent_platforms.values.tolist()]
    stores=reco_df.stores.values.tolist()
    games_list=[posters,games,released,rating,genres,platforms,stores]

    return games_list
