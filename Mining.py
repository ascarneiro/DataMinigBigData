from TwitterSearch import *
try:

    ts = TwitterSearch(
        consumer_key = '', #We need yet
        consumer_secret = '', #We need yet
        access_token = '', #We need yet
        access_token_secret = '', #We need yet
     )

    tso = TwitterSearchOrder()
    tso.set_keywords(['iphone']) #Palavra a pesquisar
    tso.set_language('pt') #Linguagem

    for tweet in ts.search_tweets_iterable(tso):
        print( '@%s tweeted: %s' % ( tweet['user']['screen_name'], tweet['text'] ) )

except TwitterSearchException as e:
    print(e)