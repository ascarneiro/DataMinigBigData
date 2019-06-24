from TwitterSearch import *
try:

    ts = TwitterSearch(
        # Chaves e tokens. Cadastrar API no Tweeter
        consumer_key='7BaiwVN9g6jQVRP72qUqyRDlB',
        consumer_secret='rDFun0w15jVcLmO8Ctk7g04Xeblx9MZJLEPLneEXoqqSuNBehk',
        access_token='876812531481882628-KSUZx4Qb29SCYnnEErOF4ATWbei56nC',
        access_token_secret='xqsO7f4f8tGopFfcTZovAJyqPp1OY1Ud0rnfpjuEiXun7'

    )

    tso = TwitterSearchOrder()
    tso.set_keywords(['bolsonaro']) #Palavra a pesquisar
    tso.set_language('pt') #Linguagem

    for tweet in ts.search_tweets_iterable(tso):
        print('@%s tweetado: %s' % (tweet['user']['screen_name'], tweet['text']))

except TwitterSearchException as e:
    print(e)