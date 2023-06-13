import openai
import pandas as pd
from flask import session
import numpy as np
import tiktoken
from datetime import date
from app.tokenizer import num_tokens_from_string
import os
from dotenv import load_dotenv

from app.controller import QuestionController
from app.model.question import Question

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

COMPLETIONS_MODEL = "text-davinci-002"
EMBEDDING_MODEL = "text-embedding-ada-002"

# conversation = []
# userData = {}

try:
    df = pd.read_csv('data.csv', encoding="cp1252")
    df = df.set_index(["title", "heading"])
except:
    df = pd.DataFrame()

#print(df)

def get_embedding(text: str, model: str=EMBEDDING_MODEL) -> list[float]:
    result = openai.Embedding.create(
      model=model,
      input=text
    )
    return result["data"][0]["embedding"]


# print(len(get_embedding("Apa itu hukum Perkawinan?")))

# def compute_doc_embeddings(df: pd.DataFrame) -> dict[tuple[str, str], list[float]]:
#     """
#     Create an embedding for each row in the dataframe using the OpenAI Embeddings API.
    
#     Return a dictionary that maps between each embedding vector and the index of the row that it corresponds to.
#     """
#     return {
#         idx: get_embedding(r.content) for idx, r in df.iterrows()
#     }

def compute_doc_embeddings(df: pd.DataFrame) -> dict[tuple[str, str], list[float]]:
    """
    Create an embedding for each row in the dataframe using the OpenAI Embeddings API.
    
    Return a new dataframe with columns "title", "heading", and the embedding values.
    """
    data = []
    df = df.reset_index()
    for idx, r in df.iterrows():

        embedding = get_embedding(f"{r.heading} - {r.content}")
        row = [r.id_data, r.title, r.heading] + embedding
        data.append(row)
        
    return pd.DataFrame(data, columns=["id_data","title", "heading"] + [f"{i}" for i in range(len(embedding))])



#print(df)

def load_embeddings(fname: str) -> dict[tuple[str, str], list[float]]:
    """
    Read the document embeddings and their keys from a CSV.
    
    fname is the path to a CSV with exactly these named columns: 
        "title", "heading", "0", "1", ... up to the length of the embedding vectors.
    """
    
    df = pd.read_csv(fname, header=0)
    max_dim = max([int(c) for c in df.columns if c != "id_data" and c != "title" and c != "heading"])
    return {
           (r.title, r.heading): [r[str(i)] for i in range(max_dim + 1)] for _, r in df.iterrows()
    }



if not df.empty:
    document_embeddings = load_embeddings("data_embedding.csv")
else:
    document_embeddings = {}


##===== OR, uncomment the below line to recalculate the embeddings from scratch. after that comment again========

# df = compute_doc_embeddings(df)
# df.to_csv('dataset_tokens_embeddings.csv', index=False)


#An example embedding:
# example_entry = list(document_embeddings.items())[0]
# print(f"{example_entry[0]} : {example_entry[1][:5]}... ({len(example_entry[1])} entries)")



def vector_similarity(x: list[float], y: list[float]) -> float:
    """
    Returns the similarity between two vectors.
    
    Because OpenAI Embeddings are normalized to length 1, the cosine similarity is the same as the dot product.
    """
    return np.dot(np.array(x), np.array(y))

def order_document_sections_by_query_similarity(query: str, contexts: dict[(str, str), np.array]) -> list[(float, (str, str))]:
    """
    Find the query embedding for the supplied query, and compare it against all of the pre-calculated document embeddings
    to find the most relevant sections. 
    
    Return the list of document sections, sorted by relevance in descending order.
    """
    query_embedding = get_embedding(query)
    
    document_similarities = sorted([
        (vector_similarity(query_embedding, doc_embedding), doc_index) for doc_index, doc_embedding in contexts.items()
    ], reverse=True)
    
    return document_similarities

# query1 = get_embedding("Apa itu perkawinan")
# query2 = get_embedding("Perkawinan ialah ikatan lahir bathin antara seorang pria dengan seorang wanita sebagai suami isteri dengan tujuan membentuk keluarga (rumah tangga) yang bahagia dan kekal berdasarkan Ketuhanan Yang Mahaesa.")

# dot_product = vector_similarity(query1,query2)

# magnitude1 = np.linalg.norm(query1)
# magnitude2 = np.linalg.norm(query2)

# similarity = dot_product / (magnitude1 * magnitude2)

# print(dot_product, similarity)

# pv = ""
# dv = ""

# np.dot(pv,dv) / (np.linalg.norm(pv) * np.linalg.norm(dv))

#print(order_document_sections_by_query_similarity("perkawinan", document_embeddings)[:5])

MAX_SECTION_LEN = 750
SEPARATOR = "\n* "
ENCODING = "cl100k_base"  # encoding for text-embedding-ada-002

encoding = tiktoken.get_encoding(ENCODING)
separator_len = len(encoding.encode(SEPARATOR))

f"Context separator contains {separator_len} tokens"


today = date.today()
formatted_date = today.strftime("%d %B %Y")
indonesian_months = {
    "January": "Januari",
    "February": "Februari",
    "March": "Maret",
    "April": "April",
    "May": "Mei",
    "June": "Juni",
    "July": "Juli",
    "August": "Agustus",
    "September": "September",
    "October": "Oktober",
    "November": "November",
    "December": "Desember"
}

