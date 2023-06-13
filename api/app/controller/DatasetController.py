from app.model.dataset import Dataset
from app import response, app, db, embedding_api as ea, tokenizer
from flask import request
import pandas as pd

def index():
    try:
        user = Dataset.query.all()
        data = formatArray(user)
        return response.succeed(data,"success")
    except Exception as e:
        print(e)

def formatArray(datas):
    array = []

    for i in datas:
        array.append(singleObject(i))
    
    return array

def singleObject(data):
    data = {
        'id_data': data.id_data,
        'title': data.title,
        'heading':data.heading,
        'content':data.content,
    }

    return data


def save():
    
    try:
        data = request.get_json()
        title = data['title']
        heading = data['heading']
        content = data['content']

        dataset = Dataset(title=title,heading=heading,content=content)

        db.session.add(dataset)
        db.session.flush()
        tokens = tokenizer.num_tokens_from_string(dataset.heading, "text-davinci-003") + tokenizer.num_tokens_from_string(dataset.content, "text-davinci-003")
        data = {
            'id_data':[dataset.id_data],
            'title':[dataset.title],
            'heading':[dataset.heading],
            'content':[dataset.content],
            'tokens':[tokens]
            }
        df = pd.DataFrame(data)
        df_embedding = ea.compute_doc_embeddings(df)

        


        # Load the existing CSV file (if it exists)
        try:
            existing_df = pd.read_csv('data.csv')
        except:
            existing_df = pd.DataFrame()

        try:
            existing_df_embedding = pd.read_csv('data_embedding.csv')
        except:
            existing_df_embedding = pd.DataFrame()

        # Append the new data to the existing DataFrame
        updated_df = pd.concat([existing_df, df], ignore_index=True)
        updated_df_embedding = pd.concat([existing_df_embedding, df_embedding], ignore_index=True)

        # Save the updated DataFrame to the CSV file
        updated_df.to_csv('data.csv', index=False)
        updated_df_embedding.to_csv('data_embedding.csv', index=False)

        # ea.df = updated_df.set_index(["title", "heading"])
        # ea.document_embeddings = ea.load_embeddings("data_embedding.csv")

        #print(ea.document_embeddings)
        db.session.commit()
        
        return response.succeed({
            'id_data':dataset.id_data,
            'title':dataset.title,
            'heading':dataset.heading,
            'content':dataset.content
            },"BERHASIL MENAMBAH")
    except Exception as e:
        print(e)
        return response.badRequest(False, "error")
    finally:
        db.session.close()


def update(id_data):
    try:
        data = request.get_json()
        title = data['title']
        heading = data['heading']
        content = data['content']

        #dataset = Dataset(title=title,heading=heading,content=content)
        dataset = Dataset.query.filter_by(id_data=id_data).first()
        dataset.title = title
        dataset.heading = heading
        dataset.content = content

        
        df = pd.read_csv('data.csv')
        df = df.set_index('id_data')
        
        tokens = tokenizer.num_tokens_from_string(dataset.heading, "text-davinci-003") + tokenizer.num_tokens_from_string(dataset.content, "text-davinci-003")
        df.loc[id_data, 'title'] = dataset.title
        df.loc[id_data, 'heading'] = dataset.heading
        df.loc[id_data, 'content'] = dataset.content
        df.loc[id_data, 'tokens'] = tokens

        df_embedding = pd.read_csv('data_embedding.csv')
        df_embedding = df_embedding.set_index('id_data')

        new_row = pd.DataFrame({
            'id_data':[dataset.id_data],
            'title': [dataset.title],
            'heading': [dataset.heading],
            'content': [dataset.content],
            'tokens': [tokens]
        })
        data = ea.compute_doc_embeddings(new_row)
        data = data.set_index('id_data')
        df_embedding.loc[id_data] = data.iloc[0]

        df = df.reset_index()
        df_embedding = df_embedding.reset_index()

        df.to_csv('data.csv', index=False)
        df_embedding.to_csv('data_embedding.csv', index=False)

        
        # ea.df = df.set_index(["title", "heading"])
        # ea.document_embeddings = ea.load_embeddings("data_embedding.csv")
        #print(ea.document_embeddings)

        db.session.commit()
        db.session.close()
        
        return response.succeed({
            'id_data':dataset.id_data,
            'title':dataset.title,
            'heading':dataset.heading,
            'content':dataset.content
            },"BERHASIL UPDATE")
    except Exception as e:
        print(e)
    finally:
        db.session.close()



def delete():
    try:
        data = request.get_json()
        ids = data['ids']

        for id in ids:
            dataset = Dataset.query.filter_by(id_data = id).first()
            db.session.delete(dataset)
        
        

        df = pd.read_csv('data.csv')
        df = df.set_index('id_data')
        df_embedding = pd.read_csv('data_embedding.csv')
        df_embedding = df_embedding.set_index('id_data')
        
        df = df.drop(ids)
        df_embedding = df_embedding.drop(ids)

        df = df.reset_index()
        df_embedding = df_embedding.reset_index()

        df.to_csv('data.csv', index=False)
        df_embedding.to_csv('data_embedding.csv', index=False)

        # ea.df = df.set_index(["title", "heading"])
        # ea.document_embeddings = ea.load_embeddings("data_embedding.csv")
        #print(ea.document_embeddings)

        db.session.commit()
        db.session.close()

        return response.succeed(ids,"BERHASIL MENGHAPUS")
    except Exception as e:
        print(e)
    finally:
        db.session.close()