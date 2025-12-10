"""
Script de prueba para verificar que Any puede leer y usar el conocimiento de IAs
"""

from any_core.self_analysis import SelfAnalysis
import json

print("=" * 60)
print("PRUEBA DE CONOCIMIENTO DE IAs")
print("=" * 60)

# Crear instancia de auto-análisis
sa = SelfAnalysis()

# 1. Guardar conocimiento actualizado
print("\n1. Guardando conocimiento de IAs...")
sa.save_ai_knowledge('data/memory/ai_knowledge.json')

# 2. Cargar conocimiento
print("\n2. Cargando conocimiento de IAs...")
knowledge = sa.load_ai_knowledge('data/memory/ai_knowledge.json')

# 3. Mostrar reporte de capacidades
print("\n3. REPORTE DE IAs Y SUS ESPECIALIDADES:")
print("-" * 60)
ai_report = sa.get_ai_capabilities_report()
print(f"Total configuradas: {ai_report['total_configured']}")
print(f"Activas: {ai_report['active_count']}")
print()

for ai_name, ai_info in ai_report['ais'].items():
    if ai_info['enabled']:
        print(f"✅ {ai_name.upper()}")
        print(f"   Especialidad: {ai_info['specialty']}")
        print(f"   Mejor para: {ai_info['best_for']}")
        print(f"   Score: {ai_info['score']}/10")
        print(f"   Modelo: {ai_info['model']}")
        print()

# 4. Probar sugerencias de IA para diferentes tareas
print("\n4. SUGERENCIAS DE IA SEGÚN LA TAREA:")
print("-" * 60)

test_queries = [
    "Qué noticias hay sobre Argentina hoy?",
    "Escribime una carta formal de renuncia",
    "Cómo funciona un bucle for en Python?",
    "Resolveme esta ecuación: 2x + 5 = 13",
    "Comparame Windows vs Linux",
    "Traducí esto al francés: buenos días"
]

for query in test_queries:
    recommended = sa.get_ai_for_task(query)
    print(f"\n📝 Consulta: '{query}'")
    print(f"🎯 IAs recomendadas: {', '.join([ai.upper() for ai in recommended[:3]])}")

print("\n" + "=" * 60)
print("PRUEBA COMPLETADA ✅")
print("=" * 60)
