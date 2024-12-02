package school.sptech;

import org.apache.poi.hssf.usermodel.HSSFWorkbook;
import org.apache.poi.ss.usermodel.*;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.util.List;

public class EscritorExcel implements EscritorArquivo {

    @Override
    public ByteArrayOutputStream escreverArquivo(List<Maquina> maquinas) throws IOException {
        ByteArrayOutputStream outputStream = new ByteArrayOutputStream();
        Workbook workbook = new HSSFWorkbook(); // HSSFWorkbook para arquivos XLS

        // Criar a planilha
        Sheet sheet = workbook.createSheet("Relatório");

        // Definir cabeçalho
        String[] headers = {
                "idCaixaEletronico", "Data", "Hora", "DiaSemana", "TempoAtividade",
                "PorcentagemCPU", "FrequenciaCPU", "MemoriaUsada",
                "PorcentagemMemoria", "VelocidadeUpload", "VelocidadeDowload"
        };

        Row headerRow = sheet.createRow(0);
        for (int i = 0; i < headers.length; i++) {
            Cell cell = headerRow.createCell(i);
            cell.setCellValue(headers[i]);
            // Estilizar cabeçalho (opcional)
            CellStyle style = workbook.createCellStyle();
            Font font = workbook.createFont();
            font.setBold(true);
            style.setFont(font);
            cell.setCellStyle(style);
        }

        // Preencher as linhas com dados
        int rowIndex = 1; // Começa após o cabeçalho
        for (Maquina maquina : maquinas) {
            Row row = sheet.createRow(rowIndex++);
            row.createCell(0).setCellValue(maquina.getIdCaixaEletronico());
            row.createCell(1).setCellValue(maquina.getData());
            row.createCell(2).setCellValue(maquina.getHora());
            row.createCell(3).setCellValue(maquina.getDiaDaSemana());
            row.createCell(4).setCellValue(maquina.getTempoEmMinutos());
            row.createCell(5).setCellValue(maquina.getPorcentagemCPU());
            row.createCell(6).setCellValue(maquina.getFrequenciaCPU());
            row.createCell(7).setCellValue(maquina.getMemoriaUsada());
            row.createCell(8).setCellValue(maquina.getPorcentagemMemoria());
            row.createCell(9).setCellValue(maquina.getVelocidadeUpload());
            row.createCell(10).setCellValue(maquina.getVelocidadeDowload());
        }

        // Ajustar largura das colunas automaticamente (opcional)
        for (int i = 0; i < headers.length; i++) {
            sheet.autoSizeColumn(i);
        }

        // Escrever os dados no OutputStream
        workbook.write(outputStream);
        workbook.close();

        return outputStream;
    }
}
