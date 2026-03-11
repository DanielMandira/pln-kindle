import json
import csv
import re

def limpar_texto(texto):
    """
    Remove pontuação, números, caracteres especiais e converte para minúsculas
    """
    # Converter para minúsculas
    texto = texto.lower()
    
    # Remover pontuação, números e caracteres especiais
    # Mantém apenas letras e espaços
    texto = re.sub(r'[^a-záàâãéèêíïóôõöúçñ\s]', '', texto)
    
    # Remover espaços extras
    texto = ' '.join(texto.split())
    
    return texto

def processar_json_para_csv(arquivo_json='avaliacoes_kindle.json', arquivo_csv='avaliacoes_processadas.csv'):
    """
    Processa o JSON e converte para CSV com dados estruturados
    """
    print("=" * 60)
    print("PROCESSAMENTO DE DADOS: JSON → CSV")
    print("=" * 60)
    
    # Ler arquivo JSON
    try:
        with open(arquivo_json, 'r', encoding='utf-8') as f:
            dados = json.load(f)
        print(f"\n✓ {len(dados)} avaliações carregadas do JSON")
    except FileNotFoundError:
        print(f"\n❌ Arquivo '{arquivo_json}' não encontrado!")
        return
    except json.JSONDecodeError:
        print(f"\n❌ Erro ao ler o arquivo JSON. Verifique o formato.")
        return
    
    # Processar dados
    print("\n" + "=" * 60)
    print("PROCESSANDO E ESTRUTURANDO DADOS")
    print("=" * 60)
    
    dados_processados = []
    
    for i, item in enumerate(dados, 1):
        # Texto original
        comentario_original = item['comentario']
        
        # Texto limpo (processado)
        comentario_limpo = limpar_texto(comentario_original)
        
        # Dados estruturados
        dados_processados.append({
            'id': i,
            'comentario_original': comentario_original,
            'comentario_limpo': comentario_limpo,
            'estrelas': item['estrelas'],
            'sentimento': item['sentimento']
        })
    
    print(f"✓ {len(dados_processados)} avaliações processadas")
    
    # Salvar em CSV
    print("\n" + "=" * 60)
    print("SALVANDO DADOS EM CSV")
    print("=" * 60)
    
    with open(arquivo_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['id', 'comentario_original', 'comentario_limpo', 'estrelas', 'sentimento'])
        writer.writeheader()
        writer.writerows(dados_processados)
    
    print(f"✓ Arquivo '{arquivo_csv}' criado com sucesso!")
    
    # Estatísticas
    print("\n" + "=" * 60)
    print("ESTATÍSTICAS DOS DADOS")
    print("=" * 60)
    
    total = len(dados_processados)
    print(f"\nTotal de avaliações: {total}")
    
    # Contagem por sentimento
    sentimentos = {}
    for item in dados_processados:
        sent = item['sentimento']
        sentimentos[sent] = sentimentos.get(sent, 0) + 1
    
    print("\nDistribuição de sentimentos:")
    for sentimento, quantidade in sorted(sentimentos.items(), key=lambda x: x[1], reverse=True):
        percentual = (quantidade / total * 100)
        print(f"  {sentimento.capitalize()}: {quantidade} ({percentual:.1f}%)")
    
    # Contagem por estrelas
    estrelas_count = {}
    soma_estrelas = 0
    for item in dados_processados:
        est = item['estrelas']
        estrelas_count[est] = estrelas_count.get(est, 0) + 1
        soma_estrelas += est
    
    media_estrelas = soma_estrelas / total
    print(f"\nMédia de estrelas: {media_estrelas:.2f}")
    
    print("\nDistribuição por estrelas:")
    for estrelas, quantidade in sorted(estrelas_count.items(), reverse=True):
        print(f"  {estrelas:.1f} estrelas: {quantidade}")
    
    # Mostrar exemplos
    print("\n" + "=" * 60)
    print("EXEMPLOS DE PROCESSAMENTO")
    print("=" * 60)
    
    for sentimento in ['positivo', 'neutro', 'negativo']:
        exemplos = [d for d in dados_processados if d['sentimento'] == sentimento]
        if exemplos:
            print(f"\n{sentimento.upper()} (exemplo):")
            exemplo = exemplos[0]
            print(f"  Original: {exemplo['comentario_original'][:80]}...")
            print(f"  Limpo: {exemplo['comentario_limpo'][:80]}...")
            print(f"  Estrelas: {exemplo['estrelas']}")
    
    print("\n" + "=" * 60)
    print("PROCESSO CONCLUÍDO!")
    print("=" * 60)
    print(f"\n✓ Arquivo CSV: {arquivo_csv}")
    print(f"✓ Total de registros: {total}")
    print("\nO arquivo CSV contém:")
    print("  - id: identificador único")
    print("  - comentario_original: texto original da avaliação")
    print("  - comentario_limpo: texto processado (minúsculas, sem pontuação)")
    print("  - estrelas: avaliação numérica (1-5)")
    print("  - sentimento: classificação (positivo/neutro/negativo)")

if __name__ == "__main__":
    processar_json_para_csv()
