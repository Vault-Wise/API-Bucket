package school.sptech;

import org.apache.commons.csv.CSVFormat;
import org.apache.commons.csv.CSVPrinter;

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.util.List;

public class EscritorCsv {

    public ByteArrayOutputStream writeCsv(List<Maquina> maquinas) throws IOException {
        ByteArrayOutputStream outputStream = new ByteArrayOutputStream();

        BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(outputStream, StandardCharsets.UTF_8));
        CSVPrinter csvPrinter =
                new CSVPrinter(writer,
                        CSVFormat.DEFAULT.withHeader("idCaixaEletronico", "DataHora", "TempoAtividade"
                                , "PorcentagemCPU", "FrequenciaCPU", "TotalMemoria", "MemoriaUsada",
                                "PorcentagemMemoria", "TotalDisco", "DiscoUsado", "PorcentagemDisco",
                                "VelocidadeUpload", "VelocidadeDowload"));

        // Processar e escrever cada objeto no CSV
        for (Maquina maquina : maquinas) {
            csvPrinter.printRecord(
                    maquina.getIdCaixaEletronico(),
                    maquina.getDataHora(),
                    maquina.getTempoAtividade(),
                    maquina.getPorcentagemCPU(),
                    maquina.getFrequenciaCPU(),
                    maquina.getTotalMemoria(),
                    maquina.getMemoriaUsada(),
                    maquina.getPorcentagemMemoria(),
                    maquina.getTotalDisco(),
                    maquina.getDiscoUsado(),
                    maquina.getPorcentagemDisco(),
                    maquina.getVelocidadeUpload(),
                    maquina.getVelocidadeDowload()

            );
        }

        csvPrinter.flush();
        writer.close();

        return outputStream;
    }
}
