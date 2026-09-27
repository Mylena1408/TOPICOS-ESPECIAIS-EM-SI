*# AGENTS.md — Contexto para a tarefa de validação de Timeout*



*## Projeto*



*Este repositório é o HTTPX, uma biblioteca HTTP para Python.*



*A tarefa desta atividade consiste em corrigir a validação da classe `Timeout`, localizada em:*



*`httpx/\_config.py`*



*## Contexto da tarefa*



*Existe um caso específico em `Timeout.\_\_init\_\_` quando o argumento `timeout` recebe uma instância existente de `Timeout`.*



*Nesse ramo, existem validações baseadas em `assert` para impedir que os parâmetros `connect`, `read`, `write` e `pool` sejam fornecidos simultaneamente.*



*A tarefa deve investigar e corrigir esse comportamento para que a validação não dependa de `assert`, mantendo o comportamento válido já existente.*



*## Arquivos relevantes*



*### Implementação*



*\* `httpx/\_config.py`*



*Contém a classe `Timeout` e a lógica responsável pela configuração dos tempos de espera.*



*### Testes*



*\* `tests/test\_config.py`*

*\* `tests/test\_timeouts.py`*



*`tests/test\_config.py` contém testes de construção, comparação e representação de objetos `Timeout`.*



*`tests/test\_timeouts.py` contém testes relacionados ao comportamento dos timeouts durante operações HTTP.*



*### Documentação*



*\* `docs/advanced/timeouts.md`*



*Deve ser consultada para verificar se a documentação descreve corretamente o comportamento da configuração de timeouts.*



*## Comportamentos que devem ser preservados*



*O comportamento normal de criação de um timeout deve continuar funcionando, incluindo:*



*```python*

*httpx.Timeout(5.0)*

*```*



*e:*



*```python*

*httpx.Timeout(5.0, connect=10.0)*

*```*



*Também deve continuar funcionando a criação de um `Timeout` a partir de outro `Timeout` quando nenhuma sobrescrita conflitante for fornecida:*



*```python*

*timeout = httpx.Timeout(5.0)*

*httpx.Timeout(timeout)*

*```*



*## Problema a investigar*



*Deve ser investigado o comportamento quando uma instância de `Timeout` é fornecida juntamente com parâmetros de sobrescrita, por exemplo:*



*```python*

*httpx.Timeout(httpx.Timeout(5.0), connect=10.0)*

*```*



*A implementação atual utiliza `assert` nesse caminho.*



*A solução deve substituir a dependência dessas asserções por uma validação explícita e apropriada para código de biblioteca.*



*Também deve ser investigado o comportamento quando Python é executado com otimização (`python -O`), pois as instruções `assert` são removidas nesse modo.*



*## Testes*



*Antes de modificar a implementação, leia os testes existentes e identifique o local mais apropriado para os novos testes de regressão.*



*Os testes devem verificar:*



*1. comportamento válido de `Timeout`;*

*2. construção a partir de outro `Timeout`;*

*3. rejeição explícita de combinações conflitantes;*

*4. comportamento correto quando o Python é executado com otimização, se isso puder ser testado de maneira apropriada na estrutura atual do projeto.*



*## Comandos de teste*



*O projeto utiliza pytest.*



*Para executar os testes relacionados à configuração:*



*```powershell*

*python -m pytest tests/test\_config.py -q*

*```*



*Para executar os testes de timeout:*



*```powershell*

*python -m pytest tests/test\_timeouts.py -q*

*```*



*Antes de considerar a tarefa concluída, a suíte completa também deve ser executada:*



*```powershell*

*python -m pytest*

*```*



*## Definition of Done*



*A tarefa estará concluída quando:*



*\* a validação de `Timeout` não depender de `assert` para esse caso;*

*\* os comportamentos válidos existentes forem preservados;*

*\* existir teste de regressão para o problema;*

*\* o teste demonstrar que uma configuração conflitante não é silenciosamente ignorada;*

*\* os testes relacionados a `Timeout` passarem;*

*\* a suíte completa do projeto passar;*

*\* a documentação for verificada e atualizada somente se necessário;*

*\* as alterações estiverem limitadas ao escopo da tarefa;*

*\* não forem introduzidas alterações não relacionadas ao problema.*



*## Regra importante*



*Antes de modificar arquivos, o agente deve ler e compreender a implementação existente e os testes relacionados.*



*Não alterar arquivos sem primeiro verificar como o comportamento atual é utilizado pelo projeto.*
