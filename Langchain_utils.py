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

    def __init__(
            self,
            api_key: str,
            chunk_size: int,
            chunk_overlap: int,
            model: str,
            query: str
    ):
        """
        初期化メソッド。APIキー、ファイルパス、チャンクサイズ、チャンクオーバーラップ、モデル、クエリを設定します。

        :param api_key: APIキー
        :param chunk_size: チャンクのサイズ
        :param chunk_overlap: チャンクのオーバーラップ
        :param model: 使用するモデル
        :param query: クエリ文字列
        """
        self.api_key = api_key  # APIキーを設定
        self.chunk_size = chunk_size  # チャンクサイズを設定
        self.chunk_overlap = chunk_overlap  # チャンクオーバーラップを設定
        self.model = model  # 使用するモデルを設定
        self.query = query  # クエリ文字列を設定

    def get_pdf_contents(self, file_path) -> list:
        """
        PDFの内容を取得し、ページごとに分割します。

        :param file_path: PDFファイルのパス
        :return: 分割されたドキュメントのリスト
        """
        loader = PyPDFLoader(file_path)  # PDFローダーを初期化
        document = loader.load_and_split()  # PDFを読み込み、ページごとに分割
        return document  # 分割されたドキュメントを返す

    def get_contents(self, document: list) -> list:
        """
        ドキュメントをチャンクに分割します。

        :param document: 分割するドキュメントのリスト
        :return: チャンクに分割されたドキュメントのリスト
        """
        text_splitter = CharacterTextSplitter(
            chunk_size=self.chunk_size,  # チャンクサイズを指定
            chunk_overlap=self.chunk_overlap  # チャンクオーバーラップを指定
        )
        # self.documentをdocumentに変更
        return text_splitter.split_documents(document)  # ドキュメントをチャンクに分割して返す

    def get_embeddings(self) -> OpenAIEmbeddings:
        """
        OpenAIの埋め込みを取得します。

        :return: OpenAIEmbeddingsオブジェクト
        """
        return OpenAIEmbeddings(api_key=self.api_key, model=self.model)  # 埋め込みオブジェクトを返す

    def get_retriever(self, document: list) -> Chroma:
        """
        ドキュメントからリトリーバーを取得します。

        :param document: リトリーバーを作成するためのドキュメントのリスト
        :return: Chromaリトリーバーオブジェクト
        """
        docs = self.get_contents(document)  # ドキュメントをチャンクに分割
        embeddings = self.get_embeddings()  # 埋め込みを取得
        db = Chroma.from_documents(docs, embeddings)  # Chromaデータベースを作成
        return db.as_retriever()  # リトリーバーを返す

    def get_chatgpt_model(self, model_name):
        """
        ChatGPTモデルを取得します。

        :param model_name: 使用するモデルの名前
        :return: ChatOpenAIオブジェクト
        """
        return ChatOpenAI(
            api_key=os.environ['OPENAI_KEY'],  # 環境変数からAPIキーを取得
            model_name=model_name,  # モデル名を指定
            temperature=0  # 温度を設定（決定論的な応答）
        )

    def get_answer(self, model_name, retriever, query):
        """
        モデルを使用して質問に対する回答を取得します。

        :param model_name: 使用するモデルの名前
        :param retriever: リトリーバーオブジェクト
        :param query: 質問文字列
        :return: 回答文字列
        """
        prompt = ChatPromptTemplate.from_template('''
        以下の文脈から質問に答えてください。
        文脈:{context}
        質問:{question}
        ''')

        model = self.get_chatgpt_model(model_name=model_name)  # ChatGPTモデルを取得

        chain = (
            {"context": retriever, "question": RunnablePassthrough()}  # コンテキストと質問を設定
            | prompt  # プロンプトを適用
            | model  # モデルを適用
            | StrOutputParser()  # 出力を解析
        )

        return chain.invoke(query)  # 質問を実行して回答を返す
