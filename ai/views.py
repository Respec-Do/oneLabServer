import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
import pandas as pd
from community.models import Community
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class AiView(View):
    def post(self, request):
        print('들어옴')
        data = json.loads(request.body)
        title = data.get('title')
        print(title)

        radio_active = data.get('radio_active')
        print(radio_active)

        translated_radio = self.translate_status(radio_active)
        print(translated_radio)

        summed_title = title + ' ' + translated_radio
        print(summed_title)

        similar_communities = self.get_similar_communities(summed_title)
        print(similar_communities)

        return JsonResponse({'similar_communities': similar_communities})

    def get_similar_communities(self, title):

        communities = Community.objects.all()

        df = self.make_dataframe(communities)

        count_v = CountVectorizer()
        count_matrix = count_v.fit_transform(df['combined_features'])

        title_vector = count_v.transform([title])

        c_s = cosine_similarity(count_matrix, title_vector)

        similar_community = list(enumerate(c_s))
        similar_community_sorted = sorted(similar_community, key=lambda x: x[1], reverse=True)

        similar_communities = []
        similar_content = []

        for i in range(1, 4):
            index = similar_community_sorted[i][0]
            title = df.iloc[index]['community_title']
            similar_communities.append(title)
            content = df.iloc[index]['community_content']
            similar_content.append(content)

        return similar_content
    def make_dataframe(self, communities):
        columns = ['community_title', 'community_content', 'post_status']

        df = pd.DataFrame(list(communities.values('community_title', 'community_content', 'post_status')))

        df['post_status'] = df['post_status'].apply(self.translate_status)
        df['combined_features'] = df.apply(self.concatenate, axis=1)
        return df

    def translate_status(self, x):
        if x == "3":
            return '기타'
        elif x == "2":
            return '질문'
        elif x == "1":
            return '자료요청'

    def concatenate(self, features):
        return features.community_title + ' ' + features.community_content + ' ' + features.post_status

    def get_index_from_title(self, df, title):
        return df[df.community_title == title].index[0]