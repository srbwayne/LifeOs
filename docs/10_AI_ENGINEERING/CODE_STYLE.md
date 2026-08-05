# CODE_STYLE.md

> Política oficial de estilo, organização e qualidade de código do projeto LifeOS.

**Versão:** 1.0
**Status:** Ativo
**Responsável:** Software Architect
**Aplicação:** Obrigatória para todos os desenvolvedores e agentes de Inteligência Artificial.

---

# 1. Objetivo

Este documento define o padrão oficial de escrita, organização e qualidade do código-fonte do projeto LifeOS.

Seu objetivo é garantir que todo código produzido seja:

- legível;
- consistente;
- previsível;
- testável;
- facilmente revisável;
- alinhado à arquitetura oficial;
- sustentável durante toda a evolução do projeto.

O estilo de código faz parte da arquitetura do sistema e deverá ser tratado como um requisito técnico obrigatório.

---

# 2. Escopo

Esta política aplica-se a todo o código do projeto, incluindo:

- Application;
- Domain;
- Infrastructure;
- Presentation;
- Shared Kernel;
- testes automatizados;
- migrations;
- scripts;
- ferramentas internas.

Também se aplica ao código produzido por:

- desenvolvedores;
- Codex;
- Gemini;
- OpenCode;
- outros agentes de Inteligência Artificial.

---

# 3. Documentos Relacionados

Este documento complementa:

- DEFINITION_OF_DONE.md;
- CODE_REVIEW_CHECKLIST.md;
- DEPENDENCY_POLICY.md;
- COMMIT_GUIDELINES.md;
- BRANCHING_STRATEGY.md;
- DEVELOPMENT_WORKFLOW.md;
- ADR_TEMPLATE.md;
- documentação oficial da arquitetura.

Em caso de conflito, prevalecerão:

1. ADRs aprovadas;
2. documentação oficial de arquitetura;
3. este documento.

---

# 4. Princípios Gerais

O código do LifeOS deverá seguir os princípios abaixo.

## 4.1. Clareza

O código deverá priorizar legibilidade.

Sempre que existirem duas soluções tecnicamente equivalentes, deverá ser escolhida aquela que seja mais fácil de compreender.

---

## 4.2. Consistência

Todo código deverá seguir o mesmo padrão.

Diferenças de estilo entre módulos não são permitidas.

A consistência possui prioridade sobre preferências individuais.

---

## 4.3. Simplicidade

O código deverá resolver apenas o problema atual.

Não deverão ser criadas abstrações antecipadas sem necessidade comprovada.

Evitar:

- classes genéricas;
- helpers universais;
- managers sem responsabilidade clara;
- factories desnecessárias;
- abstrações especulativas.

---

## 4.4. Responsabilidade Única

Cada:

- classe;
- função;
- método;
- módulo;
- arquivo;

deverá possuir apenas uma responsabilidade principal.

Quando uma classe precisar ser explicada utilizando vários verbos diferentes, sua estrutura deverá ser revisada.

---

## 4.5. Domínio Explícito

O código deverá utilizar a linguagem oficial do domínio do LifeOS.

Exemplos:

- User;
- Character;
- Player;
- Quest;
- Habit;
- Workout;
- Reading;
- Therapy;
- Achievement.

Evitar nomes excessivamente técnicos quando existir um conceito de domínio mais adequado.

---

## 4.6. Arquitetura Visível

A organização do código deverá refletir claramente a arquitetura do projeto.

As responsabilidades deverão permanecer separadas entre:

- Domain;
- Application;
- Infrastructure;
- Presentation;
- Shared.

O código não deverá ocultar violações arquiteturais através de utilitários genéricos.

---

## 4.7. Testabilidade

Todo código deverá ser escrito pensando em testes automatizados.

O projeto deverá favorecer:

- baixo acoplamento;
- alta coesão;
- inversão de dependência;
- isolamento de responsabilidades.

---

## 4.8. Evolução

O código deverá facilitar futuras evoluções.

Evitar decisões que aumentem:

- acoplamento;
- complexidade;
- duplicação;
- dependências entre Capabilities.

