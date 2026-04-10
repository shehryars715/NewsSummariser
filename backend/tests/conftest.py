import sys
import types
from importlib.machinery import ModuleSpec
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


if "fastapi" not in sys.modules:
    fastapi_module = types.ModuleType("fastapi")
    fastapi_module.__spec__ = ModuleSpec("fastapi", loader=None)

    class HTTPException(Exception):
        def __init__(self, status_code: int, detail: str):
            super().__init__(detail)
            self.status_code = status_code
            self.detail = detail

    fastapi_module.HTTPException = HTTPException
    sys.modules["fastapi"] = fastapi_module


if "faiss" not in sys.modules:
    faiss_module = types.ModuleType("faiss")
    faiss_module.__spec__ = ModuleSpec("faiss", loader=None)

    class IndexFlatL2:
        def __init__(self, dimension):
            self.dimension = dimension
            self.vectors = []
            self.ntotal = 0

        def add(self, embeddings):
            self.vectors.extend(embeddings)
            self.ntotal = len(self.vectors)

    faiss_module.IndexFlatL2 = IndexFlatL2
    faiss_module.serialize_index = lambda index: b""
    faiss_module.read_index = lambda path: None
    sys.modules["faiss"] = faiss_module


if "sentence_transformers" not in sys.modules:
    sentence_transformers_module = types.ModuleType("sentence_transformers")
    sentence_transformers_module.__spec__ = ModuleSpec("sentence_transformers", loader=None)

    class SentenceTransformer:
        def __init__(self, model_name):
            self.model_name = model_name

        def get_sentence_embedding_dimension(self):
            return 3

        def encode(self, texts, normalize_embeddings=True, convert_to_numpy=True):
            if isinstance(texts, str):
                return [0.1, 0.2, 0.3]
            return [[0.1, 0.2, 0.3] for _ in texts]

    sentence_transformers_module.SentenceTransformer = SentenceTransformer
    sys.modules["sentence_transformers"] = sentence_transformers_module


if "langchain_google_genai" not in sys.modules:
    genai_module = types.ModuleType("langchain_google_genai")
    genai_module.__spec__ = ModuleSpec("langchain_google_genai", loader=None)

    class _Response:
        def __init__(self, content):
            self.content = content

    class ChatGoogleGenerativeAI:
        def __init__(self, *args, **kwargs):
            self.args = args
            self.kwargs = kwargs

        def __call__(self, messages):
            return _Response("stub article summary")

        def invoke(self, messages):
            return _Response("stub query summary")

    genai_module.ChatGoogleGenerativeAI = ChatGoogleGenerativeAI
    sys.modules["langchain_google_genai"] = genai_module


if "langchain.prompts" not in sys.modules:
    prompts_module = types.ModuleType("langchain.prompts")
    prompts_module.__spec__ = ModuleSpec("langchain.prompts", loader=None)

    class _PromptTemplate:
        def __init__(self, template):
            self.template = template

        @classmethod
        def from_template(cls, template):
            return cls(template)

        def format(self, **kwargs):
            return self.template.format(**kwargs)

    class ChatPromptTemplate:
        def __init__(self, messages):
            self.messages = messages

        @classmethod
        def from_messages(cls, messages):
            return cls(messages)

        def format_messages(self, **kwargs):
            return [message.format(**kwargs) for message in self.messages]

    prompts_module.ChatPromptTemplate = ChatPromptTemplate
    prompts_module.SystemMessagePromptTemplate = _PromptTemplate
    prompts_module.HumanMessagePromptTemplate = _PromptTemplate
    sys.modules["langchain.prompts"] = prompts_module
