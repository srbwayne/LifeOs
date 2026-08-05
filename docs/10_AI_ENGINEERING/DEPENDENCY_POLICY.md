# DEPENDENCY_POLICY.md

> Política oficial de seleção, inclusão, atualização, validação e remoção de dependências do projeto LifeOS.

Versão: 1.0
Status: Ativo
Aplicação: Obrigatória para desenvolvedores humanos e agentes de Inteligência Artificial

---

# 1. Objetivo

Este documento define as regras oficiais para gerenciamento de dependências do LifeOS.

Toda biblioteca externa adicionada ao projeto deverá ser:

- necessária;
- justificada;
- compatível com a arquitetura;
- declarada nos arquivos oficiais;
- validada em ambiente limpo;
- mantida em versão controlada;
- revisada quanto a segurança, licença e manutenção.

Nenhuma dependência poderá ser introduzida apenas por conveniência momentânea.

---

# 2. Escopo

Esta política aplica-se a:

- dependências de produção;
- dependências de desenvolvimento;
- dependências de testes;
- ferramentas de build;
- ferramentas de lint;
- ferramentas de cobertura;
- bibliotecas de segurança;
- bibliotecas de persistência;
- frameworks;
- SDKs externos;
- dependências transitivas críticas.

---

# 3. Princípios Fundamentais

## 3.1. Necessidade antes da adoção

Uma dependência somente deverá ser adicionada quando houver necessidade técnica real.

Antes de adicionar uma biblioteca, verificar:

- a biblioteca padrão já resolve o problema;
- existe código oficial no projeto que já atende;
- a funcionalidade pode ser implementada de forma simples;
- a nova dependência reduz complexidade de forma relevante;
- a biblioteca possui manutenção ativa.

---

## 3.2. Menor número de dependências possível

O projeto deverá evitar bibliotecas sobrepostas.

Exemplo proibido:

```text
python-jose
PyJWT
authlib
```

Quando duas bibliotecas atenderem ao mesmo objetivo, deverá ser mantida apenas a dependência oficialmente aprovada para o projeto.

---

## 3.3. Declaração, reprodutibilidade e compatibilidade

Todo import externo deverá possuir dependência correspondente nos arquivos oficiais. É proibido depender apenas de biblioteca instalada localmente ou recebida transitivamente.

O projeto deverá ser instalável em ambiente limpo. Toda dependência deverá ser compatível com a versão oficial do Python, as demais dependências, a arquitetura e as políticas de segurança e testes.

---

# 4. Classificação das Dependências

## 4.1. Produção

Bibliotecas necessárias para instalar e executar a aplicação.

## 4.2. Teste

Bibliotecas usadas exclusivamente para validar o projeto. Não deverão ser importadas pelo código de produção.

## 4.3. Desenvolvimento

Ferramentas de apoio ao desenvolvimento, análise ou build, somente quando oficialmente aprovadas. A menção documental não autoriza sua instalação.

## 4.4. Transitivas

Bibliotecas instaladas por uma dependência direta. O projeto não deverá importá-las sem declará-las diretamente.

---

# 5. Arquivos Oficiais

O `pyproject.toml` define os metadados do pacote e organiza dependências por finalidade. O `requirements.txt` permite a instalação reproduzível e deverá permanecer compatível com o `pyproject.toml`.

Ao adicionar, remover ou alterar uma dependência, avaliar conjuntamente:

- `pyproject.toml`;
- `requirements.txt`;
- imports existentes;
- documentação afetada;
- ambiente limpo;
- testes aplicáveis.

Não deverão existir versões incompatíveis entre os arquivos oficiais.

---

# 6. Critérios de Adoção

Antes da adoção, avaliar problema, alternativas existentes, biblioteca padrão, compatibilidade arquitetural, manutenção, estabilidade, documentação, licença, segurança e dependências transitivas.

Não adotar biblioteca duplicada, sem manutenção adequada, fora do escopo ou que impeça instalação reproduzível.

---

# 7. Versionamento

Dependências diretas deverão utilizar versões controladas, compatíveis e sincronizadas. Alterações deverão ser deliberadas, rastreáveis, instaladas e validadas. É proibido ajustar versões apenas para contornar falhas locais.

---

# 8. Imports Externos

Antes de aceitar um import externo, confirmar declaração, pacote correto, camada apropriada, ausência de solução equivalente, ausência de dependência transitiva acidental e disponibilidade após instalação limpa.

Imports da biblioteca padrão e imports internos do LifeOS não são dependências externas.

---

# 9. Ambiente Limpo