---

# 5. Versão Oficial do Python

O LifeOS utilizará oficialmente a versão definida no projeto.

No momento desta documentação:

| Item | Valor |
|------|--------|
| Python | 3.10+ |

Toda nova funcionalidade deverá respeitar essa versão mínima.

Não utilizar recursos de versões superiores sem atualização oficial do projeto.

---

# 6. Ferramentas Oficiais

O projeto utilizará ferramentas automáticas para manter consistência.

## Formatação

- Ruff (formatter)
- Black (caso mantido oficialmente)

---

## Lint

- Ruff

---

## Tipagem

- Mypy (quando oficialmente adotado)

---

## Testes

- Pytest

---

## Cobertura

- pytest-cov

---

## Banco

- Alembic

---

## ORM

- SQLAlchemy

---

## API

- FastAPI

---

Todas as configurações deverão permanecer centralizadas no arquivo:

```toml
pyproject.toml
```

---

# 7. Organização dos Imports

Os imports deverão seguir obrigatoriamente a ordem abaixo.

## Grupo 1

Biblioteca padrão do Python.

Exemplos:

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Protocol
```

---

## Grupo 2

Bibliotecas externas.

Exemplos:

```python
from fastapi import APIRouter
from sqlalchemy.orm import Session
```

---

## Grupo 3

Módulos do LifeOS.

Exemplos:

```python
from app.auth.domain.aggregates.user import User
from app.shared.domain.entity import Entity
```

---

## Regras

- utilizar imports absolutos;
- remover imports não utilizados;
- evitar imports dentro de funções;
- nunca utilizar wildcard imports.

Exemplo proibido:

```python
from module import *
```

---

# 8. Convenções de Nomenclatura

## Arquivos

Utilizar sempre:

- snake_case

Exemplos:

- register_user.py
- character_repository.py
- password_hasher.py

---

## Classes

Utilizar:

- PascalCase

Exemplos:

- RegisterUserCommand
- CharacterRepository
- PasswordHasher

---

## Métodos

Utilizar:

- snake_case

Exemplos:

- register_user()
- get_character()
- revoke_session()

---

## Variáveis

Utilizar:

- snake_case

Exemplos:

- current_user
- refresh_token
- character_profile

Evitar abreviações desnecessárias.

---

## Constantes

Utilizar:

- UPPER_SNAKE_CASE

Exemplos:

```python
DEFAULT_PAGE_SIZE = 20
MAX_LOGIN_ATTEMPTS = 5
```

---

## Booleanos

Utilizar nomes que expressem claramente uma condição.

Exemplos:

- is_active
- has_expired
- can_refresh
- should_publish

Evitar:

- flag
- value
- status

---

## Eventos

Eventos deverão representar fatos ocorridos.

Exemplos:

- UserRegistered
- CharacterCreated
- SessionRevoked

---

## Erros

Todos os erros de domínio deverão terminar com o sufixo `Error`.

Exemplos:

- UserAlreadyExistsError
- CharacterNotFoundError
- InvalidPasswordError

---

## Commands

Formato obrigatório:

- RegisterUserCommand
- LoginCommand
- RefreshTokenCommand

---

## Queries

Formato obrigatório:

- GetCharacterQuery
- GetProfileQuery
- GetUserByEmailQuery

---

## Handlers

Formato obrigatório:

- RegisterUserCommandHandler
- LoginCommandHandler
- GetCharacterQueryHandler

---

# 9. Estrutura de Arquivos

A organização dos arquivos deverá refletir a arquitetura oficial do LifeOS.

Cada arquivo deverá possuir uma responsabilidade única e um propósito claramente definido.

A estrutura de diretórios deverá facilitar:

- localização de código;
- manutenção;
- testes;
- evolução das Capabilities;
- isolamento entre camadas.

---

## 9.1. Tamanho dos Arquivos

Arquivos excessivamente grandes dificultam manutenção.

Como referência:

| Tipo | Tamanho recomendado |
|-------|---------------------:|
| Value Object | até 100 linhas |
| Domain Event | até 80 linhas |
| Domain Error | até 80 linhas |
| DTO | até 150 linhas |
| Repository | até 250 linhas |
| Aggregate | até 300 linhas |
| Command Handler | até 250 linhas |
| Query Handler | até 250 linhas |

Esses limites são recomendações e poderão ser ultrapassados quando houver justificativa técnica.

---

## 9.2. Um Conceito por Arquivo

Cada arquivo deverá conter apenas um conceito principal.

Exemplos:

```text
user.py
```

```text
character_created.py
```

```text
register_user.py
```

Evitar arquivos contendo diversas responsabilidades.

---

## 9.3. Organização Interna

Sempre que possível, utilizar a seguinte ordem:

1. Imports
2. Constantes
3. Tipos auxiliares
4. Classe principal
5. Funções privadas

A estrutura deverá permanecer consistente em todo o projeto.

---

# 10. Organização das Classes

As classes deverão possuir responsabilidade única.

Uma classe deverá representar apenas um conceito.

---

## 10.1. Ordem dos Membros

Sempre que possível:

1. Constantes
2. Construtor
3. Métodos públicos
4. Métodos protegidos
5. Métodos privados

Essa organização facilita leitura e revisão.

---

## 10.2. Tamanho das Classes

Classes muito grandes tendem a concentrar responsabilidades.

Como referência:

- até 300 linhas para Aggregates;
- até 250 linhas para Handlers;
- até 200 linhas para Repositories.

Caso esses limites sejam frequentemente ultrapassados, a estrutura deverá ser revisada.

---

## 10.3. Herança

A herança deverá ser utilizada com moderação.

Preferir:

- composição;
- interfaces (Protocols);
- inversão de dependência.

Evitar hierarquias profundas.

---

# 11. Funções e Métodos

Funções deverão possuir comportamento simples e objetivo.

---

## 11.1. Responsabilidade

Cada função deverá realizar apenas uma tarefa.

Caso seja necessário utilizar "e" para explicar o método, provavelmente ele possui responsabilidades múltiplas.

---

## 11.2. Tamanho

Como referência:

- até 30 linhas para métodos comuns;
- até 50 linhas quando houver regra de negócio complexa.

Métodos muito extensos deverão ser refatorados.

---

## 11.3. Número de Parâmetros

Preferencialmente:

- até três parâmetros.

Quando houver muitos parâmetros, considerar:

- Value Objects;
- DTOs;
- objetos de configuração.

---

## 11.4. Retorno

Todo retorno deverá ser claramente definido.

Evitar múltiplos formatos de retorno.

Preferir:

```python
def execute(command: RegisterUserCommand) -> User:
    ...
