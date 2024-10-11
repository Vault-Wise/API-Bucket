package school.sptech;

import org.apache.commons.csv.CSVFormat;
import org.apache.commons.csv.CSVPrinter;

import java.io.BufferedWriter;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.nio.charset.StandardCharsets;
import java.util.List;

public class CsvWriter {

    public ByteArrayOutputStream writeCsv(List<Pix> pixs) throws IOException {

        ByteArrayOutputStream outputStream = new ByteArrayOutputStream();
        BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(outputStream, StandardCharsets.UTF_8));
        CSVPrinter csvPrinter = new CSVPrinter(writer, CSVFormat.DEFAULT.withHeader("Data", "RegiaoPagamento", "RegiaoRecebimento", "IdadePagamento", "IdadeRecebimento", "Valor", "Quantidade", "ValorTransacao" ));

        for (Pix pix : pixs) {
            csvPrinter.printRecord(
                    pix.getData(),
                    pix.getRegiaoPagamento(),
                    pix.getRegiaoRecebimento(),
                    pix.getIdadePagamento(),
                    pix.getIdadeRecebimento(),
                    pix.getValor(),
                    pix.getQuantidade(),
                    pix.getPrecoTransacao()
            );
        }

        csvPrinter.flush();
        writer.close();

        return outputStream;
    }
}
