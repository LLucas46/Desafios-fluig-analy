# Blueprint do workflow mínimo (Atividade 1)

Este é o desenho de configuração para reproduzir no Fluig Studio; ele não substitui o arquivo nativo gerado/publicado pelo Studio.

## Raias e tarefas

1. **Solicitante**: início → **Abrir chamado**. Saída do gateway `Encaminhamento da triagem?` para `Devolver` → **Ajustar chamado** → volta para **Triagem**.
2. **Técnico de laboratório**: **Triagem**. Opções de saída: `Atender agora` → **Executar atendimento**; `Precisa de peça` → **Autorizar compra**; `Improcedente` → fim **Chamado cancelado**; `Devolver` → tarefa do solicitante.
3. **Coordenação**: **Autorizar compra**. Gateway `Compra autorizada?`: `Autorizada` → **Executar atendimento**; `Negada` → fim **Chamado cancelado**.
4. **Técnico de laboratório**: **Executar atendimento** → fim **Chamado resolvido**.

## Configuração

- Usar tarefas humanas para Abrir chamado, Triagem, Autorizar compra, Executar atendimento e Ajustar chamado.
- Atribuir Triagem e Executar atendimento ao grupo de técnicos; Autorizar compra ao grupo de coordenação. Criar os grupos no ambiente antes de testar.
- Configurar as condições dos gateways lendo `encaminhamento` e `compraAutorizada` no formulário. Não deixar decisão manual de destino.
- Nomear explicitamente os eventos finais `Chamado resolvido` e `Chamado cancelado`.
- Registrar os IDs reais de estados/atividades e preencher `FLUIG_STAGE_BY_STATE` no formulário.
- Publicar e percorrer pelo menos um chamado; validar também o ciclo de devolução para Ajustar chamado → Triagem.
