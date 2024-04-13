from langchain_openai import ChatOpenAI
from operator import itemgetter

from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser

from procure_base_ai.utils.rag import remote_retriever, prompt, total_retriever_223, total_retriever_44, \
    terms_retriever, instructions_retriever

from langchain_anthropic import ChatAnthropic

chat_model = ChatAnthropic(model='claude-3-opus-20240229')
chat_model_gpt = ChatOpenAI(model='gpt-4')

import os
from uuid import uuid4

# Update with your API URL if using a hosted instance of Langsmith.

unique_id = uuid4().hex[0:8]
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = f"Tracing Walkthrough - {unique_id}"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = "ls__1ff4fe77d1ce4af3a8e90c67fb122a1f"  # Update with your API key
project_name = "RST"  # Update with your project name

from langsmith import Client

client = Client()


def format_docs(docs):
    return "\n\n\n".join(
        [f"Статья {d.metadata.get('article')}. Пункт {d.metadata.get('point')}.\n{d.page_content}" if d.metadata.get(
            'point') else d.page_content for d in docs]
    )


rag_chain_from_docs = (
        RunnablePassthrough.assign(context=(lambda x: format_docs(x["context"])))
        | prompt
        | chat_model
        | StrOutputParser()
)

qa_chain = RunnableParallel(
    {"context": remote_retriever, "question": RunnablePassthrough()}
).assign(answer=rag_chain_from_docs)

from langchain.prompts import PromptTemplate

classifier_prompt_template = """
Ты классификатор, который определяет вопрос пользователя в одни из классов, следующим образом 
Если в вопросе есть слова контракт, бюджет ИЛИ если вопрос содержит 44-ФЗ ты относишь его в класс 44
Если в вопросе есть слова договор, комерческий ИЛИ если вопрос содержит 223-ФЗ, ты относишь его в класс 223
Если ответ на вопрос пользователя  требует рукодство действия ты отвносишь его в класс инструкции
Если вопрос пользователя справшивает определения, то ты относишь его в класс термины
Если в вопрос пользователя нет ни слова контаркт, ни договор, но этот вопрос относиться к закону государственных закупок, ты относишь его в класс закон
В ответе напиши ТОЛЬКО класс к которому ты отпределил вопрос
Вопрос пользователя: "{question}"
Ответ AI:"""

prompt_classifier = PromptTemplate(
    template=classifier_prompt_template, input_variables=["question"]
)


def get_retriever(question: str):
    classifier_chain = (
            prompt_classifier
            | chat_model_gpt
            | StrOutputParser()
    )
    cls_name = classifier_chain.invoke(question)

    data = {
        "223": total_retriever_223,
        "44": total_retriever_44,
        "термины": terms_retriever,
        "инструкции": instructions_retriever,
    }

    return data.get(cls_name, total_retriever_44)


qa_chain_2 = (
        {"context": itemgetter("question") | RunnableLambda(get_retriever) | format_docs,
         "question": itemgetter("question")}
        | RunnablePassthrough.assign(context=itemgetter("context"))
        | {"answer": prompt | chat_model | StrOutputParser(), "contexts": itemgetter("context")}
)

eval_prompt_template = """
Ты Эксперт разбирающий ответ и дающий процент уверенности на основе контекста. 

Для получения процента уверенности ты выполняешь следующий алгоритм: 
1. В контекста источники информации на основе которых составлен ответ . 
2. Проанализируй контекст и определи как много из них являются ссылками на законодательство. В зависимости от этого выстави оценку от 0 до 100, где 0 - полное отсутствие ссылок на законодательство, а 100 - все источники являются ссылками на законодательство.
3. Проанализируй ответ  и определи как много в ответe употреблено ссылко на законодательство. В зависимости от этого выстави оценку от 0 до 100, где 0 - полное отсутствие ссылок на законодательство, а 100 - все источники являются ссылками на законодательство. Этот параметр учитывай выше чем параметр выше.
5. Найди среднее между двумя оценками и напиши ТОЛЬКО процент уверенности
Ответ: {answer}
Контекст:
{context}
AI:"""

eval_prompt = PromptTemplate(
    template=eval_prompt_template, input_variables=["question", "answer", "context"]
)

eval_chain = (
        eval_prompt
        | chat_model
        | StrOutputParser()
)
