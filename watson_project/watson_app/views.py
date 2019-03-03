from django.shortcuts import render
from django.http import HttpResponse
import json
import requests

# Create your views here.
from django.views.generic.edit import FormView
from .forms import CommentForm

import json
from os.path import join, dirname
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, CategoriesOptions, ConceptsOptions, EntitiesOptions, KeywordsOptions, RelationsOptions, MetadataOptions



name=''
age=''

natural_language_understanding = NaturalLanguageUnderstandingV1(
   version='2018-11-17',
   iam_apikey='EOzxlpOmLm_Nt9INGu2qLlzZkxOSKhvNFMzDxOBWT1_t',
   url='https://gateway-fra.watsonplatform.net/natural-language-understanding/api'
)

#txt='Rohan Saxena is very talented. He lives in Kolkata. He is a good friend of Nikhil Jain who is 16 years old. His number is 1234567890123456.

"""-----------------------------------------------------------------------"""
"""NLU Service from IBM Cloud"""


def index(request):

    if request.method == 'POST':
        form =CommentForm(request.POST)
        if form.is_valid():

            name =form.cleaned_data['txt']

            print(name)

            # Watson dependencies

            txt=name


            response1 = natural_language_understanding.analyze(
               text=txt,
               features=Features(entities=EntitiesOptions(sentiment=False,model='2607453f-47be-46d9-8d1e-671ed0f5280d',limit=50))).get_result()

            response2 = natural_language_understanding.analyze(
               text=txt,
               features=Features(entities=EntitiesOptions(sentiment=False,limit=50))).get_result()

            #
            # print(json.dumps(response1, indent=2))
            # print(json.dumps(response2, indent=2))

            # print(json.dumps(response4, indent=2))

            # print(json.dumps(response5, indent=2))


            """extracting data from json"""

            """extracting data from json"""
            aadhar_list=[]
            locate1={}
            i=0
            l=len(response1['entities'])
            for i in range(l):
                locate1=response1['entities'][i]
                flag=0
                for key,values in locate1.items():
                    if flag==1:
                        aadhar_list.append(values)
                        flag=0
                        continue
                    if values=='aadharno':
                        flag=1
                        continue
                    flag=0

                i=i+1

            print(aadhar_list)

            info_list=[]
            locate2={}
            i=0
            l=len(response2['entities'])

            for i in range(l):
                locate2=response2['entities'][i]
                flag=0
                for key,values in locate2.items():
                    if flag==1:
                        info_list.append(values)
                        flag=0
                        continue
                    if values=='Person' or values=='Location' or values=='Company' :
                        flag=1
                        continue
                    flag=0

                i=i+1
            print(info_list)

            aadhar_list_singled=[]
            for j in range(len(aadhar_list)):
                for word in aadhar_list[j].split():
                    aadhar_list_singled.append(word)

            info_list_singled=[]
            for j in range(len(info_list)):
                for word in info_list[j].split():
                    if word=='years':
                        continue
                    info_list_singled.append(word)


            print(info_list_singled)

            txt1=txt.replace(".","")
            txt1=txt1.replace(",","")




            for word in txt1.split():
                # print(word)
                if word in aadhar_list or word in info_list_singled:
                    len_word=len(word)
                    mask="x"*len_word
                    txt=txt.replace(word,mask)

            print(txt)

            # Watson authentication
            #alchemy_language = NaturalLanguageUnderstandingV1(api_key=APIKEY)

            if txt != "" :
                form=txt
                return render(request, './watson_app/comment1.html',{'form':form})






    form=CommentForm()
    return render(request, './watson_app/comment.html',{'form':form})






class CommentView(FormView):
    template_name = 'comment.html'
    form_class = CommentForm
    success_url = '.'

    def form_valid(self, form):
        serialized_json = json.dumps(form.ask_watson() , sort_keys=True, indent=4)
        return HttpResponse(serialized_json, content_type="application/json")