Toda alteração deverá ser validada em ambiente isolado:

1. criar ou selecionar ambiente limpo;
2. instalar pelos arquivos oficiais;
3. verificar pacotes instalados;
4. executar `pip check`;
5. executar testes aplicáveis;
6. validar a aplicação quando necessário.

---

# 10. `pip check`

Executar:

```bash
python -m pip check
```

Resultado esperado:

```text
No broken requirements found.
```

Incompatibilidades deverão ser corrigidas antes da conclusão.

---

# 11. Atualizações

Antes de atualizar, registrar motivação, revisar mudanças, verificar compatibilidade e segurança e definir testes. Depois, sincronizar arquivos, instalar em ambiente limpo, executar `pip check`, testes e validações impactadas. Atualizações fora do escopo não deverão ser agrupadas.

---

# 12. Remoções

Remover dependência sem uso válido, duplicada, substituída ou incompatível. Verificar usos diretos e indiretos; depois sincronizar arquivos, validar imports, ambiente limpo e testes.

---

# 13. Dependências Transitivas

Uma dependência transitiva somente deverá ser declarada diretamente quando for importada pelo projeto ou quando controle explícito for justificado. Conflitos não deverão ser ocultados por instalações manuais.

---

# 14. Dependências de Segurança

Bibliotecas de autenticação, autorização, criptografia, hashing, tokens ou dados sensíveis exigem revisão de finalidade, manutenção, configuração, vulnerabilidades e compatibilidade com `SECURITY_POLICY.md`.

É proibido reduzir garantias sem autorização. Segredos, tokens e credenciais nunca deverão constar nos arquivos de dependências.

---

# 15. Dependências de Teste

Deverão possuir finalidade clara, permanecer nos grupos apropriados e não alterar o comportamento de produção. Poderão apoiar testes unitários, integração, End-to-End, arquitetura e cobertura.

---

# 16. Dependências Privadas ou via Git

Exigem autorização explícita e registro de origem, responsável, versão, tag ou commit imutável, autenticação, licença, disponibilidade e estratégia de atualização.

É proibido registrar credenciais na URL, usar origem não verificável ou branch mutável sem justificativa.

---

# 17. Agentes de Inteligência Artificial

O agente deverá confirmar escopo, localizar imports, verificar alternativas, justificar a adoção, sincronizar arquivos, instalar em ambiente limpo, executar `python -m pip check` e testes e informar resultados reais.

Não deverá instalar sem declarar, introduzir ferramenta não aprovada, atualizar fora do escopo, ocultar conflito ou afirmar compatibilidade sem validação.

---

# 18. Checklist de Inclusão

- [ ] Necessidade técnica confirmada.
- [ ] Ausência de solução equivalente aprovada.
- [ ] Manutenção, licença e segurança avaliadas.
- [ ] Dependências transitivas revisadas.
- [ ] Arquivos e versões sincronizados.
- [ ] Imports validados.
- [ ] Instalação limpa executada.
- [ ] `python -m pip check` executado.
- [ ] Testes aplicáveis executados.
- [ ] Evidências registradas.

---

# 19. Checklist de Atualização ou Remoção

- [ ] Motivação registrada.
- [ ] Usos localizados.
- [ ] Compatibilidade e segurança analisadas.
- [ ] Arquivos oficiais sincronizados.
- [ ] Ausência de imports quebrados.
- [ ] Ambiente limpo e `pip check` validados.
- [ ] Testes aplicáveis executados.
- [ ] Escopo autorizado preservado.

---

# 20. Não Conformidades

São bloqueantes:

- import externo sem declaração;
- versões incompatíveis;
- instalação dependente do ambiente anterior;
- falha no `pip check`;
- dependência ausente ou duplicada sem justificativa;
- ferramenta não aprovada;
- credencial na configuração;
- dependência privada sem origem rastreável;
- remoção que quebre imports ou testes;
- validação declarada sem execução.

---

# 21. Auditoria

Toda alteração deverá identificar motivo, responsável, arquivos, versões, imports, validações, impacto de segurança e tarefa autorizadora.

---

# 22. Regra Final

Uma dependência somente poderá integrar o LifeOS quando necessária, aprovada, declarada, compatível, segura e reproduzível em ambiente limpo.

Nenhuma alteração será concluída com imports inválidos, conflitos de versão, dependências ausentes ou validações pendentes.

---

# Histórico de Versões

| Versão | Data | Descrição |
|---------|------|-----------|
| 1.0 | A definir | Criação da política oficial de gerenciamento de dependências do LifeOS. |
