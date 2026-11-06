# BLACKMAMBA MOBILITY AI

**README operacional · especificación v0.2.0-draft · 2026-11-06**

> Estado: arquitectura propuesta para v0.2. No representa un sistema industrial desplegado. El antecedente ejecutable es AutoFactory AI v0.1, simulador de producción con datos sintéticos y cálculo de OEE. No hay conexiones verificadas con PLC, CAN, OBD-II, ERP, MES ni vehículos reales.

## Misión

Construir una plataforma modular para fabricación, inspección, mantenimiento, trazabilidad y administración de flotas de bicicletas, motocicletas, automóviles y vehículos de servicio público. Un núcleo común permitirá agregar reglas y adaptadores por tipo de activo.

**Principio:** simular → medir → validar → integrar → operar → mejorar.

## Alcance

| Dominio | Casos iniciales | Indicadores |
|---|---|---|
| Bicicletas | Ensamble, torque, calidad | Tiempo de ciclo, defectos |
| Motocicletas | Componentes, inspección, mantenimiento | Defectos/lote, MTBF, MTTR |
| Automóviles | Estaciones, producción, trazabilidad | OEE, takt, WIP, scrap |
| Flotas gubernamentales | Disponibilidad, mantenimiento, auditoría | Disponibilidad y costo/km |

Se excluye control autónomo de máquinas, vehículos, frenos, dirección, acelerador y sistemas de seguridad o emergencia. La parte gubernamental se limita a logística y mantenimiento autorizado, no vigilancia.

## Arquitectura objetivo

```text
Fuentes sintéticas / equipos autorizados / ERP-MES / telemetría
                         |
             Ingesta + validación + permisos
                         |
             Bus de eventos + histórico
                         |
       +-----------------+----------------+
       |                 |                |
    Producción         Activos          Calidad
    (OEE/WIP)       (flotas/OT)       (inspección)
       +-----------------+----------------+
                         |
           Simulador / análisis / IA
                         |
          API + tablero + auditoría
                         |
            Recomendación humana
```

- **Core:** activos, organizaciones, estaciones, lotes, roles, órdenes y eventos.
- **Adaptadores:** CSV/JSON en primera etapa; MQTT/OPC UA en banco autorizado; CAN/OBD-II solo lectura y con autorización.
- **Simulación:** turnos, colas, defectos, tiempos, averías.
- **IA futura:** predicción, visión artificial, detección de anomalías y optimización contrastada con líneas base.
- **Entrega:** API, dashboard, reportes y alertas explicables.

## Datos previstos

| Entidad | Campos |
|---|---|
| `asset` | `asset_id`, `asset_type`, `serial_ref`, `site_id`, `status` |
| `station` | `station_id`, `site_id`, `process_type`, `capacity` |
| `production_event` | `event_id`, `station_id`, `timestamp_utc`, `units_total`, `units_good`, `downtime_s` |
| `inspection` | `inspection_id`, `asset_id`, `result`, `defect_code` |
| `work_order` | `order_id`, `asset_id`, `priority`, `state`, `approved_by` |
| `telemetry` | `asset_id`, `timestamp_utc`, `signal`, `value`, `unit`, `quality_flag` |
| `model_run` | `model_version`, `dataset_version`, `metrics`, `approved_for_use` |
| `audit_event` | `actor`, `action`, `timestamp_utc`, `target`, `outcome` |

Tiempos UTC, unidades explícitas, identificadores estables, validación de rangos, control de duplicados, retención proporcional y trazabilidad del origen. Evitar datos personales innecesarios.

## Operación diaria prevista

1. **Inicio:** verificar roles, conectividad, estado de servicios, seguridad, sensores y versiones.
2. **Ingesta:** validar esquemas, timestamp, idempotencia y rangos; aislar eventos inválidos.
3. **Monitoreo:** visualizar OEE, WIP, tiempo de ciclo, defectos y activos.
4. **Detección:** crear alertas explicables diferenciando reglas de modelos.
5. **Aprobación:** supervisor valida recomendaciones y autoriza cualquier cambio operativo.
6. **Cierre:** conciliar unidades, paros, órdenes, evidencias y reporte auditable.
7. **Mejora:** comparar contra línea base y promover cambios tras pruebas.

## Indicadores

- Disponibilidad = tiempo operativo / tiempo planificado.
- Rendimiento = tiempo de ciclo ideal × unidades totales / tiempo operativo.
- Calidad = unidades buenas / unidades totales.
- **OEE = disponibilidad × rendimiento × calidad.**
- Takt = tiempo disponible / demanda.
- FPY = unidades buenas sin retrabajo / unidades procesadas.
- MTBF = tiempo operativo / número de fallas.
- MTTR = tiempo de reparación / número de reparaciones.
- Disponibilidad de flota = vehículos operativos / vehículos totales.

**Convención:** denominadores cero se informan como no disponibles. OEE por encima de 100 % es inconsistencia de datos que se debe investigar; no se debe ocultar mediante truncamiento.

## Ejecución del prototipo v0.1

Desde `autofactory_v0_1/`:

```bash
python3 simulator.py
python3 -m unittest discover -s . -p 'test_*.py' -v
```

Los resultados son sintéticos. No usar como controlador industrial.

## Seguridad

- IA en modo observación/recomendación.
- Segmentar redes OT/IT; menor privilegio, autenticación, cifrado y auditoría.
- Los cambios físicos requieren análisis de riesgo y aprobación responsable.
- La IA no sustituye protecciones certificadas ni PLC de seguridad.
- Contemplar ISO 9001, IATF 16949, ISO 26262, ISO 13849, IEC 62061, IEC 62443, ISO 21434, APQP, PPAP y FMEA según su aplicabilidad. **No se declara certificación ni conformidad.**

## Roadmap

| Versión | Entrega | Aceptación |
|---|---|---|
| v0.2 | Esquemas comunes y escenarios para 4 tipos de activos | Simulación reproducible y pruebas |
| v0.3 | Estaciones, colas, turnos y paros | Métricas contra escenarios conocidos |
| v0.4 | API, dashboard, permisos y auditoría | Permisos probados y exportación |
| v0.5 | Predicción y anomalías | Evaluación temporal fuera de muestra vs línea base |
| v0.6 | Adaptadores de laboratorio de solo lectura | Pruebas de desconexión y datos corruptos |
| v1.0 | Piloto supervisado | Aprobación, revisión de seguridad y rollback |

## Experimentos

- **E1 Producción:** throughput, WIP y espera con iguales semillas y demanda.
- **E2 Mantenimiento:** precision, recall, falsos positivos y anticipación frente a reglas simples.
- **E3 Calidad:** evaluación por lotes independientes, recall de defectos y latencia.
- **E4 Flotas:** costo y tiempo fuera de servicio con mantenimiento preventivo simulado.

Promover módulos de propuesto → implementado → probado → integrado → piloto solo con evidencia reproducible, revisión de riesgos y responsable.

## Estado del repositorio

- **Implementado:** simulador AutoFactory AI v0.1 y cinco pruebas locales.
- **Documentado:** arquitectura y operación de Mobility AI v0.2.
- **Pendiente:** modelos tipados, escenarios por vehículo, CI, analítica y panel.
- **No desplegado:** ninguna planta, flota o equipo real.

**BlackMamba Corp — Ingeniería reutilizable, resultados verificables.**