```

Em vez de:

```python
def execute(command):
    ...
```

---

# 12. Tipagem

Todo código novo deverá utilizar tipagem explícita.

---

## 12.1. Métodos

Sempre informar:

- parâmetros;
- retorno.

Exemplo:

```python
def register_user(command: RegisterUserCommand) -> User:
    ...
```

---

## 12.2. Variáveis

Quando melhorar a clareza:

```python
user: User
```

```python
character: Character
```

---

## 12.3. Collections

Preferir:

```python
list[User]
```

```python
dict[str, int]
```

---

## 12.4. Optional

Utilizar:

```python
User | None
```

Quando compatível com a versão oficial do Python.

---

# 13. Docstrings

O projeto utilizará docstrings apenas quando agregarem valor.

Não documentar o óbvio.

---

## Utilizar docstrings para

- APIs públicas;
- interfaces;
- algoritmos complexos;
- regras de negócio importantes;
- integrações externas.

---

## Evitar

```python
def save():
    """Save."""
```

Esse tipo de documentação não agrega informação.

---

# 14. Comentários

Comentários deverão explicar decisões.

Nunca descrever o código linha por linha.

---

## Comentários aceitáveis

- regra de negócio;
- decisão arquitetural;
- limitação conhecida;
- workaround temporário;
- referência a ADR.

---

## Comentários proibidos

```python
# incrementa i
i += 1
```

O código já demonstra isso.

---

## TODO

Somente permitido quando:

- houver justificativa;
- existir rastreabilidade;
- estiver relacionado a uma Issue ou ADR.

Exemplo:

```python
# TODO(ADR-012): substituir EventBus em memória por RabbitMQ.
```

---

# 15. Tratamento de Erros

O tratamento de erros deverá utilizar erros específicos do domínio.

---

## Utilizar

```python
UserAlreadyExistsError
```

```python
CharacterNotFoundError
```

```python
SessionExpiredError
```

---

## Evitar

```python
Exception
```

```python
RuntimeError
```

como mecanismo de regra de negócio.

---

## Captura

Capturar apenas erros que possam ser tratados.

Não utilizar:

```python
except Exception:
    ...
