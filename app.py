#import pysqlite3
import sys
#sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import streamlit as st
from MyLLM import MyLLM

gpt = MyLLM.GPT4o_mini # model='gpt-4o-mini'
llama = MyLLM.GROQ_LLAMA # model='groq/llama-3.2-3b-preview'


from post_crew import CrewPostagem
crew_postagem = CrewPostagem()
# Configuração do Streamlit
st.title ('Sistema de Postagem com CrewAI')

tema = st.text_input ('Digite o tópico para a postagem ', 'IA na saúde ')

st.markdown("###### LLM: llama-3.2-3b-preview")

# Botão para iniciar o processo
if st.button ('Iniciar Processo ') :
# Quanto clicar no botão carrega um loader
    with st.spinner ('Executando tarefas do Crew ... ') :
        result = crew_postagem.kickoff ( inputs ={ 'topic': tema })
        st.success ('Processo concluído!')
    # Exibindo resultados
    st.subheader ('Postagem Gerada ')
    st.markdown("### "+tema.upper())
    st.write ( result )