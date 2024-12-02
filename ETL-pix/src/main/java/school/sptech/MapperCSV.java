package school.sptech;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;

public class MapperCSV extends Mapper {
    List<Pix> map(InputStream inputStream) throws IOException {
        List<Pix> pixFormat = new ArrayList<>();
        String linha;
        String separador = ",";

        System.out.println("Classe mapperCSV acessada");

        try (BufferedReader br = new BufferedReader(new InputStreamReader(inputStream))) {
            // Pulando cabeçalho
            br.readLine();

            while ((linha = br.readLine()) != null) {
                Pix pix = getData(linha, separador);
                pixFormat.add(pix);
            }
        }

        return pixFormat;
    }

    // Mapeando conteúdo do CSV e transformando em objeto
    public Pix getData(String linha, String separador) {
        String[] dados = linha.split(separador);

        // Mapeando dados através de gets da classe
        Pix pix = new Pix();
        pix.setData(dados[0]);
        pix.setRegiaoPagamento(dados[1]);
        pix.setRegiaoRecebimento(dados[2]);
        pix.setIdadePagamento(dados[3]);
        pix.setIdadeRecebimento(dados[4]);
        pix.setValor(Double.parseDouble(dados[5]));
        pix.setQuantidade(Integer.parseInt(dados[6]));
        return pix;
    }
}
