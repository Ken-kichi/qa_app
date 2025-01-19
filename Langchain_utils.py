from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
import os


class Langchain_utils:

    def __init__(self, api_key: str, chunk_size: int, chunk_overlap: int, model: str, query: str):
        """
        初期化メソッド。APIキー、ファイルパス、チャンクサイズ、チャンクオーバーラップ、モデル、クエリを設定します。

        :param api_key: APIキー
        :param chunk_size: チャンクのサイズ
        :param chunk_overlap: チャンクのオーバーラップ
        :param model: 使用するモデル
        :param query: クエリ文字列
        """
        self.api_key = api_key
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.model = model
        self.query = query

    def get_pdf_contents(self, file_path) -> list:
        """
        PDFの内容を取得し、ページごとに分割します。

        :return: 分割されたドキュメントのリスト
        """
        loader = PyPDFLoader(file_path)
        document = loader.load_and_split()  # PDFを読み込み、ページごとに分割
        return document

    def get_contents(self, document: list) -> list:
        """
        ドキュメントをチャンクに分割します。

        :param document: 分割するドキュメントのリスト
        :return: チャンクに分割されたドキュメントのリスト
        """
        text_splitter = CharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap
        )
        # self.documentをdocumentに変更
        return text_splitter.split_documents(document)

    def get_embeddings(self) -> OpenAIEmbeddings:
        """
        OpenAIの埋め込みを取得します。

        :return: OpenAIEmbeddingsオブジェクト
        """
        return OpenAIEmbeddings(api_key=self.api_key, model=self.model)

    def get_retriever(self, document: list) -> Chroma:
        """
        ドキュメントからリトリーバーを取得します。

        :param document: リトリーバーを作成するためのドキュメントのリスト
        :return: Chromaリトリーバーオブジェクト
        """
        docs = self.get_contents(document)
        embeddings = self.get_embeddings()
        db = Chroma.from_documents(docs, embeddings)
        return db.as_retriever()

    def get_chatgpt_model(self, model_name):
        return ChatOpenAI(
            api_key=os.environ['OPENAI_KEY'],
            model_name=model_name,
            # model_name="gpt-4o-mini",
            temperature=0)

    def get_answer(self, model_name, retriever, query):

        prompt = ChatPromptTemplate.from_template('''
        以下の文脈から質問に答えてください。
        文脈:{context}
        質問:{question}
        ''')

        model = self.get_chatgpt_model(model_name=model_name)

        chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | model
            | StrOutputParser()
        )

        return chain.invoke(query)