```

sem justificativa técnica.

---

# 16. Logging

O logging deverá registrar informações úteis para auditoria e diagnóstico.

---

## Registrar

- inicialização;
- eventos importantes;
- erros inesperados;
- integrações externas;
- operações críticas.

---

## Não registrar

- senhas;
- refresh tokens;
- access tokens;
- hashes;
- secrets;
- dados sensíveis.

---

## Níveis

Utilizar adequadamente:

- DEBUG
- INFO
- WARNING
- ERROR
- CRITICAL

---

## Estrutura

As mensagens deverão conter contexto suficiente para investigação, sem expor informações confidenciais.

---

# 17. Value Objects

Os Value Objects representam conceitos do domínio definidos exclusivamente por seus valores.

Eles deverão ser:

- imutáveis;
- comparáveis por valor;
- livres de identidade própria;
- responsáveis por validar suas próprias invariantes.

---

## 17.1. Responsabilidades

Um Value Object deverá:

- validar seus dados;
- impedir estados inválidos;
- encapsular regras de domínio;
- fornecer comportamento relacionado ao seu valor.

Não deverá:

- acessar banco de dados;
- depender de infraestrutura;
- possuir efeitos colaterais.

---

## 17.2. Imutabilidade

Todo Value Object deverá ser imutável.

Exemplo:

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Email:
    value: str
```

Após sua criação, o estado não poderá ser alterado.

---

## 17.3. Validação

Toda validação deverá ocorrer durante a construção.

Exemplo:

```python
@dataclass(frozen=True)
class PlayerName:
    value: str

    def __post_init__(self) -> None:
        if not self.value.strip():
            raise InvalidPlayerNameError()
```

Nunca permitir Value Objects inválidos.

---

# 18. Aggregates

Aggregates representam a principal unidade de consistência do domínio.

São responsáveis por proteger as regras de negócio e manter suas invariantes.

---

## 18.1. Aggregate Root

Cada Aggregate deverá possuir apenas um Aggregate Root.

Toda alteração deverá ocorrer através dele.

Não é permitido modificar entidades internas diretamente.

---

## 18.2. Responsabilidades

Um Aggregate deverá:

- proteger invariantes;
- gerar Domain Events;
- controlar alterações internas;
- manter consistência.

Não deverá:

- acessar banco de dados;
- chamar APIs;
- enviar e-mails;
- acessar infraestrutura.

---

## 18.3. Construção

Sempre que possível, utilizar métodos de fábrica explícitos.

Exemplo:

```python
user = User.register(
    email=email,
    password=hashed_password,
)
```

Evitar construtores excessivamente complexos.

---

# 19. Commands e Queries

O LifeOS utiliza CQRS como padrão arquitetural.

Commands e Queries possuem responsabilidades distintas.

---

## 19.1. Commands

Commands representam alterações de estado.

Exemplos:

- RegisterUserCommand
- LoginCommand
- RefreshTokenCommand
- ResetPasswordCommand

Commands não deverão retornar modelos ricos do domínio.

Seu retorno deverá ser:

- DTO;
- identificador;
- resultado simples.

---

## 19.2. Queries

Queries representam leitura.

Não deverão alterar estado.

Exemplos:

- GetCharacterQuery
- GetProfileQuery
- GetWorkoutHistoryQuery

