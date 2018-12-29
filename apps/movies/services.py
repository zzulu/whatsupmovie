from django.conf import settings
import requests
from bs4 import BeautifulSoup
from django.core.files.uploadedfile import SimpleUploadedFile
from math import sqrt
from numpy import seterr, corrcoef, isnan
from django.contrib.auth.models import User
from .models import Movie

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
    
    sum_score = {} # 영화별 평점 합
    sum_r = {} # 영화별 유사도 합
    for r, user in pcc:
        if r > 0:
            for movie_id, score in user.rating_set.exclude(movie__in=current_user_ratings.keys()).values_list('movie_id','score'): 
                sum_score.setdefault(movie_id, 0) 
                sum_score[movie_id] += score * r # 영화 평점 * 유사도
 
                sum_r.setdefault(movie_id, 0) 
                sum_r[movie_id] += r
 
    result = []
    for movie_id, score in sum_score.items():
        result.append(((score / sum_r[movie_id]), Movie.objects.get(pk=movie_id)))

    return sorted(result, reverse=True, key=lambda m: m[0])[:12] # 추천 최대 12개까지만


def set_movie_posters():
    movies = Movie.objects.all()

    for movie in movies:
        print(movie.pk)
        url = 'https://openapi.naver.com/v1/search/movie.json'
        headers = {
            'X-Naver-Client-Id': settings.X_NAVER_CLIENT_ID,
            'X-Naver-Client-Secret': settings.X_NAVER_CLIENT_SECRET
        }

        query = movie.title

        res = requests.get(url, params={'query': query}, headers=headers)
        info = res.json()

        if info.get('items')[0] is not None:
            movie_code = info.get('items')[0].get('link').split('?code=')[-1]

            url = f'https://movie.naver.com/movie/bi/mi/photoViewPopup.nhn?movieCode={movie_code}'

            res = requests.get(url).text
            img_tag = BeautifulSoup(res, 'html.parser').select_one('#targetImage')

            if img_tag is not None:
                img_url = img_tag.get('src')

                binary_img_file = requests.get(img_url, stream=True).raw.read()

                movie.image = SimpleUploadedFile(str(movie.pk), binary_img_file)
                movie.save()

    return 'Complete.'
