# EPIC-HAB ? Habits

## Objetivo

Gerenciar defini??es de h?bitos e o checklist di?rio do Player dentro do LifeOS. Habits V1 ? owner-scoped, owner-private e n?o integra com Game/Logos, Analytics externo, AI/Noema ou eventos externos.

## Features

- HAB-001 ? Cadastro de h?bitos
- HAB-002 ? Checklist di?rio
- HAB-003 ? Sequ?ncia (Streak)
- HAB-004 ? Frequ?ncia
- HAB-005 ? Estat?sticas

V1 = HAB-001 + HAB-002. HAB-003..005 = DEFERRED. Rotinas, execu??o quantitativa, frequ?ncia, streaks e estat?sticas permanecem conceitos futuros; registro de execu??o/checklist pertence a HAB-002.

## Regras V1

Habit ? uma defini??o reutiliz?vel com owner, nome obrigat?rio e ?nico por owner, descri??o opcional e estado ativo. O owner pode desativar e reativar; n?o h? rename ou delete em V1.

HabitCompletion ? bin?rio e representa a conclus?o declarada pelo owner para uma data civil expl?cita (`record_date`). Existe no m?ximo um fato por `(owner_id, habit_id, record_date)`; repeti??o ? idempotente e remo??o corrige o fato. H?bito inativo n?o aceita nova conclus?o, mas o hist?rico existente continua consult?vel.

## Conceitos futuros

Rotinas, agendas recorrentes, lembretes, notifica??es, frequ?ncia, Streak, estat?sticas, evolu??o, analytics, Game Engine, progression, Logos e AI/Noema podem ser considerados em decis?es futuras. Nenhuma dessas integra??es ou dispatches ? realizada por Habits V1.