Queries deverão retornar DTOs de leitura.

---

## 19.3. Handlers

Cada Command ou Query deverá possuir exatamente um Handler responsável.

Exemplos:

- RegisterUserCommandHandler
- LoginCommandHandler
- GetCharacterQueryHandler

Handlers deverão orquestrar o caso de uso.

A lógica de negócio deverá permanecer no domínio.

---

# 20. Repositories

Repositories representam a porta de acesso aos Aggregates.

---

## 20.1. Interfaces

As interfaces deverão permanecer na camada Domain.

Exemplo:

```python
class UserRepository(Protocol):
    ...
```

---

## 20.2. Implementações

As implementações deverão permanecer na Infrastructure.

Exemplos:

- SqlAlchemyUserRepository
- SqlAlchemyCharacterRepository

---

## 20.3. Responsabilidades

Repositories deverão:

- persistir Aggregates;
- recuperar Aggregates;
- ocultar detalhes de persistência.

Não deverão conter:

- regras de negócio;
- validações de domínio;
- lógica de aplicação.

---

# 21. Domain Events

Eventos representam fatos já ocorridos no domínio.

---

## 21.1. Nomenclatura

Sempre utilizar verbo no passado.

Exemplos:

- UserRegistered
- CharacterCreated
- PasswordResetRequested

---

## 21.2. Publicação

Eventos deverão ser publicados apenas após o commit bem-sucedido do Unit of Work.

A ordem oficial é:

1. Aggregate gera o evento.
2. Repository persiste o Aggregate.
3. Unit of Work realiza o commit.
4. Event Bus publica os eventos.

---

## 21.3. Responsabilidade

Eventos não deverão ser utilizados para garantir consistência transacional.

Sua finalidade é:

- integração;
- notificações;
- efeitos secundários.

---

# 22. DTOs

DTOs representam objetos de transporte entre camadas.

---

## Regras

DTOs deverão:

- ser simples;
- ser serializáveis;
- não possuir regras de negócio;
- não acessar infraestrutura.

---

## Organização

Preferencialmente:

```text
application/dtos/
```

Um DTO deverá representar apenas um contrato.

---

# 23. Mappers

Mappers são responsáveis por converter objetos entre camadas.

---

## Conversões permitidas

- Domain → ORM
- ORM → Domain
- Domain → DTO
- DTO → Domain (quando aplicável)

---

## Conversões proibidas

Mappers não deverão:

- acessar banco;
- executar regras de negócio;
- modificar estado.

Sua única responsabilidade é a transformação de dados.

---

# 24. Services

O termo "Service" deverá ser utilizado com cautela.

---

## Domain Services

Devem conter regras de domínio que não pertencem naturalmente a um Aggregate.

Exemplos:

- PasswordHasher
- CharacterFactory

---

## Infrastructure Services

Representam integrações externas.

Exemplos:

- SmtpMailSender
- JwtTokenProvider
- Argon2PasswordHasher

---

## Evitar

Não criar classes genéricas como:

- UserService
- CharacterService
- GameService

sem uma responsabilidade claramente definida.

O nome da classe deverá refletir exatamente sua finalidade.

---

# 25. Presentation Layer

A camada de Presentation é responsável exclusivamente pela interação com clientes externos.

Ela representa o ponto de entrada da aplicação.

Exemplos:

- REST API;
- CLI;
- gRPC;
- WebSocket.

---

## 25.1. Responsabilidades

A Presentation deverá:

- receber requisições;
- validar entrada;
- converter Requests em Commands ou Queries;
- chamar a camada de Application;
- converter respostas em DTOs;
- retornar códigos HTTP apropriados.

Não deverá:

- conter regras de negócio;
- acessar banco de dados;
- utilizar ORM diretamente;
- executar consultas SQL;
- acessar infraestrutura.

---

## 25.2. Controllers / Routers

Cada Router deverá possuir responsabilidade única.

Exemplo:

```text
auth/
character/
health/
workout/
reading/
therapy/
game/
```

Evitar concentrar diversos domínios em um único Router.

---

## 25.3. Schemas

