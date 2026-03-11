// SCRIPT PARA COLETAR AVALIAÇÕES DA AMAZON NO CONSOLE DO NAVEGADOR
// Como usar:
// 1. Acesse a página de avaliações do produto na Amazon
// 2. Abra o console do navegador (F12 -> Console)
// 3. Cole este script completo e pressione Enter
// 4. Os dados serão coletados automaticamente e exibidos no final
// 5. Copie o JSON gerado e salve em um arquivo .json

(async function coletarAvaliacoes() {
    const PAGINAS_PARA_COLETAR = 5; // Ajuste quantas páginas quer coletar
    const DELAY_ENTRE_PAGINAS = 2000; // 2 segundos entre páginas
    
    let todasAvaliacoes = [];
    let paginaAtual = 1;
    
    console.log('🚀 Iniciando coleta de avaliações...');
    console.log('⏱️ Aguarde enquanto coletamos os dados...\n');
    
    function extrairAvaliacoesPaginaAtual() {
        const avaliacoes = [];
        const reviews = document.querySelectorAll('[data-hook="review"]');
        
        reviews.forEach((review, index) => {
            try {
                // Extrair estrelas
                const ratingElement = review.querySelector('[data-hook="review-star-rating"]');
                let estrelas = 0;
                if (ratingElement) {
                    const ratingText = ratingElement.textContent.trim();
                    const match = ratingText.match(/(\d+[,.]?\d*)/);
                    if (match) {
                        estrelas = parseFloat(match[1].replace(',', '.'));
                    }
                }
                
                // Extrair comentário
                const comentarioElement = review.querySelector('[data-hook="review-body"]');
                const comentario = comentarioElement ? comentarioElement.textContent.trim() : '';
                
                // Classificar sentimento
                let sentimento = 'neutro';
                if (estrelas <= 2) {
                    sentimento = 'negativo';
                } else if (estrelas >= 4) {
                    sentimento = 'positivo';
                }
                
                if (comentario && estrelas > 0) {
                    avaliacoes.push({
                        comentario: comentario,
                        estrelas: estrelas,
                        sentimento: sentimento
                    });
                }
            } catch (error) {
                console.warn(`⚠️ Erro ao processar avaliação ${index + 1}:`, error);
            }
        });
        
        return avaliacoes;
    }
    
    function irParaProximaPagina() {
        const proximoBotao = document.querySelector('.a-pagination .a-last a');
        if (proximoBotao && !proximoBotao.classList.contains('a-disabled')) {
            proximoBotao.click();
            return true;
        }
        return false;
    }
    
    function aguardar(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
    
    // Coletar páginas
    while (paginaAtual <= PAGINAS_PARA_COLETAR) {
        console.log(`📄 Coletando página ${paginaAtual}...`);
        
        // Aguardar página carregar
        await aguardar(1000);
        
        // Extrair avaliações da página atual
        const avaliacoesPagina = extrairAvaliacoesPaginaAtual();
        todasAvaliacoes.push(...avaliacoesPagina);
        
        console.log(`   ✓ ${avaliacoesPagina.length} avaliações coletadas`);
        
        // Se chegou na última página desejada, parar
        if (paginaAtual >= PAGINAS_PARA_COLETAR) {
            break;
        }
        
        // Tentar ir para próxima página
        console.log(`   ⏳ Aguardando ${DELAY_ENTRE_PAGINAS/1000}s antes da próxima página...`);
        await aguardar(DELAY_ENTRE_PAGINAS);
        
        if (!irParaProximaPagina()) {
            console.log('   ⚠️ Não há mais páginas disponíveis');
            break;
        }
        
        paginaAtual++;
    }
    
    // Resultados finais
    console.log('\n' + '='.repeat(60));
    console.log('✅ COLETA CONCLUÍDA!');
    console.log('='.repeat(60));
    console.log(`📊 Total de avaliações coletadas: ${todasAvaliacoes.length}`);
    
    // Estatísticas
    const stats = {
        positivo: todasAvaliacoes.filter(a => a.sentimento === 'positivo').length,
        neutro: todasAvaliacoes.filter(a => a.sentimento === 'neutro').length,
        negativo: todasAvaliacoes.filter(a => a.sentimento === 'negativo').length
    };
    
    console.log('\n📈 Distribuição de sentimentos:');
    console.log(`   Positivo: ${stats.positivo}`);
    console.log(`   Neutro: ${stats.neutro}`);
    console.log(`   Negativo: ${stats.negativo}`);
    
    // Gerar JSON
    console.log('\n📋 COPIE O JSON ABAIXO:');
    console.log('='.repeat(60));
    console.log(JSON.stringify(todasAvaliacoes, null, 2));
    console.log('='.repeat(60));
    
    // Criar arquivo para download
    const dataStr = JSON.stringify(todasAvaliacoes, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'avaliacoes_kindle.json';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    
    console.log('\n💾 Arquivo "avaliacoes_kindle.json" baixado automaticamente!');
    console.log('📝 Agora execute: python importar_json.py');
    
    return todasAvaliacoes;
})();
