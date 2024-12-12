import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool
from dotenv import load_dotenv
import streamlit as st
from MyLLM import MyLLM

gpt = MyLLM.GPT4o_mini # model='gpt-4o-mini'
llama = MyLLM.GROQ_LLAMA # model='groq/llama-3.2-3b-preview'

st.markdown("##### LLM: llama-3.2-3b-preview")

load_dotenv()

class CrewPostagem:
    def __init__(self):
        self.search_tool = SerperDevTool()
        self.llm = llama
        self.crew = self._criar_crew()

    def _criar_crew(self):
        # Definindo os agentes
        pesquisador = Agent(
            role='Pesquisador',
            goal='Encontrar informações relevantes sobre {topic}',
            verbose=True,
            memory=True,
            backstory='''Você é um pesquisador especializado em descobrir 
            informações úteis e relevantes para escrever sobre {topic}.''',
            tools=[self.search_tool]
        )

        escritor = Agent(
            role='Escritor',
            goal='Criar uma postagem convincente sobre {topic}',
            verbose=True,
            memory=True,
            backstory='''Você é um redator experiente que transforma 
            informações em conteúdos interessantes e informativos.'''
        )

        revisor = Agent(
            role='Revisor',
            goal='Revisar e melhorar a postagem sobre {topic}',
            verbose=True,
            memory=True,
            backstory='''Você é um revisor detalhista, especializado em ajustar 
            o tom, a clareza e a gramática de textos.'''
        )

        # Tarefas
        pesquisa_tarefa = Task(
            description='''Pesquise informações detalhadas sobre {topic}. Foque 
            em identificar pontos importantes e um resumo geral.''',
            expected_output='Um resumo detalhado sobre {topic}.',
            tools=[self.search_tool],
            agent=pesquisador
        )

        escrita_tarefa = Task(
            description='''Escreva uma postagem com base no conteúdo pesquisado. 
            A postagem deve ser clara, interessante e envolvente.''',
            expected_output='''Uma postagem completa sobre {topic} com 3 parágrafos.''',
            agent=escritor,
            context=[pesquisa_tarefa]
        )

        revisao_tarefa = Task(
            description='''Reveja a postagem criada, ajustando a clareza e 
            corrigindo possíveis erros.''',
            expected_output='Uma postagem revisada e otimizada.',
            agent=revisor,
            context=[escrita_tarefa]
        )

        # Criando o Crew
        return Crew(
            agents=[pesquisador, escritor, revisor],
            tasks=[pesquisa_tarefa, escrita_tarefa, revisao_tarefa],
            process=Process.sequential
        )

    def kickoff(self, inputs):
        # Executa o Crew com o tópico fornecido
        resposta = self.crew.kickoff(inputs=inputs)
        return resposta.raw
