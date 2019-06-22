import numpy as np
import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob


class TweetterBigData(object):

    def __init__(self):
        # Chaves e tokens. Cadastrar API no Tweeter
        consumer_key = '7BaiwVN9g6jQVRP72qUqyRDlB'
        consumer_secret = 'rDFun0w15jVcLmO8Ctk7g04Xeblx9MZJLEPLneEXoqqSuNBehk'
        access_token = '876812531481882628-KSUZx4Qb29SCYnnEErOF4ATWbei56nC'
        access_token_secret = 'xqsO7f4f8tGopFfcTZovAJyqPp1OY1Ud0rnfpjuEiXun7'

        # autenticacao
        try:
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            # seta access token e secret
            self.auth.set_access_token(access_token, access_token_secret)
            # cria objeto de API com as credenciais
            self.api = tweepy.API(self.auth)
        except:
            print("Erro: Falha na autenticacao")

    def formatar_texto_tweet(self, tweet):
        '''
        funcao utilitaria que formata o texto do tweet removendo caracteres para facilitar analise
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\ / \ / \S+)", " ", tweet).split())

    def obter_sentimento_tweet(self, tweet):
        #Funcao utilitaria que classifica o sentimento do tweet passado

        # cria um TextBlob object passando o texto do tweet
        analysis = TextBlob(self.formatar_texto_tweet(tweet))
        # define o sentimento com base na polarity
        if analysis.sentiment.polarity > 0:
            return 'positivo'
        elif analysis.sentiment.polarity == 0:
            return 'neutro'
        else:
            return 'negativo'

    def obter_tweetes(self, query, count=50):
        '''
        funcao que faz a obtencao dos tweets e o parse dos mesmos.
        '''
        # lista para armazenar os tweets
        tweets = []

        try:
            # chama API do tweetes para obter ps tweets
            fetched_tweets = self.api.search(q=query, count=count)

            # faz o parse dos tweets um por um
            for tweet in fetched_tweets:
                # dictionary vazio para armazenar os parametros essenciais do tweet
                parsed_tweet = {}

                # armazena o texto do tweet
                parsed_tweet['text'] = tweet.text
                # armazena o sentimento do tweet
                parsed_tweet['sentiment'] = self.obter_sentimento_tweet(tweet.text)

                # faz append na list de tweets
                if tweet.retweet_count > 0:
                    # Se o tweet tiver retweets, garantir que ele seja anexado apenas uma vez
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)

            return tweets

        except tweepy.TweepError as e:
            print("Erro : " + str(e))


def main():
    api = TweetterBigData()
    # chamando function para obter os tweetes
    tweets = api.obter_tweetes(query='Bolsonaro', count=200)

    #Obtendo os tweeetes positivos
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positivo']
    # Percentual de Tweetes positivos
    print("Percentual de tweetes positivos: {} %".format(100 * len(ptweets) / len(tweets)))
    # pegando tweets negativos de tweets
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negativo']
    # Percentual de Tweetes positivos
    print("Percentual de tweetes negativos: {} %".format(100 * len(ntweets) / len(tweets)))
    # percentual de tweets neutros
    qtT = len(tweets)
    qtN = len(ntweets)
    ctP = len(ptweets)
    qt = 100 * (qtT - (qtN + ctP)) / len(tweets)
    print("Percentual de Tweetes neutros: {} %".format(qt))

    # Mostra os primeiros 5 tweets positivos
    print("\n\nTweetes positivos:")
    for tweet in ptweets[:10]:
        print(tweet['text'])

    # Mostra os primeiros 5 tweets negativos
    print("\n\nTweetes negativos:")
    for tweet in ntweets[:10]:
        print(tweet['text'])

if __name__ == "__main__":
    main()