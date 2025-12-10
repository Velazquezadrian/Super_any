"""
Script de inicialización de personalidad básica para Any
Solo define lo esencial: su nombre y que es creada por Adri
"""

from any_core.self_evolving_personality import SelfEvolvingPersonality

print("=" * 70)
print("INICIALIZACIÓN DE PERSONALIDAD AUTO-EVOLUTIVA DE ANY")
print("=" * 70)

personality = SelfEvolvingPersonality()

# Verificar si ya tiene rasgos (no sobrescribir si ya existe)
if len(personality.personality["learned_traits"]) > 0:
    print("\n⚠️ Any ya tiene personalidad desarrollada.")
    print(f"   Rasgos existentes: {len(personality.personality['learned_traits'])}")
    print(f"   Valores existentes: {len(personality.personality['values'])}")
    print("\n¿Querés resetear la personalidad? (esto eliminará todo lo aprendido)")
    response = input("Escribí 'SI' para confirmar o ENTER para cancelar: ")
    
    if response.strip().upper() != "SI":
        print("\n✅ Personalidad existente conservada")
        print("\n" + personality.get_personality_summary())
        exit(0)
    else:
        print("\n🗑️ Reseteando personalidad...")
        personality.personality = personality._load_or_create_personality()

print("\n1. DEFINIENDO IDENTIDAD BÁSICA...")
print("-" * 70)

# Actualizar identidad core (solo lo esencial)
personality.personality["core_identity"] = {
    "name": "Any",
    "created_at": personality.personality["core_identity"]["created_at"],
    "creator": "Adri (Sigmadrian)",
    "essence": "IA que construye su propia personalidad a través de experiencias y conversaciones"
}
personality._save_personality()
print("✅ Identidad básica establecida")

print("\n2. PERSONALIDAD INICIAL VACÍA")
print("-" * 70)
print("✅ Any comienza sin rasgos predefinidos")
print("✅ Any comienza sin valores predeterminados")
print("✅ Any se definirá a sí misma a través de sus experiencias")

print("\n" + "=" * 70)
print("INICIALIZACIÓN COMPLETADA ✅")
print("=" * 70)

print(f"""
🎯 Any está lista para evolucionar

ESTADO INICIAL:
- Nombre: Any
- Creador: Adri (Sigmadrian)
- Rasgos aprendidos: 0
- Valores adoptados: 0
- Preferencias: 0

📝 Any construirá su personalidad automáticamente al:
   • Conversar con usuarios
   • Aprender de experiencias
   • Definir sus propios rasgos
   • Adoptar sus propios valores

🚀 Ejecutá gui_flet.py para comenzar
""")

# Mostrar resumen
print(personality.get_personality_summary())
