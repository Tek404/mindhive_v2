from rest_framework import serializers, generics
from .models import Outlet
from transformers import Pipeline

class OutletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Outlet
        fields = '__all__'

class OutletList(generics.ListAPIView):
    queryset = Outlet.objects.all()
    serializer_class = OutletSerializer

class OutletSearchList(generics.ListAPIView):
    serializer_class = OutletSerializer
    def get_queryset(self):
        query = self.request.query_params.get('query', '')
        outlets = Outlet.objects.all()

        if query:
            # use question-answering pipeline? inaccurate results
            nlp = pipeline("question-answering", model="bert-base-uncased")
            
            for outlet in outlets:
                if outlet.address:
                    outlet.description_score = nlp(query, outlet.address)['score']
                else:
                    outlet.description_score = 0  
            outlets = [outlet for outlet in outlets if outlet.description_score > 0.005]

        return outlets

# Rag version to generate answers? (doesnt work with current dataset, need external or modify own dataset)
    
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from transformers import RagRetriever, RagTokenizer, RagTokenForGeneration, pipeline
# from django.db.models import Q
# from .models import Outlet

# @csrf_exempt
# def search_outlets(request):
#     if request.method == 'POST':
#         query = request.POST.get('query', '')

#         relevant_data = get_relevant_data(query)
#         answer = generate_answer(query, relevant_data)

#         return JsonResponse({'answer': answer})

#     return JsonResponse({'error': 'Invalid request method'})

# def get_relevant_data(query):
#     outlets = Outlet.objects.all()
#     serializer = OutletSerializer(outlets, many=True)
#     return serializer.data

# def generate_answer(query, relevant_data):
#     # initialize RAG models
#     rag_tokenizer = RagTokenizer.from_pretrained("facebook/rag-token-base")
#     rag_retriever = RagRetriever.from_pretrained("facebook/rag-token-base", index_name="exact")
#     rag_generator = RagTokenForGeneration.from_pretrained("facebook/rag-token-base")

#     # prepare input for RAG
#     input_dict = rag_tokenizer.prepare_input(
#         query,
#         relevant_data,
#         return_tensors="pt",
#     )

#     retrieved_docs = rag_retriever.retrieve(input_dict)

#     generated_output = rag_generator.generate(**retrieved_docs, max_length=100)

#     answer = rag_tokenizer.batch_decode(generated_output, skip_special_tokens=True)[0]
#     return answer

