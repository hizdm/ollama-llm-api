# -*- coding: utf-8 -*-
# Author: zzl
# Date: 2025.01.08

import chromadb

"""
ChromaDB数据库基础操作类
"""
class ChromaHelper:
    def __init__(self, persist_directory: str = "./chromadb_data"):
        self.client = chromadb.PersistentClient(persist_directory)
        # self.client = chromadb.HttpClient(host='localhost', port=8000)

    """
    @brief 创建集合
    """
    def createCollection(self, name: str):
        try:
            if name in self.client.list_collections():
                # raise ValueError(f"Collection '{name}' already exists.")
                return False
            return self.client.create_collection(name)
        except Exception as e:
            return False

    """
    @brief 获取集合
    """
    def getCollection(self, name: str):
        try:
            return self.client.get_collection(name)
        except Exception as e:
            # raise ValueError(f"Collection '{name}' does not exist. Error: {e}")
            return False

    """
    @brief 删除集合
    """
    def deleteCollection(self, name: str):
        try:
            self.client.delete_collection(name)
        except Exception as e:
            # raise ValueError(f"Failed to delete collection '{name}'. Error: {e}")
            return False

    """
    @brief 添加文档
    """
    def addDocuments(self, collection_name: str, ids: list, documents: list, metadatas: list = None, embeddings: list = None):
        if not ids or not documents or len(ids) != len(documents):
            # raise ValueError("'ids' and 'documents' must have the same length and cannot be empty.")
            return False
        collection = self.client.get_collection(collection_name)
        collection.add(ids=ids, documents=documents, metadatas=metadatas, embeddings=embeddings)
        return True

    """
    @brief 查询文档
    """
    def queryDocuments(self, collection_name: str, query_embeddings: list, n_results: int = 5):
        collection = self.client.get_collection(collection_name)
        return collection.query(query_embeddings=query_embeddings, n_results=n_results)

    """
    @brief 删除文档
    """
    def deleteDocuments(self, collection_name: str, ids: list):
        if not ids:
            return False
            # raise ValueError("'ids' cannot be empty.")

        collection = self.get_collection(collection_name)
        collection.delete(ids=ids)

    """
    @brief 获取集合列表
    """
    def listCollections(self):
        return self.client.list_collections()


# # Demo of usage
# def main():
#     # Initialize ChromaDB Manager
#     db_manager = ChromaHelper(persist_directory="./chromadb_data")

#     # Create a collection
#     collection_name = "test_collection003"
#     try:
#         db_manager.create_collection(collection_name)
#         print(f"Collection '{collection_name}' created.")
#     except ValueError as e:
#         print(e)

#     # Add documents to the collection
#     ids = ["doc1", "doc2", "doc3", "doc4"]
#     documents = [
#         "This is the first document.",
#         "This is the second document.",
#         "This is the third document.",
#         "This is the first sql."
#     ]
#     db_manager.add_documents(collection_name, ids, documents)
#     print(f"Added {len(documents)} documents to '{collection_name}'.")

#     # Query the collection
#     query_result = db_manager.query_documents(collection_name, ["first document sql"], n_results=2)
#     print("Query result:", query_result)

#     # List all collections
#     print("Collections:", db_manager.list_collections())

#     # Delete a document
#     db_manager.delete_documents(collection_name, ["doc1"])
#     print("Deleted 'doc1'.")

if __name__ == "__main__":
    pass
    # main()
