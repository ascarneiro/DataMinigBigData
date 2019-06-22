from TwitterSearch import *
try:

    ts = TwitterSearch(
        # Chaves e tokens. Cadastrar API no Tweeter

    )

    tso = TwitterSearchOrder()
    tso.set_keywords(['bolsonaro']) #Palavra a pesquisar
    tso.set_language('pt') #Linguagem

    for tweet in ts.search_tweets_iterable(tso):
        print('@%s tweetado: %s' % (tweet['user']['screen_name'], tweet['text']))

except TwitterSearchException as e:
    print(e)