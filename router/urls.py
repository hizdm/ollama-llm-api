# -*- coding: utf-8 -*-
# Author: zzl
# Date: 2024.07.15

from controller import home # home page
from controller import chat
from controller import auth
from controller import generate
from controller import embeddings
from controller import rag
from controller import chroma

# Routers
urls = [
    (r"/", home.IndexHandler),
    (r"/rag", rag.RagHandler),
	(r"/auth", auth.AuthHandler),
	(r"/chat", chat.ChatHandler),
	(r"/generate", generate.GenerateHandler),
	(r"/embeddings", embeddings.EmbeddingsHandler),
	(r"/createcollection", chroma.CreateCollectionHandler),
	(r"/adddocument", chroma.AddDocumentHandler),
	(r"/querydocument", chroma.QueryDocumentHandler),
	(r"deletecollection", chroma.DeleteCollectionHandler)
]