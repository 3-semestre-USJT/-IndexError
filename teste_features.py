#!/usr/bin/env python
"""Script de teste para validar todas as novas features"""

print("=== Teste de Importação de Módulos ===\n")

try:
    from src.logic.dificuldade import GerenciadorDificuldade, NivelDificuldade
    print("✅ dificuldade.py")
except Exception as e:
    print(f"❌ dificuldade.py: {e}")

try:
    from src.logic.achievements import GerenciadorAchievements
    print("✅ achievements.py")
except Exception as e:
    print(f"❌ achievements.py: {e}")

try:
    from src.logic.historico import GerenciadorHistorico
    print("✅ historico.py")
except Exception as e:
    print(f"❌ historico.py: {e}")

try:
    from src.logic.controles import MapeadorControles
    print("✅ controles.py")
except Exception as e:
    print(f"❌ controles.py: {e}")

try:
    from src.logic.powerups import GerenciadorPowerups, TipoPowerup
    print("✅ powerups.py")
except Exception as e:
    print(f"❌ powerups.py: {e}")

try:
    from src.logic.multiplayer import GerenciadorMultiplayer
    print("✅ multiplayer.py")
except Exception as e:
    print(f"❌ multiplayer.py: {e}")

try:
    from src.logic.animacoes import GeradorParticulas, AnimadorTransicao
    print("✅ animacoes.py")
except Exception as e:
    print(f"❌ animacoes.py: {e}")

try:
    from src.logic.pontuacao import GerenciadorPontuacao
    print("✅ pontuacao.py (modificado)")
except Exception as e:
    print(f"❌ pontuacao.py: {e}")

try:
    from src.ui.som import alternar_musica, alternar_som_efeitos
    print("✅ som.py (modificado)")
except Exception as e:
    print(f"❌ som.py: {e}")

print("\n=== Teste de Funcionamento ===\n")

try:
    # Testar Dificuldade
    dif = GerenciadorDificuldade()
    dif.definir_dificuldade(NivelDificuldade.DIFICIL)
    print(f"✅ Dificuldade: {dif.obter_nome()}")

    # Testar Achievements
    ach = GerenciadorAchievements()
    ach.desbloquear("combo_500")
    print(f"✅ Achievements desbloqueadas: {ach.obter_total_desbloqueadas()}")

    # Testar Powerups
    pw = GerenciadorPowerups()
    pw.adicionar_powerup(TipoPowerup.TEMPO_EXTRA)
    print(f"✅ Powerups no inventário: {pw.obter_quantidade()}")
    
    # Testar Controles
    ctrl = MapeadorControles()
    print(f"✅ Controles customizáveis carregados")
    
    # Testar Multiplayer
    mp = GerenciadorMultiplayer()
    mp.iniciar_modo()
    print(f"✅ Modo multiplayer inicializado")

    print("\n✅✅✅ Todos os módulos funcionando corretamente! ✅✅✅")
except Exception as e:
    print(f"\n❌ Erro durante testes: {e}")
    import traceback
    traceback.print_exc()
