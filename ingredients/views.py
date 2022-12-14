from django.shortcuts import render,redirect
from django.views.generic import ListView,DetailView,CreateView,UpdateView
from .models import Post,MnistImage
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.utils.text import slugify
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np
import pandas as pd
import logging
import tensorflow as tf
from django.db import models
from django import forms 
from django.shortcuts import render,redirect
from .models import Post, RecipeList
from .forms import TextForm
from PIL import Image
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
import logging
from django.shortcuts import render
from django.db import connection
from django.db.models.query_utils import Q
import operator
from functools import reduce


###### 나의 냉장고 목록
def post_list(request):
    posts = Post.objects.all().order_by('-pk') # 데이터베이스에 쿼리를 날려 원하는 레코드 가져오기

    return render(
        request,
        'ingredients/post_list.html',
        {
            'posts':posts,
        }
    )


###### 로그 함수
# 로그 생성
logger = logging.getLogger()
# 로그의 출력 기준 설정
logger.setLevel(logging.INFO)
# log 출력 형식
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# log 출력
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
# log를 파일에 출력
file_handler = logging.FileHandler('my.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


###### 선택 삭제
@csrf_exempt
def delete_all(request):
    logger.info('================ delete_all')
    
    if(request.method == 'POST'):
        ids = request.POST["del_ids"]
        ids = ids.split(',')
        for idx in range(len(ids)):
            id = ids[idx]
            ingredient = Post.objects.get(id=id)
            ingredient.delete()
            
            logger.info('deleted.....')
        
        return redirect('ingredients')


###### 선택 레시피 추천    
@csrf_exempt
def recommend(request):
    logger.info('================ recommend')
    
    if(request.method == 'POST'):
        ids = request.POST["rec_ids"]
        ids = ids.split(',')
        keywords = ''
        
        q_list = []
        
        for idx in range(len(ids)):
            id = ids[idx]
            ingredient = Post.objects.get(id=id)
            keyword = ingredient.ingredient
            keywords += ' ' + keyword
            
            query = Q(rc_ing__icontains=keyword)
            q_list.append(query)
                
        
        logger.info(q_list)
        recipe_list = RecipeList.objects.all()
        recipe_list = recipe_list.filter(reduce(operator.and_, q_list)).order_by('-rc_rec')
        print(recipe_list[0].rc_name)   
        
    return render(
            request,
            'ingredients/recipe_list.html',{'recipe_list':recipe_list,'keywords': keywords})
    
    
###### 텍스트로 입력          
def upload_text(request):
    if(request.method == 'POST'):
        form=TextForm(request.POST)
        if form.is_valid():
            ing = form.save(commit=False)
            ing.save()
            return redirect('ingredients')
    else:
        form=TextForm()
    context={'form':form}
    return render(
            request,
            'ingredients/upload_text.html',context)


###### 이미지로 입력(모델 적용)
class MnistImageCreate(CreateView):
    model= MnistImage
    fields=['head_image']

def image_result(request,pk):
    data = MnistImage.objects.get(pk=pk)
    
    logging.basicConfig(level=logging.WARNING)
    logging.debug('Here you have some information for debugging.')
    logging.info('Everything is normal. Relax!')
    logging.warning('Something unexpected but not important happend.')
    logging.error('Something unexpected and important happened.')
    logging.critical('OMG!!! A critical error happend and the code cannot run!')
    
    img = np.array(Image.open(data.head_image).resize((128, 128)))
    img_list = []
    img_list.append(np.array(img))
    x = np.asarray(img_list)
    
    loaded_model = load_model("model_lb5_128_plus_vgg_8282.h5")
    pred = loaded_model.predict(x)
    pred = np.argmax(pred[0])
    
    label_index = ['당근', '계란', '대파', '양파', '깻잎']
    result = label_index[pred]
    
    data.result = result
    data.save()
    
    try:
        cursor = connection.cursor()
        query = '''INSERT INTO ingredients_post (ingredient)
                    SELECT result
                    FROM ingredients_mnistimage
                    WHERE id=(
                        SELECT max(id) FROM ingredients_mnistimage
                        )'''
        results = cursor.execute(query)
        stocks = cursor.fetchall()

        connection.commit()
        connection.close()

    except:
        connection.rollback()
        print("Failed Selecting in StockList")
    
    return render(
        request,
        'ingredients/result.html',
        {
            'result':result,
        }
    )
    

###### 레시피 페이지    
def recipe_list(request):
    recipelists = RecipeList.objects.all()


    return render(
        request,
        'ingredients/recipe_list.html',
        {
            'recipelists':recipelists,
        }
    )
