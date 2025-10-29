# Teste-Agente--Arthur-Bubolz
Este repositório apresenta a implementação de uma arquitetura multiagente desenvolvida para consumir dados da API da Wikipedia, processá-los e gerar artigos estruturados e prontos para publicação em websites, o projeto foca na automação inteligente da curadoria e construção de conteúdo.

O repositório está organizado da seguinte forma:

- **Branch `master`**: Contém o código e a lógica principal do projeto. Esta é a branch onde o desenvolvimento está ativo.
- **Branch `main`**: Usada para informações gerais sobre o projeto, como este README, bem como para versões futuras ou mudanças mais estruturais.

## **Tabela de Conteúdos**

1. [Arquitetura e Arquivos Principais](#arquitetura-e-arquivos-principais)
   1. [main.py](#mainpy)
   2. [crew.py](#crewpy)
   3. [wikipedia.py](#wikipediapy)
   4. [agents.yaml](#agentsyaml)
   5. [tasks.yaml](#tasksyaml)
   6. [request.py](#requestpy)
2. [Configuração do Docker](#configuração-do-docker)
3. [Execução do Sistema](#execução-do-sistema)
4. [Contribuindo](#contribuindo)

---

## **Visão Geral**

O sistema multiagentes desenvolvido visa otimizar a consulta a artigos da Wikipedia de maneira escalável e eficiente. Utilizando uma arquitetura baseada em agentes, o projeto permite o envio e processamento simultâneo de requisições à Wikipedia. A flexibilidade do sistema permite que novos agentes sejam facilmente integrados para diferentes tarefas.

Adicionalmente, a infraestrutura do sistema está completamente containerizada utilizando Docker, o que simplifica o processo de configuração e execução em diferentes ambientes. Embora, no momento, a API esteja configurada para funcionar apenas em localhost, a utilização do Docker já facilita a transição para um ambiente de produção, caso seja necessário no futuro.

---

## **Arquitetura e Arquivos Principais**

A seguir, estão descritos os arquivos principais do sistema e suas responsabilidades.

### **main.py**
Este é o arquivo principal de execução do sistema. Ele inicializa os componentes do sistema multiagentes, incluindo a configuração dos agentes e a execução das tarefas de consulta à Wikipedia. Nele, a lógica de controle das requisições e o fluxo de interação entre os agentes são definidos, fazendo com que o sistema funcione de maneira coordenada.

#### **Funcionamento de Código**
No início do código, são feitas as importações necessárias para o funcionamento da aplicação. As dependências são separadas em dois grupos: bibliotecas de terceiros e bibliotecas locais.

- **Dependências de Terceiros**:
    - `uvicorn`: Utilizado para rodar a aplicação FastAPI de forma eficiente e com suporte a ASGI (Asynchronous Server Gateway Interface).
    - `FastAPI` e `Pydantic`: Utilizados para criar a API e validar os dados de entrada da requisição.
  
- **Dependências Locais**:
    - `wikipedia`: Biblioteca interna que contém a lógica para interagir com a API da Wikipedia.
    - `crew`: Contém a classe `AiLatestDevelopment`, que representa a IA responsável por processar os dados extraídos da Wikipedia e gerar os artigos.

#### **Funções Principais**
Agora, será explicado cada função principal do código, explicando sua lógica e papel no fluxo geral da aplicação.

#### **Função `obter_texto_wikipedia(topico: str) -> Union[str, int]`**

Esta função tem como objetivo fazer uma consulta à Wikipedia para obter o conteúdo de um artigo com base no tópico fornecido.

- **Parâmetros**:
    - `topico`: O tópico de interesse que será pesquisado na Wikipedia.

- **Retorno**:
    - Retorna o texto do artigo (como `str`) ou um código de erro (como `int`).

- **Explicação**:
    - A função faz uma chamada à função `consulta_wikipedia` do módulo `wikipedia`, que retorna o conteúdo do artigo ou um código de erro caso a consulta falhe.
    - O código de erro é representado por um número inteiro, como o código `404` se o artigo não for encontrado.

#### **Função `gerar_artigo_com_ia(topico: str) -> Dict[str, Any] | str`**

Esta função é responsável por gerar um artigo informativo baseado no conteúdo obtido da Wikipedia e processá-lo através de uma inteligência artificial. Ela é chamada no endpoint principal da API para criar os artigos solicitados pelos usuários.

- **Parâmetros**:
    - `topico`: O tópico para o qual o artigo será gerado.

- **Retorno**:
    - Retorna um `JSON` com o título, conteúdo do artigo e palavras-chave, ou uma mensagem de erro.

- **Explicação**:
    - A função chama `obter_texto_wikipedia(topico)` para obter o conteúdo da Wikipedia.
    - Se a consulta for bem-sucedida, ela prepara os dados para o processamento pela IA, incluindo o tópico, o texto da Wikipedia e o ano atual.
    - Em seguida, a função executa a IA com o método `kickoff` da classe `AiLatestDevelopment`, que retorna o artigo gerado.
    - Caso ocorra algum erro na execução da IA ou na consulta à Wikipedia, a função trata o erro e retorna uma mensagem apropriada.

#### **FastAPI - Configuração da API**
O sistema é estruturado como uma API utilizando o FastAPI, que facilita a criação de APIs rápidas e eficientes.

#### **Função `health_check()`**

Este é um endpoint simples de verificação da saúde da API, utilizado para garantir que o servidor esteja operacional.

- **Método HTTP**: `GET`
- **Endpoint**: `/`
- **Retorno**:
    - Um JSON com o status da API e uma mensagem informando que está operacional.

#### **Função `criar_artigo(tema_requisicao: TopicRequest)`**

Este é o endpoint principal da API, que recebe uma requisição POST com o tópico desejado e retorna o artigo gerado pela IA.

- **Método HTTP**: `POST`
- **Endpoint**: `/articlemaker`
- **Parâmetros**:
    - `tema_requisicao`: Um objeto do tipo `TopicRequest`, que contém o valor do tópico a ser pesquisado na Wikipedia.

- **Fluxo**:
    - A função chama `gerar_artigo_com_ia(tema_requisicao.value)`, passando o valor do tópico recebido na requisição.
    - O resultado retornado é, então, encapsulado em um JSON para ser enviado de volta ao usuário.

#### **Função main() - Inicialização do Servidor**

A função main() é responsável por inicializar o servidor local utilizando o uvicorn, um servidor ASGI altamente performático.

- **Explicação:** 
A função imprime uma mensagem informando que o servidor está sendo iniciado e em qual URL ele estará disponível.
Em seguida, ela usa o uvicorn.run() para iniciar o servidor na porta 8000 do endereço 0.0.0.0.

### **crew.py**
Este arquivo define os agentes responsáveis por realizar as consultas à Wikipedia. Através de uma implementação modular, o arquivo contém a lógica para definir como os agentes interagem com o sistema, realizando tarefas específicas com base nas configurações fornecidas.

#### **Importação das Bibliotecas**

O arquivo começa com a importação das bibliotecas necessárias para a execução da aplicação. Entre elas estão:

- **Dependências de Terceiros**:
    - `crewai`: Usado para criar agentes e tarefas no sistema multiagentes.
    - `dotenv`: Carrega variáveis de ambiente (como chaves de API) a partir de um arquivo `.env`.
    - `pydantic`: Usado para validar dados e estruturar saídas em JSON.

- **Dependências Locais**:
    - `crewai_tools`: Contém ferramentas específicas, como `SerperDevTool`, `ScrapeWebsiteTool`, e `FileWriterTool`, que são usadas pelos agentes para buscar informações e processar dados.
  
#### **Modelo de Saída (Pydantic)**

A classe `OutputItem` define o formato da saída que os agentes devem retornar ao final do processamento. O modelo é estruturado com `Pydantic` para garantir que os dados estejam no formato correto.

### **Classe `OutputItem`**

class OutputItem(BaseModel):
    titulo: str = Field(description="O título final e otimizado do artigo.")
    conteudo: str = Field(description="O corpo completo do artigo, formatado para leitura.")
    palavras_chave: List[str] = Field(description="Lista de palavras-chave mais relevantes para SEO.")

#### Definição da Crew - Classe AiLatestDevelopment

A classe `AiLatestDevelopment` define a estrutura da "Crew", composta por agentes e tarefas que realizam o processamento da informação. Os agentes são responsáveis por ações específicas, como buscar dados e otimizar o conteúdo, enquanto as tarefas são as ações que coordenam os agentes.

#### Atributos: - Classe AiLatestDevelopment

- **titulo**: Título otimizado do artigo gerado.
- **conteudo**: Corpo do artigo, pronto para leitura.
- **palavras_chave**: Lista de palavras-chave relevantes para SEO.

#### Agentes

Abaixo estão os agentes definidos para o sistema, cada um com uma responsabilidade distinta:

- **Agente `retrieve_news`**: Buscar informações de sites relativas ao tema  
  **Responsabilidade**: Buscar informações externas relacionadas ao tema.  
  **Ferramenta**: `SerperDevTool` é usada para realizar a busca.

- **Agente `website_scraper`**: Aplicar scrapping no conteúdo complementar do site  
  **Responsabilidade**: Realizar scrapping no conteúdo relevante do website.

- **Agente `summarizer_of_websites`**: Resumir e consolidar as informações  
  **Responsabilidade**: Resumir e consolidar as informações obtidas tanto da Wikipedia quanto de fontes externas.

- **Agente `text_seo_optmizer`**: Reescrever o texto para SEO  
  **Responsabilidade**: Otimizar o conteúdo para SEO e gerar o formato JSON final.

#### Tarefas

As tarefas são as operações realizadas pelos agentes, que são definidas para coordenar e controlar o fluxo de dados entre eles.

- **Tarefa `retrieve_news_task`**: Pesquisar o tópico e itens mais recentes  
  **Responsabilidade**: Buscar as informações mais recentes relacionadas ao tópico.

- **Tarefa `website_scrape_task`**: Aplicar scrapping no conteúdo encontrado  
  **Responsabilidade**: Realizar scrapping no conteúdo do site encontrado.

- **Tarefa `summarizer_of_websites_task`**: Resumir e consolidar o conteúdo  
  **Responsabilidade**: Consolidar e resumir o conteúdo da Wikipedia e do scrapping do site.

- **Tarefa `seo_optimization_task`**: Otimizar o conteúdo para SEO  
  **Responsabilidade**: Aplicar otimização SEO no conteúdo consolidado e gerar a saída estruturada.

#### Função Crew

A função `crew` cria a "crew" principal, que consiste em um conjunto de agentes e tarefas, e define o processo sequencial para a execução das operações.  
**Responsabilidade**: Cria e retorna a crew principal com os agentes e tarefas definidos.

### **wikipedia.py**
O arquivo `wikipedia.py` contém a lógica necessária para fazer a consulta à Wikipedia. Ele interage diretamente com a API da Wikipedia, fazendo requisições HTTP e processando as respostas. O objetivo é extrair as informações pertinentes de um artigo de forma estruturada e eficiente.


#### Parâmetros da Consulta

- **action**: Especifica a ação que a API deve realizar. No caso, `query` indica uma consulta.
- **format**: Define o formato da resposta, sendo `json` para facilitar o processamento.
- **prop**: Define quais propriedades serão retornadas, neste caso, o `extract` (texto resumido).
- **exintro**: Filtra o conteúdo retornado, limitando-o a um resumo inicial da página.
- **titles**: Define o título da página que será consultada, sendo o parâmetro passado para a função.

#### Cabeçalhos da Requisição

O cabeçalho `User-Agent` é utilizado para simular uma requisição feita por um navegador, evitando bloqueios por parte da Wikipedia.

#### Requisição e Processamento

- A requisição é feita com a função `requests.get`, que retorna um objeto `response`.
- Caso o código de status HTTP seja `200` (indicando sucesso), a função extrai o conteúdo JSON da resposta e localiza a chave `extract`, que contém o resumo da página solicitada.
- Caso contrário, o código de status HTTP é retornado como um valor inteiro para indicar que houve um erro na consulta.

#### Limpeza do Texto

Após o conteúdo ser extraído, ele é passado para a função `clean_text`, responsável por limpar o texto removendo tags HTML, links e caracteres indesejados.

#### Função `clean_text`

A função `clean_text` é utilizada para processar o texto extraído da Wikipedia e remover elementos indesejados:
Remoção de Tags HTML: Usando a biblioteca `BeautifulSoup`, o texto é analisado e as tags HTML são removidas.
Remoção de URLs: As URLs, identificadas pelo padrão `http\S+`, são removidas do texto.
Remoção de Espaços em Branco Excessivos: Os espaços em branco múltiplos são substituídos por um único espaço, e o texto é "trimado" para remover espaços nas extremidades.
Remoção de Caracteres Não Alfanuméricos: A função também remove caracteres especiais, exceto os que são permitidos em um texto comum, como pontuação.

O resultado final é um texto limpo, que pode ser utilizado em outras partes do sistema.


### **agents.yaml**
Este arquivo é utilizado para configurar os agentes que vão realizar as requisições e processar os dados da Wikipedia. Nele, você define as características dos agentes, como o nome, tipo e as funções específicas que cada agente executará. Ele permite a personalização do comportamento de cada agente de acordo com as necessidades do sistema.

#### retrieve_news:
O agente de busca de artigos tem como objetivo descobrir fontes relevantes que tratam de um determinado tópico de forma diferenciada. Ele é descrito como um pesquisador experiente, com um talento especial para identificar e apresentar informações pertinentes sobre um tema. Seu trabalho é essencial para garantir que as informações coletadas sejam de alta qualidade e realmente contribuem para o aprofundamento do tema em questão.

#### website_scraper:
Este agente é especializado em técnicas de web scraping, ou seja, na extração de dados de websites. Ele navega por sites e aplica técnicas para capturar informações relevantes, fazendo uso de suas habilidades em identificar conteúdos valiosos dentro de sites complexos. Sua atuação garante que a informação coletada seja precisa e útil para a construção do conteúdo final.

#### summarizer_of_websites:
Como analista e resumidor de informações, esse agente tem a responsabilidade de analisar o conteúdo obtido dos sites e complementar o artigo existente. Ele traz novas informações, relevando detalhes e aspectos não abordados anteriormente. Seu foco é enriquecer o artigo com dados relevantes e garantir que o conteúdo tenha uma cobertura completa sobre o tópico.

#### text_seo_optimizer:
Este agente é o especialista em SEO (Search Engine Optimization), responsável por otimizar o conteúdo gerado para garantir que ele seja legível e atraente tanto para os leitores quanto para os motores de busca. Seu objetivo é ajustar o texto de modo a melhorar a fluidez e a relevância, sem perder a qualidade informativa. Ele realiza ajustes finos que garantem que o conteúdo esteja preparado para ter um bom desempenho nos rankings de busca, mantendo uma experiência de leitura agradável.

### **tasks.yaml**
O arquivo `tasks.yaml` contém a configuração das tarefas que os agentes devem executar. Nele, são definidas as requisições que serão feitas aos agentes, o que cada agente deve fazer e como as respostas devem ser processadas. Este arquivo serve como um plano de ação para a execução das consultas à Wikipedia.

#### retrieve_news_task:
Responsável por buscar as fontes mais relevantes sobre o tópico e fornecer os dados iniciais para os próximos passos.

#### website_scrape_task:
Executa o processo de scraping nos sites identificados, coletando informações cruciais.

#### summarizer_of_websites_task:
Realiza a análise e complementação das informações coletadas, garantindo que o conteúdo tenha uma visão mais ampla e detalhada.

#### seo_optimization_task:
Aplica as melhorias necessárias para otimizar o texto, garantindo que o artigo esteja preparado para alcançar bons resultados em SEO.

### **request.py**
O `request.py` gerencia as requisições HTTP realizadas aos servidores da Wikipedia. Ele contém funções para estruturar as requisições, enviar os dados para a API da Wikipedia e lidar com as respostas. Além disso, o arquivo também trata de erros de rede e falhas de requisição, garantindo que o teste do sistema seja resiliente.

#### Função request:

A função request é a responsável por enviar uma requisição HTTP POST para a API ArticleMaker, localizada no endereço http://localhost:8000/articlemaker. Ela realiza o envio de dados e trata a resposta da API.

A função recebe como parâmetro um valor (input), que é o tema ou conteúdo a ser enviado para a API. Esse valor será utilizado no campo value do corpo da requisição.

O valor de input é encapsulado em um dicionário Python com a chave "value". O dicionário resultante será enviado como o corpo da requisição (no formato JSON).

A função utiliza a biblioteca requests para enviar a requisição POST. A URL do servidor é especificada como http://localhost:8000/articlemaker. O método requests.post é utilizado para realizar a requisição, com o corpo da mensagem contendo o dicionário data convertido para JSON (usando o parâmetro json=data).

Tratamento da Resposta:

Se a resposta da API for bem-sucedida (status code 200), o conteúdo da resposta é extraído em formato JSON usando o método response.json() e retornado para quem chamou a função.

Caso o status code seja diferente de 200 (indicando falha), a função retorna uma mensagem de erro contendo o código de status da resposta, indicando que algo deu errado.

A função request permite que a aplicação interaja com a API ArticleMaker, solicitando a criação de conteúdo baseado no tema fornecido e recebendo o resultado em formato JSON.

#### Função main

A função main é o ponto de entrada para a execução do script. Ela serve como exemplo de uso da função request:

Definição do Tema (input): A variável input é definida com o valor 'Saimaa', que representa o tema que será enviado para a API. Nesse caso, é o nome de um lago na Finlândia, mas pode ser qualquer outro tema relevante.

Chamada à Função request:
A função request é chamada com o valor de input, que é o tema 'Saimaa'. O resultado da requisição (que pode ser o conteúdo gerado pela API ou uma mensagem de erro) é armazenado na variável resultado.

Impressão do Resultado:
O conteúdo retornado pela função request (seja o resultado JSON ou o erro) é impresso na tela usando o comando print(resultado).


---

## **Configuração do Docker**

O sistema utiliza Docker para garantir que a aplicação seja executada em ambientes consistentes. A configuração do Docker é feita através de um `Dockerfile`, que especifica todas as dependências necessárias para a execução do sistema.

### **Dockerfile**

O `Dockerfile` define as etapas necessárias para construir a imagem Docker do sistema. Ele instala as dependências necessárias, configura o ambiente e prepara a aplicação para ser executada dentro de um contêiner.

---

## **Execução do Sistema**

Para rodar o sistema, siga os seguintes passos:

### 1. **Clone o Repositório**

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio

### 2. Configuração do Ambiente Docker
Este projeto utiliza o Docker para facilitar a configuração do ambiente. Siga os passos abaixo para configurar o Docker:

#### 2.1 Construa a imagem Docker:
Execute o seguinte comando para construir a imagem Docker:
docker build -t NOME_DA_IMAGEM .

#### 2.2 Execute o container Docker:
Após a construção da imagem, execute o container na porta 8000:
docker run -p 8000:8000 app-crew-article

### 3 . Verificação
Para verificar se a aplicação foi iniciada corretamente, abra o navegador e acesse:

http://localhost:8000

Se tudo estiver correto, você verá a mensagem:
{"status":"OK","message":"API operacional!"}



