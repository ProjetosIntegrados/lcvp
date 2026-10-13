# Ferramenta Computacional para Dimensionamento de Lastro e Cubagem de Via Permanente (Lcvp)

> [!WARNING]
> Este projeto foi desenvolvido por estudantes no contexto de uma disciplina de graduação e possui finalidade exclusivamente educacional. Os resultados não foram necessariamente validados para uso profissional e devem ser utilizados com cautela e verificados independentemente.

## Descrição
Em uma ferrovia, o peso do trem passa pelas rodas, pelo trilho e pelo dormente e  chega ao solo por uma camada de peddra britada chamada LASTRO. Se essa camada for fina demais, o soslo cede e a linha se deforma. Se for grossa demais, a obra fica mais cara.

Esse projeto, desenvolvido para a disciplina de Projetos Integrados III (ENG01066), calcula a __espessura mínima da camada de lastro__ e a __quantidade de pedra necessária__ para um trecho de ferrovia. O método utilizado é o da aula sobre superestrutura ferroviária: sublastro e lastro, com a fórmula de Talbot administrada pelo professor Fernando Dutra Michel na disciplina Infra Fer-Hidro-Aéro-Dutoviária (ENG09030).

**Principais Funcionalidades**
Descobrir qual a altura mínima de lastro (h) que deve existir sob os dormentes para que a pressão que chega na plataforma não ultrapasse a pressão que o solo suporta com segurança. Com h definido, calcula-se quanto material de lastro será necessário no trecho (cubagem).

## Instalação



Python 3.7 ou superior
matplotlib: gera o desenho da seção tipo

Por exemplo:

```bash
pip install matplotlib
pip install tabulate # É uma biblioteca opcional que desenha tabelas bonitas no terminal
````

## Uso
segue os 8 passos da aula (P, Pg, kv, Pv, Pm, Pr, Pap, h). A altura usa Talbot


Explique como utilizar o projeto e apresente exemplos mínimos de uso.

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
│   └── lastro_ferroviario/
│       ├── __init__.py
│       ├── modelos.py         # dataclasses de entrada
│       ├── superestrutura.py  # cargas, pressões e altura h
│       ├── secao.py           # área da seção e cubagem
│       ├── interface.py       # entrada de dados e relatório
│       └── desenho.py         # secao_tipo_plot.py
├── tests/
├── exemplos/
├── README.md
├── LICENSE
└── pyproject.toml
```

## Desenvolvimento

Descreva informações relevantes para desenvolver, modificar ou contribuir com o projeto.

COMO O PROGRAMA FUNCIONA (visão geral)
--------------------------------------------------------------------------------
 1. Pergunta os dados ao usuário
 2. Calcula pesos, pressões e a espessura h
 3. Calcula o tamanho da seção e a quantidade de pedra necessária
 4. Mostra o relatório em tabelas
 
**Unidades de medidas**
* comprimento em metros (m);
* cargas em kgf para pesos;
* pressões em kgf/cm²;
* velocidade em km/h.

O programa responde a duas perguntas:
  1) Que espessura (h) a camada de pedra precisa ter para que o solo aguente?
  2) Quantos metros cúbicos de pedra devem ser comprados para o trecho todo?



## Autores

**Alunos**

* Bruna Soldera Terres (2026/2)
* Tainá Yumi Isse Sato (2026/2)

**Professores orientadores**

* Felipe Pinto da Motta Quevedo
* Felipe Schaedler de Almeida

## Referências

Slides de aula da disciplina ENG09030 - Infra Fer-Hidro-Aéro-Dutoviária do professor Fernando Dutra Michel

## Licença

Este projeto está distribuído sob a licença MIT. Consulte o arquivo [`LICENSE`](LICENSE).

```