Schemas deverão representar exclusivamente os contratos HTTP.

Não deverão:

- conter regras de domínio;
- acessar serviços;
- executar validações complexas.

Validações de negócio pertencem ao domínio.

---

# 26. Infrastructure Layer

A camada de Infrastructure contém implementações concretas das abstrações definidas pelo domínio.

---

## Responsabilidades

A Infrastructure poderá conter:

- SQLAlchemy;
- FastAPI adapters;
- SMTP;
- JWT;
- Redis;
- Cache;
- Event Bus;
- Unit of Work;
- Repositories;
- Mappers.

---

## Restrições

A Infrastructure não deverá:

- definir regras de negócio;
- alterar invariantes;
- conhecer detalhes internos de outras Capabilities.

Toda comunicação deverá ocorrer através das interfaces oficiais.

---

# 27. Performance

O código deverá priorizar clareza.

Otimizações somente deverão ser realizadas quando houver evidências concretas.

---

## Evitar

- otimizações prematuras;
- micro-otimizações sem necessidade;
- complexidade desnecessária.

---

## Utilizar

- índices de banco quando necessários;
- paginação;
- lazy loading quando apropriado;
- cache apenas quando houver benefício comprovado.

Toda otimização deverá ser mensurável.

---

# 28. Antipadrões

Os seguintes antipadrões são proibidos no LifeOS.

---

## God Class

Classes responsáveis por múltiplos conceitos.

---

## Service Genérico

Exemplos:

```text
UserService
GameService
CharacterService
```

sem responsabilidade claramente definida.

---

## Helper Genérico

Arquivos como:

```text
utils.py
helpers.py
common.py
misc.py
```

somente poderão existir mediante justificativa arquitetural.

---

## Lógica no Controller

Controllers deverão apenas orquestrar chamadas.

Toda regra de negócio pertence ao domínio.

---

## SQL espalhado

Consultas SQL deverão permanecer centralizadas na camada de persistência.

---

## Acoplamento entre Capabilities

Uma Capability não deverá acessar diretamente:

- Aggregates;
- Repositories;
- Infrastructure;

de outra Capability.

Toda integração deverá ocorrer através de:

- Ports;
- Domain Events;
- DTOs;
- APIs internas quando oficialmente definidas.

---

# 29. Checklist de Qualidade

Antes de concluir qualquer implementação, verificar:

## Código

- [ ] Compila corretamente.
- [ ] Sem imports inválidos.
- [ ] Sem código morto.
- [ ] Sem TODOs críticos.
- [ ] Sem FIXMEs críticos.

---

## Arquitetura

- [ ] Clean Architecture preservada.
- [ ] DDD preservado.
- [ ] CQRS respeitado.
- [ ] Dependências corretas.
- [ ] Nenhuma violação entre Capabilities.

---

## Domínio

- [ ] Invariantes protegidas.
- [ ] Value Objects imutáveis.
- [ ] Aggregates consistentes.
- [ ] Eventos publicados corretamente.

---

## Testes

- [ ] Testes unitários.
- [ ] Testes de integração.
- [ ] Testes E2E.
- [ ] Testes arquiteturais.

---

## Documentação

- [ ] Código legível.
- [ ] Nomes consistentes.
- [ ] Comentários somente quando necessários.
- [ ] Documentação atualizada.

---

# 30. Regra Final

O código do LifeOS deverá refletir a mesma qualidade da sua arquitetura.

Cada arquivo deverá demonstrar:

- clareza;
- simplicidade;
- consistência;
- baixo acoplamento;
- alta coesão;
- rastreabilidade;
- testabilidade.

O objetivo deste documento não é impor preferências individuais de estilo, mas estabelecer um padrão único que permita a evolução sustentável do projeto ao longo do tempo.

Toda contribuição — humana ou produzida por Inteligência Artificial — deverá seguir integralmente esta política.

---

# Histórico de Versões

| Versão | Data | Descrição |
|---------|------|-----------|
| 1.0 | A definir | Criação da política oficial de estilo e qualidade de código do LifeOS. |