import numpy
from vaderSentiment import SentimentIntensityAnalyzer
from host_name import filter_tweets
import matplotlib.pyplot as plt

corpus = numpy.load("tweetsarray.npy")


def evaluate_reaction(identifiers, corpus):
    relevant_twts = [twt_dict['tweet_text'] for twt_dict in filter_tweets(identifiers, corpus)]
    num_twts = len(relevant_twts)
    metrics = numpy.ndarray(shape=(num_twts, 4))
    sid = SentimentIntensityAnalyzer()

    for i, twt in enumerate(relevant_twts):
        ss = sid.polarity_scores(twt)
        metrics[i, :] = [ss['compound'], ss['pos'], ss['neg'], ss['neu']]

    score_order = ['compound', 'positive', 'negative', 'neutral']
    avg_scores = numpy.average(metrics, axis=0)
    for i in range(0, 4):
        print score_order[i] + ": " + str(avg_scores[i])

    return metrics

def plot_distributions(metrics, search_term):
    # plt.figure()
    ttl = "Response Sentiment Distribution for " + search_term
    f, axarr = plt.subplots(2, 2)
    plt.suptitle(ttl)
    axarr[0, 0].hist(metrics[:, 0], bins='auto')
    axarr[0, 0].set_title('Composite Score')
    axarr[0, 1].hist(metrics[:, 1], bins='auto')
    axarr[0, 1].set_title('Positive Scores')
    axarr[1, 0].hist(metrics[:, 2], bins='auto')
    axarr[1, 0].set_title('Negative Scores')
    axarr[1, 1].hist(metrics[:, 3], bins='auto')
    axarr[1, 1].set_title('Neutral Scores')
    plt.show()
    print numpy.average(metrics, axis=0)
    return metrics

jfm = evaluate_reaction(['Jimmy', 'Fallon', 'jimmyfallon'], corpus)
plot_distributions(jfm, "Jimmy Fallon")
# print 'Meryll Streep scores'
# evaluate_reaction(['Meryll', 'Streep', 'meryllstreep'], corpus)
# print 'Ryan Gosling scores'
# evaluate_reaction(['Ryan', 'Gosling', 'ryangosling'], corpus)
# print 'Emma Stone scores'
# evaluate_reaction(['Emma', 'Stone', 'emmastone'], corpus)
# print 'Viola Davis scores'
# evaluate_reaction(['Viola', 'Davis', 'violadavis'], corpus)