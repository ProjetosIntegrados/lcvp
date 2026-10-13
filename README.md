# Nome do projeto

> [!WARNING]
> Este projeto foi desenvolvido por estudantes no contexto de uma disciplina de graduação e possui finalidade exclusivamente educacional. Os resultados não foram necessariamente validados para uso profissional e devem ser utilizados com cautela e verificados independentemente.

## Descrição
Em uma ferrovia, o peso do trem passa pelas rodas, pelo trilho e pelo dormente e  chega ao solo por uma camada de peddra britada chamada LASTRO. Se essa camada for fina demais, o soslo cede e a linha se deforma. Se for grossa demais, a obra fica mais cara.

Esse projeto, desenvolvido para a disciplina de Projetos Integrados III (ENG01066), calcula a __espessura mínima da camada de lastro__ e a __quantidade de pedra necessária__ para um trecho de ferrovia. O método utilizado é o da aula sobre superestrutura ferroviária: sublastro e lastro, com a fórmula de Talbot administrada pelo professor Fernando Dutra Michel na disciplina Infra Fer-Hidro-Aéro-Dutoviária (ENG09030).

**Principais Funcionalidades**

* Entrada de dados ()
* Cálcula da carga por roda


Descobrir qual a altura mínima de lastro (h) que deve existir sob os dormentes para que a pressão que chega na plataforma não ultrapasse a pressão que o solo suporta com segurança. Com h definido, calcula-se quanto material de lastro será necessário no trecho (cubagem).

## Instalação

Descrição dos requisitos e os procedimentos necessários para instalar o projeto.

Python 3.7

Por exemplo:

```bash
pip install
poetry install
````

## Uso

Explique como utilizar o projeto e apresente exemplos mínimos de uso.

COMO O PROGRAMA FUNCIONA (visão geral)
--------------------------------------------------------------------------------
 1. Pergunta os dados ao usuário .................. classe InterfaceIO
 2. Calcula pesos, pressões e a espessura h ....... classe Superestrutura
 3. Calcula o tamanho da seção e a quantidade
    de pedra necessária ........................... classe SecaoTransversal
 4. Mostra o relatório em tabelas ................. InterfaceIO.gerar_relatorio_terminal
 
 Unidades usadas: metros (m) para medidas, kgf para pesos, kgf/cm² para
 pressões, km/h para velocidade.

```python
# Exemplo de uso
```

## Exemplos

Descreva ou indique os exemplos disponíveis no diretório [`exemplos/`](exemplos/).

## Testes

Os testes automatizados estão no diretório [`tests/`](tests/).

Para executá-los:

```bash
poetry run pytest
```

## Estrutura do projeto

```text
.
├── src/
│   └── nome_do_projeto/
├── tests/
├── exemplos/
├── docs/
├── README.md
├── LICENSE
└── pyproject.toml
```

## Desenvolvimento

Descreva informações relevantes para desenvolver, modificar ou contribuir com o projeto.

## Autores

**Alunos**

* Bruna Soldera Terres (2026/2)
* Tainá Yumi Isse Sato (2026/2)

**Professores orientadores**

* Felipe Pinto da Motta Quevedo
* Felipe Schaedler de Almeida

## Referências

Slides de aula da disciplina ENG09030 - Infra Fer-Hidro-Aéro-Dutoviária do professor Fernando Dutra Michel

Liste as normas, livros, artigos, documentação, códigos ou outras fontes utilizadas no desenvolvimento do projeto.

## Licença

Este projeto está distribuído sob a licença MIT. Consulte o arquivo [`LICENSE`](LICENSE).

```



