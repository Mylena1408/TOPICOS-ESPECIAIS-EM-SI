*# NOTES.md — Investigação inicial da tarefa Timeout*



*## Data da investigação*



*2026-09-27*



*## Objetivo*



*Investigar como o HTTPX implementa e testa a classe `Timeout` antes de realizar qualquer alteração no código.*



*## Arquivos investigados*



*Foram pesquisados inicialmente:*



*\* `httpx/\_config.py`*

*\* `tests/test\_config.py`*

*\* `tests/test\_timeouts.py`*



*Também foi identificada a documentação:*



*\* `docs/advanced/timeouts.md`*



*## Descobertas em `httpx/\_config.py`*



*A classe `Timeout` está localizada em `httpx/\_config.py`.*



*O construtor possui um tratamento específico quando o parâmetro `timeout` recebe uma instância de `Timeout`:*



*```python*

*if isinstance(timeout, Timeout):*

&#x20;   *# Passed as a single explicit Timeout.*

*```*



*Nesse caminho, os valores de `connect`, `read`, `write` e `pool` do objeto recebido são copiados para o novo objeto.*



*A investigação também identificou quatro validações com `assert` nesse ramo, relacionadas à proibição de fornecer simultaneamente uma instância de `Timeout` e valores explícitos para `connect`, `read`, `write` ou `pool`.*



*## Descobertas em `tests/test\_config.py`*



*O arquivo contém diversos testes diretamente relacionados à construção de `Timeout`.*



*Entre eles existe:*



*```python*

*def test\_timeout\_from\_config\_instance():*

&#x20;   *timeout = httpx.Timeout(timeout=5.0)*

&#x20;   *assert httpx.Timeout(timeout) == httpx.Timeout(timeout=5.0)*

*```*



*Esse teste demonstra que construir um novo `Timeout` a partir de uma instância existente é um comportamento esperado pelo projeto.*



*Também foram encontrados testes para:*



*\* `Timeout(None)`;*

*\* `Timeout(timeout=None)`;*

*\* valores individuais;*

*\* valor padrão com sobrescrita;*

*\* tupla de valores;*

*\* representação (`repr`);*

*\* igualdade entre objetos.*



*## Descobertas em `tests/test\_timeouts.py`*



*Esse arquivo contém testes relacionados ao comportamento dos timeouts durante operações HTTP.*



*Foram encontrados testes para:*



*\* `ReadTimeout`;*

*\* `WriteTimeout`;*

*\* `ConnectTimeout`;*

*\* `PoolTimeout`;*

*\* timeout durante requisições assíncronas.*



*Portanto, esse arquivo está mais relacionado ao comportamento dos timeouts durante a comunicação HTTP, enquanto `tests/test\_config.py` é o local mais diretamente relacionado à construção e validação da classe `Timeout`.*



*## Problema investigado*



*O caso de interesse é a combinação de uma instância existente de `Timeout` com parâmetros explícitos, por exemplo:*



*```python*

*httpx.Timeout(httpx.Timeout(5.0), connect=10.0)*

*```*



*A implementação atual utiliza `assert` para impedir essa combinação.*



*O problema a investigar é se essa validação deve utilizar uma exceção explícita em vez de `assert`, especialmente porque `assert` pode ser removido quando o Python é executado com otimização.*



*## Hipótese de correção*



*A validação deve ser feita de maneira explícita e permanecer ativa independentemente do modo de execução do Python.*



*A alteração deve preservar os comportamentos válidos já existentes.*



*## Linha de base*



*Antes de modificar a implementação, devem ser executados:*



*```powershell*

*python -m pytest tests/test\_config.py -q*

*```*



*```powershell*

*python -m pytest tests/test\_timeouts.py -q*

*```*



*Posteriormente deverá ser executada a suíte completa:*



*```powershell*

*python -m pytest*

*```*



*Os resultados desses testes serão registrados no diário da atividade.*



*## Próxima etapa*



*Criar ou ajustar os testes de regressão antes da implementação da correção, garantindo que o problema esteja reproduzido e que a solução possa ser verificada automaticamente.*

## Evidência do comportamento atual

Foi executado o caso:

python -c "import httpx; print(httpx.Timeout(httpx.Timeout(5.0), connect=10.0))"

O comportamento observado foi:
AssertionError em httpx/_config.py, na validação:
assert connect is UNSET

Também foi executado:

python -O -c "import httpx; print(httpx.Timeout(httpx.Timeout(5.0), connect=10.0))"

Nesse caso, o resultado foi:
Timeout(timeout=5.0)

Isso confirma que a utilização de assert faz com que a validação seja removida quando o Python é executado com a opção -O.

Foi criado o teste:
test_timeout_from_config_instance_with_override

O teste espera ValueError para impedir que um Timeout já configurado receba sobrescritas silenciosas.

Resultado antes da implementação:
28 testes passaram e 1 teste falhou, pois a implementação atual ainda produz AssertionError.
