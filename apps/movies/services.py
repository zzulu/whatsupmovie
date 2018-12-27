from math import sqrt
from django.contrib.auth.models import User
from numpy import seterr, corrcoef, isnan

def pearson(x, y):
    intersection = x.keys() & y.keys()
    x_values = [x[n] for n in intersection]
    y_values = [y[n] for n in intersection]

    seterr(divide='ignore', invalid='ignore') # ignore divide by zero, invalid case
    r = corrcoef(x_values, y_values)[0,1] 
    return r if not isnan(r) else 1

# Get Pearson Correlation Coefficient
def get_pcc(current_user, current_user_ratings):
    users = User.objects.prefetch_related('rating_set').exclude(pk=current_user.pk)

    result = []
    for user in users:
        user_ratings = dict(user.rating_set.filter(movie__in=current_user_ratings.keys()).values_list('movie_id','score'))
        result.append((pearson(current_user_ratings, user_ratings), user))

    return sorted(result[:5], reverse=True, key=lambda p: p[0])

def get_recommended_movies(current_user):
    current_user_ratings = dict(current_user.rating_set.values_list('movie_id','score'))
    pcc = get_pcc(current_user, current_user_ratings)
    print(pcc)
    
    sum_score = {} # 영화별 평점 합
    sum_r = {} # 영화별 유사도 합
    for r, user in pcc:
        if r > 0:
            for movie_title, score in user.rating_set.exclude(movie__in=current_user_ratings.keys()).values_list('movie__title','score'): 
                sum_score.setdefault(movie_title, 0) 
                sum_score[movie_title] += score * r # 영화 평점 * 유사도
 
                sum_r.setdefault(movie_title, 0) 
                sum_r[movie_title] += r
 
    result = []
    for movie_title, score in sum_score.items():
        result.append(((score / sum_r[movie_title]), movie_title))

    return sorted(result, reverse=True)
