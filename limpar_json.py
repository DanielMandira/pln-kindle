import json
import re

def limpar_comentario(texto):
    """
    Remove metadados de vídeo/imagem e mantém apenas o comentário textual
    """
    # Se o comentário começa com {" é JSON de vídeo
    if texto.strip().startswith('{"'):
        # Procurar pelo texto real após o JSON
        # O padrão geralmente é: JSON...}texto real do comentário
        
        # Remover todo JSON/HTML no início
        texto = re.sub(r'^.*?"needPlayerFactory"[^}]*}', '', texto)
        
        # Remover tags HTML e metadados de vídeo comuns
        texto = re.sub(r'O vídeo mostra o produto em uso\.', '', texto)
        texto = re.sub(r'O vídeo orienta você na configuração do produto\.', '', texto)
        texto = re.sub(r'O vídeo compara vários produtos\.', '', texto)
        texto = re.sub(r'O vídeo mostra o produto sendo desembalado\.', '', texto)
        texto = re.sub(r'Video Player is loading\..*?This is a modal window\.', '', texto, flags=re.DOTALL)
        texto = re.sub(r'A mídia não pôde ser carregada\.', '', texto)
        
        # Remover qualquer texto HTML residual
        texto = re.sub(r'<[^>]+>', '', texto)
        texto = re.sub(r'\n+', ' ', texto)
        texto = re.sub(r'\s+', ' ', texto)
        
    # Limpar espaços extras
    texto = texto.strip()
    
    return texto

def processar_json(arquivo_entrada='avaliacoes_kindle.json', arquivo_saida='avaliacoes_kindle_limpo.json'):
    """
    Processa o JSON e remove metadados de vídeo/imagem
    """
    print("=" * 60)
    print("LIMPEZA DE METADADOS DE VÍDEO/IMAGEM")
    print("=" * 60)
    
    # Ler arquivo JSON
    try:
        with open(arquivo_entrada, 'r', encoding='utf-8') as f:
            dados = json.load(f)
        print(f"\n✓ {len(dados)} avaliações carregadas")
    except FileNotFoundError:
        print(f"\n❌ Arquivo '{arquivo_entrada}' não encontrado!")
        return
    except json.JSONDecodeError:
        print(f"\n❌ Erro ao ler o arquivo JSON.")
        return
    
    # Processar comentários
    dados_limpos = []
    comentarios_modificados = 0
    
    for item in dados:
        comentario_original = item['comentario']
        comentario_limpo = limpar_comentario(comentario_original)
        
        # Só manter comentários que têm texto válido (não vazios e com mais de 5 caracteres)
        if comentario_limpo and len(comentario_limpo) > 5:
            dados_limpos.append({
                'comentario': comentario_limpo,
                'estrelas': item['estrelas'],
                'sentimento': item['sentimento']
            })
            
            if comentario_original != comentario_limpo:
                comentarios_modificados += 1
        else:
            print(f"⚠️ Comentário removido (vazio ou só metadados)")
    
    # Salvar arquivo limpo
    with open(arquivo_saida, 'w', encoding='utf-8') as f:
        json.dump(dados_limpos, f, ensure_ascii=False, indent=2)
    
    print(f"\n✓ Arquivo limpo salvo: {arquivo_saida}")
    print(f"✓ Total de avaliações: {len(dados_limpos)}")
    print(f"✓ Comentários modificados: {comentarios_modificados}")
    print(f"✓ Comentários removidos: {len(dados) - len(dados_limpos)}")
    
    # Mostrar exemplos de limpeza
    if comentarios_modificados > 0:
        print("\n" + "=" * 60)
        print("EXEMPLOS DE LIMPEZA")
        print("=" * 60)
        
        count = 0
        for i, item_original in enumerate(dados):
            comentario_original = item_original['comentario']
            comentario_limpo = limpar_comentario(comentario_original)
            
            if comentario_original != comentario_limpo and len(comentario_limpo) > 5:
                print(f"\nExemplo {count + 1}:")
                print(f"  Antes (primeiros 100 chars): {comentario_original[:100]}...")
                print(f"  Depois: {comentario_limpo[:100]}{'...' if len(comentario_limpo) > 100 else ''}")
                count += 1
                
                if count >= 3:  # Mostrar apenas 3 exemplos
                    break
    
    print("\n" + "=" * 60)
    print("PROCESSO CONCLUÍDO!")
    print("=" * 60)
    
    return dados_limpos

if __name__ == "__main__":
    processar_json()
