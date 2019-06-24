import numpy as np
import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

TITULO="Tweets sobre Bolsonaro"
QUERY='bolsonaro'
class TweetterBigData(object):

    def __init__(self):
        # Chaves e tokens. Cadastrar API no Tweeter

        # autenticacao
        try:
            consumer_key='7BaiwVN9g6jQVRP72qUqyRDlB'
            consumer_secret = 'rDFun0w15jVcLmO8Ctk7g04Xeblx9MZJLEPLneEXoqqSuNBehk'
            access_token = '876812531481882628-KSUZx4Qb29SCYnnEErOF4ATWbei56nC'
            access_token_secret = 'xqsO7f4f8tGopFfcTZovAJyqPp1OY1Ud0rnfpjuEiXun7'

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

    def obter_tweetes(self, query, count=10000000):
        '''
        funcao que faz a obtencao dos tweets e o parse dos mesmos.
        '''
        # lista para armazenar os tweets
        tweets = []

        try:
            # chama API do tweetes para obter ps tweets
            fetched_tweets = self.api.search(q=query, count=count, result_type='recent', locale='pt')

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


def plotarGraficoPizza(sizes, labels):
    # Pie chart, where the slices will be ordered and plotted counter-clockwise:
    explode = (0.1, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

    fig1, ax1 = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))
    wedges, texts, autotexts = ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.


    plt.setp(autotexts, size=20, weight="bold")
    ax1.set_title(TITULO, fontdict={'fontsize': 40, 'fontweight': 'bold'})

    plt.legend()
    plt.show()


def main():
    api = TweetterBigData()
    # chamando function para obter os tweetes
    tweets = api.obter_tweetes(query=QUERY, count=10000000)

    #Obtendo os tweeetes positivos
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positivo']
    # Percentual de Tweetes positivos
    positivos = 100 * len(ptweets) / len(tweets)
    print("Percentual de tweetes positivos: {} %".format(positivos))
    # pegando tweets negativos de tweets
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negativo']
    # Percentual de Tweetes positivos
    negativos = 100 * len(ntweets) / len(tweets)
    print("Percentual de tweetes negativos: {} %".format(negativos))
    # percentual de tweets neutros
    qtT = len(tweets)
    qtN = len(ntweets)
    ctP = len(ptweets)
    neutros = 100 * (qtT - (qtN + ctP)) / len(tweets)
    print("Percentual de Tweetes neutros: {} %".format(neutros))

    # Mostra os primeiros 5 tweets positivos
    print("\n\nTweetes positivos:")
    for tweet in ptweets[:50]:
        print(tweet['text'])

    # Mostra os primeiros 5 tweets negativos
    print("\n\nTweetes negativos:")
    for tweet in ntweets[:50]:
        print(tweet['text'])

    plotarGraficoPizza([positivos, negativos], ['Positivos', 'Negativos'])

if __name__ == "__main__":
    main()