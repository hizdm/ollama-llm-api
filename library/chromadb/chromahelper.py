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
    def create_collection(self, name: str):
        if name in self.client.list_collections():
            raise ValueError(f"Collection '{name}' already exists.")
        return self.client.create_collection(name)

    """
    @brief 获取集合
    """
    def get_collection(self, name: str):
        try:
            return self.client.get_collection(name)
        except Exception as e:
            raise ValueError(f"Collection '{name}' does not exist. Error: {e}")

    """
    @brief 删除集合
    """
    def delete_collection(self, name: str):
        try:
            self.client.delete_collection(name)
        except Exception as e:
            raise ValueError(f"Failed to delete collection '{name}'. Error: {e}")

    """
    @brief 添加文档
    """
    def add_documents(self, collection_name: str, ids: list, documents: list, metadatas: list = None):
        if not ids or not documents or len(ids) != len(documents):
            raise ValueError("'ids' and 'documents' must have the same length and cannot be empty.")

        collection = self.get_collection(collection_name)
        collection.add(ids=ids, documents=documents, metadatas=metadatas)

    """
    @brief 查询文档
    """
    def query_documents(self, collection_name: str, query_texts: list, n_results: int = 5):
        collection = self.get_collection(collection_name)
        return collection.query(query_texts=query_texts, n_results=n_results)

    """
    @brief 删除文档
    """
    def delete_documents(self, collection_name: str, ids: list):
        if not ids:
            raise ValueError("'ids' cannot be empty.")

        collection = self.get_collection(collection_name)
        collection.delete(ids=ids)

    """
    @brief 获取集合列表
    """
    def list_collections(self):
        return self.client.list_collections()


# Demo of usage
def main():
    # Initialize ChromaDB Manager
    db_manager = ChromaHelper(persist_directory="./chromadb_data")

    # Create a collection
    collection_name = "test_collection002"
    try:
        db_manager.create_collection(collection_name)
        print(f"Collection '{collection_name}' created.")
    except ValueError as e:
        print(e)

    # Add documents to the collection
    ids = ["doc1", "doc2", "doc3", "doc4"]
    documents = [
        "This is the first document.",
        "This is the second document.",
        "This is the third document.",
        "This is the first sql."
    ]
    db_manager.add_documents(collection_name, ids, documents)
    print(f"Added {len(documents)} documents to '{collection_name}'.")

    # Query the collection
    query_result = db_manager.query_documents(collection_name, ["first document sql"], n_results=2)
    print("Query result:", query_result)

    # List all collections
    print("Collections:", db_manager.list_collections())

    # Delete a document
    db_manager.delete_documents(collection_name, ["doc1"])
    print("Deleted 'doc1'.")

if __name__ == "__main__":
    pass
    # main()
