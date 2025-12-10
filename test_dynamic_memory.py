"""
Script de prueba del Sistema de Memoria Dinámica
"""

from any_core.dynamic_memory import DynamicMemory

print("=" * 70)
print("PRUEBA DE MEMORIA DINÁMICA EN TIEMPO REAL")
print("=" * 70)

# Crear instancia
memory = DynamicMemory()

print("\n1. ESCRIBIENDO MEMORIAS...")
print("-" * 70)

# Escribir diferentes tipos de memorias
memory_ids = []

memory_ids.append(memory.write_memory(
    "Adri prefiere usar Groq para análisis de código",
    category="preferences",
    importance=8,
    tags=["adri", "groq", "código"]
))

memory_ids.append(memory.write_memory(
    "Microsoft Copilot configurado con EdgeGPT usando cookies de Bing",
    category="tech",
    importance=9,
    tags=["copilot", "edgegpt", "configuración"]
))

memory_ids.append(memory.write_memory(
    "Adri es de Rosario, Argentina. Le gusta el gaming y streaming",
    category="personal",
    importance=10,
    tags=["adri", "personal"]
))

memory_ids.append(memory.write_memory(
    "Plan: Agregar más IAs gratuitas como DeepSeek y Mistral",
    category="ideas",
    importance=7,
    tags=["ias", "futuro"]
))

memory_ids.append(memory.write_memory(
    "Sistema de routing elige automáticamente la mejor IA por especialidad",
    category="learning",
    importance=8,
    tags=["sistema", "routing"]
))

print(f"\n✅ {len(memory_ids)} memorias escritas")

print("\n2. LEYENDO MEMORIA ESPECÍFICA...")
print("-" * 70)
first_memory = memory.read_memory(memory_ids[0])
print(f"ID: {first_memory['id']}")
print(f"Contenido: {first_memory['content']}")
print(f"Categoría: {first_memory['category']}")
print(f"Importancia: {first_memory['importance']}/10")
print(f"Tags: {first_memory['tags']}")
print(f"Accesos: {first_memory['access_count']}")

print("\n3. BUSCANDO MEMORIAS...")
print("-" * 70)

# Buscar por query
print("\nBúsqueda: 'Adri'")
results = memory.search_memories(query="Adri")
for i, mem in enumerate(results, 1):
    print(f"{i}. [{mem['category']}] {mem['content'][:50]}... (imp: {mem['importance']}/10)")

# Buscar por categoría
print("\nBúsqueda: categoría 'tech'")
results = memory.search_memories(category="tech")
for i, mem in enumerate(results, 1):
    print(f"{i}. {mem['content'][:50]}...")

# Buscar por tags
print("\nBúsqueda: tag 'ias'")
results = memory.search_memories(tags=["ias"])
for i, mem in enumerate(results, 1):
    print(f"{i}. {mem['content'][:50]}...")

print("\n4. ACTUALIZANDO MEMORIA...")
print("-" * 70)
updated = memory.update_memory(
    memory_ids[3],
    new_content="Plan actualizado: DeepSeek, Mistral y Ollama local",
    new_importance=9
)
print(f"Actualización: {'✅ Éxito' if updated else '❌ Fallo'}")

print("\n5. MEMORIAS IMPORTANTES (>=8)...")
print("-" * 70)
important = memory.get_important_memories(min_importance=8)
for i, mem in enumerate(important, 1):
    print(f"{i}. [{mem['category'].upper()}] {mem['content']}")
    print(f"   Importancia: {mem['importance']}/10, Accesos: {mem['access_count']}")

print("\n6. ESTADÍSTICAS DE MEMORIA...")
print("-" * 70)
stats = memory.get_memory_stats()
print(f"Total de memorias: {stats['total_memories']}")
print(f"\nPor categoría:")
for cat, count in stats['by_category'].items():
    print(f"  • {cat}: {count}")

print(f"\nPor importancia:")
for imp in range(10, 0, -1):
    count = stats['by_importance'][imp]
    if count > 0:
        print(f"  {'★' * imp} ({imp}/10): {count} memorias")

print("\n7. CONTEXTO RESUMIDO...")
print("-" * 70)
context = memory.get_context_summary(max_memories=10)
print(context)

print("\n8. ELIMINANDO UNA MEMORIA...")
print("-" * 70)
deleted = memory.delete_memory(memory_ids[0])
print(f"Eliminación: {'✅ Éxito' if deleted else '❌ Fallo'}")

print("\n9. EXPORTANDO MEMORIAS...")
print("-" * 70)
export_path = memory.export_memories()
print(f"Exportado a: {export_path}")

print("\n" + "=" * 70)
print("PRUEBA COMPLETADA ✅")
print("=" * 70)

print(f"\n💾 Memorias guardadas en: data/memory/dynamic_memory.json")
print(f"📤 Exportación en: {export_path}")
