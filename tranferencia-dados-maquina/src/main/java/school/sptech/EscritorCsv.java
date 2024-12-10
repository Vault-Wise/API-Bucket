package school.sptech;

import org.apache.commons.csv.CSVFormat;
import org.apache.commons.csv.CSVPrinter;

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.util.List;

public class EscritorCsv implements EscritorArquivo {

    @Override
    public ByteArrayOutputStream escreverArquivo(List<Maquina> maquinas) throws IOException {
        ByteArrayOutputStream outputStream = new ByteArrayOutputStream();

        BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(outputStream, StandardCharsets.UTF_8));
        CSVPrinter csvPrinter =
                new CSVPrinter(writer,
                        CSVFormat.DEFAULT.withHeader("idCaixaEletronico", "Data", "Hora", "DiaSemana",
                                "TempoAtividade", "PorcentagemCPU", "FrequenciaCPU", "MemoriaUsada",
                                "PorcentagemMemoria", "VelocidadeUpload", "VelocidadeDowload"));

        // Processar e escrever cada objeto no CSV
        for (Maquina maquina : maquinas) {
            csvPrinter.printRecord(
                    maquina.getIdCaixaEletronico(),
                    maquina.getData(),
                    maquina.getHora(),
                    maquina.getDiaDaSemana(),
                    maquina.getTempoEmMinutos(),
                    maquina.getPorcentagemCPU(),
                    maquina.getFrequenciaCPU(),
                    maquina.getMemoriaUsada(),
                    maquina.getPorcentagemMemoria(),
                    maquina.getVelocidadeUpload(),
                    maquina.getVelocidadeDowload()

            );
        }

        csvPrinter.flush();
        writer.close();

        return outputStream;
    }
}