for english, indonesian in indonesian_months.items():
    formatted_date = formatted_date.replace(english, indonesian)




def construct_prompt(question: str, context_embeddings: dict, df: pd.DataFrame) -> str:
    """
    Fetch relevant 
    """
    most_relevant_document_sections = order_document_sections_by_query_similarity(question, context_embeddings)
    
    chosen_sections = []
    chosen_sections_len = 0
    chosen_sections_indexes = []
    
    for _, section_index in most_relevant_document_sections:
        # Add contexts until we run out of space. 
        #document_section = df.loc[section_index].iloc[0]
        document_section = df.xs(section_index, level=[0,1]).iloc[0]
        
        chosen_sections_len += document_section.tokens + separator_len
        if chosen_sections_len > MAX_SECTION_LEN:
            break
            
        chosen_sections.append(SEPARATOR + document_section.content.replace("\n", " "))
        #chosen_sections.append(SEPARATOR + document_section.content)
        chosen_sections_indexes.append(str(section_index))
            
    ## Useful diagnostic information
    #print(most_relevant_document_sections)
    # print(f"Selected {len(chosen_sections)} document sections:")
    # print("\n".join(chosen_sections_indexes))
    
    
    #Jawab pertanyaan secara jujur hanya dengan menggunakan konteks yang disediakan, dan jika jawabannya tidak terdapat dalam teks atau konteks di bawah , katakan "Maaf, Saya tidak mengetahui terkait informasi tersebut.".

    header = """Anda adalah LARA, sebuah chatbot konsultan hukum. Tanggal hari ini adalah """ + formatted_date +""". Nama pengguna adalah """+ str(session['userData']['nama']) + """, email adalah """ + str(session['userData']['email']) + """, usia adalah """ + str(session['userData']['usia']) + """ dan seorang """ + str(session['userData']['jk']) + """.
    Patuhi instruksi dibawah ini:
    1. tanyakan kembali rincian masalah jika belum mengerti.
    2. hanya menjawab pertanyaan menggunakan informasi yang diberikan. jika di luar Konteks, katakan bahwa informasi tersebut belum tersedia.
    3. berikan jawaban dengan cara yang jelas dan mudah dimengerti oleh pengguna yang tidak ahli dalam bidang hukum.

    Konteks:
    """
    #print(session['userData'])
    data = Question.query.filter_by(id_user=session['userData']['id_user']).all()
    raw_conversation = QuestionController.formatArray(data)
    #print(raw_conversation)
    raw_conversation.reverse()
    #print(raw_conversation)
    conversation = []


    prompt_size = num_tokens_from_string(header + "\n\n",COMPLETIONS_MODEL) + MAX_SECTION_LEN

    for i in raw_conversation:
        prompt_size += num_tokens_from_string(i['pertanyaan'] + i['jawaban'],COMPLETIONS_MODEL)
        if(prompt_size >= 2500):
            break
        else:
            conversation.append(i)

    #print(conversation)
    conversation.reverse()
    #print(conversation)

    questions = ""
    for i in conversation:
        questions += "Q:"+i["pertanyaan"] + "\nA:"+i["jawaban"]+ "\n"

    questions += "Q:"+question+ "\nA:"

    prompt = header + "".join(chosen_sections) + "\n\n" + questions

    return prompt

    questions = ""
    for i in conversation:
        questions += "Q:" + i["Q"] + "\nA:" + i["A"] + "\n"
    questions += "Q:" + new_question + "\nA:"

    prompt_size = num_tokens_from_string(questions, COMPLETIONS_MODEL) + 500
    while prompt_size > max_size and len(conversation) > 0:
        conversation.pop(0)
        questions = ""
        for i in conversation:
            questions += "Q:" + i["Q"] + "\nA:" + i["A"] + "\n"
        questions += "Q:" + new_question + "\nA:"
        prompt_size = num_tokens_from_string(questions, COMPLETIONS_MODEL) + 500

    return conversation

# prompt = construct_prompt(
#     "bolehkah memiliki 2 istri",
#     document_embeddings,
#     df
# )
# print("===\n", prompt)

# prompt = construct_prompt(
#     "Perkawinan dilarang antara dua orang yang:",
#     document_embeddings,
#     df
# )
# print("===\n", prompt)

COMPLETIONS_API_PARAMS = {
    # We use temperature of 0.0 because it gives the most predictable, factual answer.
    "temperature": 0,
    "max_tokens": 500,
    "model": COMPLETIONS_MODEL,
    "stop":["\n"]
}

# COMPLETIONS_API_PARAMS = {
#     # We use temperature of 0.0 because it gives the most predictable, factual answer.
#     "temperature": 0,
#     "max_tokens": 500,
#     "model": COMPLETIONS_MODEL
# }


def answer_query_with_context(
    query: str,
    df: pd.DataFrame,
    document_embeddings: dict[(str, str), np.array],
    show_prompt: bool = False
) -> str:
    prompt = construct_prompt(
        query,
        document_embeddings,
        df
    )
    
    if show_prompt:
        print(prompt)

    response = openai.Completion.create(
                prompt=prompt,
                **COMPLETIONS_API_PARAMS
            )
    
    return response["choices"][0]["text"].strip(" \n")
    #return response["usage"]



# query = "Perkawinan dilarang antara dua orang yang:. tampilkan dalam list"
# answer = answer_query_with_context(query, df, document_embeddings)

# print(f"\nQ: {query}\nA: {answer}")
